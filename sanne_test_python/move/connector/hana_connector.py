import pyhdb
from sanne_test_python.move import common
from sanne_test_python.move.connector import base_connector
import logging

class HanaConnector(base_connector.BaseConnector):

    def close(self):
        self.connection.close()

    def connect(self, database_settings: common.DatabaseSettings):
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # @title Creates a connection with a database
        # @author Sanne Korzec (Alliander)
        # @param username username of your database account
        # @param password password of your database account
        # @param database database that you want to use currently only possible to HANA
        # @param server Server of the database that you want to use options are HANA: WHA/DHA/KHA/PHA
        # @param class_path Optional path to the class_path for the database HANA: ngdbc.jar file
        # @return A database connection
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

        # First check if the database is right
        if database_settings.database not in ["HANA"]:
            raise Exception("Do not recognize the database string options are: HANA. You selected:", database_settings.database)

        # Check if the server is implemented and construct the connection string
        database_settings.connection_type = "direct"
        self._set_connection_string(database_settings)
        logging.getLogger(__name__).debug(self.host)
        logging.getLogger(__name__).debug(self.port)

        # Connect and create the connection
        self.connection = pyhdb.connect(
            host=self.host,
            port=self.port,
            user=database_settings.username,
            password=database_settings.password
        )
        self.cursor = self.connection.cursor()
        
    def cursor_execute(self, query):
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return result

    def _set_connection_string(self, database_settings: common.DatabaseSettings):
        # Determine the host name based on the server that is used

        application = common.get_caller()

        # Check if the server is implemented and determine the host name based on the instance that is used
        if database_settings.instance == "WHA":
            self.host = "wsp-dpl.hec.alliander.local"
            self.port = 30441
        elif database_settings.instance == "DHA":
            self.host = "dev-dpl.hec.alliander.local"
            self.port = 30641
        elif database_settings.instance == "KHA":
            self.host = "qas-dpl.hec.alliander.local"
            self.port = 30441
        elif database_settings.instance == "PHA":
            self.host = "dpl.hec.alliander.local"
            self.port = 30241
        else:
            raise Exception("No such hana instance:" + database_settings.instance)

        if database_settings.connection_type == "ldap":
            self.connection_string = database_settings.username + '/' + database_settings.password + '@' + database_settings.instance
        elif database_settings.connection_type == "jdbc":
            self.host = "jdbc:sap://" + self.host
            self.connection_string = self.host + ':' + str(self.port) + '/?sessionVariable:APPLICATION=' + application
        else:
            # direct connection
            self.connection_string = self.host + ':' + str(self.port) + '/' + database_settings.instance

