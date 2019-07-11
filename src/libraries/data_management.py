# -*- coding: utf-8 -*-
'''
This file contains the functions to load and manage the data.
'''

from libraries import *
from libraries.bridge import *
import gc

PATH = r"C:\TFM\data"

selected_fields = [DATE, AXIS_X_POS, AXIS_Y_POS, AXIS_Z_POS, SPDL_C_POS, SPDL_A_POS, PROGRAM_NAME, PROG_BLK_NUM,
                   AXIS_X_LOAD, AXIS_Y_LOAD, AXIS_Z_LOAD, SPINDLE_LOAD, CHATTER_EXIST, SEVERIDAD_X, SEVERIDAD_Y,
                   AXIS_OVERRIDE, SPINDLE_OVERRIDE, CYCLE_IS_ON]

# selected_new_fields = [DATE, PROGRAM_NAME, PROG_BLK_NUM, SPINDLE_LOAD, TOOL_NUMBER, OPERATION_CODE]
selected_new_fields = [PROGRAM_NAME, PROG_BLK_NUM, TOOL_NUMBER, OPERATION_CODE]

def clean_data():

    file_path = r'C:\TFM\data\weka\2018.csv'


    with open(file_path, "r") as f:
        reader = csv.reader(f)
        i = next(reader)

        delete_list = [x for x in i if x not in selected_fields]

        df = pd.read_csv(file_path, header=0, delimiter=',')

        for colName in delete_list:
            try:
                del df[colName]
            except KeyError as ke:
                print(ke)
                pass

        df.to_csv(file_path, index=False)
        del df
        gc.collect()

    return

    folders = os.listdir(PATH)

    for item in folders:
        files = os.listdir(PATH + "\\" + item)
        for file in files:

            file_path = str(PATH) + "\\" + str(item) + "\\" + str(file)
            print(file_path)
            delete_list = []

            with open(file_path, "r") as f:
                reader = csv.reader(f)
                i = next(reader)

                delete_list = [x for x in i if x not in selected_fields]

                df = pd.read_csv(PATH + "\\" + item + "\\" + file, header=0, delimiter=',')

                for colName in delete_list:
                    try:
                        del df[colName]
                    except KeyError:
                        pass

                '''
                for colName in selected_fields:
                    if colName == 'Cnc_Program_Name_RT':
                        df.dropna(subset=[colName], axis=0, inplace=True)
                        try:
                            new_text = df[colName].str.split(os.sep).str[-1]
                            # print(new_text)
                            df[colName] = new_text
                        except:
                            pass
                '''

                df.to_csv(file_path, index=False)
                del df
                gc.collect()


def join_csv_files():

    extension = 'csv'
    folders = os.listdir(PATH)

    for item in folders:
        os.chdir(PATH + "\\" + item)

        print(PATH + "\\" + item)

        all_filenames = [i for i in glob.glob('*.{}'.format(extension))]

        # combine all files in the list
        combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames])
        # export to csv
        combined_csv.to_csv("combined_csv.csv", index=False, encoding='utf-8-sig')


def split_program_name():

    folders = os.listdir(PATH)

    for item in folders:
        files = os.listdir(PATH + "\\" + item)
        for file in files:

            file_path = str(PATH) + "\\" + str(item) + "\\" + str(file)
            print(file_path)

            df = pd.read_csv(PATH + "\\" + item + "\\" + file, header=0, delimiter=',')
            df.dropna(subset=[PROGRAM_NAME], axis=0, inplace=True)

            try:
                new_text = df[PROGRAM_NAME].str.split(os.sep).str[-1]
                # print(new_text)
                df[PROGRAM_NAME] = new_text

            except:
                pass

            df.to_csv(file_path, index=False)
            del df
            gc.collect()


def hide_program_name():

    folders = os.listdir(PATH)

    for item in folders:
        files = os.listdir(PATH + "\\" + item)
        for file in files:

            file_path = str(PATH) + "\\" + str(item) + "\\" + str(file)
            print(file_path)

            df = pd.read_csv(PATH + "\\" + item + "\\" + file, header=0, delimiter=',')
            df.dropna(subset=[PROGRAM_NAME], axis=0, inplace=True)

            try:
                new_text = str(df[PROGRAM_NAME])
                new_text = zlib.adler32(new_text.encode('utf8'))
                df[PROGRAM_NAME] = str(new_text)

            except Exception as ex:
                print(ex)
                pass

            df.to_csv(file_path, index=False)
            del df
            gc.collect()


def update_time():

    folders = os.listdir(PATH)

    for item in folders:
        files = os.listdir(PATH + "\\" + item)
        for file in files:

            file_path = str(PATH) + "\\" + str(item) + "\\" + str(file)
            print(file_path)

            df = pd.read_csv(PATH + "\\" + item + "\\" + file, header=0, delimiter=',')
            # df.dropna(subset=['Date'], axis=0, inplace=True)

            try:
                new_text = pd.to_datetime(df[DATE].str[:-4])
                df[DATE] = new_text

            except Exception as ex:
                print(ex)

            df.to_csv(file_path, index=False)
            del df
            gc.collect()


def split_csv_by_months():
    folders = os.listdir(PATH)

    for item in folders:
        files = os.listdir(PATH + "\\" + item)
        for file in files:
            file_path = str(PATH) + "\\" + str(item) + "\\" + str(file)
            print(file_path)

            df = pd.read_csv(PATH + "\\" + item + "\\" + file, header=0, delimiter=',')
            cols = df.columns
            try:
                df['Month'] = df[DATE].apply(lambda x: x.split('-')[1])
                for i in set(df.Month):  # for classified by months files
                    filename = PATH + "\\" + item + "\\" + i + ".csv"
                    df.loc[df.Month == i].to_csv(filename, index=False, columns=cols)

            except Exception as ex:
                print(ex)

            del df
            gc.collect()


def load_data():
    df = pd.read_csv(r'J:\TFM\SW\BCK\data\2016\07.csv', header=0, delimiter=',')
    print(df[PROGRAM_NAME].isnull().equals(True))


def replace_program_name():

    PATH = r'C:\TFM\data\year'

    files = os.listdir(PATH)

    for file in files:

        pgName = str(file)

        file_path = PATH + "\\hide_" + file



        print(file)
        df = pd.read_csv(PATH + "\\" + file, header=0, delimiter=',', parse_dates=[DATE])
        pgm_name = df[PROGRAM_NAME].unique()
        pgm_name = pgm_name.tolist()

        # print(df['Cnc_Program_Name_RT'].apply(lambda x: str(zlib.adler32(x.encode('utf8')))))

        df[PROGRAM_NAME] = df[PROGRAM_NAME].apply(lambda x: str(zlib.adler32(x.encode('utf8'))))

        df.to_csv(file_path, index=False)
        del df
        gc.collect()
        '''
        for name in pgm_name:
            try:

                # df.replace(name, str(zlib.adler32(name.encode('utf8'))))
            except Exception as ex:
                print(ex)

            return

            # print(name + " " + str(zlib.adler32(name.encode('utf8'))))

        df.to_csv(file_path, index=False)
        del df
        gc.collect()
        '''


def int_cycle_is_on():

    PATH = r'C:\TFM\data\year'

    files = os.listdir(PATH)

    for file in files:

        pgName = str(file)

        file_path = PATH + "\\" + file

        print(file)
        df = pd.read_csv(PATH + "\\" + file, header=0, delimiter=',', parse_dates=['Date'])
        # pgm_name = df['Cnc_IsCycleOn_RT'].unique()
        # pgm_name = pgm_name.tolist()

        # print(df['Cnc_Program_Name_RT'].apply(lambda x: str(zlib.adler32(x.encode('utf8')))))

        try:
            print(df[df[CYCLE_IS_ON].isnull()])
            df[CYCLE_IS_ON] = pd.to_numeric(df[CYCLE_IS_ON], errors='coerce')
            df = df.dropna(subset=[CYCLE_IS_ON])
            df[CYCLE_IS_ON] = df[CYCLE_IS_ON].astype(int)
            # df['Cnc_IsCycleOn_RT'] = df['Cnc_IsCycleOn_RT'].apply(lambda x: int(x) if type(x) is float else 0)
        except Exception as ex:
            print(ex)
            pass

        df.to_csv(file_path, index=False)
        del df
        gc.collect()


def get_tool_op(row):

    PATH = r'C:\TFM\tool\tool.csv'
    df = pd.read_csv(PATH, header=0, delimiter=',')
    return df.loc[df[TOOL_NUMBER] == row, 'TYP'].iloc[0]


def add_tool_operation():

    PATH = r'C:\TFM\data'
    PATH2 = r'C:\TFM\tool\tool.csv'

    folders = os.listdir(PATH)

    df2 = pd.read_csv(PATH2, header=0, delimiter=',')

    for item in folders:
        files = os.listdir(PATH + "\\" + item)
        for file in files:
            file_path = str(PATH) + "\\" + str(item) + "\\" + str(file)
            print(file_path)

            df = pd.read_csv(file_path, header=0, delimiter=',', parse_dates=['Date'])
            tool_table = df[TOOL_NUMBER].unique()
            tool_table = tool_table.tolist()

            for tool in tool_table:
                valor = df2.loc[df2[TOOL_NUMBER] == tool, 'TYP'].iloc[0]
                try:
                    df.loc[df[TOOL_NUMBER].eq(tool), OPERATION_CODE] = valor
                except Exception as ex:
                    print('Error: %s' % ex)

            '''
            for index, row in df.iterrows():
                # print(row['Cnc_Tool_Number_RT'], row['TYP'])
                valor = df2.loc[df2['Cnc_Tool_Number_RT'] == row['Cnc_Tool_Number_RT'], 'TYP'].iloc[0]
                df.loc[index, 'CNC_Operation_Code'] = valor
                print(valor)
            '''

            df.to_csv(file_path, index=False)
            del df
            gc.collect()


def join_all_years():

    extension = 'csv'
    path = r'C:\TFM\data\year'
    output_file = r'C:\TFM\data\outputcsv.csv'

    os.chdir(path)

    all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
    print(all_filenames)

    # combine all files in the list
    combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames])
    # export to csv
    combined_csv.to_csv(output_file, index=False, encoding='utf-8-sig')


def characterization_table():

    file_path = r'C:\TFM\data\2018\10.csv'
    output_file_csv = r'C:\TFM\data\output_2018_10.csv'
    output_file_json = r'C:\TFM\data\output_2018_10.json'
    output_file_txt = r'C:\TFM\data\output_2018_10.txt'

    df = pd.read_csv(file_path, header=0, delimiter=',', parse_dates=[DATE])
    grupos = df.groupby([PROGRAM_NAME, TOOL_NUMBER]).apply(lambda x: x[PROG_BLK_NUM]
                                                           .unique().tolist())

    print(type(grupos))
    print(type(grupos.to_dict(OrderedDict)))
    print(str(grupos))

    f = open(output_file_txt, 'w+')
    f.writelines(str(grupos))
    f.close()



    # dict_df = pd.DataFrame.from_dict(grupos, orient='index')
    # df.groupby(['A']).apply(lambda x: x['B'].tolist()).to_dict()
    grupos.to_csv(output_file_csv, index=False, encoding='utf-8-sig')
    grupos.to_json(output_file_json)


def split_tool_program_name():
    file_path = r'C:\TFM\auxdata\hist.csv'

    df = pd.read_csv(file_path, header=0, delimiter=',')
    df.dropna(subset=[PROGRAM_TOOL], axis=0, inplace=True)

    try:
        new_text = df[PROGRAM_TOOL].str.split(os.sep).str[-1]
        program_pattern = new_text.str.split('-').str[0]
        program_path = new_text.str.split('-').str[1]
        tool_number = new_text.str.split('-').str[-1]
        # print(new_text)
        df[PROGRAM_TOOL] = program_pattern + '-' + program_path + '-' + tool_number

    except Exception as ex:
        print(ex)
        pass

    df.to_csv(file_path, index=False)
    del df
    gc.collect()


def split_aux_data_name():

    file_path = r'C:\TFM\auxdata\hist_protected.csv'

    df = pd.read_csv(file_path, header=0, delimiter=';')

    print(df[PROGRAM_NAME])
    # df.dropna(subset=[PROGRAM_NAME], axis=0, inplace=True)
    #
    try:
        new_text = df[PROGRAM_NAME].str.split(os.sep).str[-1]
        # print(new_text)
        df[PROGRAM_NAME] = new_text

    except:
        pass

    df.to_csv(file_path, index=False)
    del df
    gc.collect()


def hide_aux_data_name():

    path = file_path = r'C:\TFM\auxdata\hist_protected.csv'

    df = pd.read_csv(file_path, header=0, delimiter=',')
    pgm_name = df[PROGRAM_NAME].unique()
    pgm_name = pgm_name.tolist()

    # print(df['Cnc_Program_Name_RT'].apply(lambda x: str(zlib.adler32(x.encode('utf8')))))

    df[PROGRAM_NAME] = df[PROGRAM_NAME].apply(lambda x: str(zlib.adler32(x.encode('utf8'))))

    print(df[PROGRAM_NAME])
    df.to_csv(file_path, index=False)
    del df
    gc.collect()
