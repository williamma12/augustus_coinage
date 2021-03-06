import pandas as pd
import BokehPlots as bp
import CleanData as cd
from bokeh.plotting import show
from bokeh.models import Range1d, HoverTool
from bokeh.palettes import linear_palette, viridis, grey
from bokeh.layouts import gridplot

def coinsFromDates(df, date_range, col_name='date'):
    '''
    Parameters
    ----------
    df : Pandas dataframe
        Dataframe containing coins and dates
    date_range : tuple
        Tuple of length two containing date range
    col_names : str
        Column name of dates
        
    Return
    ------
    Returns a dataframe containing only the rows that have the correct dates
    '''
    begin = date_range[0]
    end = date_range[1]
    return df.apply(lambda x: intWithinTupleRange(x[col_name], begin, end), axis=1)


def intWithinTupleRange(tup, begin, end):
    '''Checks if the integer is within the boundaries given'''
    in_range = False
    if len(tup) == 1:
        if tup[0] >= begin and tup[0]<= end:
            in_range = True
    elif len(tup) == 2:
        if tup[0] >= begin and tup[1]<= end:
            in_range = False
    else:
        in_range = False
    return in_range


def containKeyword(df, keys, col_names):
    '''
    Parameters
    ----------
    df : Pandas dataframe
        Dataframe containing coincs and column to look for keyword in
    keys : list
        list of strings to look for in each row of given column
    col_name : list
        list of columns of where to search for keyword in 'keys' list, respectively
    
    Return
    ------
    Returns a dataframe containing only rows that have the keyword in the given column
    '''
    def containIn(obj, key):
        if type(obj) == str:
            if key.lower() in obj.lower():
                return True
            else:
                return False
        else:
            for item in obj:
                if key.lower() in obj.lower():
                    return True
                else:
                    return False
    

    if len(keys) != len(col_names):
        raise ValueError('length of keys does not equal length of columns')
        
    for i, key in enumerate(keys):
        try:
            result = df[col_names[0]].str.contains(keys[0], na=False)
            df = df[result]
        except:
            raise ValueError('Missing keys')
    return df


def makeTitle(dates=[], subjects=[]):
    '''
    Parameters
    ----------
    dates : tuple
        tuple of length two with date range
    subject : list
        list of strings of the subjects
        
    Return
    ------
    Returns a string of an appropriate title
    
    Doctest
    -------
    >>> makeTitle([-44, -31], ['star'])
    "'Star' in coinage from 44BC to 31BC"
    '''
    result = ''
    if subjects:
        for i, sub in enumerate(subjects):
            result += "'" + sub[0].upper() + sub[1:] + "'"
            if len(subjects) > 1:
                if i != len(subjects)-1:
                    result += ', '
                if i == len(subjects) - 2:
                    result += 'and '
                    
        result += ' in coinage from '
    else:
        result += 'Coinage from '
    
    if dates:
        str_dates = []
        for date in dates:
            if date < 0:
                str_dates.append(str(abs(date)) + 'BC')
            else:
                str_dates.append(str(date) + 'BC')
        
        result += str_dates[0] + ' to ' + str_dates[1]
        
    return result


def makeCoinageStackedBar(df, x_col='mint', stack_col='denomination', 
        y_label='Location Counts', y_range=[], legend_location='top_right', 
        plot_size=('responsive',), colors=viridis, title='', sort_bars=True,
        sort_x=False, sort_stacks=True, stack_order=[]):
    '''
    '''
    bar_plot = bp.makeStackedBar(df, x_col, stack_col, sort_bars=sort_bars, 
            bars_ascending=False, sort_stacks=sort_stacks, stacks_agg='sum', 
            stacks_ascending=False, colors=colors, title=title, 
            plot_size=plot_size, sort_x=sort_x, stack_order=stack_order)

    bar_plot.yaxis.axis_label=y_label
    if y_range:
        bar_plot.y_range = Range1d(y_range[0], y_range[1], bounds=y_range)
    bar_plot.legend.location = legend_location
    bar_plot.add_tools(HoverTool(tooltips=[(stack_col, '@'+stack_col), 
                                           (stack_col + ' count', '@height'),
                                           (x_col + ' count', '@Sum')]))

    return bar_plot


def makeCoinageMap(df, title='', mint_col='mint', x_ranges=(-2.0e6, 5e6), y_ranges=(3.5e6, 7e6),
                   pt_size=lambda x: x, colors=grey, colors_ascending=False):
    '''
    '''
    counts = cd.prepareDataframeForMapping(df, col_name=mint_col)

    map_plot = bp.makeMap(counts, mint_col, 'Count', x_ranges=x_ranges, y_ranges=y_ranges, 
                          mintsFile='../GeoJSON/mints.geojson', path='../GeoJSON/', ext='html', 
                          pt_size=pt_size, colors_ascending=colors_ascending, palette=colors)
    return map_plot


if __name__ == "__main__":
        import doctest
        doctest.testmod()
