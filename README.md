# Quantum-Django
Website in-development for a Quantum Computer

1. git clone thisrepo
2. virtualenv TestQuantumDjangoEnv -p python3.10
3. source TestQuantumDjangoEnv/bin/activate
4. cd TestWebGui
5. pip3 install -r requirements.txt
6. Install redis and mongodb dockers
    a. docker run -p 6379:6379 -d redis:5
    b. docker run -p 27017:27017 --name mymongo -d mongo
7. cd myworld 
8. python manage.py collectstatic
9. python3 manage.py runserver

Note: In file `mydjangoenv/lib/python3.10/site-packages/redis/client.py`, change the function `def parse_zadd(response, **options):` to the following:

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
