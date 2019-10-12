"""
This script generates the online characterization included in the machine
"""
from libraries import *
from libraries.bridge import *

# This libraries only exists inside CNC
try:
    import pyjh
    pyjh.require('3.0')
    import jh
except Exception as ex:
    print(ex)
    print('Execution environment is not CNC\n')
    pass

import re

path = r'C:\TFM\pgm\92G10.H'
output_json = r'C:\TFM\data\characterization\online_output.json'


def find_tool_call(file_content, keyword=KEYWORD_TCALL):
    """
    This function gets all the calls for different tools
    :param file_content: Complete file text where the keyword has to be found.
    :param keyword: this value defines the word to match and find in the file.
    """

    cursor = 0
    keyword_position = []

    for line in file_content:
        if keyword in line:
            if cursor:
                keyword_position.append(cursor)
            else:
                cursor += 1
        cursor += 1

    keyword_position.append(cursor-1)

    return keyword_position


def operation_characterization():

    """
    Function to generate the characterization table in json format.
    """

    active_pgm = ''

    try:
        active_pgm = jh.ResPath(ACTIVE_PROGRAM_NAME)
    except Exception as ex:
        active_pgm = path
    with open(active_pgm, 'r') as f:
        file_content = f.readlines()

    element = find_tool_call(file_content)

    act_pgm_name = active_pgm.split(os.sep)[-1]
    act_pgm_name = zlib.adler32(act_pgm_name.encode('utf8'))

    idx_counter = 0
    operation_dict = {}
    last_number = element[-1]
    for index in element[:-1]:
        diccionario = {}
        words = file_content[index].split(KEYWORD_TCALL)

        bloque_1 = file_content[element[idx_counter]].split(KEYWORD_TCALL)[0]

        if idx_counter == len(element)-2:
            bloque_2 = file_content[element[idx_counter + 1]].split(KEYWORD_ENDPGM)[0]
        else:
            bloque_2 = file_content[element[idx_counter + 1]].split(KEYWORD_TCALL)[0]

        tool_number = words[1].split(' ')[0]
        try:
            operation_type = jh.Get(TYP_TABLE_PATH % tool_number)
        except Exception as ex:
            operation_type = -1
            print(ex)
            print('Execution environment is not CNC')

        diccionario['Program'] = act_pgm_name
        diccionario['Tool'] = tool_number
        diccionario['Blocks']=[bloque_1, bloque_2]
        diccionario['Operation'] = operation_type

        operation_dict[idx_counter+1] = diccionario
        idx_counter += 1

    dict_json = json.dumps(operation_dict)
    print(dict_json)
    with open(output_json, 'w') as outfile:
        json.dump(operation_dict, outfile, ensure_ascii=False, indent=4)

