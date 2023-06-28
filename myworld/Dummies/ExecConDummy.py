from RPC_server.backend.hermione_server import hermione_server
import logging

class ExecConDummy:

    def __init__(self):
        pass

    def set_values(self, func_name, *args, **kwargs):
        print('Setting', func_name, 'to', args, kwargs)
        return True

    def exec_exp(self, exp_name, *args, **kwargs):
        print('Executing', exp_name, 'with parameters', args, kwargs)
        return True

    def test(self, message):
        print('test message:', message)
        return True



def main():

    #switch_address = 'tcp://host.docker.internal:52021'
    switch_address = 'tcp://127.0.0.1:52021'
    alt_keypath = '../myworld/switchkey/env-network-transport-layer.txt'


    api = hermione_server()

    try: # when run from repository
        keypath = 'switch_key.key'
        print('getting keys from', keypath)
        api.init(switch_address, keypath, log_level=logging.INFO)

    except: # when run locally
        print('failed...')
        keypath = alt_keypath
        print('getting keys from', keypath)
        api.init(switch_address, keypath, log_level=logging.INFO)

    ExecConD = ExecConDummy()
    api.add_object(ExecConD, 'ExecConD') # address functions with ExecConD.function_name
    api.serve('ExecConDummy') # registration name for switch; use this string as the target parameter in the client when sending a request


if __name__ == '__main__':
    main()