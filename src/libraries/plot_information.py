from libraries import *


from bokeh.plotting import figure, show, output_file
from bokeh.transform import factor_cmap
from bokeh.palettes import viridis
from bokeh.models import CategoricalColorMapper, ColumnDataSource

def plot_block_number():
    """
    Function to plot the block numbers in a defined time period.
    """

    df = pd.read_csv(r'C:\TFM\data\2018\03.csv', header=0, delimiter=',', parse_dates=['Date'])
    # df['Cnc_Tool_Number_RT'] = df['Cnc_Tool_Number_RT'].astype(str)
    # hta = df['Cnc_Tool_Number_RT'].unique()
    # hta.tolist()
    # for tool in hta:
    #     print(tool)
    # return
    longitud = len(df.Cnc_Program_Name_RT.unique())

    group = df.groupby(by=['Cnc_Program_Name_RT', 'Date'])

    p = figure(x_axis_type="datetime", plot_width=1000, plot_height=600,
               title="Ejecución de los bloques a lo largo del tiempo")
    p.xaxis.axis_label = 'Fecha'
    p.yaxis.axis_label = 'Numero de bloque'

    # Get the number of colors we'll need for the plot.


    # Create a map between factor and color.
    # pallette = {i: colores[i] for i in df.Cnc_Program_Name_RT.unique()}
    # print(pallette)

    # Create a list of colors for each value that we will be looking at.
    # colors = [colormap[x] for x in df['Cnc_Program_Name_RT']]

    # print(source)
    p.circle((df['Date']), df.Cnc_Program_BlockNumber_RT, fill_alpha=0.2, size=2.5)

    output_file(r'C:\TFM\output\block_number.html',
                title="Ejecucion de bloques a lo largo del tiempo")

    show(p)
    del df
    gc.collect()


