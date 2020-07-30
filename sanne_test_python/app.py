from sanne_test_python.move import common, load_common_settings
from sanne_test_python.move.connector import hana_connector, oracle_connector
import sys
import logging


def main():

    if len(sys.argv) != 2:
        raise Exception("two arguments expected: [startpath] [environment]")

    environment = sys.argv[1]
    settings = load_common_settings.load_common_settings(
        environment=environment,
        authentication_file_location_ide="auth.txt",
        seperator_ide=" ",
        seperator_targetserver=" ",
        debug_mode=True,
        force_cross_connection="",
        use_hana=True,
        use_bar=True,
        console_log_only=True)

    # HANA TEST
    logging.getLogger(__name__).debug("start hana test")
    hconnector = hana_connector.HanaConnector()
    hconnector.connect(database_settings=settings.databaseSettings['HANA'])
    hresult = hconnector.cursor_execute('SELECT * FROM "SYS"."DUMMY"')
    logging.getLogger(__name__).debug(hresult)
    hconnector.close()
    
    # ORACLE TEST
    logging.getLogger(__name__).debug("start oracle test")
    bconnector = oracle_connector.OracleConnector()
    bconnector.connect(database_settings=settings.databaseSettings['BAR'])
    bresult = bconnector.cursor_execute('SELECT 1+1 FROM dual')
    logging.getLogger(__name__).debug(bresult)
    bconnector.close()
    

if __name__ == "__main__":
    main()


