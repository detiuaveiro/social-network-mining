#!/usr/bin/python3

import sys
import os
import re

# version according PEP-0440
# - N.NaM means alpha release M of version N.N
__version__ = '0.1a8'


def capture_def(line: str, fh: type(open)) -> dict:
    """ captures and parses a function definition
    **LIMITATION:**
    - no comment allowed within and at the end an function definition
    - only pylint conform code
    - sting context is not recognized (e.g. the character `->` or `,`, '=' or `:` may miss-interpreted)
    **SUPPORTED FUNCTION STYLES (Examples):**
    - `def func ( p1 : p1hint, pn : pnhint ) -> rhint :`
    - `def func ( p1 : type(h1), pn : type(hn) ) -> type(hr) :`
    **PROCEDURE STEPS:**
    - (STEP-1) get definition: `def\s+(.*)\s*`
    - (STEP-2) split func-with-params from return-hint: `(.*)->(.*)\\s*[:].*`
        -> right part is the *return-hint*
    - (STEP-3) split func-name and param-list: `(\\S+)\\s*[(]\\*(.*)\\s*[)]`
        -> left part is the *function-name*
    - (STEP-4) split param list: `split("\\s*[,]\\s*")`
    - (STEP-5) split param from hint: `split("\\s*[:]\\s*")`
    :param line: present line
    :param fh: file-handle, points to next line
    :return: dictionary containing information about the given subject or ( *None* = there is no 'def' keyword ) :
    - 'indent' (str) = indentation (string of spaces) to the left of the function
    - 'kind' (str) = kind of compound; always 'def'
    - 'name' (str) = function name or ( *None* = there is no name )
    - 'params' (list) = list of parameter names (in the right order); this include optional initializer-strings
    - 'types' (dict) = types of parameters
    """
    res = None

    # capture a function definition, even if it extends over several lines
    rr = re.search(r'^\s*(def|class)', line)
    if rr is not None:
        while True:
            rr = re.search(r'[:]\s*$', line)
            if rr is not None:
                break
            line += fh.readline()

    # parse function definition (keyword 'def')
    # (STEP-1) get definition
    # re.groups:  1:indent 2:kind  3:definition
    rr = re.search(r'^(\s*)(def|class)\s+(.*)\s*$', line, flags=re.DOTALL | re.MULTILINE)
    if rr is not None:
        res = {'indent': rr.group(1),   # 1: indention for function definition and doxygen text
               'kind': rr.group(2),   # 2: kind of compound definition (here always 'def')
               'name': None, 'params': [], 'types': {'': ''}}
        rest = rr.group(3)  # 3: function definition

        # (STEP-2a) split function-name from the rest
        # re.groups:     1:func-name 2:rest
        rr = re.match(r'^(\w+)\b\s*(.*)', rest, flags=re.DOTALL | re.MULTILINE)
        if rr is not None:
            res['name'] = rr.group(1)  # 1: function name
            rest = rr.group(2)

            # (STEP-2b) split func-params from return-hint
            # re.groups:     1:func-params               2:return-hint
            rr = re.match(r'^([(]\s*.*\s*[)])\s*[-][>]\s*(.*)\s*[:].*', rest, flags=re.DOTALL | re.MULTILINE)
            if rr is not None:
                rest = rr.group(1)  # 1: function parameters
                res['types'][''] = rr.group(2)  # 2: optional return type-hint

            # (STEP-3) extract param-list
            # re.groups:     1:params
            rr = re.match(r'^[(]\s*(.*)\s*[)].*', rest, flags=re.DOTALL | re.MULTILINE)
            if rr is not None:
                rest = rr.group(1)  # 2: parameter-list with optional type-hints (comma separated)
                if rest is not None and rest is not '':
                    # (STEP-4) split param list
                    params = re.split(r'\s*[,]\s*', rest, flags=re.DOTALL | re.MULTILINE)

                    # (STEP-5) split param from hint
                    # .. NOTE: [''] is added to ensure two list elements if there is no type-hint
                    params2 = []    # [0]=name; [1]=type-hint; [2]=initializer
                    for pp in params:
                        pp2 = (re.split(r'\s*[=]\s*', pp) + [''])[:2]   # separate initializer
                        pp2 = (re.split(r'\s*[:]\s*', pp2[0]) + [''])[:2] + [pp2[1]]    # separate type-hint
                        params2.append(pp2)
                    # assign 'params' name with optional initializer; 'types' mapping name to type
                    res['params'] = []
                    for [a, b, c] in params2:
                        res['params'].append(a if c is '' else '{}={}'.format(a, c))
                        res['types'][a] = b
                else:
                    pass  # ignored: no parameters
            else:
                pass  # (End Step-3) ignored: no parentheses
        else:
            pass  # (End Step-2a) ignored: no function-name
    else:
        pass  # (End Step-1) ignored: no compound definition
    return res


def capture_docstr(line: str, fh: type(open)) -> dict:
    """captures and parses a doc-string
    :param line: present line
    :param fh: file-handle, points to next line
    :return: dictionary containing information about the given subject or None:
    - 'lines' = (list) docstring lines:
       - 'indent' = (str) indentation within the docstring
       - 'param' = (str) parameter name OR '' for return OR None if undefined
       - 'text' = (str) remaining text
    - 'types' = (dict) types captured from the doc-string
    """
    res = {'lines': [], 'types': {}}

    # capture a doc-string, even if it extends over several lines
    rr = re.search(r'^(\s*)[ru]*"""(.*)$', line)
    if rr is not None:
        line = rr.group(1) + rr.group(2) + '\n'  # first line without leading triple-quotes
        while True:
            ll = {}
            rr = re.search(r'^(.*)"""\s*$', line)  # check for tailing triple-quotes
            if rr is not None:
                line = rr.group(1) + '\n'  # (last) line without leading triple-quotes
            rr2 = re.match(r'^(\s*)(.*)\n$', line)  # separate indent from the rest
            if rr2 is not None:
                ll['indent'] = rr2.group(1)
                ll['param'] = None
                line = rr2.group(2)
                rr2 = re.match(r'^[:](\w+[^:]*)[:]\s*(.*)', line)  # check for ':param ...'/':return:'
                if rr2 is not None:
                    g21 = rr2.group(1)
                    g22 = rr2.group(2)

                    rr3 = re.match(r'^[r]?type\s*(.*)\s*$', g21)
                    if rr3 is not None:
                        g31 = rr3.group(1)
                        res['types'][g31] = g22
                        line = None  # suppress this line from output
                    else:
                        param = re.sub(r'param\s*', '', g21)
                        param = re.sub(r'return', '', param)
                        ll['param'] = param
                        line = g22
            if line is not None:
                ll['text'] = line
                res['lines'].append(ll)
            if rr is not None:
                break
            line = fh.readline()

    return res


def perform_fh(fh: type(open)) -> None:
    """ perform filter on a given file handle
    converts python code to a doxygen convenient format.
    This contains the following work-around about the disadvantages at Doxygen v1.8.14:
    - function definition may contain type hints;
    - python docstrings are converted into regular doxygen format;
    - type annotation is included into the doxygen format (from type hints XOR docstring types);
    Output is written to standard output stream.
    Error messages are written to standard error stream.
    :param fh: input file handle
    :return: None
    """
    print('# generated by {} {}'.format(os.path.basename(__file__), __version__))
    for line in fh:
        by_pass = True

        # capture function definition
        fstr = capture_def(line, fh)
        # do only if a function definition has found
        if fstr is not None:
            # ensure that function-name exists, otherwise put an error-message 
            if fstr['name'] is not None:
                # only perform removing if there are type-hints
                if any(list(fstr['types'].values())):
                    params = ', '.join(fstr['params'])
                    func_str = '{}{} {}({}): # type-hints removed'.format(fstr['indent'], fstr['kind'], fstr['name'],
                                                                          params)
                else:
                    func_str = re.sub(r'\n$', '', line)  # no type-hints

                line = fh.readline()

                # capture doc-string
                dstr = capture_docstr(line, fh)

                # use the appropriate set-of-types
                types = fstr['types']
                if any(dstr['types'].values()) is True:
                    if any(fstr['types'].values()) is True:
                        print("{}: WARNING: type-hints are applied instead of docstring-types at '{} {}()'"
                              .format(fh.name, fstr['kind'], fstr['name']), file=sys.stderr)
                    else:
                        types = dstr['types']

                # iterate over lines of docstring
                for ii in range(len(dstr['lines'])):
                    comment = '#'
                    param = dstr['lines'][ii]['param']
                    text = dstr['lines'][ii]['text']
                    indent = dstr['lines'][ii]['indent']
                    if ii == 0:
                        comment = '##'
                    if param is None:
                        print('{}{} {}{}'.format(fstr['indent'], comment, indent, text))
                    else:
                        if param == '':
                            print(r'{}{} \return ({}) {}'.format(fstr['indent'], comment, types[param], text))
                        elif param in types:
                            print(r'{}{} \param {} ({}) {}'.format(fstr['indent'], comment, param, types[param], text))
                        else:
                            print("{}: WARNING: parameter '{}' unknown at '{} {}()' is not applied"
                                  .format(fh.name, param, fstr['kind'], fstr['name']), file=sys.stderr)

                print(func_str)
                if len(dstr['lines']) != 0:
                    by_pass = False
            else:
                print("{}: ERROR: unable to capture '{}'".format(fh.name(), line.rstrip()), file=sys.stderr)
        else:
            pass  # no function definition
        if by_pass is True:
            print(line, end='')


def main(file: str) -> None:
    """ filter main procedure
    For further details cf. perform_fh().
    :param file: input file name or '-' for input stream
    :return:
    """
    if file == '-':
        perform_fh(sys.stdin)
    else:
        try:
            with open(file, 'r') as fh:
                perform_fh(fh)
        except OSError as err:
            print("ERROR: can't open '{}' for read: {} (errno={})".format(err.filename, err.strerror, err.errno),
                  file=sys.stderr)


if __name__ == '__main__':
    if len(sys.argv) >= (1+1):
        main(sys.argv[1])
    else:
        pname = os.path.basename(__file__)
        print('{} {}\n\nUSAGE: {} <name>.py'.format(pname, __version__, pname), file=sys.stderr)

# EOF #
