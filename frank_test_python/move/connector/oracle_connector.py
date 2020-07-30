import cx_Oracle
from sanne_test_python.move import common
from sanne_test_python.move.connector import base_connector
import logging


class OracleConnector(base_connector.BaseConnector):

    def close(self):
        self.connection.close()

    def connect(self, database_settings: common.DatabaseSettings):
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # @title Creates a connection with a database
        # @author Sanne Korzec (Alliander)
        # @param username username of your database account
        # @param password password of your database account
        # @param database database that you want to use currently only possible to ORACLE
        # @param server Server of the database that you want to use options are ORACLE: e.g. BARO/BART/BARA/BARP
        # @param class_path Optional path to the class_path for the database ORACLE: ogdbc.jar file
        # @return A database connection
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

        # First check if the database is right
        if database_settings.database not in ["ORACLE"]:
            raise Exception("Do not recognize the database string options are: ORACLE. You selected:", database_settings.database)

        # Check if the server is implemented and construct the connection string
        database_settings.connection_type = "ldap"
        self._set_connection_string(database_settings)
        logging.getLogger(__name__).debug(self.connection_string)

        # Connect and create the connection
        self.connection = cx_Oracle.connect(self.connection_string)
        self.cursor = self.connection.cursor()

    def _set_connection_string(self, database_settings: common.DatabaseSettings):
        # Determine the host name based on the server that is used

        self.port = 1521

        if database_settings.instance == "BARO":
            self.host = "lt0063.alliander.local"
        elif database_settings.instance == "BART":
            self.host = "lt0063.alliander.local"
        elif database_settings.instance == "BARA":
            self.host = "la0105.alliander.local"
        elif database_settings.instance == "BARP":
            self.host = "lp0100.alliander.local"
        elif database_settings.instance == "APXAMO2":
            self.host = "odaetld1.rdc.local"
        elif database_settings.instance == "AMBT":
            self.host = "lt0029.alliander.local"
        elif database_settings.instance == "AMBA":
            self.host = "larac1-scan.alliander.local"
        elif database_settings.instance == "AMBP":
            self.host = "lprac3-scan.alliander.local"
        elif database_settings.instance == "AMBP_SVC":
            self.host = "lprac3-scan.alliander.local"
        elif database_settings.instance == "APXAMP2":
            self.host = "odpapxd1.rdc.local"
        elif database_settings.instance == "NORP":
            self.host = "odprac2-scan.rdc.local"
        elif database_settings.instance == "NORGP":
            self.host = "odprac4-scan.rdc.local"
        elif database_settings.instance == "CDBO":
            self.host = "ld0004.alliander.local"
        elif database_settings.instance == "CDBP":
            self.host = "lprac3-scan.alliander.local"
        elif database_settings.instance == "MASP":
            self.host = "lprac4-scan.alliander.local"
        else:
            raise Exception("No such oracle instance:" + database_settings.instance)

        if database_settings.connection_type == "ldap":
            self.connection_string = database_settings.username + '/' + database_settings.password + '@' + database_settings.instance
        elif database_settings.connection_type == "jdbc":
            #TODO: check which one it is and remove the other
            #self.connection_string = "jdbc:oracle:thin:" + username + '/' + password + "@//" + \
            #                         self.host + ":" + self.port + "/" + server
            self.connection_string = "jdbc:oracle:thin:@//" + self.host + ":" + str(self.port) + "/" + database_settings.instance
        else:
            # direct connection
            self.connection_string = database_settings.username + '/' + database_settings.password + '@' + \
                                        self.host + ':' + str(self.port) + '/' + database_settings.instance

    def cursor_execute(self, query):
        """
        Execute sql statement from existing cursor
        """

        '''
        on = cx_Oracle.connect(os.environ.get('ORACLE_CDBO'))
        cursor = con.cursor()

        sql = """
        SELECT *
        FROM CDB.EMS_MSGS m
        JOIN CDB.EMS_MSG_POINTS p ON p.MSG_POINT = m.MSG_POINT
        WHERE 1=1
        AND m.MSG_TIMESTAMP > to_timestamp('2017-01-01 23:59:59', 'yyyy-mm-dd hh24:mi:ss')
        ORDER BY m.MSG_TIMESTAMP DESC
        FETCH FIRST 5 ROWS ONLY
        """

        cursor.execute(sql)

        data = []
        for row in cursor:
            data.append(row)

        con.close()

        return data
        '''

        try:
            self.cursor.execute(query)
            result = self.cursor.fetchall()
            logging.debug(f'Sql statement executed, result {result}...')
            return result
        except Exception as e:
            logging.exception(f'SQL: {query}')
            logging.debug(e)


    def commit(self):
        self.connection.commit()
