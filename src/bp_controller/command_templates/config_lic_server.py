#!/usr/bin/python
# -*- coding: utf-8 -*-

from cloudshell.cli.command_template.command_template import CommandTemplate


ADD_SERVER = CommandTemplate("$bps iluAddLicenseServers {lic_server_address}")
DELETE_SERVER = CommandTemplate("$bps iluDeleteLicenseServers {lic_server_address}")
