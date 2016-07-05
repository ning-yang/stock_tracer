from os import chdir, getcwd, path
from alembic import command
from alembic.config import Config

import stock_tracer
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from stock_tracer.common import Configuration, Logger
from stock_tracer.common.db import db_base_url, db_name_ut

class UnitTest(object):
    """UnitTest"""

    @classmethod
    def setup_class(cls):
        """setup_class"""
        Configuration.set('__unit_test__', 'True')
        logging_config = Configuration.get('logging')
        logging_config['file'] = False
        logging_config['es'] = False

class DBUnitTest(UnitTest):
    """DBUnitTestMixin"""

    @property
    def migration_root(self):
        """migration_root"""
        return path.dirname(stock_tracer.__file__)

    def setup_method(self, method):
        """setup_method

        :param method:
        """
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
            command.upgrade(alembic_config, "head")
        finally:
            chdir(cwd)

        self.logger = Logger.get(self.__class__.__name__)

    def teardown_method(self, method):
        """teardown_method

        :param method:
        """
        pass
