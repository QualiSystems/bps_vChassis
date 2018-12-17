#!/usr/bin/python
# -*- coding: utf-8 -*-

from bp_controller.actions.config_licese_server_actions import ConfigLicenseServerActions


class BreakingPointConfigLicenseServerFlow(object):

    def __init__(self, cli_handler):
        self._cli_handler = cli_handler

    def execute_flow(self, license_server_address):
        """ Execute flow which configure license server on BreakingPoint Controller """

        with self._cli_handler.get_cli_service(self._cli_handler.config_mode) as config_session:
            configure_actions = ConfigLicenseServerActions(config_session)

            configure_actions.add_license_server(license_server_address=license_server_address)
            # configure_actions.delete_license_server(license_server_address="localhost")
