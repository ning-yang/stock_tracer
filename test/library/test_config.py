from stock_tracer.library import get_configuration

class TestConfig(object):

    def test_get_configuration(self):
        configs = get_configuration('global')

        assert configs
        assert configs

    def test_get_configuration_not_exist(self):
        config = get_configuration('not_exist', missing_ok=True)

        assert len(config) == 0
