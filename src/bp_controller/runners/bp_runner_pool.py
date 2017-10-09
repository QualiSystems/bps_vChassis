from threading import Lock

from bp_controller.reservation_info import ReservationInfo
from bp_controller.runners.bp_test_runner import BPTestRunner
from cloudshell.devices.driver_helper import get_logger_with_thread_id, get_api


class InstanceLocker(object):
    """
    Lock for each runner instance
    """
    def __init__(self, instance):
        self.__lock = Lock()
        self._instance = instance

    @property
    def instance(self):
        return self._instance

    @instance.setter
    def instance(self, value):
        self._instance = value

    def __enter__(self):
        """

        :return:
        :rtype: BPTestRunner
        """
        self.__lock.acquire()
        return self._instance

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__lock.release()


class BPRunnersPool(object):
    """
    Pool for runner instances
    """
    def __init__(self, reservation_info=ReservationInfo()):
        self._runners = {}
        self._reservation_info = reservation_info

    def actual_runner(self, context):
        """
        Return runner instance for specific reservation id
        :param context:
        :return:
        :rtype: InstanceLocker
        """
        logger = get_logger_with_thread_id(context)
        api = get_api(context)

        reservation_id = context.reservation.reservation_id
        if reservation_id not in self._runners:
            runner_locker = InstanceLocker(BPTestRunner(context, logger, api, self._reservation_info))
            self._runners[reservation_id] = runner_locker
        else:
            runner_locker = self._runners[reservation_id]
            runner_locker.instance.context = context
            runner_locker.instance.logger = logger
            runner_locker.instance.api = api
        return runner_locker
