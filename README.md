# Quantum-Django
Website in-development for a Quantum Computer

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
