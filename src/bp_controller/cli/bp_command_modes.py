#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import OrderedDict

from cloudshell.cli.command_mode import CommandMode


class DefaultCommandMode(CommandMode):
    PROMPT = r">\s*$"
    ENTER_COMMAND = ""
    EXIT_COMMAND = ""

    def __init__(self):
        """
        Initialize Default command mode, only for cases when session started not in enable mode

        :param context:
        """

        CommandMode.__init__(self,
                             DefaultCommandMode.PROMPT,
                             DefaultCommandMode.ENTER_COMMAND,
                             DefaultCommandMode.EXIT_COMMAND,
                             enter_action_map=self.enter_action_map(),
                             exit_action_map=self.exit_action_map(),
                             enter_error_map=self.enter_error_map(),
                             exit_error_map=self.exit_error_map())

    def enter_action_map(self):
        return OrderedDict()

    def enter_error_map(self):
        return OrderedDict()

    def exit_action_map(self):
        return OrderedDict()

    def exit_error_map(self):
        return OrderedDict()


class ConfigCommandMode(CommandMode):
    PROMPT = r"%\s*$"
    ENTER_COMMAND = "bpsh"
    EXIT_COMMAND = "exit"

    def __init__(self):
        """
        Initialize Config command mode

        :param context:
        """

        exit_action_map = {self.PROMPT: lambda session, logger: session.send_line("exit", logger)}
        CommandMode.__init__(self,
                             ConfigCommandMode.PROMPT,
                             ConfigCommandMode.ENTER_COMMAND,
                             ConfigCommandMode.EXIT_COMMAND,
                             enter_action_map=self.enter_action_map(),
                             exit_action_map=exit_action_map,
                             enter_error_map=self.enter_error_map(),
                             exit_error_map=self.exit_error_map())

    def enter_action_map(self):
        return OrderedDict()

    def enter_error_map(self):
        return OrderedDict()

    def exit_error_map(self):
        return OrderedDict()


CommandMode.RELATIONS_DICT = {
    DefaultCommandMode: {
        ConfigCommandMode: {}
    }
}
