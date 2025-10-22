import logging

def setup_logging(logfile="raceclock.log"):
    logging.basicConfig(
        filename=logfile,
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s"
    )

def log_error(error):
    logging.error(str(error))

def log_info(msg):
    logging.info(msg)
