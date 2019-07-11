from libraries import *
from libraries.bridge import *
from dtaidistance import dtw
from dtaidistance import dtw_visualisation as dtwvis
from dtaidistance import clustering

import gc
import matplotlib.pyplot as plt

output_path = r'C:\TFM\dtw\dtw%s.png'
output_path = r'C:\TFM\dtw\dtw_full.png'
output_matrix = r'C:\TFM\dtw\dtw_matrix%s.png'


def print_dtw(series_1, series_2, output_path):

    contador = 0
    series_1 = series_1
    series_2 = series_2
    # series_1 = series_1[:1200]
    # series_2 = series_2[:1200]
    # series_1 = np.split(series_1, 12)
    # series_2 = np.split(series_2, 12)

    # for i in range(len(series_1)):
    #     path = dtw.warping_path(series_1[i], series_2[i])
    #     dtwvis.plot_warping(series_1[i], series_2[i], path, filename=output_path % contador)
    #     contador +=1

    path = dtw.warping_path(series_1, series_2)
    dtwvis.plot_warping(series_1, series_2, path, filename=output_path)




def print_dtw_matrix(series_1, series_2, output_matrix):

    contador = 0
    series_1 = series_1[:1200]
    series_2 = series_2[:1200]
    series_1 = np.split(series_1, 12)
    series_2 = np.split(series_2, 12)

    for i in range(len(series_1)):
        d, paths = dtw.warping_paths(series_1[i], series_2[i], window=25, psi=5)
        best_path = dtw.best_path(paths)
        dtwvis.plot_warpingpaths(series_1[i], series_2[i], paths, best_path, filename=output_matrix % contador)
        contador += 1

# def plot_pattern(series_1, series_2):
#
#     s1 = figure(x_axis_type="datetime", plot_width=1000, plot_height=600,
#                title="Ejecución de los bloques a lo largo del tiempo")
#     s1.xaxis.axis_label = 'Fecha'
#     s1.yaxis.axis_label = 'Carga del cabezal'
#
#     s2 = figure(x_axis_type="datetime", plot_width=1000, plot_height=600,
#                 title="Ejecución de los bloques a lo largo del tiempo")
#     s2.xaxis.axis_label = 'Fecha'
#     s2.yaxis.axis_label = 'Carga del cabezal'
#
#     s1.line((series_1[DATE]), series_1[SPINDLE_LOAD], fill_alpha=0.2, size=2.5)
#     s2.line((series_2[DATE]), series_2[SPINDLE_LOAD], fill_alpha=0.2, size=2.5)
#
#     output_file(r'C:\TFM\dtw\pattern.html',
#                 title="Ejecucion de bloques a lo largo del tiempo")
#
#     p = vplot(s1, s2)
#     show(p)
#     gc.collect()




def get_times():

    aux_file_path = r'C:\TFM\auxdata\hist.csv'
    data_path = r'C:\TFM\data\2018\2018.csv'

    df_aux = pd.read_csv(aux_file_path, header=0, delimiter=',', parse_dates=[SEGMENT_BEGIN, SEGMENT_END])
    df_data = pd.read_csv(data_path, header=0, delimiter=',', parse_dates=[DATE])

    # print(df_aux[SEGMENT_BEGIN, SEGMENT_END][df_data[OPERATION_ID_NUMBER] == 4])

    op_no = 8
    program_number = 1108805036

    begin_date = (df_aux[(df_aux[OPERATION_ID_NUMBER] == op_no)
                         & (df_aux[PROGRAM_NAME] == program_number)][SEGMENT_BEGIN])
    end_date = (df_aux[(df_aux[OPERATION_ID_NUMBER] == op_no)
                       & (df_aux[PROGRAM_NAME] == program_number)][SEGMENT_END])

    data_index = begin_date.index
    print(data_index)
    return
    series1_begin = begin_date[data_index[0]]
    series1_end = end_date[data_index[0]]
    series2_begin = begin_date[data_index[1]]
    series2_end = end_date[data_index[1]]

    series_1 = df_data.loc[(df_data[DATE] >= series1_begin) & (df_data[DATE] <= series1_end)]
    series_2 = df_data.loc[(df_data[DATE] >= series1_begin) & (df_data[DATE] <= series1_end)]

    df_spload_1 = series_1[SPINDLE_LOAD]
    df_spload_2 = series_2[SPINDLE_LOAD]

    # df_spload_1.plot.line()
    # df_spload_2.plot.line()

    # ax = plt.gca()
    # series_1.plot(kind='line', x=DATE, y=SPINDLE_LOAD, color='blue', ax=ax)
    # series_2.plot(kind='line', x=DATE, y=SPINDLE_LOAD, color='red', ax=ax)
    # plt.show()

    df_spload_1 = df_spload_1.values
    df_spload_2 = df_spload_2.values
    print_dtw(df_spload_1, df_spload_2, output_path)
    print_dtw_matrix(df_spload_1, df_spload_2, output_matrix)


def get_cluster():

    series = []
    aux_file_path = r'C:\TFM\auxdata\hist_protected.csv'
    data_path = r'C:\TFM\data\2018\2018.csv'

    hierarchical_plot = r'C:\TFM\dtw\hierarchical_cluster.png'
    linkage_plot = r'C:\TFM\dtw\linkage_cluster.png'

    df_aux = pd.read_csv(aux_file_path, header=0, delimiter=',', parse_dates=[SEGMENT_BEGIN, SEGMENT_END])
    df_data = pd.read_csv(data_path, header=0, delimiter=',', parse_dates=[DATE])

    # print(df_aux[SEGMENT_BEGIN, SEGMENT_END][df_data[OPERATION_ID_NUMBER] == 4])

    op_no = 12
    program_number = 1108805036

    # df1 = df[(df.a != -1) & (df.b != -1)]
    # begin_date = (df_aux.loc[(df_aux[OPERATION_ID_NUMBER] == op_no)][SEGMENT_BEGIN])

    begin_date = (df_aux[(df_aux[OPERATION_ID_NUMBER] == op_no)
                        & (df_aux[PROGRAM_NAME] == program_number)][SEGMENT_BEGIN])
    end_date = (df_aux[(df_aux[OPERATION_ID_NUMBER] == op_no)
                       & (df_aux[PROGRAM_NAME] == program_number)][SEGMENT_END])

    data_index = begin_date.index

    # data_index = data_index[:30]

    for item in data_index:
        if item > YEAR_INDEX_LIMIT:
            break
        else:
            series_begin = begin_date[item]
            series_end = end_date[item]
            aux_series = df_data.loc[(df_data[DATE] >= series_begin) & (df_data[DATE] <= series_end)]
            if not aux_series.empty:
                df_spload = aux_series[SPINDLE_LOAD]
                df_spload = np.array(df_spload)
                series.append(df_spload)

    # Custom Hierarchical clustering
    model1 = clustering.Hierarchical(dtw.distance_matrix_fast, {})
    cluster_idx = model1.fit(series)

    try:
        # Augment Hierarchical object to keep track of the full tree
        model2 = clustering.HierarchicalTree(model1)
        cluster_idx = model2.fit(series)
        model2.plot(hierarchical_plot, show_tr_label=True)
    except Exception as ex:
        print(ex)
    # SciPy linkage clustering
    try:
        model3 = clustering.LinkageTree(dtw.distance_matrix_fast, {})
        cluster_idx = model3.fit(series)
        model3.plot(linkage_plot, show_tr_label=True)
    except Exception as ex:
        print(ex)

