# -*- coding: utf-8 -*-
'''
__author__ = "Rob Knight, Gavin Huttley, and Peter Maxwell"
__copyright__ = "Copyright 2007, The Cogent Project"
__credits__ = ["Rob Knight", "Peter Maxwell", "Gavin Huttley",
                    "Matthew Wakefield"]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Rob Knight"
__email__ = "rob@spot.colorado.edu"
__status__ = "Production"
This file contains the functions to load and manage the data.
'''

from libraries import *
import gc

PATH = r"C:\TFM\data"

selected_fields = ['Date', 'Axis_X_positionActualMCS_mm_d10000', 'Axis_Y_positionActualMCS_mm_d10000',
                   'Axis_Z_positionActualMCS_mm_d10000', 'Spindle_C_deg', 'Spindle_A_Deg', 'Cnc_Program_Name_RT',
                   'Cnc_Program_BlockNumber_RT', 'Cnc_Tool_Number_RT', 'Axis_X1_power_percent', 'Axis_Y_power_percent',
                   'Axis_Z_power_percent', 'Spindle_Power_percent', 'System_DAS_Chatter', 'System_DAS_SeveridadActualX',
                   'System_DAS_SeveridadActualY', 'Cnc_Override_Axis', 'Cnc_Override_Spindle', 'Cnc_IsCycleOn_RT']


def clean_data():

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
            df.dropna(subset=['Cnc_Program_Name_RT'], axis=0, inplace=True)

            try:
                new_text = df['Cnc_Program_Name_RT'].str.split(os.sep).str[-1]
                # print(new_text)
                df['Cnc_Program_Name_RT'] = new_text

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
            df.dropna(subset=['Cnc_Program_Name_RT'], axis=0, inplace=True)

            try:
                new_text = str(df['Cnc_Program_Name_RT'])
                new_text = zlib.adler32(new_text.encode('utf8'))
                df['Cnc_Program_Name_RT'] = str(new_text)

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
                new_text = pd.to_datetime(df['Date'].str[:-4])
                df['Date'] = new_text

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
                df['Month'] = df['Date'].apply(lambda x: x.split('-')[1])
                for i in set(df.Month):  # for classified by months files
                    filename = PATH + "\\" + item + "\\" + i + ".csv"
                    df.loc[df.Month == i].to_csv(filename, index=False, columns=cols)

            except Exception as ex:
                print(ex)

            del df
            gc.collect()


def load_data():
    df = pd.read_csv(r'J:\TFM\SW\BCK\data\2016\07.csv', header=0, delimiter=',')
    print(df['Cnc_Program_Name_RT'].isnull().equals(True))


def replace_program_name():

    PATH = r'C:\TFM\data\year'

    files = os.listdir(PATH)

    for file in files:

        pgName = str(file)

        file_path = PATH + "\\hide_" + file



        print(file)
        df = pd.read_csv(PATH + "\\" + file, header=0, delimiter=',', parse_dates=['Date'])
        pgm_name = df['Cnc_Program_Name_RT'].unique()
        pgm_name = pgm_name.tolist()

        # print(df['Cnc_Program_Name_RT'].apply(lambda x: str(zlib.adler32(x.encode('utf8')))))

        df['Cnc_Program_Name_RT'] = df['Cnc_Program_Name_RT'].apply(lambda x: str(zlib.adler32(x.encode('utf8'))))

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
            print(df[df['Cnc_IsCycleOn_RT'].isnull()])
            df['Cnc_IsCycleOn_RT'] = pd.to_numeric(df['Cnc_IsCycleOn_RT'], errors='coerce')
            df = df.dropna(subset=['Cnc_IsCycleOn_RT'])
            df['Cnc_IsCycleOn_RT'] = df['Cnc_IsCycleOn_RT'].astype(int)
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
    return df.loc[df['Cnc_Tool_Number_RT'] == row, 'TYP'].iloc[0]


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
            tool_table = df['Cnc_Tool_Number_RT'].unique()
            tool_table = tool_table.tolist()

            for tool in tool_table:
                valor = df2.loc[df2['Cnc_Tool_Number_RT'] == tool, 'TYP'].iloc[0]
                try:
                    df.loc[df['Cnc_Tool_Number_RT'].eq(tool), 'CNC_Operation_Code'] = valor
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

    files = os.listdir(path)

    for item in files:
        os.chdir(path)

        print(path + "\\" + item)

        all_filenames = [i for i in glob.glob('*.{}'.format(extension))]

        # combine all files in the list
        combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames])
        # export to csv
        combined_csv.to_csv("full_csv.csv", index=False, encoding='utf-8-sig')