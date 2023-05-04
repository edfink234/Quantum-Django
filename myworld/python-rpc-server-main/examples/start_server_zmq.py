from RPC_server.backend.zmq_server import zmq_server


api = zmq_server()
api.init("tcp://*:5556")

@api.add_function
def hello(name: str):
    """
    Greets someone.

    Parameters
    ----------
    name : str
        Name of the person to be greeted.

    Returns
    -------
    str
        the greeting
    """
    return "Hi " + name + '!'

@api.add_function
def add_numbers(a, b = 0):
    """
    Adds two numbers.
    If no second number is given, returns first number.

    Parameters
    ----------
    a : int
        a number
    b : int, optional
        another number, by default 0

    Returns
    -------
    c : int
        sum of a and b
    """
    c = a + b
    return c

@api.add_function
def rpc_info():
    return api.rpc_info()

@api.add_class
class TestJig():
    """
    Just here to test interface generation.
    """
    def test01(a,b):
        """
        test summary

        Parameters
        ----------
        a : int
            test a
        b : int
            test b

        Returns
        -------
        int
            a plus b
        """
        return a+b
api.serve()