import logging
import datetime


class MyLog(object):
    def __init__(self, appname):
        self.logger = logging.getLogger(appname)
        self.logger.setLevel(logging.INFO)

        filename = datetime.datetime.today().strftime('%Y-%m-%d') + '-' + appname
        logfile = 'log/' + filename + '.log'

        format = '%(asctime)s - %(levelname)s - %(name)s - %(funcName)s - %(lineno)d : %(message)s'

        formatter = logging.Formatter(format)

        streamhandler = logging.StreamHandler()
        streamhandler.setFormatter(formatter)
        streamhandler.setLevel(logging.ERROR)
        self.logger.addHandler(streamhandler)

        filehandler = logging.FileHandler(logfile)
        filehandler.setFormatter(formatter)
        self.logger.addHandler(filehandler)

    def debug(self, msg):
        self.logger.debug(msg)

    def info(self, msg):
        self.logger.info(msg)

    def warning(self, msg):
        self.logger.warning(msg)

    def error(self, msg):
        self.logger.error(msg)

    def critical(self, msg):
        self.logger.critical(msg)

    def log(self, level, msg):
        self.logger.log(level, msg)

    def setLevel(self, level):
        self.logger.setLevel(level)

    def disable(self):
        logging.disable(50)