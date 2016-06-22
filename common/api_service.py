import abc

def API(service, api_name):
    """implements decorator

    :param service:
    """
    def dec(api):
        service.map_api(api, api_name)
        return api
    return dec

class APIService(object):
    """APIService"""
    operations = {}

    @classmethod
    @abc.abstractmethod
    def map_api(cls, api):
        """map_api

        :param api:
        """
        return None
