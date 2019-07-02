from libraries import *


from bokeh.plotting import figure, show, output_file
from bokeh.transform import factor_cmap
from bokeh.palettes import brewer


def plot_block_number():

    df = pd.read_csv(r'C:\TFM\data\2018\2018.csv', header=0, delimiter=',', parse_dates=['Date'])
    df['Cnc_Tool_Number_RT'] = df['Cnc_Tool_Number_RT'].astype(str)
    hta = df['Cnc_Tool_Number_RT'].unique()
    hta.tolist()
    for tool in hta:
        print(tool)
    return
    p = figure(x_axis_type="datetime", plot_width=1000, plot_height=600,
               title="Ejecución de los bloques a lo largo del tiempo")
    p.xaxis.axis_label = 'Fecha'
    p.yaxis.axis_label = 'Numero de bloque'

    '''
    # Get the number of colors we'll need for the plot.
    colors = brewer["Spectral"][len(df.Cnc_Program_Name_RT.unique())]
    print(colors)

    # Create a map between factor and color.
    colormap = {i: colors[i] for i in df.Cnc_Program_Name_RT.unique()}

    # Create a list of colors for each value that we will be looking at.
    colors = [colormap[x] for x in df['Cnc_Program_Name_RT']]
    '''

    p.circle((df['Date']), df.Cnc_Program_BlockNumber_RT, fill_alpha=0.2, size=2.5)

    output_file(r'J:\TFM\SW\output_graphs\block_number.html',
                title="Ejecucion de bloques a lo largo del tiempo")

    show(p)
    del df
    gc.collect()


