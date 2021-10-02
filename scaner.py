import socket
import sys
import threading
import time
from datetime import datetime


class Scaner:
    MAX_SECONDS_TIMEOUT_SOCKET = 2
    MAX_RANGE_PORT = 65535

    def scan_ip_range_and_port_range(self, begin_ip: str, end_ip: str, begin_port: int, end_port: int):
        last_node_in_begin_ip = int(self.get_last_node_in_ip(begin_ip))
        last_node_in_last_ip = int(self.get_last_node_in_ip(end_ip))
        if last_node_in_begin_ip > last_node_in_last_ip:
            buf_last_node_in_begin_ip = last_node_in_begin_ip
            last_node_in_begin_ip = last_node_in_last_ip
            last_node_in_last_ip = buf_last_node_in_begin_ip

        for last_node in range(last_node_in_begin_ip, last_node_in_last_ip):
            parsed_begin_ip = self.parse_ip(begin_ip)
            ip = '.'.join(parsed_begin_ip[:3]) + '.' + str(last_node)
            self.scan_ip_in_range_port(ip=ip, begin_port=begin_port, end_port=end_port)

    def scan_ip_in_range_port(self, ip: str, begin_port: int, end_port: int):
        if end_port > self.MAX_RANGE_PORT:
            end_port = self.MAX_RANGE_PORT

        if begin_port > end_port:
            buf_begin_port = begin_port
            begin_port = end_port
            end_port = buf_begin_port

        for port in range(begin_port, end_port):
            task = threading.Thread(target=self.scan_thread, args=(ip, port))
            status_code = task.start()

    def scan_thread(self, ip: str, port: int):
        status = self.scan_ip_port(ip, port)
        if status == 1:
            print(ip + ':' + str(port), ' its open.')

    def scan_ip_port(self, ip: str, port: int) -> int:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(self.MAX_SECONDS_TIMEOUT_SOCKET)
        try:
            connect = sock.connect((ip, port))
            sock.close()
            return 1
        except:
            pass

        return 0

    def get_last_node_in_ip(self, ip: str):
        return self.parse_ip(ip)[3]

    def parse_ip(self, ip: str) -> list:
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
    print('Скан завершился... времени прошло : {}'.format(ends - start))
    input()
