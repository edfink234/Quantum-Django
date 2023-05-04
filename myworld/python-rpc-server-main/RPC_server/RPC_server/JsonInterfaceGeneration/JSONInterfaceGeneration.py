import json
import inspect
import re


def read_section(docstr_lines, start, indent, is_para=True):
    """
    Generates a dictionary for a section of a docstring, e.g. Parameters or Returns.

    Parameters
    ----------
    docstr_lines : list
        Full docstring, divided into lines.
    start : int
        Line number where the section starts.
    indent : int, optional
        factor describing the indentation, by default 1, for functions inside a class 2.

    Returns
    -------
    section_dict : dict
        Dictionary that contains name, type and info for each variable in the section.
    """

    line = start
    section_dict = {}
    anonym_count = 1
    indent_offset = '    ' * indent

    # catch None
    if docstr_lines[line].strip().startswith('None'):
        return section_dict

    # section ends when line empty or doesn't contain any letters
    while docstr_lines[line].startswith(indent_offset) and any(c.isalpha() for c in docstr_lines[line]):

        is_optional = False

        # get name and type from 'name : type' line
        if ':' in docstr_lines[line]:
            temp = docstr_lines[line].split(':', 1)
            name = temp[0].strip()
            type_ = temp[1].strip()
        # get type for anonymous value
        else:
            if is_para:
                name = docstr_lines[line].strip()
                type_ = 'not specified'
            else:
                name = 'anonymous value ' + str(anonym_count)
                anonym_count += 1
                type_ = docstr_lines[line].strip()

        # if variables are bunched together, they need to be seperated
        names = name.split(',')
        name = names[0].strip()

        # create empty dict in section dict for this variable
        section_dict[name] = {}

        default = ''
        # check if parameter is marked optional (not type 'Optional'!)
        # optional has to be in lowercase letters
        if 'optional' in type_:
            type_ = type_.split(', optional')[0]
            is_optional = True
        elif 'default' in type_.lower():
            temp = type_.split(', default')
            type_ = temp[0]
            default = temp[1].replace(' ', '').replace(
                '=', '').replace(':', '').replace('\"', "'")
            is_optional = True
        if '{' in type_:
            default = type_.split(',')[0].replace('{', '').strip()
            is_optional = True

        # add type to section dict
        section_dict[name]['type'] = type_

        # get info from the following lines
        line += 1
        info = ''
        # info part end when indentation ends or when the line doesn't contain any letters
        while docstr_lines[line].startswith(indent_offset + '    ') and any(c.isalpha() for c in docstr_lines[line]):
            # check for default in different styles and case insensitive, remove from info
            if is_optional:
                if default:
                    section_dict[name]['default'] = default
                elif 'by default' in docstr_lines[line].lower():
                    temp = re.split(
                        'by default', docstr_lines[line], flags=re.IGNORECASE)
                    default = temp[1].replace(
                        '.', '').replace('\"', "'").strip()
                    docstr_lines[line] = temp[0].replace(',', '').strip()
                    section_dict[name]['default'] = default
                elif 'the default is' in docstr_lines[line].lower():
                    temp = re.split('the default is',
                                    docstr_lines[line], flags=re.IGNORECASE)
                    default = temp[1].replace(
                        '.', '').replace('\"', "'").strip()
                    docstr_lines[line] = temp[0].replace(',', '').strip()
                    section_dict[name]['default'] = default
                else:
                    section_dict[name]['WARNING'] = 'parameter is optional, but no default value found'

            info += docstr_lines[line].strip() + ' '
            line += 1

        # add info to section dict
        section_dict[name]['info'] = info.strip()

        # if multiple variables were described together, they all have the same type, (default,) info
        if len(names) > 1:
            for n in names[1:]:
                section_dict[n] = section_dict[name]

    return section_dict


def generate_func(input_, indent=1):
    """
    Generates a dictionary describing info, parameters and returns of a function from its docstring.

    Parameters
    ----------
    input_ : function
        The function to be described.
    indent : int, optional
        Factor describing the indentation, by default 1, for functions inside a class 2.

    Returns
    -------
    func_dict : dict
        Dictionary that contains info, parameters and returns of a function.
    """
    # check if docstring exists and is not empty
    if input_.__doc__ and input_.__doc__.strip():
        # read out docstring from function
        docstr = input_.__doc__
        docstr_lines = docstr.split('\n')
        docstr_lines.append('')

        func_dict = {}

        # get function info from first line that is not empty
        l = 0
        info = ''
        while docstr_lines[l].strip() == '':
            l += 1
        while docstr_lines[l].strip() != '':
            info += docstr_lines[l].strip() + ' '
            l += 1
        func_dict['info'] = info.strip()

        # get parameters and returns for the function
        param_dict = {}
        return_dict = {}
        for i, line in enumerate(docstr_lines):
            # sections are recognized by their keyword and '----' in the following line
            if 'parameters' in line.lower() and '----' in docstr_lines[i+1]:
                # docstrings might have sections 'Parameters' and 'Other Paramters', both are added to the parameters dictionary
                param_dict.update(read_section(docstr_lines, i+2, indent))
            elif 'returns' in line.lower() and '----' in docstr_lines[i+1]:
                return_dict = read_section(docstr_lines, i+2, indent, is_para=False)
        func_dict['parameters'] = param_dict
        func_dict['returns'] = return_dict
        return func_dict

    else:
        return {'WARNING': 'No docstring or empty docstring'}


def generate(input_):
    """
    Generates a JSON interface for a function or class.

    Parameters
    ----------
    input_ : [class, function]
        Function or class to be described.

    Returns
    -------
    str
        JSON interface containing information about the function/class.
    """

    # function interface generation
    if inspect.isfunction(input_):
        full_dict = generate_func(input_)

    # class interface generation
    # generates function interface for each function in the class
    # function starting with '_' are ignored
    if inspect.isclass(input_):

        if input_.__doc__:
            info = ' '.join([x.strip()
                            for x in input_.__doc__.split('\n')]).strip()
        else:
            info = ''

        func_dict = {}
        func_list = [x for x in dir(input_) if not x.startswith('_')]
        for func in func_list:
            func_dict[func] = generate_func(getattr(input_, func), 2)
        full_dict = {'info': info, 'functions': func_dict}

    # returns json interface
    # use indent=4 for easily readable format
     #return json.dumps({input_.__name__: full_dict})#, indent=4)

    # returns dictionary
    return {input_.__name__: full_dict}
