import pandas as pd
import logging
import os


def get_authentication_from_file(
                        filepath="tests/test_source_scripts/auth.txt",
                        separator=" ",
                        column_names=["ENVIRONMENT", "USERNAME", "PASSWORD"]):
    # Retrieves authentication variables from a file
    #
    # filepath = characters specifying full file path to an authentication file
    # separator = separator between items
    # column_names = character specifying authentication table column names,
    #  defaults to c("ENVIRONMENT","USERNAME", "PASSWORD")

    data = pd.read_csv(filepath, sep=separator, header=None, index_col=False)
    data.columns = column_names
    logging.getLogger(__name__).info("Finished reading file: " + filepath)
    print(data)
    return data


def get_authentication_from_env(column_names=["ENVIRONMENT", "USERNAME", "PASSWORD"]):
    # Retrieves authentication variables from the environment variables
    #
    # column_names = character specifying authentication table column names,
    #  defaults to c("ENVIRONMENT","USERNAME", "PASSWORD")

    environments = []
    users = []
    pwds = []

    for database in ['HANA', 'BAR', 'CDB', 'NOR', 'APEX']:

        environment_variable = database + 'DBINSTANCE'
        env = os.environ.get(environment_variable)
        if env is not None:
            environments.append(env)
            users.append(os.environ.get(database + 'DBUSERNAME'))
            pwds.append(os.environ.get(database + 'DBPASSWORD'))

    data = {'ENVIRONMENT': environments, 'USERNAME': users, 'PASSWORD': pwds}
    df = pd.DataFrame(data, columns=column_names, index=False)
    return df
