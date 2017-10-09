#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import time

from cloudshell.cli.command_mode_helper import CommandModeHelper
from cloudshell.cli.session.ssh_session import SSHSession
from bp_command_modes import DefaultCommandMode, ConfigCommandMode


class BreakingPointCliHandler(object):
    def __init__(self, cli, resource_address, username, password):
        self._cli = cli
        self.resource_address = resource_address
        self.username = username
        self.password = password
        self.modes = CommandModeHelper.create_command_mode()

    @property
    def default_mode(self):
        return self.modes[DefaultCommandMode]

    @property
    def config_mode(self):
        return self.modes[ConfigCommandMode]

    def _new_sessions(self):
        new_sessions = self._ssh_session()
        return new_sessions

    def _ssh_session(self):
        return SSHSession(self.resource_address, self.username, self.password)

    def _enter_config_mode(self, session, logger):
        max_retries = 5
        error_message = "Failed to enter config mode, please check logs, for details"
        output = session.hardware_expect(ConfigCommandMode.ENTER_COMMAND,
                                         '{0}|{1}'.format(ConfigCommandMode.PROMPT, DefaultCommandMode.PROMPT), logger)

        if not re.search(ConfigCommandMode.PROMPT, output):
            retries = 0
            while not re.search(r"[Cc]onfiguration [Ll]ocked", output, re.IGNORECASE) or retries == max_retries:
                time.sleep(5)
                output = session.hardware_expect(ConfigCommandMode.ENTER_COMMAND,
                                                 '{0}|{1}'.format(ConfigCommandMode.PROMPT, DefaultCommandMode.PROMPT),
                                                 logger)
            if not re.search(ConfigCommandMode.PROMPT, output):
                raise Exception('_enter_config_mode', error_message)

    def get_cli_service(self, command_mode):
        """Use cli.get_session to open CLI connection and switch into required mode

        :param CommandMode command_mode: operation mode, can be default_mode/enable_mode/config_mode/etc.
        :return: created session in provided mode
        :rtype: CommandModeContextManager
        """
        return self._cli.get_session(self._new_sessions(), command_mode)
