# -*- coding: utf-8 -*-
"""
Created on Thu Mar 17 2022

@author: Christian Melzer
"""

from typing import Union, List, Optional

def function_with_args(string:str, *args:bytes) -> None:
    """
    Function with positional arguments.

    Parameters
    ----------
    string : str
        A dummy string.
    *args : bytes
        Dummy positional bytes arguments.

    Returns
    -------
    None.

    """
    
    pass

def function_with_kwargs(string:str, **kwargs:int) -> bool:
    """
    Function with keyword arguments.

    Parameters
    ----------
    string : str
        A dummy string.
    **kwargs : int
        Dummy integer keyword arguments.

    Returns
    -------
    bool
        Always True.

    """
    
    return True

def function_with_default_values(integer:int, string:str="x") -> int:
    """
    Function that has a parameter with a default value.

    Parameters
    ----------
    integer : int
        A dummy integer.
    string : str, optional
        An optional string, by default "x".

    Returns
    -------
    int
        Always 1.

    """
    
    return 1

def function_with_different_indent(boolean:bool) -> None:
   """
   A function with a weird indent of 3.

   Parameters
   ----------
   boolean : bool
      A dummy parameter.

   Returns
   -------
   None.

   """

def function_with_union(union:Union[int, float]) -> Union[None, int]:
    """
    A function that takes and return a union.
    Be careful! The union annotations change in Python 3.10! 'Union[int, float]' -> 'int | float'

    Parameters
    ----------
    union : Union[int, float]
        Can be either int or float.

    Returns
    -------
    Union[None, int]
        Can be either None or int.

    """
    
    return 2

def function_with_default_triple_union(union:Union[int, str, list]="x") -> None:
    """
    A more complex union parameter is expected for this function.
    Be careful! The union annotations change in Python 3.10! 'Union[int, float]' -> 'int | float'

    Parameters
    ----------
    union : Union[int, str, list], optional
        Some more complex union. The default is "x".

    Returns
    -------
    None.

    """
    
    pass

def function_explicitely_returning_none() -> None:
    """
    A function that explicitely returns None. Alternative to doing it implicitely.

    Returns
    -------
    None
        This looks different due to explicitely returning None.

    """
    
    return None

def function_with_optional(opt_int: Optional[int]) -> Optional[str]:
    """
    Optional means that the given type or None is expected.

    Parameters
    ----------
    opt_int : Optional[int]
        Optional integer.

    Returns
    -------
    Optional[str]
        Optional string.

    """
    
    return None

def function_with_any(x: any) -> any:
    """
    Anything allowed for parameteres and return value.

    Parameters
    ----------
    x : any
        Anything allowed.

    Returns
    -------
    any
        Might be anything.

    """
    
    pass

def function_with_old_list(the_list:List[str]) -> List[int]:
    """
    The old way to annotate lists (before Python 3.8).

    Parameters
    ----------
    the_list : List[str]
        A dummy list.

    Returns
    -------
    List[int]
        List as return value.

    """
    
    return []

def function_with_default_list(the_list:Optional[list]=None) -> list[int]:
    """
    Optional list via the new way.

    Parameters
    ----------
    the_list : Optional[list], optional
        New way of annotation list. The default is None.

    Returns
    -------
    list[int]
        A integer list.

    """
    
    return [1, 4]


