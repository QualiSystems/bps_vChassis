#!/usr/bin/python
# -*- coding: utf-8 -*-

from cloudshell.cli.command_template.command_template import CommandTemplate


GET_STRIKE_PACK_VERSION = CommandTemplate("${conn_name} getStrikepackId")
REINIT_CONNECTION = "set {conn_name} [bps::connect 127.0.0.1 {login} {password}]"
INSTALL_STRIKE_PACK = CommandTemplate("${conn_name} installStrikepack -url {strike_pack_url}")
REBOOT = CommandTemplate("${conn_name} reboot")
