#subscriber

from channels.layers import get_channel_layer
from time import sleep
import asyncio
import zmq
import sys
import signal
from asgiref.sync import async_to_sync
from multiprocessing import Process
from shared_memory_dict import SharedMemoryDict
import re
from pymongo import MongoClient


from threading import Thread


#Receives data from the consumer class function 'receive' which received data from the Raman.html
#via the Javascript 'signal' button
async def func_receive(channel_layer):
    users = set() #set of unique users, not used, but hey, if you need it, why not
    client = MongoClient()
    db = client.test_database
#    print(db.posts.find_one({"user": "edwardfinkelstein"}))
    try:
        while True:
            x = await channel_layer.receive("ZMQ")
#            print(x)
            if smd_config.get("status"):

                if x.get('text_data')=='"increase!"':
                    smd_config["status"]+=1e-5
                    print(smd_config["status"],end="\r",flush=True)
                elif x.get('text_data')=='"decrease!"':
                    smd_config["status"]-=1e-6
                    print(smd_config["status"],end="\r",flush=True)
            if x.get('text_data')=='"hi friend"':
                print("🥳"*1000,end="\n\n")

            #get mongodb data if it's an html string

            regex = r"user = (.+);" #'user = ' followed by 1 or more instances of anything
            html_string = x.get('text_data')
            match = re.search(regex, html_string) #search through html_string for regex pattern
            if match: #if regex pattern found
                user = match.group(1) #get part matched by (.+)
                
                users.add(user) #add user to set of users for the heck of it.
                
                #extract the html part of the string, i.e., the data
                html_string = html_string[match.end()+1:-1].replace("\\", "")
                
                #Now, add/update the user with the corresponding html string
                if db.posts.find_one({"user": user}):
                    db.posts.find_one_and_update({"user": user}, { '$set': {"user": user, "data":html_string}})
                else: #if user is not registered in the mongdb database
                    #add the user with the user's data
                    db.posts.insert_one({"user": user, "data":html_string})
                
                print(db.posts.find_one({"user": user}))
            
    except asyncio.CancelledError as e:
        print("Break it out")
        raise(e)

def between_callback(args):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

#    loop = asyncio.get_event_loop()

    loop.run_until_complete(asyncio.gather(func_receive(args)))
    loop.close()

smd_config = SharedMemoryDict(name='config', size=1024)
#Receiving data from the camera and sending it to the group
async def TrueServerZMQ(socket, channel_layer):
    while True:
#        smd_config["status"] = False
##        smd_config["group_send_status"] = False
##        print("hi")
        try:
            message = socket.recv_multipart(flags=zmq.NOBLOCK)
            
        #            print(message)
        #            smd_config["status"] = True
            await channel_layer.group_send("ZMQ",{"type": "chat.message", "text": [i.decode() for i in message]})
        #            print("😅")
            
#            print(smd_config["status"])

        except zmq.Again:
#            print(smd_config["status"])
            continue
        
#        message = socket.recv_multipart()
#        await channel_layer.group_send("ZMQ",{"type": "chat.message", "text": [i.decode() for i in message]})
#        smd_config["status"] = True
#import signal
#while True:
#    try:
#        signal.alarm(1)
#    except:
#        print("bye")
#    else:
#        print("hi")
#        continue


#    finally:
#        print("hi")
#        continue
        
#        try:
##            signal.alarm(1)
#            message = socket.recv_multipart()
#        except:
#
#            print("hi")
#        else:
#            continue
#        finally:
#            try:
#                message
#                smd_config["status"] = True
#            except NameError:
#                continue
#        print(message)
#        print(count)
#        count+=1
        
#        await channel_layer.group_send("ZMQ",{"type": "chat.message", "text": [i.decode() for i in message]})
#        smd_config["group_send_status"] = True
#        print("done")
#        socket.send_string("World")
'''
async def TrueServerZMQReceive():
    while True:
        x = await channel_layer.receive("ZMQ")
        print(x)
def process():
    asyncio.run(TrueServerZMQReceive())
'''

#p = Process(target=process)
#p.start()

#async def main():
#    # create a subprocess using create_subprocess_shell()
#    process = await asyncio.create_subprocess_shell('python dum.py', stdout=asyncio.subprocess.PIPE)
#    # read data from the subprocess
#    data, _ = await process.communicate()
#    # report the data
#    print(data)
#
#asyncio.run(main())
#_thread = Thread(target=between_callback, args=(channel_layer,))
#_thread.start()

if __name__ == '__main__':
    ZMQ_server_context = zmq.Context()
    socket = ZMQ_server_context.socket(zmq.SUB)
    socket.setsockopt(zmq.RCVHWM, 1000000)
    socket.connect("tcp://127.0.0.1:5555")
    ZMQ_server_loaded = True
    socket.setsockopt(zmq.SUBSCRIBE, b"CAMERA")
    channel_layer = get_channel_layer()
    print("Here is the ",channel_layer)
#    count=0
#    sleep(1)
    p = Process(target=between_callback, args=(channel_layer,))
    p.start()

    #Thread(target=asyncio.run, args=(func_receive(channel_layer),)).start()

    asyncio.run(TrueServerZMQ(socket, channel_layer))

        
