# Quantum-Django
Website in-development for a Quantum Computer

https://www.dropbox.com/scl/fi/2nfqjofcp1c70ow1azwav/Quantum-Computer-Mainz-Demo.mov?rlkey=usmny4efksuzsn6jfakk4x5kv&dl=0 

1. `git clone thisrepo`
2. `virtualenv TestQuantumDjangoEnv -p python3.10`
3. `source TestQuantumDjangoEnv/bin/activate`
4. `cd TestWebGui`
5. `pip3 install -r requirements.txt`
6. Install redis and mongodb dockers
```
    a. docker run -p 6379:6379 -d redis:5
    b. docker run -p 27017:27017 --name mymongo -d mongo
```
7. `cd myworld`
8. `python manage.py collectstatic`
9. Run seperate processes starting from TestWebGui/myworld:
```
    Terminal 1
	a. source TestQuantumDjangoEnv/bin/activate
	b. python3 manage.py shell
	c. import os
	d. os.system("python3 HardwareSubscriber.py")
    Terminal 2
	a. source TestQuantumDjangoEnv/bin/activate
	b. python3 manage.py runserver
    Terminal 3
	a. source TestQuantumDjangoEnv/bin/activate
	b. python3 manage.py shell
	c. import os
	d. os.system("python3 dummy\_dds\_zmq.py")
    Terminal 4
	a. source mydjangoenv/bin/activate
	b. cd ../Dummies/
	c. python3 HardwareDummy.py
```	

Note: In file `TestQuantumDjangoEnv/lib/python3.10/site-packages/redis/client.py`, change the function `def parse_zadd(response, **options):` to the following:

```python
def parse_zadd(response, **options):
    if response is None:
        return None
    if options.get("as_score"):
        try:
            return float(response)
        except TypeError:
            return response
    try:
        return int(response)
    except TypeError:
        return response
```
