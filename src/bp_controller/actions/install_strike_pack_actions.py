#!/usr/bin/python
# -*- coding: utf-8 -*-

import re

from bp_controller.command_templates import install_strikes
from cloudshell.cli.command_template.command_template_executor import CommandTemplateExecutor


class InstallStrikePackActions(object):
    TIMEOUT = 600

    def __init__(self, cli_service, logger):
        """ Strike pack installation actions

        :param cli_service: default mode cli_service
        """

        self._cli_service = cli_service
        self._logger = logger

    def get_strike_pack_version(self, conn_name="bps"):
        """ Get current installed strike pack version """

        output = CommandTemplateExecutor(self._cli_service,
                                         install_strikes.GET_STRIKE_PACK_VERSION,
                                         timeout=self.TIMEOUT).execute_command(conn_name=conn_name)

        match = re.search(r"(?P<version>\d+)", output, re.DOTALL)

        if not match:
            raise Exception(self.__class__.__name__, "Strike Pack version determination failed: {}".format(output))

        return match.groupdict().get("version")

    def reinit_connection(self, conn_name="quali"):
        """ Re-initialize BPS Connection installed strike pack version """

        command = install_strikes.REINIT_CONNECTION.format(conn_name=conn_name,
                                                           login=self._cli_service.session.username,
                                                           password=self._cli_service.session.password)

        self._logger.debug("Re-init session: {}".format(command))

        output = self._cli_service.send_command(command, timeout=self.TIMEOUT)

        self._logger.debug("Re-init session finished: {}".format(output))

        # output = CommandTemplateExecutor(self._cli_service,
        #                                  install_strikes.REINIT_CONNECTION).execute_command(conn_name=conn_name,
        #                                                                                     login=self._cli_service.session.username,
        #                                                                                     password=self._cli_service.session.password)

        if not re.search(r"bPSConnection\d+", output):
            raise Exception(self.__class__.__name__, "Re-initialize BPS connection failed: {}".format(output))

        return conn_name

    def install_strike_pack(self, strike_pack_url, conn_name="bps"):
        """ Install strike pack """

        self._logger.debug("Install strike pack: URL - {}, CONN - {}".format(strike_pack_url, conn_name))

        output = CommandTemplateExecutor(self._cli_service,
                                         install_strikes.INSTALL_STRIKE_PACK,
                                         timeout=self.TIMEOUT).execute_command(conn_name=conn_name,
                                                                               strike_pack_url=strike_pack_url)

        self._logger.debug("Install strike pack finished: {}".format(output))

        # if not re.search(r"iluAddLicenseServers ended", output):
        #     raise Exception(self.__class__.__name__, "Add License Server failed with error: {}".format(output))

    def reload_device(self, timeout=600, conn_name="bps"):
        """ Reload device

        :param timeout: session reconnect timeout
        :param conn_name: BPS connection name
        :param action_map: actions will be taken during executing commands, i.e. handles yes/no prompts
        :param error_map: errors will be raised during executing commands, i.e. handles Invalid Commands errors
        """

        self._logger.debug("Start reload device")
        try:
            output = CommandTemplateExecutor(self._cli_service,
                                             install_strikes.REBOOT,
                                             timeout=self.TIMEOUT).execute_command(conn_name=conn_name)

            self._logger.debug("Reboot output: {}".format(output))
        except Exception as e:
            self._logger.debug("Connection closed: {}".format(e))
            pass

        self._logger.debug("Waiting for session reconnect")
        self._cli_service.reconnect(timeout)
