from cloudshell.tg.breaking_point.rest_api.rest_json_client import RestJsonClient
from os.path import basename


class TestConfigurationActions(object):
    def __init__(self, rest_service, logger):
        """ Reboot actions
        :param rest_service:
        :type rest_service: RestJsonClient
        :param logger:
        :type logger: Logger
        :return:
        """
        self._rest_service = rest_service
        self._logger = logger

    def import_test(self, test_file_path):
        """ Upload test file to the BP controller
        :param test_name:
        :type test_name: str
        :param test_file:
        :type test_file: file
        :return:
        """
        self._logger.debug('Importing test {}'.format(test_file_path))
        uri = '/api/v1/bps/upload'
        json_data = {'force': True}
        file_name = basename(test_file_path)
        files = {'file': (file_name, open(test_file_path, 'rb'))}
        data = self._rest_service.request_post_files(uri, json_data, files)
        result = data
        return result

    def export_test(self, test_name):
        self._logger.debug('Exporting test {0}'.format(test_name))
        uri = '/api/v1/bps/export/bpt/testname/' + test_name
        data = self._rest_service.request_get(uri)
        result = data
        return result

    def reserve_port(self, slot, port_list):
        self._logger.debug('Reserving ports {0} on slot {1}'.format(port_list, slot))
        uri = '/api/v1/bps/ports/operations/reserve'
        json_data = {"slot": slot, "portList": port_list, "group": "1", "force": "true"}
        data = self._rest_service.request_post(uri, json_data)
        result = data
        return result

    def unreserve_port(self, slot, port_list):
        self._logger.debug('Unreserving ports {0} on slot {1}'.format(port_list, slot))
        uri = '/api/v1/bps/ports/operations/unreserve'
        json_data = {"slot": slot, "portList": port_list}
        data = self._rest_service.request_post(uri, json_data)
        result = data
        return result
