import socket
import sys
import threading
import time
from datetime import datetime


class Scaner:
    MAX_SECONDS_TIMEOUT_SOCKET = 0.5
    MAX_RANGE_PORT = 65535
    _list_of_messages = []

    def scan_ip_range_and_port_range(self, begin_ip, end_ip, begin_port, end_port):
        last_node_in_begin_ip = int(self.get_last_node_in_ip(begin_ip))
        last_node_in_last_ip = int(self.get_last_node_in_ip(end_ip))
        if last_node_in_begin_ip > last_node_in_last_ip:
            last_node_in_begin_ip, last_node_in_last_ip = last_node_in_last_ip, last_node_in_begin_ip

        for last_node in range(last_node_in_begin_ip, last_node_in_last_ip):
            parsed_begin_ip = self.parse_ip(begin_ip)
            ip = '.'.join(parsed_begin_ip[:3]) + '.' + str(last_node)
            self.scan_ip_in_range_port(ip=ip, begin_port=begin_port, end_port=end_port)

        self.print_message_list()

    def scan_ip_in_range_port(self, ip, begin_port, end_port):
        if end_port > self.MAX_RANGE_PORT:
            end_port = self.MAX_RANGE_PORT

        if begin_port > end_port:
            begin_port, end_port = end_port, begin_port

        for port in range(begin_port, end_port):
            task = threading.Thread(target=self.scan_thread, args=(ip, port))
            task.start()

        self.print_message_list()

    def scan_thread(self, ip, port):
        status, out_info_about_port = self.scan_ip_port(ip, port)
        if status == 1:
            self._list_of_messages.append(ip + ':' + str(port) + ' its open.' + 'info -> ' + out_info_about_port)

    def scan_ip_port(self, ip, port) -> [int, str]:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(self.MAX_SECONDS_TIMEOUT_SOCKET)
        try:
            connect = sock.connect((ip, port))
            try:
                bytes = sock.recv(2048)
                out_info_about_port = bytes.decode('utf-8').strip()
            except:
                out_info_about_port = "Not found info"
            sock.close()
            return 1, out_info_about_port
        except:
            pass

        return 0, None

    def print_message_list(self):
        [print(message) for message in self._list_of_messages]

    def get_last_node_in_ip(self, ip):
        return self.parse_ip(ip)[3]

    def parse_ip(self, ip):
        return ip.rsplit('.')


if __name__ == '__main__':
    start = datetime.now()
    scaner = Scaner()
    if len(sys.argv) - 1 == 4:
        scaner.scan_ip_range_and_port_range(begin_ip=sys.argv[1], end_ip=sys.argv[2], begin_port=int(sys.argv[3]), end_port=int(sys.argv[4]))
    elif len(sys.argv) - 1 == 3:
        scaner.scan_ip_in_range_port(ip=sys.argv[1], begin_port=int(sys.argv[2]), end_port=int(sys.argv[3]))
    else:
        scaner.scan_ip_in_range_port(ip='127.0.0.1', begin_port=1, end_port=10000)
    ends = datetime.now()
    print('Scan is ended with count seconds : {}'.format(ends - start))
    input()
