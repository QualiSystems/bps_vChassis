#!/usr/bin/python
# -*- coding: utf-8 -*-

from bp_controller.flows.bp_config_lic_server_flow import BreakingPointConfigLicenseServerFlow
from bp_controller.cli.bp_cli_handler import BreakingPointCliHandler


class BreakingPointConfigurationRunner(object):
    def __init__(self, cli, resource_address, username, password):
        self._cli = cli
        self.resource_address = resource_address
        self.username = username
        self.password = password

    @property
    def cli_handler(self):
        """ CLI Handler property """

        return BreakingPointCliHandler(self._cli, self.resource_address, self.username, self.password)

    @property
    def configure_license_server_flow(self):
        return BreakingPointConfigLicenseServerFlow(cli_handler=self.cli_handler)

    def configure_license_server(self, license_server_address):
        """ """

        self.configure_license_server_flow.execute_flow(license_server_address=license_server_address)
