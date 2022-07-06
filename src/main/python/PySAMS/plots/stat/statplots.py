from config.logging_conf import logger
import matplotlib
# matplotlib.use('TkAgg')  # switch to a different backend in order to make the cursor mpldatawork
matplotlib.use('Qt5Agg')
from PyQt5.QtWidgets import QInputDialog
from database.pysamsdb import mydb
import matplotlib.pyplot as plt
import matplotlib.dates as dates
import mpldatacursor  # a datacursor for matlibplot, make sure to run the correct backend
import seaborn as sns  # by importing this all the matlibplots will look better
import math
import datetime
import plots.utils.plotutils as plotutils

# set logger name to the name of the module
logger.name = __name__

# turn interactive mode of matplotlib on so that the error "event loop is already running doesn't appear
plt.ion()

####################################################################################
# plot received samples per year
#####################################################################################
def plot_received() -> object:
    """
    create a plot of received samples per year
    use the rows from two database queries (function: query_db) in order to plot the data;

    Returns:
        None
    """

    def autolabel(rects):
        # attach some text labels below the top of the bars
        for rect in rects:
            height = rect.get_height()
            ax.text(rect.get_x() + rect.get_width() / 2., 1 * height - 150,
                    '%d' % int(height),
                    ha='center', va='bottom')

    titel = 'received C14 samples per year'
    logger.info('plot -- creating plot: ' + titel)
    
    query = """select year(project_t.in_date) AS x_data, count(sample_t.sample_nr) as y_data
                 from sample_t
                 INNER JOIN project_t ON sample_t.project_nr = project_t.project_nr
                 INNER JOIN user_t ON project_t.user_nr = user_t.user_nr
                 WHERE sample_t.type NOT IN ('oxa2', 'oxa1', 'blank')
                 AND sample_t.user_label NOT LIKE '%IAEA%'
                 AND year(in_date) > 2009
                 group by year(project_t.in_date)"""
    dataframe = mydb.querydb(query)

    # if enough data where provided, do the math and create the plot
    if (dataframe is not None) > 0:

        dataframe.dropna(inplace=True)

        # extract data from results of query
        logger.info('plot -- ' + titel + ': preparing data...')

        # calculate means and stdev
        logger.info('plot -- ' + titel + ': calculating statistics...')
        y_mean = dataframe['y_data'].mean()
        logger.info('plot -- ' + titel + ': mean dc13 = ' + str(y_mean))

        # create plot

        # set plot styles using seaborn
        sns.set()
        sns.set_style("dark")
        sns.set_palette('Set2')
        sns.despine()

        logger.info('plot -- ' + titel + ': creating plot...')
        fig, ax = plt.subplots()
        # received samples
        p1 = ax.bar(x='x_data', height='y_data', data=dataframe, label='received C14 samples', align='center',
                    color='green', alpha=0.5)
        ax.set_title(titel)
        ax.set_ylabel('number of C14 samples')
        ax.set_xlabel('year')
        ax.grid(True)
        # ax.axhline(y_mean, label=('received samples per year = ' + str(round(y_mean, 0))))
        ax.legend(loc='upper left')

        autolabel(p1)

        logger.info('plot -- ' + titel + ': saving figure to disk')
        path = 'pics/received_samples'
        fig.savefig(path + '.png', dpi=600)
        dataframe.to_csv(path + '.csv')

        plt.draw()
        plt.show()

        return fig

    else:
        # no records where given to the function
        logger.warning('plot -- ' + titel + ': no records received for plotting')


####################################################################################
# plot projects per year
#####################################################################################
def plot_projects_per_year() -> object:
    """
    create a plot of projects per year
    use the rows from two database queries (function: query_db) in order to plot the data;

    Returns:
        None
    """

    def autolabel(rects):
        # attach some text labels below the top of the bars
        for rect in rects:
            height = rect.get_height()
            ax.text(rect.get_x() + rect.get_width() / 2., 1 * height - 50,
                    '%d' % int(height),
                    ha='center', va='bottom')

    titel = 'projects per year'
    logger.info('plot -- creating plot: ' + titel)

    query = """select year(project_t.in_date) AS x_data, count(project_t.project_nr) as y_data
                 from project_t
                 WHERE year(in_date) > 2009
                 group by year(project_t.in_date)"""
    dataframe = mydb.querydb(query)

    # if enough data where provided, do the math and create the plot
    if (dataframe is not None) > 0:

        dataframe.dropna(inplace=True)

        # extract data from results of query
        logger.info('plot -- ' + titel + ': preparing data...')

        # calulcate means and stdev
        logger.info('plot -- ' + titel + ': calculating statistics...')
        y_mean = dataframe['y_data'].mean()
        logger.info('plot -- ' + titel + ': mean projects = ' + str(y_mean))

        # create plot

        # set plot styles using seaborn
        sns.set()
        sns.set_style("dark")
        sns.set_palette('Set2')
        sns.despine()

        logger.info('plot -- ' + titel + ': creating plot...')
        fig, ax = plt.subplots()
        # received samples
        p1 = ax.bar(x='x_data', height='y_data', data=dataframe, label='projects', align='center',
                    color='green', alpha=0.5)
        ax.set_title(titel)
        ax.set_ylabel('number of projects')
        ax.set_xlabel('year')
        ax.grid(True)
        # ax.axhline(y_mean, label=('received samples per year = ' + str(round(y_mean, 0))))
        ax.legend(loc='upper left')

        autolabel(p1)

        logger.info('plot -- ' + titel + ': saving figure to disk')
        path = 'pics/projects_per_year'
        fig.savefig(path + '.png', dpi=600)
        dataframe.to_csv(path + '.csv')

        plt.draw()
        plt.show()

        return fig

    else:
        # no records where given to the function
        logger.warning('plot -- ' + titel + ': no records received for plotting')

####################################################################################
# plot throughput
#####################################################################################
def plot_throughput() -> object:
    """
    create a plot of throughput data
    use the rows from two database queries (function: query_db) in order to plot the data;

    Returns:
        None
    """

    def autolabel(rects):
        # attach some text labels below the top of the bars
        for rect in rects:
            height = rect.get_height()
            ax.text(rect.get_x() + rect.get_width() / 2., 1 * height - 150,
                    '%d' % int(height),
                    ha='center', va='bottom')

    def autolabel_above(rects):
        # attach some text labels below the top of the bars
        for rect in rects:
            height = rect.get_height()
            ax.text(rect.get_x() + rect.get_width() / 2., 1 * height + 10,
                    '%d' % int(height),
                    ha='center', va='bottom')

    titel = 'measurements per year'
    logger.info('plot -- creating plot: ' + titel)

    query1 = """select CAST(SUBSTRING(magazine, 3, 2) AS UNSIGNED) AS x_data, count(sample_nr) as y_data
                        from target_v
                        WHERE type NOT IN ('oxa2', 'oxa1', 'blank')
                        AND user_label NOT LIKE '%IAEA%'
                        AND magazine LIKE 'MA%'
                        AND CAST(SUBSTRING(magazine, 3, 2) AS UNSIGNED) > '10'
                        AND fm IS NOT NULL
                        group by CAST(SUBSTRING(magazine, 3, 2) AS UNSIGNED)"""
    dataframe1 = mydb.querydb(query1)
    # all measured targets per year
    query2 = """select CAST(SUBSTRING(magazine, 3, 2) AS UNSIGNED) AS x_data, count(sample_nr) as y_data
                         from target_v
                         WHERE target_v.type NOT IN ('')
                         AND fm IS NOT NULL
                         AND magazine LIKE 'MA%'
                         AND CAST(SUBSTRING(magazine, 3, 2) AS UNSIGNED) > '10'
                         group by CAST(SUBSTRING(magazine, 3, 2) AS UNSIGNED)"""
    dataframe2 = mydb.querydb(query2)
    # number of measure EIL samples
    query3 = """select CAST(SUBSTRING(magazine, 3, 2) AS UNSIGNED) AS x_data, count(sample_nr) as y_data
                         from target_v
                         WHERE fm IS NOT NULL
                         AND magazine LIKE 'MA%'
                         AND CAST(SUBSTRING(magazine, 3, 2) AS UNSIGNED) > '10'
                         AND user_label LIKE '%EIL%'
                         group by CAST(SUBSTRING(magazine, 3, 2) AS UNSIGNED)"""
    dataframe3 = mydb.querydb(query3)

    # if enough data where provided, do the math and create the plot
    if (dataframe1 is not None) > 0:

        dataframe1.dropna(inplace=True)
        dataframe2.dropna(inplace=True)
        dataframe3.dropna(inplace=True)

        # extract data from results of query
        logger.info('plot -- ' + titel + ': preparing data...')

        # calulcate means and stdev
        logger.info('plot -- ' + titel + ': calculating statistics...')
        y_mean = dataframe2['y_data'].mean()
        logger.info('plot -- ' + titel + ': mean targets = ' + str(y_mean))

        # create plot
        # set plot styles using seaborn
        sns.set()
        sns.set_style("dark")
        sns.set_palette('Set2')
        sns.despine()

        logger.info('plot -- ' + titel + ': creating plot...')
        fig, ax = plt.subplots()
        # all targets
        p1 = ax.bar(x='x_data', height='y_data', data=dataframe2, label='all targets', align='center', color='blue',
                    alpha=0.5)
        # samples only
        p2 = ax.bar(x='x_data', height='y_data', data=dataframe1, label='samples only (no oxas, blanks or QC)', align='center', color='green',
                    alpha=0.5)
        # EIL samples
        p3 = ax.bar(x='x_data', height='y_data', data=dataframe3, label='express samples', align='center', color='red',
                    alpha=0.5)
        ax.set_title(titel)
        ax.set_ylabel('number of samples')
        ax.set_xlabel('year')
        ax.grid(True)
        # ax.axhline(y_mean, label=('mean measured samples per year = ' + str(round(y_mean, 0))), color='blue')
        ax.legend(loc='upper left')

        autolabel(p1)
        autolabel(p2)
        autolabel_above(p3)

        # start the data cursor of the mpldatacursor
        # mpldatacursor.datacursor(formatter=plotutils.myformatter)

        logger.info('plot -- ' + titel + ': saving figure to disk')
        path = 'pics/throughput'
        fig.savefig(path + '.png', dpi=600)
        dataframe1.to_csv(path + '.csv')
        path = 'pics/throughput_all'
        dataframe2.to_csv(path + '.csv')
        path = 'pics/throughput_express'
        dataframe3.to_csv(path + '.csv')

        plt.draw()
        plt.show()

        return fig

    else:
        # no records where given to the function
        logger.warning('plot -- ' + titel + ': no records received for plotting')


####################################################################################
# plot age precision
#####################################################################################
def plot_age_precision() -> object:
    """
    create a plot age precision data
    use the rows from two database queries (function: query_db) in order to plot the data;

    Returns:
        None
    """

    titel = 'precision of C14 ages'
    logger.info('plot -- creating plot: ' + titel)

    query = """ select target_t.c14_age AS x_data, target_t.c14_age_sig AS y_data, fm, fm_sig
                from target_t
                INNER JOIN sample_t ON target_t.sample_nr=sample_t.sample_nr
                WHERE sample_t.type NOT IN ('oxa2', 'oxa1', 'blank')
                AND target_t.magazine LIKE 'MA%'
                AND target_t.c14_age IS NOT NULL
                AND target_t.c14_age_sig IS NOT NULL
                AND target_t.c14_age < 15000
                AND target_t.C14_age >0
                AND target_t.c14_age_sig < 100"""
    dataframe = mydb.querydb(query)

    # if enough data where provided, do the math and create the plot
    if (dataframe is not None) > 0:

        dataframe.dropna(inplace=True)

        # extract data from results of query
        logger.info('plot -- ' + titel + ': preparing data...')

        # calulcate means and stdev
        logger.info('plot -- ' + titel + ': calculating statistics...')
        y_mean = dataframe['y_data'].mean()
        logger.info('plot -- ' + titel + ': mean dc13 = ' + str(y_mean))

        # create plot
        # set plot styles using seaborn
        sns.set()
        sns.set_style("dark")
        sns.set_palette('Set2')
        sns.despine()

        logger.info('plot -- ' + titel + ': creating plot...')
        fig, ax = plt.subplots()
        p1 = plt.scatter(x='x_data', y='y_data', data=dataframe, label='C14 age precision', color='green', alpha=0.1)
        ax.set_title(titel)
        ax.set_xlabel('C14 Age (years)')
        ax.set_ylabel('C14 Age Error (years)')
        ax.grid(True)
        # ax.axhline(y_mean, label=('mean precision = ' + str(round(y_mean, 0)) + ' years'), color='green',
        #                alpha=0.1)
        ax.legend(loc='upper left')

        # start the data cursor of the mpldatacursor
        mpldatacursor.datacursor()

        plt.draw()
        plt.show()
        fig.savefig('pics/age_precision.png')

        # draw a seaborn jointplot
        p3 = sns.jointplot(x="x_data", y="y_data", data=dataframe, kind="reg", height=7, ratio=3,
                           xlim=(-100, dataframe['x_data'].max()))
        x0, x1 = p3.ax_joint.get_xlim()
        p3.ax_joint.text(1000, 115, 'measured C14 ages')
        p3.ax_joint.plot([x0, x1], [y_mean, y_mean])

        p3.set_axis_labels("C14 age (years)", "C14 age precision (years)")
        plt.show()
        logger.info('plot -- ' + titel + ': saving figure to disk')
        p3.savefig('pics/age_precision_joint.png', dpi=600)

        return fig

    else:
        # no records where given to the function
        logger.warning('plot -- ' + titel + ': no records received for plotting')


####################################################################################
# plot oxas stdev per magazine
#####################################################################################
def plot_oxas_stdev_mag() -> object:
    """
    create a plot age precision data
    use the rows from two database queries (function: query_db) in order to plot the data;

    Returns:
        None
    """

    titel = 'oxas stdev per magazine 2014 - 2021'
    logger.info('plot -- creating plot: ' + titel)

    query = """SELECT magazine, s.type, count(t.fm) AS count, STD(t.fm) AS y_data, STD(t.dc13) AS y_data2
                      FROM target_t t
                      INNER JOIN sample_t s ON t.sample_nr=s.sample_nr
                      WHERE s.type LIKE "Oxa2"
                      AND fm IS NOT NULL
                      AND magazine LIKE "MA14%"
                      OR magazine LIKE "MA15%"
                      OR magazine LIKE "MA16%"
                      OR magazine LIKE "MA17%"
                      OR magazine LIKE "MA18%"
                      OR magazine LIKE "MA19%"
                      OR magazine LIKE "MA20%"
                      OR magazine LIKE "MA21%"
                      GROUP BY t.magazine, s.type
                      HAVING count(t.fm) > 1 AND STD(t.fm) < 0.01
                      ORDER BY magazine"""
    dataframe = mydb.querydb(query)

    # if enough data where provided, do the math and create the plot
    if (dataframe is not None) > 0:

        dataframe.dropna(inplace=True)

        # extract data from results of query
        logger.info('plot -- ' + titel + ': preparing data...')

        # since there are no x-data, generate those from the number of rows
        xdata = list(range(len(dataframe.index)))

        # calulcate means and stdev
        logger.info('plot -- ' + titel + ': calculating statistics...')
        # mean stdev fm
        y_mean = dataframe['y_data'].mean()
        # mean stdev d13C
        y2_mean = dataframe['y_data2'].mean()
        logger.info('plot -- ' + titel + ': mean dc13 = ' + str(y_mean))
        logger.info('plot -- ' + titel + ': mean dc13 = ' + str(y2_mean))

        # find years
        year_positions = plotutils.find_year_positions(dataframe)

        # create plot
        # set plot styles using seaborn
        sns.set()
        sns.set_style("dark")
        sns.set_palette('Set2')
        sns.despine()

        logger.info('plot -- ' + titel + ': creating plot...')
        fig, (ax, ax2) = plt.subplots(ncols=1, nrows=2)
        p1 = ax.scatter(x=xdata, y='y_data', data=dataframe, label='fm - oxas stdev per magazine', color='green',
                        alpha=0.5)
        ax.set_xlim(0, max(xdata))
        ax.set_ylim((0, 0.006))
        ax.set_title(titel)
        # ax.set_xlabel('Magazine')
        ax.set_ylabel('fm sigma')
        ax.grid(True)
        p2 = ax.axhline(y_mean, label=('mean = ' + str(round(y_mean, 4))), color='green', alpha=0.5)

        # insert vertical lines for the transitions of the years
        for pos in year_positions:
            ax.axvline(pos, color='y', alpha=0.5)

        ax.legend(loc='upper left')

        ax2.scatter(x=xdata, y='y_data2', data=dataframe, label='d13C - oxas stdev per magazine', color='green',
                    alpha=0.5)
        ax2.set_xlim(0, max(xdata))
        ax2.set_ylim((0, 0.006))
        ax2.set_xlabel('Magazine')
        ax2.set_ylabel('d13C sigma')
        ax2.grid(True)
        ax2.axhline(y2_mean, label=('mean = ' + str(round(y2_mean, 4))), color='green', alpha=0.5)

        # insert vertical lines for the transitions of the years
        for pos in year_positions:
            ax2.axvline(pos, color='y', alpha=0.5)

        ax2.legend(loc='upper left')

        # start the data cursor of the mpldatacursor
        mpldatacursor.datacursor(formatter=plotutils.myformatter)

        plt.draw()
        plt.show()

        logger.info('plot -- ' + titel + ': saving figure to disk')
        path = 'pics/oxas_stdev'
        fig.savefig(path + '.png', dpi=600)
        dataframe.to_csv(path + '.csv')

        return fig

    else:
        # no records where given to the function
        logger.warning('plot -- ' + titel + ': no records received for plotting')


####################################################################################
# plot age distribution
#####################################################################################
def plot_age_hist() -> object:
    """
    create a histogram of the age distribution of arch samples
    use the rows from two database queries (function: query_db) in order to plot the data;

    Returns:
        None
    """

    titel = 'ages of "arch" samples (from 2008 on)'
    logger.info('plot -- creating plot: ' + titel)

    query = """SELECT sample_t.c14_age AS x_data
                FROM sample_t
                INNER JOIN target_t ON sample_t.sample_nr = target_t.sample_nr
                WHERE type LIKE 'arch'
                AND sample_t.c14_age IS NOT NULL
                AND sample_t.c14_age < 10000
                AND sample_t.c14_age > -200
                # AND sample_t.material = 'bone'
                AND magazine LIKE 'MA%' """
    dataframe = mydb.querydb(query)

    # if enough data where provided, do the math and create the plot
    if (dataframe is not None) > 0:

        dataframe.dropna(inplace=True)

        # extract data from results of query
        logger.info('plot -- ' + titel + ': preparing data...')

        # calulcate means and stdev
        logger.info('plot -- ' + titel + ': calculating statistics...')
        x_mean = dataframe['x_data'].mean()
        logger.info(titel + ': mean = ' + str(x_mean))

        # create plot
        # set plot styles using seaborn
        sns.set()
        sns.set_style("dark")
        sns.set_palette('Set2')
        sns.despine()

        logger.info('plot -- ' + titel + ': creating plot...')
        fig, ax = plt.subplots()
        p = ax.hist(x='x_data', bins=50, data=dataframe, label='ages', histtype='bar', color='green',
                    alpha=0.5)
        ax.set_title(titel)
        ax.set_xlabel('C14 Age (years)')
        ax.set_ylabel('number of samples')
        ax.grid(True)
        # p2 = ax.axhline(x_mean, label=('mean = ' + str(round(y_mean,0))), color='green', alpha=0.5)
        ax.legend(loc='upper left')

        # start the data cursor of the mpldatacursor
        mpldatacursor.datacursor(formatter=plotutils.myformatter)

        plt.draw()
        plt.show()

        logger.info('plot -- ' + titel + ': saving figure to disk')
        path = 'pics/ages_hist'
        fig.savefig(path + '.png', dpi=600)
        dataframe.to_csv(path + '.csv')

        return fig

    else:
        # no records where given to the function
        logger.warning('plot -- ' + titel + ': no records received for plotting')


####################################################################################
# plot material distribution
#####################################################################################
def plot_material() -> object:
    """
    create a pyplot of the distribution of materials
    use the rows from two database queries (function: query_db) in order to plot the data;

    Returns:
        None
    """

    titel = 'sample material'
    logger.info('plot -- creating plot: ' + titel)

    query = """SELECT material AS label, year(graphitized) AS year, count(target_t.sample_nr) as y_data
                FROM sample_t
                INNER JOIN target_t ON sample_t.sample_nr = target_t.sample_nr
                WHERE type LIKE 'arch'
                AND material IS NOT NULL
                AND sample_t.c14_age IS NOT NULL
                AND magazine LIKE 'MA%'
                GROUP BY material, year(graphitized)"""
    dataframe = mydb.querydb(query)

    # if enough data where provided, do the math and create the plot
    if (dataframe is not None) > 0:

        # extract data from results of query
        logger.info('plot -- ' + titel + ': preparing data...')
        # filter data from specific years in order to avoid all data that have bad years entered
        # use the query command on the dataframe, "inplace" ensures that the dataframe is changed
        # that ther is no copy generated
        logger.info('filtering dataframe...')
        dataframe.query(
            'year == 2012 or year == 2013 or year == 2014 or year == 2015 or year == 2016 or year == 2017 or year == 2018 or year == 2019 or year == 2020 or year == 2021',
            inplace=True)
        dataframe.query('y_data > 1', inplace=True)
        logger.info(dataframe.head(5))
        # sort dataframe by year
        logger.info('sorting dataframe...')
        dataframe.sort_values(['year'], ascending=True)
        logger.info(dataframe.head(5))
        # reshape the dataframe so that the years are the columns
        logger.info('reshaping data...')
        dataframe_rs = dataframe.pivot(index='label', columns='year', values='y_data')
        # remove NaN rows
        dataframe_rs.dropna(axis=0, how='any', inplace=True)
        logger.info(dataframe_rs.head(5))
        # calculate fractions for every year
        logger.info('caluclating sums...')
        dataframesum = dataframe_rs.sum(axis=0, skipna=True)
        logger.info(dataframesum.head(5))
        logger.info('caluclating factions...')
        # now calculate fraction for Y-data and sums of the same year
        logger.info('calculating fractions and adding to dataframe...')
        dataframe_frac = dataframe_rs.divide(dataframesum, axis=1)
        # print(dataframe_frac.head(5))

        # create plot
        # set plot styles using seaborn
        sns.set()
        sns.set_style("dark")
        sns.set_palette('Set2')
        sns.despine()

        logger.info('plot -- ' + titel + ': creating plot...')
        ax = dataframe_frac.T.plot(kind='bar', stacked=True, sort_columns=False, colormap='Paired',
                                   title='material distibution')
        fig = ax.get_figure()
        ax.set_title(titel)
        ax.set_xlabel('year')
        ax.set_ylabel('faction of samples')
        ax.set_ylim(0,1)
        ax.grid(True)
        ax.legend(loc='center left', bbox_to_anchor=(0.99, 0.5))

        # start the data cursor of the mpldatacursor
        mpldatacursor.datacursor(formatter=plotutils.myformatter)

        plt.draw()
        plt.show()

        logger.info('plot -- ' + titel + ': saving figure to disk')
        path = 'pics/materials'
        fig.savefig(path + '.png', dpi=600)
        dataframe.to_csv(path + '.csv')

        return fig

    else:
        # no records where given to the function
        logger.warning('plot -- ' + titel + ': no records received for plotting')


####################################################################################
# plot various turnaround times as histogram
#####################################################################################
def plot_turnaround() -> object:
    """
    create histograms of the turnaround times of samples
    in_date->prep_end, prep_end->graphitized, graphitized->out_date, in_date->out_date,
    use the rows from two database queries (function: query_db) in order to plot the data;

    Returns:
        None
    """

    # dialog to ask for the magazine year
    # calculate todays year as a default year
    now = datetime.datetime.now()
    num, ok = QInputDialog.getInt(None, "Year of Measurement", "enter year (2-digits)", now.year - 2000, 10, 50, 1)
    if ok:
        search_mag = 'MA' + str(num) + '%'
        logger.info('dialog (year) -- ok: ' + search_mag)
    else:
        search_mag = 'MA16%'
        logger.info('dialog (year) -- not ok, use default: ' + search_mag)

    titel = 'turnaround (' + search_mag + ') in -> graph'
    logger.info('plot -- creating plot: ' + titel)

    query = """ select target_t.sample_nr, project_t.in_date, preparation_t.prep_end, target_t.graphitized, project_t.out_date,
                TIMESTAMPDIFF(day, project_t.in_date, preparation_t.prep_end) AS inprep_data,
                TIMESTAMPDIFF(day, preparation_t.prep_end, target_t.graphitized) AS prepgraph_data,
                TIMESTAMPDIFF(day, target_t.graphitized, project_t.out_date) AS graphout_data,
                TIMESTAMPDIFF(day, project_t.in_date, project_t.out_date) AS inout_data
                from target_t
                INNER JOIN sample_t ON target_t.sample_nr=sample_t.sample_nr
                INNER JOIN project_t ON sample_t.project_nr=project_t.project_nr
                INNER JOIN preparation_t ON sample_t.sample_nr=preparation_t.sample_nr
                INNER JOIN user_t on project_t.user_nr=user_t.user_nr
                WHERE sample_t.type NOT IN ('oxa2', 'oxa1', 'blank')
                AND user_label NOT LIKE '%IAEA%'
                AND user_label NOT LIKE '%HEI%'
                AND user_label NOT LIKE '%Pferd%'
                AND user_label NOT LIKE '%Baunach%'
                and last_name not in ("intern", "Levin", "Hoffmann", "Deininger", "Frank", "Fohlmeister")
                AND target_t.graphitized IS NOT NULL
                AND project_t.in_date IS NOT NULL
                AND preparation_t.prep_end IS NOT NULL
                AND project_t.out_date IS NOT NULL
                AND target_t.magazine LIKE "{0}"
                AND target_t.c14_age IS NOT NULL
                AND TIMESTAMPDIFF(day, project_t.in_date, preparation_t.prep_end) BETWEEN 0 AND 200
                AND TIMESTAMPDIFF(day, preparation_t.prep_end, target_t.graphitized) BETWEEN 0 AND 80
                AND TIMESTAMPDIFF(day, target_t.graphitized, project_t.out_date) BETWEEN 0 AND 100
                AND TIMESTAMPDIFF(day, project_t.in_date, project_t.out_date) BETWEEN 0 AND 200
                ORDER BY target_t.sample_nr
                """
    # insert search phrase into query string
    query_formatted = query.format(search_mag)
    logger.debug(query_formatted)

    dataframe = mydb.querydb(query_formatted)

    # if enough data where provided, do the math and create the plot
    if (dataframe is not None) > 0:

        dataframe.dropna(inplace=True)

        # extract data from results of query
        logger.info('plot -- ' + titel + ': preparing data...')

        # calulcate means and stdev
        # print('plot -- ' + titel + ': calculating statistics...')
        # x_mean = dataframe['x_data'].mean()
        # print(titel + ': mean = ' + str(x_mean))

        # create plots
        # set plot styles using seaborn
        sns.set()
        sns.set_style("dark")
        sns.set_palette('Set2')
        sns.despine()

        logger.info('plot -- ' + titel + ': creating plot...')

        fig = plt.figure(figsize=(9, 8))
        fig.suptitle('turnaround times')

        # hist: in_date->prep_end
        ax = fig.add_subplot(221)
        # determine the number if bins by the square root of the number of data
        ax.hist(x='inprep_data', bins=2*int(math.sqrt(dataframe['inprep_data'].count())), data=dataframe,
                label='in -> prep end',
                histtype='bar', color='green', alpha=0.5)
        ax.set_xlim(0, 125)
        # ax.set_title('in -> prep end')
        ax.set_ylabel('number of samples')
        ax.grid(True)
        ax.axvline(30, color='y', alpha=0.5, label='1 month')
        ax.axvline(60, color='y', alpha=0.5, label='2 month')
        ax.axvline(90, color='y', alpha=0.5, label='3 month')
        ax.legend(['in -> prep end'], loc='upper right', fancybox=False, frameon=True, facecolor='lightgreen')

        # hist: prep_end->graphitized
        ax2 = fig.add_subplot(222)
        ax2.hist(x='prepgraph_data', bins=2*int(math.sqrt(dataframe['prepgraph_data'].count())), data=dataframe,
                 label='prep end -> graphitized', histtype='bar', color='green', alpha=0.5)
        ax2.set_xlim(0, 65)
        # ax2.set_title('prep end -> graphitized')
        ax2.grid(True)
        ax2.axvline(30, color='y', alpha=0.5, label='1 month')
        ax2.axvline(60, color='y', alpha=0.5, label='2 month')
        ax2.axvline(90, color='y', alpha=0.5, label='3 month')
        ax2.legend(['prep end -> graph'], loc='upper right', fancybox=False, frameon=True, facecolor='lightgreen')

        # hist: graphitized->report
        ax3 = fig.add_subplot(223)
        ax3.hist(x='graphout_data', bins=2*int(math.sqrt(dataframe['graphout_data'].count())), data=dataframe,
                 label='graphitized -> report', histtype='bar', color='green', alpha=0.5)
        ax3.set_xlim(0, 65)
        # ax3.set_title('graphitized -> report')
        ax3.set_xlabel('days')
        ax3.set_ylabel('number of samples')
        ax3.grid(True)
        ax3.axvline(30, color='y', alpha=0.5, label='1 month')
        ax3.axvline(60, color='y', alpha=0.5, label='2 month')
        ax3.axvline(90, color='y', alpha=0.5, label='3 month')
        ax3.legend(['graph -> report'], loc='upper right', fancybox=False, frameon=True, facecolor='lightgreen')

        # hist: in_date->out_date (sum of all of the above)
        ax4 = fig.add_subplot(224)
        ax4.hist(x='inout_data', bins=2*int(math.sqrt(dataframe['inout_data'].count())), data=dataframe,
                 label='in -> report', histtype='bar', color='green', alpha=0.5)
        ax4.set_xlim(0, 200)
        # ax4.set_title('in -> report')
        ax4.set_xlabel('days')
        ax4.set_ylabel('number of samples')
        ax4.grid(True)
        ax4.axvline(30, color='y', alpha=0.5, label='1 month')
        ax4.axvline(60, color='y', alpha=0.5, label='2 month')
        ax4.axvline(90, color='y', alpha=0.5, label='3 month')
        ax4.axvline(120, color='y', alpha=0.5, label='4 month')
        ax4.legend(['in -> report'], loc='upper right', fancybox=False, frameon=True, facecolor='lightgreen')

        plt.draw()
        plt.show()

        logger.info('plot -- ' + titel + ': saving figure to disk')
        path = 'pics/turnaround_hist'
        fig.savefig(path + '.png', dpi=600)
        dataframe.to_csv(path + '.csv')

        return fig

    else:
        # no records where given to the function
        logger.warning('plot -- ' + titel + ': no records received for plotting')


####################################################################################
# plot number of express samples per year
#####################################################################################
def plot_express_samples() -> object:
    """
    create a histogram of the number of express samples per year
    use the rows from two database queries (function: query_db) in order to plot the data;

    Returns:
        None
    """

    titel = 'number of received express samples'
    logger.info('plot -- creating plot: ' + titel)

    query = """SELECT YEAR(in_date) AS year, count(sample_nr) AS y_data
                       FROM sample_t
                       INNER JOIN project_t ON sample_t.project_nr=project_t.project_nr
                       WHERE user_label like '%EIL%'
                       GROUP BY year
                       HAVING year > '2010'"""
    dataframe = mydb.querydb(query)

    # if enough data where provided, do the math and create the plot
    if (dataframe is not None) > 0:

        dataframe.dropna(inplace=True)

        # extract data from results of query
        logger.info('plot -- ' + titel + ': preparing data...')

        # calulcate means and stdev
        # print('plot -- ' + titel + ': calculating statistics...')
        # x_mean = dataframe['x_data'].mean()
        # print(titel + ': mean = ' + str(x_mean))

        # create plot
        # set plot styles using seaborn
        sns.set()
        sns.set_style("dark")
        sns.set_palette('Set2')
        sns.despine()

        logger.info('plot -- ' + titel + ': creating plot...')
        ax = dataframe.plot.bar(x='year',color='green', alpha=0.5)
        fig = ax.get_figure()
        #fig, ax = plt.subplots()
        #p = ax.bar(left='year', height='y_data', data=dataframe, label='number of express samples', color='green', alpha=0.5)
        # ax.set_xlim(0, 200)
        ax.set_title(titel)
        ax.set_xlabel('year')
        ax.set_ylabel('number of express samples')
        ax.grid(True)
        ax.legend(['number of express samples'], loc='upper left')

        # # start the data cursor of the mpldatacursor
        # datacursor()

        plt.draw()
        plt.show()

        logger.info('plot -- ' + titel + ': saving figure to disk')
        path = 'pics/express_samples'
        fig.savefig(path + '.png', dpi=600)
        dataframe.to_csv(path + '.csv')

        return fig

    else:
        # no records where given to the function
        logger.warning('plot -- ' + titel + ': no records received for plotting')


####################################################################################
# plot bone collagen distribution
#####################################################################################
def plot_bone_collagen() -> object:
    """
    create a histogram of the collagen distribution of bone samples
    use the rows from two database queries (function: query_db) in order to plot the data;

    Returns:
        None
    """

    titel = 'bone collagen content (all years > 2010)'
    logger.info('plot -- creating plot: ' + titel)

    query = """SELECT sample_t.sample_nr, sample_t.material, preparation_t.weight_start, preparation_t.weight_end, (preparation_t.weight_end / preparation_t.weight_start * 100) AS y_data
               FROM sample_t
               INNER JOIN preparation_t ON sample_t.sample_nr = preparation_t.sample_nr
               WHERE material = 'bone'
               AND (preparation_t.weight_end/preparation_t.weight_start) > 0
               AND preparation_t.weight_end > 0
               AND preparation_t.weight_start > 0
               AND (preparation_t.weight_end / preparation_t.weight_start) < 0.2
               AND year(preparation_t.prep_end) > '2010'"""
    dataframe = mydb.querydb(query)

    # if enough data where provided, do the math and create the plot
    if (dataframe is not None) > 0:

        dataframe.dropna(inplace=True)

        # extract data from results of query
        logger.info('plot -- ' + titel + ': preparing data...')

        # calulcate means and stdev
        logger.info('plot -- ' + titel + ': calculating statistics...')
        y_mean = dataframe['y_data'].mean()
        logger.info(titel + ': mean = ' + str(y_mean))

        # create plot
        # set plot styles using seaborn
        sns.set()
        sns.set_style("dark")
        sns.set_palette('Set2')
        sns.despine()

        logger.info('plot -- ' + titel + ': creating plot...')
        fig, ax = plt.subplots()
        ax.hist(x='y_data', bins=50, data=dataframe, label='ages', histtype='bar', color='green', alpha=0.5)
        ax.set_title(titel)
        ax.set_xlabel('bone collagen %')
        ax.set_ylabel('number of samples')
        ax.grid(True)
        # mayor_ticks = np.arange(0, 20, 5)
        # ax.set_xticks(mayor_ticks)
        # minor_ticks = np.arange(0, 5, 0.5)
        # ax.set_xticks(minor_ticks, minor=True)
        # ax.grid(b=True, which='minor', color='w', linewidth=0.5)
        ax.axvline(0.5, label='0.5% cutoff', color='green', alpha=0.5)
        ax.legend(loc='upper right')

        # start the data cursor of the mpldatacursor
        # datacursor()

        plt.draw()
        plt.show()

        logger.info('plot -- ' + titel + ': saving figure to disk')
        path = 'pics/bone_collagen_hist'
        fig.savefig(path + '.png', dpi=600)
        dataframe.to_csv(path + '.csv')

        return fig

    else:
        # no records where given to the function
        logger.warning('plot -- ' + titel + ': no records received for plotting')


####################################################################################
# plot age precision vs time for different C14 ages
#####################################################################################
def plot_age_precision_time() -> object:
    """
    create plots of age precision over time for various time intervals
    use the rows from two database queries (function: query_db) in order to plot the data;

    Returns:
        None
    """

    titel = 'precison of C14 ages vs time'
    logger.info('plot -- creating plot: ' + titel)

    query = """SELECT p.project_nr, p.user_nr, u.last_name, t.sample_nr, t.graphitized AS x_data, t.c14_age AS c14_age, t.c14_age_sig AS y_data
               FROM target_t t
               INNER JOIN sample_t s ON t.sample_nr=s.sample_nr
               INNER JOIN project_t p ON s.project_nr=p.project_nr
               INNER JOIN user_t u ON p.user_nr=u.user_nr
               WHERE t.graphitized IS NOT NULL
               AND t.c14_age IS NOT NULL
               AND t.c14_age_sig < 100
               AND t.graphitized > '2011-01-01'"""
    dataframe = mydb.querydb(query)

    # if enough data where provided, do the math and create the plot
    if (dataframe is not None) > 0:

        dataframe.dropna(inplace=True)

        # extract data from results of query
        logger.info('plot -- ' + titel + ': preparing data...')
        # filter data for certain c14 age ranges
        # 1000-3000 years
        logger.info('plot -- ' + titel + ': 1000-5000 age range')
        df1 = dataframe[(dataframe['c14_age'] > 1000) & (dataframe['c14_age'] < 5000)]
        logger.info(df1.head(3))
        # 3000-5000 years
        logger.info('plot -- ' + titel + ': 5000-10000 age range')
        df2 = dataframe[(dataframe['c14_age'] > 5000) & (dataframe['c14_age'] < 10000)]
        logger.info(df2.head(3))
        # 10000-15000 years
        logger.info('plot -- ' + titel + ': 10 000 - 20 000 age range')
        df3 = dataframe[(dataframe['c14_age'] > 10000) & (dataframe['c14_age'] < 20000)]
        logger.info(df3.head(3))
        # 30000-40000 years
        logger.info('plot -- ' + titel + ': 20 000 - 40 000 age range')
        df4 = dataframe[(dataframe['c14_age'] > 20000) & (dataframe['c14_age'] < 40000)]
        logger.info(df4.head(3))

        # calulcate means and stdev
        logger.info('plot -- ' + titel + ': calculating statistics...')
        # mean c14age_sigma
        y_mean1 = df1['y_data'].mean()
        logger.info('plot -- ' + titel + ': mean c14age_sigma (1000-5000) = ' + str(y_mean1))
        y_mean2 = df2['y_data'].mean()
        logger.info('plot -- ' + titel + ': mean c14age_sigma (5000-10000) = ' + str(y_mean2))
        y_mean3 = df3['y_data'].mean()
        logger.info('plot -- ' + titel + ': mean c14age_sigma (10000-20000) = ' + str(y_mean3))
        y_mean4 = df4['y_data'].mean()
        logger.info('plot -- ' + titel + ': mean c14age_sigma (20000-40000) = ' + str(y_mean4))

        # create plot
        # set plot styles using seaborn
        sns.set()
        sns.set_style("dark")
        sns.set_palette('Set2')
        sns.despine()

        logger.info('plot -- ' + titel + ': creating plot...')
        fig, (ax, ax2, ax3) = plt.subplots(ncols=1, nrows=3)
        df1.plot(ax=ax, x='x_data', y='y_data', style='.', alpha=0.8, label='C14 age = 1000 - 5000 years')
        df2.plot(ax=ax2, x='x_data', y='y_data', style='.', alpha=0.8, label='C14 age = 5000 - 10000 years')
        df3.plot(ax=ax3, x='x_data', y='y_data', style='.', alpha=0.8, label='C14 age = 10 000 - 20 000 years')
        # df4.plot(ax=ax4, x='x_data', y='y_data', style='.', alpha=0.8, label='C14 age = 20 000 - 30 000 years')

        # ax.set_xlim(0, df1['x_data'].max())
        ax.set_ylim((10, 40))
        ax.set_title(titel)
        ax.set_ylabel('C14-age Sigma')
        ax.grid(True)
        # p2 = ax.axhline(y_mean1, label=('mean = ' + str(round(y_mean1, 4))), color='green', alpha=0.5)
        ax.legend(loc='upper left')

        # ax2.set_xlim(0, df2['x_data'].max())
        ax2.set_ylim((15, 45))
        ax2.set_ylabel('C14-age Sigma')
        ax2.grid(True)
        # p4 = ax2.axhline(y_mean2, label=('mean = ' + str(round(y_mean2, 4))), color='green', alpha=0.5)
        ax2.legend(loc='upper left')

        # ax3.set_xlim(0, df3['x_data'].max())
        # ax3.set_ylim((20, 50))
        ax3.set_ylabel('C14-age Sigma')
        ax3.set_xlabel('measurement year')
        ax3.grid(True)
        # p4 = ax2.axhline(y_mean2, label=('mean = ' + str(round(y_mean2, 4))), color='green', alpha=0.5)
        ax3.legend(loc='upper left')

        # ax4.set_xlim(0, df4['x_data'].max())
        # ax4.set_ylim((30, 60))
        # ax4.set_xlabel('graphitization date')
        # ax4.set_ylabel('C14-age Sigma')
        # ax4.grid(True)
        # p4 = ax4.axhline(y_mean2, label=('mean = ' + str(round(y_mean2, 4))), color='green', alpha=0.5)
        # ax4.legend(loc='upper left')

        # start the data cursor of the mpldatacursor
        mpldatacursor.datacursor()

        plt.draw()
        plt.show()

        logger.info('plot -- ' + titel + ': saving figure to disk')
        path = 'pics/age_precision_time'
        fig.savefig(path + '.png', dpi=600)
        dataframe.to_csv(path + '.csv')

        return fig

    else:
        # no records where given to the function
        logger.warning('plot -- ' + titel + ': no records received for plotting')


####################################################################################
# plot MAG parameters (pressure, H2/CO2 ratio etc etc)
#####################################################################################
def plot_MAG_params() -> object:
    """
    create plots of various parameters regarding the graphitization using AGE for Oxa2
    e.g. pressures, H2/CO2 ratio, ...

    Returns:
        None
    """

    titel = 'MAG Parameters (Oxa2)'
    logger.info('plot -- creating plot: ' + titel)

    # distinguish between AGE and MAG by using hydro_init
    # hydro_init is NULL for MAG

    # data for H2/CO2 ratio
    query1 = """SELECT t.sample_nr, prep_nr, target_nr, fm, co2_init, co2_final, hydro_final, dc13, graphitized,
               (co2_final-co2_init)/co2_init AS H2FactorMAG
               FROM target_t t
               INNER JOIN sample_t s ON t.sample_nr=s.sample_nr
               WHERE graphitized IS NOT NULL
               AND t.fm IS NOT NULL
               AND t.hydro_init IS NULL
               AND (co2_final-co2_init)/co2_init > 1
               AND s.type LIKE '%oxa2%'
               AND t.graphitized > '2013-01-01'
               order by sample_nr asc"""
    dataframe1 = mydb.querydb(query1)

    # if enough data where provided, do the math and create the plot
    if (dataframe1 is not None) > 0:
        dataframe1.dropna(inplace=True)
        # extract data from results of query
        logger.info('plot -- ' + titel + ': preparing data...')

        # since there are no x-data, generate those from the number of rows
        # xdata1 = list(range(len(dataframe1.index)))
        # xdata2 = list(range(len(dataframe2.index)))
        xdata1 = dates.date2num(dataframe1.graphitized)

        # create plot
        # set plot styles using seaborn
        sns.set()
        sns.set_style("dark")
        sns.set_palette('Set2')
        sns.despine()

        logger.info('plot -- ' + titel + ': creating plot...')
        fig, (ax, ax2, ax3) = plt.subplots(ncols=1, nrows=3)
        ax.scatter(x=xdata1, y='H2FactorMAG', data=dataframe1, label='H2/CO2 ratio', color='green',
                   alpha=0.5)
        ax.xaxis_date()  # set x axis to date format
        ax.set_title(titel)
        ax.set_ylabel('H2/CO2 ratio')
        ax.grid(True)
        ax.legend(loc='upper left')

        ax2.scatter(x=xdata1, y='hydro_final', data=dataframe1, label='final presure H2', color='green',
                    alpha=0.5)
        ax2.xaxis_date()
        ax2.set_ylabel('final pressure H2')
        ax2.grid(True)
        ax2.legend(loc='upper left')

        ax3.scatter(x=xdata1, y='co2_init', data=dataframe1, label='CO2 initial', color='green',
                    alpha=0.5)
        ax3.xaxis_date()
        ax3.set_xlabel('Graph Date')
        ax3.set_ylabel('CO2 initial')
        ax3.grid(True)

        ax2.legend(loc='upper left')

        plt.draw()
        plt.show()

        logger.info('plot -- ' + titel + ': saving figure to disk')
        path = 'pics/MAG_params'
        fig.savefig(path + '.png', dpi=600)
        dataframe1.to_csv(path + '.csv')

    else:
        # no records where given to the function
        logger.warning('plot -- ' + titel + ': no records received for plotting')


####################################################################################
# plot AGE parameters (pressure, H2/CO2 ratio etc etc)
#####################################################################################
def plot_AGE_params() -> object:
    """
    create plots of various parameters regarding the graphitization using AGE for Oxa2
    e.g. pressures, H2/CO2 ratio, ...

    Returns:
        None
    """

    titel = 'AGE Parameters (Oxa2)'
    logger.info('plot -- creating plot: ' + titel)

    # distinguish between AGE and MAG by using hydro_init
    # hydro_init is NULL for MAG and NOT NULL for AGE

    # data for H2/CO2 ratio
    query1 = """SELECT t.sample_nr, prep_nr, target_nr, fm, co2_init, co2_final, hydro_init, hydro_final, dc13, graphitized,
               (hydro_init-(co2_final*0.54))/(co2_final*0.54) AS H2FactorAGE
               FROM target_t t
               INNER JOIN sample_t s ON t.sample_nr=s.sample_nr
               WHERE graphitized IS NOT NULL
               AND t.fm IS NOT NULL
               AND t.hydro_init IS NOT NULL
               AND (hydro_init-(co2_final*0.54))/(co2_final*0.54) > 1
               AND s.type LIKE '%oxa2%'
               AND t.graphitized > '2013-01-01'
               order by sample_nr asc"""
    dataframe1 = mydb.querydb(query1)

    # if enough data where provided, do the math and create the plot
    if (dataframe1 is not None) > 0:
        dataframe1.dropna(inplace=True)
        # extract data from results of query
        logger.info('plot -- ' + titel + ': preparing data...')

        # since there are no x-data, generate those from the number of rows
        # xdata1 = list(range(len(dataframe1.index)))
        # xdata2 = list(range(len(dataframe2.index)))
        xdata1 = dates.date2num(dataframe1.graphitized)

        # create plot
        # set plot styles using seaborn
        sns.set()
        sns.set_style("dark")
        sns.set_palette('Set2')
        sns.despine()

        logger.info('plot -- ' + titel + ': creating plot...')
        fig, (ax, ax2, ax3) = plt.subplots(ncols=1, nrows=3)
        ax.scatter(x=xdata1, y='H2FactorAGE', data=dataframe1, label='H2/CO2 ratio', color='green',
                   alpha=0.5)
        ax.xaxis_date()  # set x axis to date format
        ax.set_title(titel)
        ax.set_ylabel('H2/CO2 ratio')
        ax.grid(True)
        ax.legend(loc='upper left')

        ax2.scatter(x=xdata1, y='hydro_final', data=dataframe1, label='final pressure H2', color='green',
                    alpha=0.5)
        ax2.xaxis_date()
        ax2.set_ylabel('final pressure H2')
        ax2.grid(True)
        ax2.legend(loc='upper left')

        ax3.scatter(x=xdata1, y='co2_init', data=dataframe1, label='CO2 initial', color='green',
                    alpha=0.5)
        ax3.xaxis_date()
        ax3.set_xlabel('Graph Date')
        ax3.set_ylabel('CO initial')
        ax3.grid(True)

        ax2.legend(loc='upper left')

        plt.draw()
        plt.show()

        logger.info('plot -- ' + titel + ': saving figure to disk')
        path = 'pics/AGE_Params'
        fig.savefig(path + '.png', dpi=600)
        dataframe1.to_csv(path + '.csv')

    else:
        # no records where given to the function
        logger.warning('plot -- ' + titel + ': no records received for plotting')