#!/usr/bin/python
# -*- coding: utf-8 -*-

import re

from bp_controller.command_templates import config_lic_server
from cloudshell.cli.command_template.command_template_executor import CommandTemplateExecutor


class ConfigLicenseServerActions(object):
    def __init__(self, cli_service):
        """ Save and Restore device configuration actions

        :param cli_service: default mode cli_service
        """

        self._cli_service = cli_service

    def add_license_server(self, license_server_address):
        """ """

        output = CommandTemplateExecutor(self._cli_service,
                                         config_lic_server.ADD_SERVER).execute_command(
            lic_server_address=license_server_address)

        if not re.search(r"iluAddLicenseServers ended", output):
            raise Exception(self.__class__.__name__, "Add License Server failed with error: {}".format(output))

    def delete_license_server(self, license_server_address="localhost"):
        """ """

        output = CommandTemplateExecutor(self._cli_service,
                                         config_lic_server.DELETE_SERVER).execute_command(
            lic_server_address=license_server_address)

        if not re.search(r"iluDeleteLicenseServers ended", output):
            raise Exception(self.__class__.__name__, "Delete License Server failed with error: {}".format(output))
