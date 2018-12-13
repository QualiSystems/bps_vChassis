#!/usr/bin/python
# -*- coding: utf-8 -*-

from bp_controller.actions.install_strike_pack_actions import InstallStrikePackActions


class BreakingPointInstallStrikePackFlow(object):

    def __init__(self, cli_handler, logger):
        self._cli_handler = cli_handler
        self._logger = logger

    def execute_flow(self, strike_pack_url):
        """ Execute flow which configure license server on BreakingPoint Controller """

        with self._cli_handler.get_cli_service(self._cli_handler.config_mode) as config_session:
            configure_actions = InstallStrikePackActions(config_session, self._logger)

            cur_version = configure_actions.get_strike_pack_version()
            self._logger.debug("[FLOW] Current version: {}".format(cur_version))

            bps_connection_name = configure_actions.reinit_connection()
            self._logger.debug("[FLOW] New connection 1: {}".format(bps_connection_name))

            configure_actions.install_strike_pack(strike_pack_url=strike_pack_url, conn_name=bps_connection_name)
            self._logger.debug("[FLOW] Strike pack installation finished")

            # configure_actions.reload_device(conn_name=bps_connection_name)
            # self._logger.info("[FLOW] Reload device finished")
            bps_connection_name = configure_actions.reinit_connection()
            self._logger.debug("[FLOW] New connection 2: {}".format(bps_connection_name))

            new_version = configure_actions.get_strike_pack_version(conn_name=bps_connection_name)
            self._logger.debug("[FLOW] New version: {}".format(new_version))

            if cur_version == new_version:
                raise Exception(self.__class__.__name__, "Strike Pack didn't installed properly")
