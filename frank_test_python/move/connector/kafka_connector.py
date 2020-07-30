from sanne_test_python.move import common
from sanne_test_python.move.connector import base_connector
import logging

#from confluent_kafka import Producer
import logging
import os
import time
import socket
#import hashlib
#import glob
#import signal
#import redis
#from health import health  # fastapi health server in directory 'health'
import json
import shutil

"""
# TODO: here is some example code for a kafka producer. This should be rewritten in a generic kafka connector
# TODO: which does basic consuming and basic producing on any topic with any message.
# TODO: anonymous en kerberos needs to be supported.
# TODO: please take a look in the alliander-common.csharp repository on github for the general idea.
"""
class KafkaConnector(base_connector.BaseConnector):

    host = None
    port = None
    connection_string = None
    connection = None

    def close(self):
        self.connection.close()

    def connect(self, database_settings: common.DatabaseSettings):
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # @title Creates a connection a kafka bus
        # @author Sanne Korzec (Alliander)
        # @param username username of your database account
        # @param password password of your database account
        # @param database database that you want to use currently only possible to HANA
        # @param server Server of the database that you want to use options are HANA: WHA/DHA/KHA/PHA
        # @param class_path Optional path to the class_path for the database HANA: ngdbc.jar file
        # @return A database connection
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        print("meh..")

    def cursor_execute(self, query):
        print("meh..")

'''
class GracefullExit:
    terminate = False

    def __init__(self):
        logging.info("Registering SIGINT and SIGTERM")
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

    def exit_gracefully(self, signum, frame):
        logging.info('(SIGTERM) Terminating...')
        self.terminate = True


def md5(fname):
    """  read a file and return its md5 hexdigest """
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()
'''


def tcp_connect(host, port):
    """ return True if a tcp connection could be made, else return False """
    retval = False

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    try:
        s.connect((host, port))
        retval = True
    except Exception as msg:
        logging.error("Socket Error: {}".format(msg))
    finally:
        s.close()

    return retval


def health_kafka():
    # try a simple tcp connect to the first bootstrap server
    connection = 0
    try:
        host, port = os.environ.get("BOOTSTRAP_SERVERS").split(";")[0].split(":")
        description = f"Kafka connection on {host}:{port}"
        if tcp_connect(host, int(port)):
            connection = 1
    except Exception as msg:
        logging.error(msg)
        description = "Could not determine kafka server"

    return {
        "name": "kafka",
        "description": description,
        "connection": connection,
    }


def health_logstash():
    # try a socket connection to Logstash and return the result
    LOGSTASH_HOST = os.environ.get("LOGSTASH_HOST")
    LOGSTASH_PORT = int(os.environ.get("LOGSTASH_PORT"))

    connection = 0
    if tcp_connect(LOGSTASH_HOST, LOGSTASH_PORT):
        connection = 1

    return {
        "name": "logstash",
        "description": f"Logstash connection on {LOGSTASH_HOST}:{LOGSTASH_PORT}",
        "connection": connection,
    }

''' 
def health_redis():
    # try a socket connection to Redis and return the result
    REDIS_HOST = os.environ.get("REDIS_HOST")
    REDIS_PORT = int(os.environ.get("REDIS_PORT"))

    connection = 0
    data = {
        "file_queue_length": -1,
        "kafka_queue_length": -1,
        "error_queue_length": -1,
        "processing_queue_length": -1
    }

    try:
        redis_conn = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)
        redis_conn.ping()
        connection = 1
        data = {
            "file_queue_length": redis_conn.llen('file'),
            "kafka_queue_length": redis_conn.llen('kafka'),
            "error_queue_length": redis_conn.llen('error'),
            "processing_queue_length": redis_conn.llen('processing')
        }
    except Exception:
        pass

    return {
        "name": "redis",
        "description": f"Redis connection on {REDIS_HOST}:{REDIS_PORT}",
        "connection": connection,
        "data": data
    }
'''

def health_mbs_file_path():
    """ Test if the share is accessible """
    MBS_FILE_PATH = os.environ.get('MBS_FILE_PATH')

    connection = 0
    data = {
        "nr_of_files": -1
    }
    if os.access(MBS_FILE_PATH, os.R_OK | os.X_OK):
        connection = 1

    # count files in directory
    try:
        data = {
            "nr_of_files": len([name for name in os.listdir(MBS_FILE_PATH) if os.path.isfile(os.path.join(MBS_FILE_PATH, name))])
        }
    except Exception:
        pass

    return {
        "name": "mbs_file_path",
        "description": f"File connection to {MBS_FILE_PATH}",
        "connection": connection,
        "data": data
    }


def delivery_report(err, msg):
    """ Called once for each message produced to indicate delivery result.
        Triggered by poll() or flush(). """
    if err is not None:
        logging.error(f"delivery_report: {err}")
    else:
        pass
        # logging.info('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))
        # so delete msg from redis?


def error_cb(err):
    logging.error(f"error_cb: {err.str()}")

'''
def get_valid_mbs_file(path):
    """ read directory and collect .mbs files
    then collect md5 files
    123456.mbs     -> data file
    123456.mbs.md5 -> contains hash of file above
    123456.mbs.err -> corrupt file, please send again
    return sorted array with valid .mbs files
    """

    # search for all files ending with .mbs.md5
    files = glob.glob(f"{path}/*.mbs.md5")
    files.sort(key=os.path.getmtime)
    res = []

    for file in files:
        logging.debug(f"Found file {file}")
        mbsfile, ext = os.path.splitext(file)
        # file:    123456.mbs.md5
        # mbsfile: 123456.mbs

        # test if the mbs data file actually exists
        if not os.path.isfile(mbsfile):
            logging.error(f"md5 file {file} found but the data file {mbsfile} is missing. {file} will be removed.")
            os.remove(file)
            continue

        # so we have a md5 and a data file. test if contents are valid
        with open(file) as f:
            if f.readline().strip() != md5(mbsfile).strip():
                logging.debug(f"Corrupt file {mbsfile} detected. File will be removed.")
                os.rename(file, mbsfile + ".err")
                os.remove(mbsfile)
                continue

        res.append(mbsfile)

    return res

def send_to_kafka():
    """ read redis queue 'kafka' and send each record to kafka
    using kafka producer p and MBS class mbs"""

    count = 0
    count_total = 0
    flush_size = 1000
    time_start = time.time()
    raw_byte_size = 0

    try:
        if r.llen('kafka') == 0:
            return

        logging.info(f"Kafka sender is starting, found {r.llen('kafka')} messages on kafka queue ...")
        while(r.llen('kafka') != 0):
            raw_bytes = r.rpop('kafka')
            raw_byte_size = raw_byte_size + len(raw_bytes)

            # Asynchronously produce a message, the delivery report callback
            # will be triggered from poll() above, or flush() below, when the message has
            # been successfully delivered or failed permanently.
            p.produce(
                os.environ.get("TOPIC"),
                raw_bytes,
                callback=delivery_report,
            )
            count_total = count_total + 1
            count = count + 1

            # log progress each flush
            if count_total % flush_size == 0:
                p.flush()
                duration = time.time() - time_start
                logging.info(f"{count_total} records produced @ {round(raw_byte_size/count)} byte/r @ {round(count/duration)} r/s, {r.llen('kafka')} msg to do ")
                time_start = time.time()
                count = 0
                raw_byte_size = 0

            if g.terminate:
                logging.info(f"Got termination signal in send_to_kafka function")
                break

        logging.info(f"Flushing remaining records to kafka")
        p.flush()

    except redis.exceptions.ConnectionError:
        logging.error("send_to_kafka: Could not connect to Redis")

    return

def send_to_logstash(filename):
    """ send valid files to logstash.
    return True on success, False on fail """
    LOGSTASH_HOST = os.environ.get("LOGSTASH_HOST")
    LOGSTASH_PORT = int(os.environ.get("LOGSTASH_PORT"))

    # initialize metrics
    start = time.time()
    event_count = 0

    # our return value
    retval = False

    # and process the file
    try:
        logging.info(f"Processing file {filename} with md5sum {hashlib.md5(open(filename, 'rb').read()).hexdigest()}")
        logging.debug(f"Connecting to {LOGSTASH_HOST}:{LOGSTASH_PORT}")
        # create socket for writing. You cannot reuse the socket!
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)
        s.connect((LOGSTASH_HOST, LOGSTASH_PORT))
        with open(filename) as f:
            # set the filename
            fn = os.path.basename(filename)

            # set the header, it is the first line
            cur_line = 1
            num_lines = 0
            for _ in open(filename): num_lines += 1
            header = f.readline()[:-1]
            f.seek(0, 0)  # Send header again as data
            for line in f:
                # and construct the message to send
                # "202003231400.mbs;PC com1      2020-03-23 14:00 ;32666;00000005;Alk-S   9001174G10-1V3  V3                  I            0.00A       act 20200323140000000  20200323130000000 PC"
                msg = (fn + ";" + header + ";" + "{:d}".format(num_lines) + ";" + "{:08d}".format(cur_line) + ";" + line)
                s.sendall(msg.encode('utf-8'))
                event_count += 1
                cur_line += 1
        s.close()
        retval = True

    except socket.error as msg:
        logging.error("Socket Error: {}".format(msg))
        # resume operation, the connection can be back later
    except IOError as e:
        logging.error("I/O error({}): {}: {}".format(e.errno, e.strerror, e.filename))
    except OSError as e:
        logging.error("OS error({}): {}".format(e.errno, e.strerror))

    elapsed = time.time() - start
    logging.info("Processed {li} lines in {e:1.2f} seconds".format(li=event_count, e=elapsed))

    return retval


def load_into_redis(filename):
    """ Open a file and load each line into Redis. Use pipeline to ensure atomic operation """
    logging.info(f"loading {filename} to redis")
    count = 0

    try:
        pipeline = r.pipeline()

        with open(filename, "r") as f:
            header = next(f).rstrip()
            data = [line.rstrip() for line in f]

            for message in data:
                json_message = {
                    "line": message,
                    "filename": filename,
                    "created": round(time.time())
                }
                # store each line in the 'file' queue as json message
                pipeline.lpush('file', json.dumps(json_message))
                count = count + 1

                # TODO run some tests on stopping the producer with SIGTERM
                # terminate myself
                # if count > 100:
                #     os.kill(os.getpid(), signal.SIGTERM)

        pipeline.execute()

        logging.info(f"added {count} lines with header {header} to redis")

    except redis.exceptions.ConnectionError:
        logging.error(f"load_into_redis: Could not connect to Redis. File {filename} was not loaded into redis")

    except Exception as msg:
        logging.error(f"While loading {filename} into Redis, an error occured: {msg}")

    return count

def move_force(filename, dest):
    """ move a file to a destination. If the file exists at destination,
    delete it first
    filename: path to file
    dest: destination directory """

    try:
        real_dst = os.path.join(dest, shutil._basename(filename))
        if os.path.exists(real_dst):
            logging.info(f"Deleting existing file: {real_dst}")
            os.unlink(real_dst)

        res = shutil.move(filename, dest)
        logging.info(f"Saved {res}")
    except:
        logging.warning(f"Could not move {filename} to {dest}")


if __name__ == "__main__":
    MBS_FILE_PATH = os.environ.get('MBS_FILE_PATH')
    MBS_FILE_PATH_SAVE = os.environ.get('MBS_FILE_PATH_SAVE', "")
    APPLICATION_VERSION = os.environ.get('APPLICATION_VERSION', 'unknown')
    SEND_TO_KAFKA = int(os.environ.get('SEND_TO_KAFKA', 1))

    logging.info(f"Starting Kafka producer version {APPLICATION_VERSION}")
    if MBS_FILE_PATH_SAVE:
        logging.info(f"Saving processed .mbs files on {MBS_FILE_PATH_SAVE}")

    if SEND_TO_KAFKA == 0:
        logging.info(f"Kafka is disabled")

    logging.info("starting health endpoint")
    health.register(health_kafka)
    health.register(health_mbs_file_path)
    if os.environ.get('SEND_TO_LOGSTASH') == "1":
        health.register(health_logstash)
    health.register(health_redis)

    health.init()  # todo fix this
    logging.info("started health endpoint")

    config = {
        "bootstrap.servers": os.environ.get("BOOTSTRAP_SERVERS"),
        "group.id": os.environ.get("GROUPID"),
        # 'auto.offset.reset': 'earliest',
        "debug": os.environ.get('LIBRDKAFKA_DEBUG'),

        "batch.num.messages": 10000,  # Maximum number of messages batched in one MessageSet. The total MessageSet size is
        # also limited by message.max.bytes (which defaults to 1MB). Default 10000
        "queue.buffering.max.ms": 1000,  # Delay in milliseconds to wait for messages in the producer queue to accumulate
        # before constructing message batches (MessageSets) to transmit to brokers. A higher value allows larger and more
        # effective (less overhead, improved compression) batches of messages to accumulate at the expense of increased
        # message delivery latency. Default 0.5
        "queue.buffering.max.messages": 100000,  # Maximum number of messages allowed on the producer queue. This queue
        # is shared by all topics and partitions. Default 100000
        "compression.codec": "gzip",  # Compression codec to use for compressing message sets: none, gzip or snappy.
        "message.timeout.ms": 300000,  # Local message timeout. This value is only enforced locally and limits
        # the time a produced message waits for successful delivery. A time of 0 is infinite. This is the maximum
        # time librdkafka may use to deliver a message (including retries). Default 300000 (300 seconds / 5 min)
        "message.send.max.retries": 2,  # How many times to retry sending a failing Message. Note: retrying may cause
        # reordering unless enable.idempotence is set to true. Default 2. Range 0-10000000
    }

    if os.environ.get("TESTMODE", False) == "1":
        logging.info("TESTMODE activated")
    else:
        logging.info("TESTMODE not activated, adding security config")
        config.update(
            {
                "sasl.mechanism": "GSSAPI",
                "sasl.kerberos.service.name": "kafka",
                "sasl.kerberos.principal": os.environ.get("KERBEROS_PRINCIPAL"),
                "sasl.kerberos.keytab": os.environ.get("KEYTAB_FILE"),  # "/mnt/secrets2/some-keytab.keytab",
                "security.protocol": "SASL_SSL",
                "ssl.ca.location": os.environ.get("KAFKA_SSL_CERT")
            }
        )

    # create the producer
    if SEND_TO_KAFKA:
        logging.info(f"Creating Kafka producer on {os.environ.get('BOOTSTRAP_SERVERS')}")
        p = Producer(config)

    # create the redis cache
    REDIS_HOST = os.environ.get("REDIS_HOST")
    REDIS_PORT = int(os.environ.get("REDIS_PORT"))
    r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)

    # init signal handlers
    g = GracefullExit()

    # main program loop testing for files and processing them
    while True:
        if SEND_TO_KAFKA:
            # Trigger any available delivery report callbacks from previous produce() calls
            p.poll(1)

        # the read directory returns valid files, ie with a valid md5 has
        files = get_valid_mbs_file(MBS_FILE_PATH)

        if files:
            filename = files[0]
            logging.info(f"processing file {filename} ...")

            # logstash is the legacy architecture
            if os.environ.get('SEND_TO_LOGSTASH') == "1":
                send_to_logstash(filename)

            if MBS_FILE_PATH_SAVE:
                move_force(f"{filename}.md5", MBS_FILE_PATH_SAVE)
            else:
                os.unlink(f"{filename}.md5")

            load_into_redis(filename)

            if MBS_FILE_PATH_SAVE:
                move_force(filename, MBS_FILE_PATH_SAVE)
            else:
                os.unlink(filename)

            logging.info(f"processing file {filename} done")

            if SEND_TO_KAFKA:
                send_to_kafka()

        else:
            if SEND_TO_KAFKA:
                send_to_kafka()
            logging.info(f"Waiting for files in {MBS_FILE_PATH}...")
            time.sleep(10)

        if g.terminate:
            logging.info("Producer terminated gracefully")
            break

        time.sleep(1)
'''
