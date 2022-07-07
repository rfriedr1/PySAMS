"""
All the database stuff
"""

from config.logging_conf import logger
import mysql.connector
from mysql.connector import errorcode
import pandas.io.sql as sql
from pandas import DataFrame
import PyQt5.QtSql as QtSql
import PyQt5.QtWidgets as QtWidgets
from config.config import myconfig  # myconfig calss will be loaded here

# set logger name to the name of the module
logger.name = __name__


def query_db(query):
    """
    used for plots only!!!!

    Connect to a database using the db_params and run the query.

    Connect to a database as specified in db_params and run
    a MySql query. While doing so, the function will print
    some information about it's current status and will eventually
    also display the data returned in the dataframe.

    Args:
        query: full MySql query

    Returns:
        dataframe: a pandas dataframe
    """

    # database configuration parameters
    logger.debug('run function: query_db')
    # get myconfig object instance from config module
    #myconfig = config.myconfig

    # db_params = {
    #     'user': 'mams',
    #     'password': 'Micadas.1',
    #     #'host': '127.0.0.1',
    #     'host': '192.168.123.30',
    #     'database': 'db_dmams',
    #     'raise_on_warnings': True,
    # }

    logger.debug('read db settings from the config class')
    db_params = {
        'user': myconfig.get('database', 'dbuser'),
        'password': myconfig.get('database', 'dbpasswd'),
        'host': myconfig.get('database', 'dbhost'),
        'database': myconfig.get('database', 'dbname'),
        'raise_on_warnings': True,
    }

    logger.info('############# Start Database Process ###########')
    try:
        # connect to database using db_params
        db_conn = mysql.connector.connect(**db_params)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            logger.error('Database Error')
            logger.error("Something is wrong with user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            logger.error('Database Error')
            logger.error("Database does not exist")
        else:
            logger.error(err)
    else:
        logger.debug("connected to database: " + db_params['database'])
        # create cursor that returns values are dictionaries
        db_cursor = db_conn.cursor(dictionary=True)
        # alternatively also use the pandas data frame
        logger.info('run query:')
        logger.debug(query)
        dataframe = sql.read_sql(query, db_conn)
        # query the database (returns the number of records)
        db_cursor.execute(query)
        # fetch all the data in order to copy the data into memory
        rows = db_cursor.fetchall()
        # display number of records
        row_count = db_cursor.rowcount
        logger.info("Number of Records: " + str(row_count))
        # cleaning up
        db_cursor.close()
        db_conn.close()
        logger.info('db procedure finished')
        logger.debug('show data frame (first 3 rows)')
        logger.debug(dataframe.head(30))

        # return the rows
        return dataframe

'''
class MyDatabaseQt(QtSql.QSqlDatabase):
    """
    Class that handles the AMS Database
    - Class inherits from the PyQT5 Database class QSqlDatabase
    - during init, the database info are read from the config file
    - connect to the database with method: "openDB"

    Returns:
        db: database object

    """

    def __init__(self, *args):
        logger.debug('perform: __init__')
        logger.debug('init MyDatabase Object')

        super(MyDatabaseQt, self).__init__(*args)

        # get myconfig object instance from the config.py
        logger.debug('read db settings from the config class')
        myconfig = config.myconfig

        self.dbtype = 'QMYSQL'
        logger.debug('set db type to: ' + self.dbtype)

        self.db = QtSql.QSqlDatabase.addDatabase(self.dbtype, 'AMSDB')
        if not self.db.isValid():
            logger.error('invalid database ' + self.dbtype)

        # get database settings from the config file
        # self.setHostName('127.0.0.1')
        self.hostName = myconfig.get('database', 'dbhost')
        self.db.setHostName(self.hostName)
        logger.debug('hostname set successfully: ' + self.db.hostName())
        self.userName = myconfig.get('database', 'dbuser')
        self.db.setUserName(self.userName)
        logger.debug('user name set successfully: ' + self.db.userName())
        self.password = myconfig.get('database', 'dbpasswd')
        self.db.setPassword(self.password)
        logger.debug('password set successfully')
        self.dbName = myconfig.get('database', 'dbname')
        self.db.setDatabaseName(self.dbName)
        logger.debug('db name set successfully: ' + self.databaseName())

        # for debugging show some extra information
        logger.debug('show last error: ' + self.db.lastError().text())
        logger.debug('PyQt5 available divers: ' + ''.join(self.db.drivers()))

    def set_hostname(self, hostname):
        logger.debug('set_hostname = ' + hostname)
        self.hostName = hostname

    def set_username(self, username):
        logger.debug('set_username = ' + username)
        self.userName = username

    def set_password(self, password):
        logger.debug('set_password = ' + password)
        self.password = password

    def set_dbname(self, dbname):
        logger.debug('set_dbname = ' + dbname)
        self.dbName = dbname

    def set_dbtype(self, dbtype):
        logger.debug('set_dbtype = ' + dbtype)
        self.dbtype = dbtype

    def get_dbversion(self) -> str:
        """
        returns the database version of the connected DB

        Returns:
            str: Database version
        """
        # create Query object connected to the database and execute
        logger.debug('hostName = ' + self.db.hostName())
        logger.debug('userName = ' + self.db.userName())
        logger.info('try opening database')
        if not self.db.open():
            QtWidgets.QMessageBox.critical(None, QtWidgets.qApp.tr("Cannot open database: " + self.lastError().text()),
                                           QtWidgets.qApp.tr("An error occured during opening the database connection.\n\n"
                                         + self.lastError().text() + "\n\n"
                                         "Make sure the database parameters are set "
                                         "correctly and the database is available \n\n"
                                         "Click Cancel to exit."),
                                           QtWidgets.QMessageBox.Cancel)
            logger.error('Cannot open database: ' + self.db.lastError().text())
            return 'none'
        else:
            logger.info('connection successful')
            dbquery = QtSql.QSqlQuery(self.db)
            query_str = 'SELECT VERSION()'
            logger.info('query: ' + query_str)
            if dbquery.exec(query_str):
                logger.info('query successful')
                logger.debug('query size ' + str(dbquery.size()))
                dbquery.first()
                return dbquery.value(0)
            else:
                logger.info('query unsuccessful')
                dbquery.lastError()
                return 'none'

    def opendb(self) -> bool:
        """
        - open the database connection
        - database connection info are read from the config file
        - if an error occurs a messagebox pops up

        Returns:
            boolean:  true if everything is okay, false if error occured

        """
        logger.debug('MyDatabase (OpenDB) -- try opening database')
        if not self.db.open():
            QtWidgets.QMessageBox.critical(None, QtWidgets.qApp.tr("Cannot open database: " + self.lastError().text()),
                                           QtWidgets.qApp.tr("An error occured during opening the database connection.\n\n"
                                         + self.lastError().text() + "\n\n"
                                         "Make sure the database parameters are set "
                                         "correctly and the database is available \n\n"
                                         "Click Cancel to exit."),
                                           QtWidgets.QMessageBox.Cancel)
            logger.error('Cannot open database: ' + self.db.lastError().text())
            return False
        else:
            logger.debug('successful')
            return True

    def querydb(self, query_str: str) -> QtSql.QSqlQuery:
        """
        - query the database using the query-string

        the function opens the database first
        if there is no error the query is being processed
        and the result returned

        Args:
            query: MySql query string

        Returns:
            str: result of the query as a QSqlQuery Object
        """

        logger.debug('opening DB')
        # open database and query
        if self.opendb():
            logger.debug('opened DB successfully')
            logger.debug('query: ' + query_str)

            # create Query object connected to the database and execute
            dbquery = QtSql.QSqlQuery(self.db)
            if dbquery.exec(query_str):
                logger.debug('execute query')
                logger.debug('query size ' + str(dbquery.size()))
                # return the dbquery object
                return dbquery
            else:
                logger.error('query NOT successful')
                logger.error(dbquery.lastError().text())
                return dbquery

    def querydb_single_string(self, query_str: str) -> str:
        """
        query the database with a query that returns only one string

        Args:
            query_str: Query that returns a single string

        Returns:
            str: string that is returned from the Query

        """

        logger.debug('try querying DB: ' + query_str)
        # open database and query
        if self.opendb():
            logger.debug('opened DB successfully')
            logger.debug('query: ' + query_str)

            # create Query object connected to the database and execute
            dbquery = QtSql.QSqlQuery(self.db)
            if dbquery.exec(query_str):
                logger.debug('query successful')
                logger.debug('query size ' + str(dbquery.size()))
                dbquery.first()
                logger.debug('returned: ' + str(dbquery.value(0)))
                return str(dbquery.value(0))
            else:
                logger.error('query NOT successful')
                logger.error(dbquery.lastError().text())
                return 'none'

    def get_number_of_unprepped_samples(self) -> str:
        """
        return the number of unprepped samples

        Returns:
            str: number of unprepped samples

        """

        query_str = """SELECT count(sample_t.sample_nr) FROM sample_t
                    INNER JOIN preparation_t ON sample_t.sample_nr = preparation_t.sample_nr
                    INNER JOIN target_t ON sample_t.sample_nr = target_t.sample_nr
                    WHERE prep_end IS NULL 
                    AND av_fm IS NULL
                    AND target_t.fm IS NULL
                    AND target_t.magazine IS NULL"""
        return self.querydb_single_string(query_str)
'''

class MyDatabase:
    """
    Class that handles the AMS Database
    - Class inherits from the PyQT5 Database class QSqlDatabase
    - during init, the database info are read from the config file
    - connect to the database with method: "openDB"

    Returns:
        db: database object

    """

    def __init__(self, *args):
        logger.debug('perform: __init__')
        logger.debug('init MyDatabase Object')

        super(MyDatabase, self).__init__(*args)

        # get myconfig object instance from the config.py
        logger.debug('read db settings from the config class')
        #myconfig = config.myconfig

        self.dbtype = 'MYSQL'
        logger.debug('set db type to: ' + self.dbtype)

        # get database settings from the config file
        # self.setHostName('127.0.0.1')
        self.hostName = myconfig.get('database', 'dbhost')
        logger.debug('hostname read successfully: ' + self.hostName)
        self.userName = myconfig.get('database', 'dbuser')
        logger.debug('user name read successfully: ' + self.userName)
        self.password = myconfig.get('database', 'dbpasswd')
        logger.debug('password read successfully')
        self.dbName = myconfig.get('database', 'dbname')
        logger.debug('db name read successfully: ' + self.dbName)

        # assign database settings
        self.db_params = {
            'user': self.userName,
            'password': self.password,
            'host': self.hostName,
            'database': self.dbName,
            'raise_on_warnings': True,
        }

    def set_hostname(self, hostname):
        logger.debug('set_hostname = ' + hostname)
        self.hostName = hostname

    def set_username(self, username):
        logger.debug('set_username = ' + username)
        self.userName = username

    def set_password(self, password):
        logger.debug('set_password = ' + password)
        self.password = password

    def set_dbname(self, dbname):
        logger.debug('set_dbname = ' + dbname)
        self.dbName = dbname

    def set_dbtype(self, dbtype):
        logger.debug('set_dbtype = ' + dbtype)
        self.dbtype = dbtype

    def opendb(self) -> mysql.connector.connection.MySQLConnection:
        """
        - open the database connection

        Returns:
            db:  db connection
        """
        logger.debug('MyDatabase -- try opening database')
        try:
            logger.debug('hostName = ' + self.hostName)
            logger.debug('userName = ' + self.userName)
            logger.debug('try opening database')
            db = mysql.connector.connect(**self.db_params)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                logger.error('Database Connection Error: Wrong with user name or password')
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                logger.error('Database Connection Error: Database does not exist')
            else:
                logger.error(err)
            return db
        else:
            logger.info('connection successful')
            return db

    def get_dbversion(self) -> str:
        """
        returns the database version of the connected DB

        Returns:
            str: Database Server version
        """
        # create Query object connected to the database and execute
        try:
            db = self.opendb()
        except mysql.connector.Error as err:
            logger.error('cant get server version')
        else:
            server_version = str(db.get_server_version())
            logger.info('Sever Version = ' + server_version)
            logger.debug('closing db connection')
            db.close()
            return server_version

    def querydb(self, query_str: str) -> DataFrame:
        """
        - query the database using the query-string

        the function opens the database first
        if there is no error the query is being processed
        and the result returned

        Args:
            query_str: MySql query string

        Returns:
            DataFrame: returns a Pandas Dataframe
        """

        logger.debug('query: ' + query_str)
        # open database and query
        db = self.opendb()
        dataframe = sql.read_sql(query_str, db)
        db.close()
        logger.debug(dataframe.head(10))
        return dataframe


    def querydb_single_string(self, query_str: str) -> str:
        """
        query the database with a query that returns only one string

        Args:
            query_str: Query that returns a single string

        Returns:
            str: string that is returned from the Query
        """

        logger.debug('query: ' + query_str)
        # open database and query
        db = self.opendb()
        cursor = db.cursor()
        cursor.execute(query_str)
        result = cursor.fetchall()
        cursor.close()
        db.close()
        return str(result[0][0])

    def get_number_of_unprepped_samples(self) -> str:
        """
        return the number of unprepped samples

        Returns:
            str: number of unprepped samples

        """
        query_str = """SELECT count(sample_t.sample_nr) FROM sample_t
                    INNER JOIN preparation_t ON sample_t.sample_nr = preparation_t.sample_nr
                    INNER JOIN target_t ON sample_t.sample_nr = target_t.sample_nr
                    INNER JOIN project_t on sample_t.project_nr=project_t.project_nr
                    INNER JOIN user_t on project_t.user_nr = user_t.user_nr
                    WHERE prep_end IS NULL 
                    AND sample_t.c14_age IS NULL
                    AND target_t.fm IS NULL
                    AND type not in ('blank', 'oxa1', 'oxa2')
                    AND graphitized IS NULL
                    AND last_name not in ('Levin', 'intern')
                    AND year(in_date)>2010
                    AND sample_t.sample_nr>9999
                    AND preparation_t.stop=0
                    AND sample_t.not_tobedated=0"""
        return self.querydb_single_string(query_str)

    def get_number_of_samples_ready_for_graph(self) -> str:
        """
        return the number of samples that are prepped and ready for graphitization

        Returns:
            str: number of samples ready for graph

        """
        query_str = """SELECT DISTINCT count(sample_t.sample_nr)
                   FROM sample_t
                   INNER JOIN project_t ON project_t.project_nr=sample_t.project_nr
                   INNER JOIN user_t ON user_t.user_nr=project_t.user_nr
                   INNER JOIN preparation_t ON preparation_t.sample_nr=sample_t.sample_nr
                   INNER JOIN target_t ON target_t.sample_nr=sample_t.sample_nr
                   WHERE preparation_t.prep_end IS NOT NULL and target_t.graphitized IS NULL
                   AND target_t.target_pressed IS NULL
                   AND target_t.calcset is NULL
                   AND sample_t.not_tobedated=0
                   AND preparation_t.stop=0
                   AND target_t.stop=0
                   AND project_t.out_date IS NULL
                   AND sample_t.type NOT LIKE 'oxa%'
                   AND NOT (user_t.last_name = 'intern' AND user_t.first_name ='intern')
                   ORDER BY sample_t.sample_nr"""
        return self.querydb_single_string(query_str)

    def get_number_of_samples_ready_for_analysis(self) -> str:
        """
        return the number of samples that are prepped and ready for analysis

        Returns:
            str: number of samples ready for analysis

        """
        query_str = """SELECT DISTINCT count(sample_t.sample_nr)
                   FROM sample_t
                   INNER JOIN project_t ON project_t.project_nr=sample_t.project_nr
                   INNER JOIN user_t ON user_t.user_nr=project_t.user_nr
                   INNER JOIN preparation_t ON preparation_t.sample_nr=sample_t.sample_nr
                   INNER JOIN target_t ON target_t.sample_nr=sample_t.sample_nr
                   WHERE preparation_t.prep_end IS NOT NULL and target_t.graphitized IS NOT NULL
                   and target_t.target_pressed IS NOT NULL and target_t.calcset is NULL and sample_t.not_tobedated=0
                   and preparation_t.stop=0 and  target_t.stop=0
                   and project_t.out_date IS NULL
                   and target_t.fm is NULL
                   and sample_t.type NOT LIKE 'blank%'
                   and sample_t.type NOT LIKE 'oxa%'
                   and user_label NOT LIKE 'HEI_%'
                   ORDER BY sample_t.sample_nr"""
        return self.querydb_single_string(query_str)

    def get_number_of_samples_express(self) -> str:
        """
        return the number of samples that are express service

        Returns:
            str: number of express samples

        """
        query_str = """SELECT DISTINCT count(sample_t.sample_nr)
                   FROM sample_t 
                   INNER JOIN project_t ON project_t.project_nr=sample_t.project_nr
                   INNER JOIN user_t ON user_t.user_nr=project_t.user_nr
                   INNER JOIN preparation_t ON preparation_t.sample_nr=sample_t.sample_nr
                   INNER JOIN target_t ON target_t.sample_nr=sample_t.sample_nr
                   WHERE sample_t.user_label LIKE '%eil%'
                   and target_t.calcset is NULL and sample_t.not_tobedated=0
                   and preparation_t.stop=0 and  target_t.stop=0 
                   and (project_t.out_date < '1900-01-01' or project_t.out_date IS NULL)
                   ORDER BY sample_t.sample_nr"""

        return self.querydb_single_string(query_str)

    def get_number_available_oxas(self) -> str:
        """
        return the number of available oxas

        Returns:
            str: number of available oxas

        """
        query_str = """SELECT count(target_t.sample_nr) FROM target_t
                INNER JOIN sample_t ON target_t.sample_nr=sample_t.sample_nr
                WHERE magazine IS NULL 
                AND graphitized IS NOT NULL 
                AND stop=0
                AND sample_t.type like 'oxa%'
                AND sample_t.user_label like 'oxa%' """

        return self.querydb_single_string(query_str)

    def get_number_available_blanks(self) -> str:
        """
        return the number of available blanks

        Returns:
            str: number of available blanks

        """
        query_str = """SELECT count(target_t.sample_nr) FROM target_t
                INNER JOIN sample_t ON target_t.sample_nr=sample_t.sample_nr
                WHERE magazine IS NULL 
                AND graphitized IS NOT NULL 
                AND stop=0
                AND sample_t.type like 'blank%'
                AND sample_t.user_label like 'Phthalic%' """

        return self.querydb_single_string(query_str)


# already instantiate the MyDatabase Object here
# that allows sharing this single instance across modules
logger.debug('Instantiate the MyDatabase object instance while importing the module')
mydb = MyDatabase()
