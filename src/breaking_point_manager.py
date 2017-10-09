#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import requests
import ssl

from retrying import retry
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager
from requests_manager import get_assign_slot_request
requests.packages.urllib3.disable_warnings()


RETRY_SECOND = 1000
RETRY_MINUTE = RETRY_SECOND * 60


class MyAdapter(HTTPAdapter):
    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = PoolManager(num_pools=connections, maxsize=maxsize, block=block,
                                       ssl_version=ssl.PROTOCOL_TLSv1)


def pretty_print_requests(req):
    request = req.request
    print('\n\n{}\n{}\n{}\n\n{}'.format(
        '-----------REQUEST START-----------',
        request.method + ' ' + request.url,
        '\n'.join('{}: {}'.format(k, v) for k, v in request.headers.items()),
        request.body,
    ))
    print '-----------REQUEST END-----------'
    print '\n\n-----------RESPONSE START-----------'
    print req.status_code
    print '\n'
    print req.headers.get('content-type')
    print req.content
    print '-----------RESPONSE END-----------'
    print '\n\n'


class BPS(object):
    def __init__(self, ip_string, username, password):
        self._cli = None
        self.ip_string = ip_string
        self.username = username
        self.password = password
        self.session = requests.Session()
        self.session.mount('https://', MyAdapter())

    @retry(stop_max_delay=RETRY_MINUTE * 10, wait_fixed=RETRY_SECOND * 60)
    def login_rest(self, enable_request_prints=False):
        """ """

        service = 'https://' + self.ip_string + '/api/v1/auth/session'
        headers = {'content-type': 'application/json'}
        data = json.dumps({'username': self.username, 'password': self.password})
        r = self.session.post(service, data=data, headers=headers, verify=False)
        if enable_request_prints:
            pretty_print_requests(r)
        if r.status_code == 200:
            print 'Login successful. Welcome ' + self.username
        else:
            raise Exception('{0}: Failed to logon chassis {1}:\n{2}'.format(r.status_code, self.ip_string, r.content))

    def logout_rest(self):
        self.session = None

    @retry(stop_max_delay=RETRY_MINUTE * 5, wait_fixed=RETRY_SECOND * 15)
    def assign_slots(self, host, vm_name, slot_id, number_of_test_nics, enable_request_prints=False):
        """ """

        request = get_assign_slot_request(host, vm_name, slot_id, number_of_test_nics)
        service = 'https://' + self.ip_string + '/api/v1/admin/vmdeployment/controller/assignSlotsToController'
        headers = {'content-type': 'application/json'}
        # data = {'username': self.username, 'password': self.password}
        # headers.update(data)
        r = self.session.post(service, data=json.dumps(request), headers=headers, verify=False)
        if enable_request_prints:
            pretty_print_requests(r)
        if r.status_code == 200:
            print 'Assign slot successful.'
        else:
            raise Exception(
                '{0}: Failed to assign {1} to chassis {2}:\n{3}'.format(r.status_code, vm_name, self.ip_string,
                                                                        r.content))
