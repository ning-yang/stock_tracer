from os import chdir, getcwd, path
from functools import partial
from alembic import command
from alembic.config import Config

import stock_tracer
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from stock_tracer.library.db import db_base_url, db_name_ut, transaction

transaction = partial(transaction, env="ut")


class DBUnitTestMixin(object):

    @property
    def migration_root(self):
        return path.dirname(stock_tracer.__file__)

    def setup_method(self, method):
        # drop database at the beginning of each test
        try:
            default_db = create_engine(db_base_url)
            default_db.execute('DROP DATABASE {0}'.format(db_name_ut))
        except OperationalError:
            # Ignore error if db doesn't exist
            pass

        cwd = getcwd()
        try:
            chdir(self.migration_root)
            alembic_config = Config("alembic.ini")
            alembic_config.set_main_option("__unit_test__", "True")
            command.upgrade(alembic_config, "head")
        finally:
            chdir(cwd)

    def teardown_method(self, method):
        pass
