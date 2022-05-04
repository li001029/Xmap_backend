import os 
from app import application 
from app.logger import logger

LOG = logger.get_root_logger(os.environ.get('ROOT_LOGGER', 'root'))

@application.route("/")
def hello():
  return "Hello X-Map!"
  
if __name__ == "__main__":
    LOG.info('running environment: %s', os.environ.get('APP_ENV'))
    application.run()
