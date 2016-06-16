from __future__ import with_statement
from os import path
from alembic import context
from sqlalchemy import engine_from_config, pool, create_engine
from sqlalchemy.exc import OperationalError
from logging.config import fileConfig
from stock_tracer.library import Configuration
from stock_tracer.library.db import db_base_url, db_ut_url, db_prod_url
from stock_tracer.model.base import Base

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

is_unit_test = Configuration.getInstance().get("__unit_test__")
db_url = db_ut_url if is_unit_test else db_prod_url
config.set_main_option("sqlalchemy.url", db_url)

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def __create_db_if_not_exist(db_url, db_base_url):
    try:
        engine = create_engine(db_url)
        with engine.connect():
            pass
    except OperationalError:
        default_db = create_engine(db_base_url)
        default_db.execute("CREATE DATABASE {0}".format(path.basename(db_url)))

def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    __create_db_if_not_exist(db_url, db_base_url)
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url, target_metadata=target_metadata, literal_binds=True)

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    __create_db_if_not_exist(db_url, db_base_url)
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix='sqlalchemy.',
        poolclass=pool.NullPool)

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
