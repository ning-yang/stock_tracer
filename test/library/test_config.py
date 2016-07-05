from stock_tracer.common import Configuration
from stock_tracer.test.base import UnitTest

class TestConfig(UnitTest):

    def test_get_configuration(self):
        configs = Configuration.get_configuration('global')
        assert configs

    def test_get_configuration_not_exist(self):
        config = Configuration.get_configuration('not_exist', missing_ok=True)
        assert len(config) == 0
