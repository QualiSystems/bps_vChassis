from threading import Lock


class PortReservationException(Exception):
    pass


class ReservationInfo(object):
    def __init__(self, groups_limit=12):
        self.__lock = Lock()
        self._groups_limit = groups_limit
        self._initialize()

    def _initialize(self):
        self._groups = {group: None for group in xrange(1, self._groups_limit + 1)}
        self._reserved_ports = {}

    def _get_and_reserve_group_id(self, reservation_id):
        available_group = None
        for group_id, existing_res_id in self._groups.iteritems():
            if (not existing_res_id and not available_group) or (existing_res_id and existing_res_id == reservation_id):
                available_group = group_id
        if not available_group:
            raise PortReservationException(self.__class__.__name__,
                                           'Cannot find available group id for reservation {0}'.format(reservation_id))
        return available_group

    def _check_and_reserve_ports(self, reservation_id, port_list):
        for port in port_list:
            if port not in self._reserved_ports:
                self._reserved_ports[port] = reservation_id
            elif self._reserved_ports[port] != reservation_id:
                raise PortReservationException(self.__class__.__name__,
                                               'Port {0} has been reserved by {1}'.format(port, self._reserved_ports[port]))

    def _unreserve_group(self, reservation_id):
        for group_id, res_id in self._groups.iteritems():
            if res_id == reservation_id:
                self._groups[group_id] = None

    def _unreserve_ports(self, reservation_id):
        ports = self.reserved_ports(reservation_id)
        for port in ports:
            del self._reserved_ports[port]
        return ports

    def reserve(self, reservation_id, port_list):
        with self.__lock:
            self._check_and_reserve_ports(reservation_id, port_list)
            return self._get_and_reserve_group_id(reservation_id)

    def unreserve(self, reservation_id):
        with self.__lock:
            reserved_ports = self._unreserve_ports(reservation_id)
            self._unreserve_group(reservation_id)
            return reserved_ports

    def reserved_ports(self, reservation_id):
        ports = []
        for port, res_id in self._reserved_ports.iteritems():
            if res_id == reservation_id:
                ports.append(port)
        return ports

    def unreserve_all(self):
        reserved_ports = self._reserved_ports.values()
        self._initialize()
        return reserved_ports
