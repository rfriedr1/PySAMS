from config.logging_conf import logger
import matplotlib
# matplotlib.use('TkAgg')  # switch to a different backend in order to make the cursor mpldatawork
matplotlib.use('Qt5Agg')
from database.pysamsdb import mydb
import matplotlib.pyplot as plt
import mpldatacursor  # a datacursor for matplotlib
import seaborn as sns  # by importing this all the matlibplots will look different
import pandas
import numpy as np
import plots.utils.plotutils as plotutils

# set logger name to the name of the module
logger.name = __name__

# tunr interactive mode of matplotlib on so that the error "event loop is already running doesn't appear
plt.ion()

####################################################################################
def plot_standards(dataframe: pandas.DataFrame, consensus: float, titel: str) -> object:
    """
    create two scatter plots as subplots
    plot 1 shows: fm
    plot 2 shows: d13c
    averages and standard deviations are calculated and plotted as well

    use the rows from a database query (function: query_db) in order to plot the data

    Args:
        dataframe: a pandas Dataframe holding the data called 'xdata', 'fm' and 'dc13'. More data could be included
        but will not be displayed.
        consensus: consensus value of those standards, will plot a horizontal line
        titel: the titel of the plot

    Returns:
        None
    """

    # if enough datapoints are provided, do some math and create the plot
    if (dataframe is not None) > 0:

        dataframe.dropna(inplace=True)

        # extract data from the dataframe
        logger.info('plot: ' + titel + ': preparing data...')
        # decided what to use as xdata, use the index for now
        xdata = list(range(len(dataframe.index)))
        # xdata = [x+1 for x in xdata]  # add 1 to the index so that it starts with 1 and not 0
        # xdata = dataframe['xdata']
        # generate column for the y2err for dc13 data (dc13 has no errors in the database)
        y2err = [0.003]*len(dataframe.index)

        # calculate means, stdev and chi^2 of fm and dc13
        logger.info('plot: ' + titel + ': calculating statistics...')
        #
        y1_mean = dataframe['fm'].mean()
        logger.info('plot: ' + titel + ': mean fm = ' + str(y1_mean))
        y1_std = dataframe['fm'].std()
        logger.info('plot: ' + titel + ': stdev fm = ' + str(y1_std))
        chi2_fm = np.sum(((dataframe['fm'].values - y1_mean)/dataframe['fm_sig'].values) ** 2)
        chi2_fm_reduced = chi2_fm/(dataframe['fm'].size - 1)
        logger.info('plot: ' + titel + ': chi^2-reduced fm = ' + str(chi2_fm_reduced))
        #
        y2_mean = dataframe['dc13'].mean()
        logger.info('plot: ' + titel + ': mean dc13 = ' + str(y2_mean))
        y2_std = dataframe['dc13'].std()
        logger.info('plot: ' + titel + ': stdev dc13 = ' + str(y2_std))
        chi2_dc13 = np.sum(((dataframe['dc13'].values - y2_mean)/y2err) ** 2)
        chi2_dc13_reduced = chi2_dc13/(dataframe['dc13'].size - 1)
        logger.info('plot: ' + titel + ': chi^2-reduced dc13 = ' + str(chi2_dc13_reduced))
        #

        # find positions of years
        year_positions = plotutils.find_year_positions(dataframe)

        # === create plots with error bars using matplotlib
        # set plot styles using seaborn
        sns.set()
        sns.set_style("dark")
        sns.set_palette('Set2')
        sns.despine()

        # fm
        logger.info('plot: ' + titel + ': creating plot...')
        fig, (ax, ax2) = plt.subplots(nrows=2, sharex=True)
        ax.errorbar(x=xdata, y=dataframe['fm'], yerr=dataframe['fm_sig'], fmt='-o', picker=5)
        ax.set_title(titel)
        ax.set_ylabel('fm')
        ax.grid(True)
        ax.axhline(y1_mean, label=('mean = ' + str(round(y1_mean, 4)) + ', stdev = ' + str(round(y1_std, 4))
                                   + ', chi^2= ' + str(round(chi2_fm_reduced,2))))
        ax.axhline(y1_mean - y1_std, linestyle='dashed')
        ax.axhline(y1_mean + y1_std, linestyle='dashed')
        # consensus value
        ax.axhline(consensus, color='brown', alpha=0.7, label=('consensus = ' + str(consensus)))

        # insert vertical lines for the transitions of the years
        for pos in year_positions:
            ax.axvline(pos, color='y', alpha=0.5)

        # add legend
        ax.legend()

        # dc13
        ax2.errorbar(x=xdata, y=dataframe['dc13'], yerr=y2err, fmt='o', picker=5)
        ax2.set_xlabel('record')
        ax2.set_ylabel('dc13')
        ax2.grid(True)
        ax2.axhline(y2_mean, label=('mean = ' + str(round(y2_mean, 4)) + ', stdev = ' + str(round(y2_std, 4))
                                    + ', chi^2= ' + str(round(chi2_dc13_reduced,2))))
        ax2.axhline(y2_mean - y2_std, linestyle='dashed')
        ax2.axhline(y2_mean + y2_std, linestyle='dashed')

        # insert vertical lines for the transitions of the years
        for pos in year_positions:
            ax2.axvline(pos, color='y', alpha=0.5)

        # add legend
        ax2.legend()

        # instantiate the DataCursor class that enables the datapoints to be clicked
        # it's not necessary to use fig.canvas.mpl_connect('pick_event', xxx) event
        # DataCursor([ax, ax2])
        mpldatacursor.datacursor(formatter=plotutils.myformatter)

        plt.draw()
        plt.show()

        # save image of the plot to a png file and the raw data of the plot to a csv file
        path = 'pics/' + titel
        logger.info('plot: ' + titel + ': saving figure to disk: ' + path)
        fig.savefig(path + '.png', dpi=600)
        logger.info('plot: ' + titel + ': saving data to csv file: ' + path)
        dataframe.to_csv(path + '.csv')

        return fig

    else:
        # no records where given to the function
        logger.warning('plot: ' + titel + ': no records received for plotting')


####################################################################################
# plot blanks values fm of pthalic acids
#####################################################################################
def plot_blank_data(dataframe: pandas.DataFrame, titel: str) -> object:
    """
    creates scatter plot of blank values (pthalic acid samples) of fm, dc13 and C14 age

    Args:
        dataframe: a pandas Dataframe holding the data returned from a MySql Query
        titel: the titel of the plot

    Returns:
        None
    """

    # if enough data where provided, do some math and create the plots
    if (dataframe is not None) > 0:

        dataframe.dropna(inplace=True)

        # calulcate means and stdev
        logger.info('plot: ' + titel + ': calculating statistics...')
        fm_mean = round(dataframe['fm'].mean(), 4)
        fm_std = round(dataframe['fm'].std(), 4)
        logger.info(titel + ': mean = ' + str(fm_mean) + ' +- ' + str(fm_std))
        chi2_fm = np.sum(((dataframe['fm'].values - fm_mean)/dataframe['fm_sig'].values) ** 2)
        chi2_fm_reduced = chi2_fm/(dataframe['fm'].size - 1)
        logger.info('plot: ' + titel + ': chi^2-reduced fm = ' + str(chi2_fm_reduced))

        dc13_mean = round(dataframe['dc13'].mean(), 3)
        dc13_std = round(dataframe['dc13'].std(), 3)
        logger.info(titel + ': mean2 = ' + str(dc13_mean) + ' +- ' + str(dc13_std))
        dc13err = [0.003] * len(dataframe.index)  # typical error of delt13C
        chi2_dc13 = np.sum(((dataframe['dc13'].values - dc13_mean)/dc13err) ** 2)
        chi2_dc13_reduced = chi2_dc13/(dataframe['dc13'].size - 1)
        logger.info('plot: ' + titel + ': chi^2-reduced dc13 = ' + str(chi2_dc13_reduced))

        age_mean = round(dataframe['c14_age'].mean(), 0)
        age_std = round(dataframe['c14_age'].std(), 0)
        logger.info(titel + ': mean3 = ' + str(age_mean) + ' +- ' + str(age_std))

        # find indices in dataframe with transitions from one year to the other (by magazine name)
        year_positions = plotutils.find_year_positions(dataframe)
        # find the indices in the dataframe where revisions happened (by magazine name)
        revision_positions = plotutils.find_revisions(dataframe)

        # create plot using pandas
        # set plot styles
        sns.set()
        sns.set_style("dark")
        sns.set_palette('Set2')
        sns.despine()

        logger.info('plot: ' + titel + ': creating plot...')

        fig, axes = plt.subplots(nrows=3, ncols=1, sharex=True)
        ax1 = dataframe['fm'].plot(ax = axes[0], label='fm', color='green', alpha=0.5)
        ax2 = dataframe['dc13'].plot(ax=axes[1], label='dc13', color='green', alpha=0.5)
        ax3 = dataframe['c14_age'].plot(ax=axes[2], label='C14_age', color='green', alpha=0.5)

        h1 = ax1.axhline(fm_mean, label=('mean = ' + str(fm_mean) + ' +- ' + str(fm_std) +
                                         ', chi^2= ' + str(round(chi2_fm_reduced,2))), color='green', alpha=0.9)
        ax1.axhline(fm_mean - fm_std, linestyle='dashed', color='green', alpha=0.9)
        ax1.axhline(fm_mean + fm_std, linestyle='dashed', color='green', alpha=0.9)

        # insert vertical lines for the transitions of the years
        for pos in year_positions:
            ax1.axvline(pos, color='y', alpha=0.5, label='years')
        # Plot where Source revisions happened
        for rev in revision_positions:
            ax1.axvline(rev, color='r', alpha=0.2, label='revisions')

        h2 = ax2.axhline(dc13_mean, label=('mean = ' + str(dc13_mean) + ' +- ' + str(dc13_std)
                                           + ', chi^2= ' + str(round(chi2_dc13_reduced, 2))), color='green', alpha=0.9)
        ax2.axhline(dc13_mean - dc13_std, linestyle='dashed', color='green', alpha=0.9)
        ax2.axhline(dc13_mean + dc13_std, linestyle='dashed', color='green', alpha=0.9)
        # insert vertical lines for the transitions of the years
        for pos in year_positions:
            ax2.axvline(pos, color='y', alpha=0.5, label='years')
        # Plot where Source revisions happened
        for rev in revision_positions:
            ax2.axvline(rev, color='r', alpha=0.2, label='revisions')

        h3 = ax3.axhline(age_mean, label=('mean = ' + str(age_mean) + ' +- ' + str(age_std)), color='green', alpha=0.9)
        ax3.axhline(age_mean - age_std, linestyle='dashed', color='green', alpha=0.9)
        ax3.axhline(age_mean + age_std, linestyle='dashed', color='green', alpha=0.9)

        # insert vertical lines for the transitions of the years
        for pos in year_positions:
            ax3.axvline(pos, color='y', alpha=0.5, label='years')
        # Plot where Source revisions happened
        for rev in revision_positions:
            ax3.axvline(rev, color='r', alpha=0.2, label='revisions')

        ax1.set_title('Performance of Blanks (Phthalic Acid)')
        ax3.set_xlabel('number')

        ax1.set_ylabel('F14C')
        ax2.set_ylabel('d13C')
        ax3.set_ylabel('C14 Age')
        ax3.invert_yaxis()
        #
        ax1.legend(handles=[h1], loc='upper right')
        ax2.legend(handles=[h2], loc='upper right')
        ax3.legend(handles=[h3], loc='upper right')

        plt.show()

        path = 'pics/qc_blanks'
        logger.info('plot: ' + titel + ': saving figure to disk: ' + path)
        fig.savefig(path + '.png', dpi=600)
        logger.info('plot: ' + titel + ': saving data to csv file: ' + path)
        dataframe.to_csv(path + '.csv')

        return fig

    else:
        # no records where given to the function
        logger.warning('plot: ' + titel + ': no records received for plotting')


####################################################################################
# queries for the individual plots that use the above function
# in order to create the plots
#####################################################################################
def plot_blanks():
    """
    query the database and generate a plot
    by calling the functions stored in other modules

    creates a plot that shows fm or C14 ages of the blanks
    """
    query = """SELECT user_label, graphitized AS date, fm, fm_sig, dc13, c14_age, magazine
               FROM target_v
               WHERE user_label LIKE '%Pthalic%'
               OR user_label LIKE '%phthalic%'
               AND fm > 0
               AND graphitized IS NOT NULL
               AND dc13 < 0
               AND c14_age > 0
               AND target_v.magazine IS NOT NULL
               order by sample_nr"""
    dataframe = mydb.querydb(query)
    plot_blank_data(dataframe, 'blanks values')


def plot_c1():
    """
    query the database and generate a plot
    by calling the functions stored in other modules
    """
    query = ("""SELECT Concat(substring(magazine,3,2),'-',substring(magazine,5,2),'-',substring(magazine,7,2)) as measdate,
                fm, fm_sig, dc13, magazine
                FROM target_v
                where user_label like '%IAEA%C1%'
                AND fm IS NOT NULL
                AND fm < 0.004
                Order By magazine;""")
    logger.debug(query)
    dataframe = mydb.querydb(query)
    plot_standards(dataframe, 0, 'IAEA-C1')


def plot_c2():
    """
    query the database and generate a plot
    by calling the functions stored in other modules
    """
    query = ("""SELECT Concat(substring(magazine,3,2),'-',substring(magazine,5,2),'-',substring(magazine,7,2)) as measdate,
                fm, fm_sig, dc13, magazine
                FROM target_v
                where user_label like '%IAEA%C2%'
                AND fm IS NOT NULL
                AND fm < 0.43
                Order By magazine;""")
    dataframe = mydb.querydb(query)
    plot_standards(dataframe, 0.4114, 'IAEA-C2')


def plot_c3():
    """
    query the database and generate a plot
    by calling the functions stored in other modules
    """
    query = ("""SELECT Concat(substring(magazine,3,2),'-',substring(magazine,5,2),'-',substring(magazine,7,2)) as measdate,
                fm, fm_sig, dc13, magazine
                FROM target_v
                where user_label like '%IAEA%C3%'
                AND fm IS NOT NULL
                AND fm > 1.27
                Order By magazine;""")
    dataframe = mydb.querydb(query)
    plot_standards(dataframe, 1.2941, 'IAEA-C3')


def plot_c6():
    """
    query the database and generate a plot
    by calling the functions stored in other modules
    """
    query = ("""SELECT Concat(substring(magazine,3,2),'-',substring(magazine,5,2),'-',substring(magazine,7,2)) as measdate,
                fm, fm_sig, dc13, magazine
                FROM target_v
                where user_label like '%IAEA%C6%'
                AND fm IS NOT NULL
                Order By magazine;""")
    dataframe = mydb.querydb(query)
    plot_standards(dataframe, 1.5016, 'IAEA-C6')


def plot_hei3():
    """
    query the database and generate a plot
    by calling the functions stored in other modules
    """
    query = ("""SELECT Concat(substring(magazine,3,2),'-',substring(magazine,5,2),'-',substring(magazine,7,2)) as measdate,
                fm, fm_sig, dc13, magazine
                FROM target_v
                where user_label like '%HEI_3%'
                AND fm IS NOT NULL
                Order By magazine;""")
    dataframe = mydb.querydb(query)
    plot_standards(dataframe, 0, 'ICOS-HEI_3')


def plot_hei10():
    """
    query the database and generate a plot
    by calling the functions stored in other modules
    """
    query = ("""SELECT Concat(substring(magazine,3,2),'-',substring(magazine,5,2),'-',substring(magazine,7,2)) as measdate,
                fm, fm_sig, dc13, magazine
                FROM target_v
                where user_label like '%HEI_10%'
                AND fm IS NOT NULL
                Order By magazine;""")
    dataframe = mydb.querydb(query)
    plot_standards(dataframe, 0, 'ICOS-HEI_10')


def plot_horses():
    """
    query the database and generate a plot
    by calling the functions stored in other modules
    """
    query = ("""SELECT Concat(substring(magazine,3,2),'-',substring(magazine,5,2),'-',substring(magazine,7,2)) as measdate,
                fm, fm_sig, dc13, magazine
                FROM target_v
                where user_label like '%Pferd%'
                AND fm IS NOT NULL
                AND fm > 0.9
                Order By magazine;""")
    dataframe = mydb.querydb(query)
    plot_standards(dataframe, 0.966, 'Latdorf-Pferde')

