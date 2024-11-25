import os
import sys
import redis

from celery import Celery
from dotenv import load_dotenv
from loguru import logger
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from configurations.cache import CacheConfiguration, CacheConfigurationDTO
from configurations.celery import CeleryConfiguration, CeleryConfigurationDTO
from configurations.db import DBConfiguration, DBConfigurationDTO

logger.add(sys.stderr, colorize=True, format="<green>{time:MMMM-D-YYYY}</green> | <black>{time:HH:mm:ss}</black> | <level>{level}</level> | <cyan>{message}</cyan> | <magenta>{name}:{function}:{line}</magenta> | <yellow>{extra}</yellow>")

logger.debug("Loading environment variables from .env file")
load_dotenv()
logger.debug("Loaded environment variables from .env file")

logger.info("Loading environment variables")
APP_NAME: str = os.environ.get('APP_NAME')
logger.info("Loaded environment variables")

logger.info("Loading Configurations")
cache_configuration: CacheConfigurationDTO = CacheConfiguration().get_config()
celery_configuration: CeleryConfigurationDTO = CeleryConfiguration().get_config()
db_configuration: DBConfigurationDTO = DBConfiguration().get_config()
logger.info("Loaded Configurations")

logger.info("Initializing Redis database")
redis_session = redis.Redis(
    host=cache_configuration.host,
    port=cache_configuration.port,
    password=cache_configuration.password
)

logger.info("Initializing Celery")
redis_url: str = celery_configuration.backend_url.format(
    password=cache_configuration.password,
    host=cache_configuration.host,
    port=cache_configuration.port,
    db=celery_configuration.db
)
celery = Celery(
    APP_NAME,
    backend=redis_url,
    broker=redis_url,
    include=[
        "tasks.scrape.products"
    ]
)
logger.info("Initialized Celery")

logger.info("Initializing PostgreSQL database")
engine = create_engine(f'postgresql+psycopg2://atlys:ATLYS12345@{db_configuration.host}:5432/atlys')
Session = sessionmaker(bind=engine)
db_session = Session()
Base = declarative_base()
logger.info("Initialized PostgreSQL database")