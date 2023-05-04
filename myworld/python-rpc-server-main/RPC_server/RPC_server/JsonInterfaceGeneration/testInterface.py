import JSONInterfaceGeneration as jig
import annotated_dummy_functions as adf


def foo(var1, var2, *args, long_var_name='hi', only_seldom_used_keyword=0, **kwargs):
    r"""Summarize the function in one line.

    Several sentences providing an extended description. Refer to
    variables using back-ticks, e.g. `var`.

    Parameters
    ----------
    var1 : array_like
        Array_like means all those objects -- lists, nested lists, etc. --
        that can be converted to an array.  We can also refer to
        variables like `var1`.
    var2 : int
        The type above can either refer to an actual Python type
        (e.g. ``int``), or describe the type of the variable in more
        detail, e.g. ``(N,) ndarray`` or ``array_like``.
    *args : iterable
        Other arguments.
    long_var_name : {'hi', 'ho'}, optional
        Choices in brackets, default first when optional.

    Returns
    -------
    type
        Explanation of anonymous return value of type ``type``.
    describe : type
        Explanation of return value named `describe`.
    out : type
        Explanation of `out`.
    type_without_description

    Other Parameters
    ----------------
    only_seldom_used_keyword : int, optional
        Infrequently used parameters can be described under this optional
        section to prevent cluttering the Parameters section.
    **kwargs : dict
        Other infrequently used keyword arguments. Note that all keyword
        arguments appearing after the first parameter specified under the
        Other Parameters section, should also be described under this
        section.

    Raises
    ------
    BadException
        Because you shouldn't have done that.

    See Also
    --------
    numpy.array : Relationship (optional).
    numpy.ndarray : Relationship (optional), which could be fairly long, in
                    which case the line wraps here.
    numpy.dot, numpy.linalg.norm, numpy.eye

    Notes
    -----
    Notes about the implementation algorithm (if needed).

    This can have multiple paragraphs.

    You may include some math:

    .. math:: X(e^{j\omega } ) = x(n)e^{ - j\omega n}

    And even use a Greek symbol like :math:`\omega` inline.

    References
    ----------
    Cite the relevant literature, e.g. [1]_.  You may also cite these
    references in the notes section above.

    .. [1] O. McNoleg, "The integration of GIS, remote sensing,
       expert systems and adaptive co-kriging for environmental habitat
       modelling of the Highland Haggis using object-oriented, fuzzy-logic
       and neural-network techniques," Computers & Geosciences, vol. 22,
       pp. 585-588, 1996.

    Examples
    --------
    These are written in doctest format, and should illustrate how to
    use the function.

    >>> a = [1, 2, 3]
    >>> print([x + 3 for x in a])
    [4, 5, 6]
    >>> print("a\nb")
    a
    b
    """
    # After closing class docstring, there should be one blank line to
    # separate following codes (according to PEP257).
    # But for function, method and module, there should be no blank lines
    # after closing the docstring.
    pass


class DDS_Interface():
    """
    information about the class DDS_Interface.
    This is another line.

    This line is NOT ignored.
    """
    def __init__(self):
        pass

    def set_state(self, frequency, amplitude, phase):
        """
        sets the triple frequency, amplitude and phase.

        Parameters
        ----------
        frequency : float
            DDS frequency in Hz.
        amplitude : float
            Amplitude in dB. Max limit is 26dB.
        phase : float
            Offset Phase in radiant to atomic clock, if connected.
        """
        pass

    def get_overtemp(self):
        """
        returns true if the DDS core temperature is to hot.

        Returns
        -------
        temperature : bool
            true, if too hot.
        """
        pass

    def _intern(self):
        """
        Some internal function, that should not appear in the json interface.
        """
        pass

    def __intern2(self):
        """
        Some internal protected function, that should not appear in the json interface.
        References
        ----------
        https://stackoverflow.com/questions/1301346/
        what-is-the-meaning-of-single-and-double-underscore-before-an-object-name#:~:
        text=Single%20underscore%20at%20the%20beginning,not%20part%20of%20the%20API.
        """
        pass

def foo2(g, k, x1=8, x2=8, a=1, b='hello', c = 34, d = 128, e = 0, f = 6, h='hi', i=8, j=9):
    """
    info foo2.
    This has two lines.

    But this does not appear in the interface.

    Parameters
    ----------
    a : int, optional
        a description. By default 1.
    b : str, optional
        b description, by default "hello"
    c : int, optional
        c description, the default is 34.
    d : int, optional
        d description. The default is 128.
    e : int, optional
        e description. I forgot to write down the default.
    f : int, default : 6
        this is another way to describe an optional parameter
    h : str, default = "hi"
        another way
    i : int, default 8
        yet another way
    j : {9,10,11,12}
        choices in brackets, first is default
    x1, x2: int, optional
        description for x1 and x2, the default is 8
    g, k: int
        g and k description
    

    Returns
    -------
    t : bool
        always True
    """
    t = True
    return t

def problem(a,b,c, other_parameter):
    """
    info for this function
    this appears in the interface

    this does not appear in the interface

    Parameters
    ----------
    a : int
        a description
    b : int
        b description

    c : int
        c description; this does not appear in the interface
    
    Returns
    ---------
    bool
        always True

    Next section
    ---------
    This is something else

    Other Parameters
    other_parameter : str
        this does not appear in the interface because of missing --
    """
    
    return True

def no_docstring():
    pass

def empty_docstring():
    """
    
    
    """
    pass

class TestClass():
    """
    Description for TestClass.

    Methods
    -------
    tc_func
    """
    def tc_func(a,b=2):
        """
        Description for tc_func.

        Parameters
        ----------
        a : int
            a description
        b : int, optional
            b description, by default 2

        Returns
        -------
        int
            return description
        """
        return 1

def test1(x,z,y):
    """
    test1 description

    Parameters
    ----------
    x : int
        x description
    z
    y 
        y description, type is not specified

    Returns
    -------
    int
        anonymous return value
    return_value_no_description
    return_name : int
        another return value
    """
    return 1

class TestJig():
    """
    Just here to test interface generation.
    """
    def __init__(self,a):
        self.a = a

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

"""
print(jig.generate(foo))
print('#########################')
print(jig.generate(DDS_Interface))
print('#########################')
print(jig.generate(jig.generate))
print('#########################')
print(jig.generate(jig.generate_func))
print('#########################')
print(jig.generate(jig.read_section))
print('#########################')
print(jig.generate(adf.function_with_args))
print('#########################')
print(jig.generate(adf.function_with_kwargs))
print('#########################')
print(jig.generate(adf.function_with_default_values))
print('#########################')
print(jig.generate(adf.function_with_different_indent)) # FAILS, IS ALLOWED TO FAIL
print('#########################')
print(jig.generate(adf.function_with_union))
print('#########################')
print(jig.generate(adf.function_with_default_triple_union))
print('#########################')
print(jig.generate(adf.function_explicitely_returning_none))
print('#########################')
print(jig.generate(TestClass))
print('#########################')
print(jig.generate(adf.function_with_optional))
print('#########################')
print(jig.generate(adf.function_with_any))
print('#########################')
print(jig.generate(adf.function_with_old_list))
print('#########################')
print(jig.generate(adf.function_with_default_list))
print('#########################')
print(jig.generate(no_docstring))
print('#########################')
print(jig.generate(empty_docstring))
print('#########################')
print(jig.generate(problem))
print('#########################')
print(jig.generate(foo2))
print('#########################')
print(jig.generate(test1))
"""

print(jig.generate(TestJig))
print('#########################')
