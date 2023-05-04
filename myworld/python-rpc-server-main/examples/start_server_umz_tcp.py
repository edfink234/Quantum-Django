from RPC_server.backend.umz_tcp_server import umz_server


api = umz_server()
api.init('localhost', 1234)

@api.add_function
def hello(name: str):
    """
    _summary_

    Parameters
    ----------
    name : str
        _description_

    Returns
    -------
    _type_
        _description_
    """
    return "Hi " + name + '!'

@api.add_function
def rpc_info():
    return api.rpc_info()
    
api.serve()