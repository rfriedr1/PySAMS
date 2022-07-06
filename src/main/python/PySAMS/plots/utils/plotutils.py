from config.logging_conf import logger

# set logger name to the name of the module
logger.name = __name__


def find_year_positions(dataframe):
    '''
    find in the dataframe the positions where a new year starts using the magazine names

    Args:
        dataframe: dataframe that holds the data, column 'magazine' must be present

    Returns:
        year_positions: list of all found positions as indices of the dataframe
    '''

    # list of names of the magazines that change with year
    years = ['MA15', 'MA16', 'MA17', 'MA18', 'MA19', 'MA20', 'MA21']
    year_positions = []
    for year in years:
        posdf = dataframe.loc[dataframe['magazine'].str.contains(year), 'magazine']
        if posdf.size > 0:
            pos = posdf.index[0]
        else:
            pos = 0
        year_positions.append(pos)
        logger.info('plot: found position of ' + year + ' at index = ' + str(pos))
    return year_positions


def find_revisions(dataframe):
    '''
    find in the dataframe the positions where a source revision happened using the magazine names
    of the first magazine after the revision

    Args:
        dataframe: dataframe that holds the data, column 'magazine' must be present

    Returns:
        revision_positions: list of all found positions as indices of the dataframe
    '''

    # list of names of the magazines that change with year
    magazines = ['MA141204', 'MA150213', 'MA150507', 'MA150722', 'MA151007', 'MA151112', 'MA160310',
                 'MA160616', 'MA161004', 'MA170117', 'MA170327', 'MA170602', 'MA170727', 'MA170830',
                 'MA171026', 'MA180109', 'MA180405']
    revision_positions = []
    for mag in magazines:
        posdf = dataframe.loc[dataframe['magazine'].str.contains(mag), 'magazine']
        if posdf.size > 0:
            pos = posdf.index[0]
        else:
            pos = 0
        revision_positions.append(pos)
        logger.info('plot: found position of revision ' + mag + ' at index = ' + str(pos))
    return revision_positions


def myformatter(**kwarg):
    '''
    this is a formatter for mpldatacorsor that shows more than just the x,y data
    '''
    label = 'My custom label at point ({x:.0f}, {y:.0f})'.format(**kwarg)
    return label
