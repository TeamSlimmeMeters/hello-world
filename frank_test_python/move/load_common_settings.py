import os
import pandas as pd
import socket
from sanne_test_python.move import common, get_authentication
import sanne_test_python.move.logger.logger as common_logger
import logging

def load_common_settings(
        environment="R",
        authentication_from_file="True",
        authentication_file_location_ide="tests/test_source_scripts/auth.txt",
        seperator_ide=" ",
        seperator_targetserver=" ",
        debug_mode=False,
        force_cross_connection="",
        use_hana=True,
        use_bar=True,
        use_apex=False,
        use_cbd=False,
        use_nor=False,
        console_log_only=False):
    """
    @title Loads the settings. This is an server_environment specific configuration file,
     which holds parameters on what to do and who to communicate with.
    @description Loads the common settings. This is an server_environment specific configuration file,
     which holds flags on what to do and who to communicate with.
    @author Sanne Korzec (Alliander)

    :param environment: string a choice of these options: 'R', 'RO', 'RT', 'RA', 'RP', 'JO', 'JT', 'JA', 'JP', 'O', 'T', 'A', 'P'.
    P = default, will expect you are running on a r studio server and set your environment automatically.
    PO, PT = expects you run source code on the python ide dev server and connect to O or T databases.
    PA, PP = expects you run source code on the python ide prd server and connect to A or P databases.
    JO, JT = expects you run post deploy tests from a jenkinsnode and connect to O or T databases.
    JA, JP = expects you run post deploy tests from a jenkinsnode and connect to A or P databases.
    O, T, A P = expects you are running a packaged application on the target deploy servers.
    :param authentication_from_file: the secrets are retrieved from a file or from the env when set to false.
    :param authentication_file_location_ide: the location of the auth.txt file on the ide or local when developing.
     It will be overwritten when on the target servers.
    :param seperator_ide: the seperator used in the authentication file when in r studio server (spaces allowed)
    :param seperator_targetserver: the seperator used in the authentication file when on the target server (does not allow for spaces)
    :param debug_mode: if set to true, all log messages (including debug and trace) will also be shown.
    :param force_cross_connection: string ('O', 'T', 'A' 'P', 'I') if set, you force a cross connection, e.g. running
      on O source code but targeting T databases. Using this settings is frowned upon. Shame on you for using this
      setting. The only time this is acceptable is when targeting WHA, the 'I' option or when your are missing
      a database in an environment.
    :param use_hana:
    :param use_bar:
    :param use_apex:
    :param use_cbd:
    :param use_nor:
    :param console_log_only:  boolean if true log appender type will be console only
    :return: collection of settings and parameters for the chosen server_environment.
    """

    working_dir = os.getcwd()

    bar_instance = None
    hana_instance = None
    apex_instance = None
    cbd_instance = None
    nor_instance = None
    authfile = None
    seperator = None

    if environment not in ["P", "PO", "PT", "PA", "PP", "JO", "JT", "JA", "JP", "O", "T", "A", "P"]:
        raise Exception("You must select one of these options: P, PO, PT, PA, PP, JO, JT, JA, JP, O, T, A, P. " +
                        "But you selected:" + environment)

    # default selection
    if environment == "P":
        nodename = socket.gethostname()
        #environment <- switch(nodename,
        #                        lt0054 = "RO",
        #                        lp0148 = "RP",
        #                            stop(paste("no such node known", nodename)))

    driverlocationbar = None
    driverlocationhana = None

    if environment in ["PO", "PT", "PA", "PP"]:

        authfile = authentication_file_location_ide
        seperator = seperator_ide

        #driverlocationbar <- get_driver_location("ojdbc7.jar")
        #driverlocationhana <- get_driver_location("ngdbc.jar")
    else:

        authfile = "auth.txt"
        seperator = seperator_targetserver

        # alliander.common.r drivers have been moved to a central location (/data/share/R/library)
        #driverlocationbar <- get_driver_location("ojdbc7.jar")
        #driverlocationhana <- get_driver_location("ngdbc.jar")

        # for OTAP take the newest alliander.common.r drivers which belongs to my application environment always, dont search for it here!
        #driverlocationbar <-  file.path(working_dir, "Rlibs/alliander.common.r/java/ojdbc7.jar")
        #driverlocationhana <- file.path(working_dir, "Rlibs/alliander.common.r/java/ngdbc.jar")

        # for OTAP take the newest alliander.common.r drivers from the post deploy folder, dont search for it here!
        #if  (environment %in% c("JO", "JT", "JA", "JP")) {
        #    driverlocationbar <-  file.path(working_dir, "/../../", "Rlibs/alliander.common.r/java/ojdbc7.jar")
        #    driverlocationhana <- file.path(working_dir, "/../../", "Rlibs/alliander.common.r/java/ngdbc.jar")
        #}

    # set environment to determine database instance
    if force_cross_connection == "":
        environment_used = environment
    else:
        environment_used = force_cross_connection

    # ONTWIKKEL
    if environment_used in ["O", "PO", "PL", "JO"]:
        bar_instance = "BARO"
        hana_instance = "DHA"
        apex_instance = "AMBO"
        nor_instance = "NORGP"
        cbd_instance = "CDBO"

    # TEST
    if environment_used in ["T", "PT", "JT"]:
        bar_instance = "BART"
        hana_instance = "DHA"
        apex_instance = "AMBT"
        nor_instance = "NORGP"
        cbd_instance = "CDBO"

    # ACCEPTATIE
    if environment_used in ["A", "PA", "JA"]:
        bar_instance = "BARA"
        hana_instance = "KHA"
        apex_instance = "AMBA"
        nor_instance = "NORGP"
        cbd_instance = "CDBP"

    # PRODUCTIE
    if environment_used in  ["P", "PP", "JP"]:
        bar_instance = "BARP"
        hana_instance = "PHA"
        apex_instance = "AMBP_SVC"
        nor_instance = "NORP"
        cbd_instance = "CDBP"

    # INNOVATIE
    if environment == "PP" and force_cross_connection == "I":
        bar_instance = "BARP"
        hana_instance = "WHA"
        apex_instance = "AMBP_SVC"
        nor_instance = "NORP"
        cbd_instance = "CDBP"

    # setup common logger
    if debug_mode:
        common_logger.setup_logger(log_level=logging.DEBUG, console_logger_only=console_log_only)
    else:
        common_logger.setup_logger(log_level=logging.INFO, console_logger_only=console_log_only)

    text = "Loading common settings while running on environment " + environment + ". "
    if use_hana:
        text = text + " hana instance: " + hana_instance + "."
    if use_bar:
        text = text + " bar instance: " + bar_instance + "."
    if use_apex:
        text = text + " apex instance: " + apex_instance + "."
    if use_cbd:
        text = text + " cbd instance: " + cbd_instance + "."
    if use_nor:
        text = text + " nor instance: " + nor_instance + "."

    logging.getLogger(__name__).info(text)

    # get authentication
    authentication = None
    if use_hana or use_bar or use_apex or use_cbd or use_nor:
        if authentication_from_file:
            path_auth = os.path.join(working_dir, authfile)
            authentication = get_authentication.get_authentication_from_file(filepath=path_auth, separator=seperator)
        else:
            authentication = get_authentication.get_authentication_from_env()
    else:
        logging.getLogger(__name__).info("Authentication file not read because no database to" +
                                         "use was specified. See use_hana, use_bar, use_nor, use_cbd " +
                                         "and use_apex arguments.")

    settings = common.CommonSettings()
    settings.environment = environment

    settings.databaseSettings = {}
    if use_hana:
        settings.databaseSettings['HANA'] = db_settings(authentication, "HANA", hana_instance, 'jdbc', driverlocationhana)

    if use_bar:
        settings.databaseSettings['BAR'] = db_settings(authentication, "ORACLE", bar_instance, 'ldap', driverlocationbar)

    if use_apex:
        settings.databaseSettings['APEX'] = db_settings(authentication, "ORACLE", apex_instance, 'ldap', driverlocationbar)

    if use_cbd:
        settings.databaseSettings['CBD'] = db_settings(authentication, "ORACLE", cbd_instance, 'ldap', driverlocationbar)

    if use_nor:
        settings.databaseSettings['NOR'] = db_settings(authentication, "ORACLE", nor_instance, 'ldap', driverlocationbar)

    return settings


def db_settings(authentication: pd.DataFrame, database, instance, connection_type, driver_path):

    # returns db_settings an object containing instance username password and driver
    record = authentication.loc[authentication['ENVIRONMENT'] == instance]
    if len(record.index) != 1:
        raise Exception("instance " + instance + " not found or duplicate entries in authentication text file")

    # create settings
    database_settings = common.DatabaseSettings()
    database_settings.database = database
    database_settings.instance = instance
    database_settings.username = record['USERNAME'].iloc[0]
    database_settings.password = record['PASSWORD'].iloc[0]
    database_settings.connection_type = connection_type
    database_settings.driver_path = driver_path

    return database_settings
