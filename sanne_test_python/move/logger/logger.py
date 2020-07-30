import sys
import logging


def setup_logger(log_level=int, console_logger_only=bool):
    """
    This logger is a singleton. Call this setup function once when you start your application.
    (This is also automatically done, when you use load_common_settings.py.)
    After that use this in any class in your project.

    import logging
    logging.getLogger(__name__).debug(message)

    :param log_level: ignores any log level below this enum. e.g. use INFO for production, use DEBUG for development
    :param console_logger_only: if set to false the log is also written to a file.
    :return: implicit singleton logger
    """

    # TODO: use the correct log layout for ELK stack
    # layout <- futile.logger::layout.format("~l [~t] ~m", datetime.fmt = "%Y-%m-%dT%H:%M:%OS3%z")
    syslog_format = '%(name)s(%(lineno)d) - %(levelname)s - %(message)s'
    stream_format = '%(asctime)-15s - ' + syslog_format
    date_format = "%Y-%m-%dT%H:%M:%OS3%z"

    if console_logger_only:
        logging.basicConfig(
            level=log_level,
            format=stream_format,
            datefmt=date_format,
            handlers=(logging.StreamHandler(sys.stdout),)
        )
    else:
        logging.basicConfig(
            filename='log.log',
            filemode='w',
            level=log_level,
            format=stream_format,
            datefmt=date_format,
            handlers=(logging.StreamHandler(sys.stdout),)
        )
