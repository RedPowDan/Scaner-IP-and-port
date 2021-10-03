import socket  # Импортирование библитотеки для дальнейшего использования
import sys  # Системная бибилиотека, она нам понадобится, чтобы считывать аргументы из консоли
import threading  # Это бибилиотека нужно чтобы сделать прослушивание сокета быстрее (для создания потоков)
from datetime import datetime  # библиотека времемени для того чтобы отсчитывать выполнение программы


class Scaner:  # Класс где реализованны функции для прослушивания портов
    MAX_SECONDS_TIMEOUT_SOCKET = 2  # Максимальное кол-во секунд для прослушивания порта
    # то есть я жду пока мне придет ответ от порта в течениии 2 секунд
    MAX_RANGE_PORT = 65535  # Ну тут понятно демаю, просто максимальное значение для порта

    def scan_ip_range_and_port_range(self, begin_ip: str, end_ip: str, begin_port: int, end_port: int):
        """Сканирует айпишники в рендже, и порты"""
        last_node_in_begin_ip = int(self.get_last_node_in_ip(begin_ip))  # перевод поможет
        last_node_in_last_ip = int(self.get_last_node_in_ip(end_ip))
        if last_node_in_begin_ip > last_node_in_last_ip:  # Проверка на то чтобы начальное значение было меньше чем конечное
            buf_last_node_in_begin_ip = last_node_in_begin_ip  # Помещаем начальный айпи в буфер, чтобы потом поменять их с конечным
            last_node_in_begin_ip = last_node_in_last_ip  # Меняем
            last_node_in_last_ip = buf_last_node_in_begin_ip  # И присваеваем начальный к конечному

        for last_node in range(last_node_in_begin_ip, last_node_in_last_ip):
            parsed_begin_ip = self.parse_ip(begin_ip)
            ip = '.'.join(parsed_begin_ip[:3]) + '.' + str(last_node)
            self.scan_ip_in_range_port(ip=ip, begin_port=begin_port, end_port=end_port)

    def scan_ip_in_range_port(self, ip: str, begin_port: int, end_port: int):
        if end_port > self.MAX_RANGE_PORT:
            end_port = self.MAX_RANGE_PORT

        if begin_port > end_port:  # тут тоже самое что и в верху
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
        scaner.scan_ip_range_and_port_range(begin_ip=sys.argv[1], end_ip=sys.argv[2], begin_port=int(sys.argv[3]),
                                            end_port=int(sys.argv[4]))
    elif len(sys.argv) - 1 == 3:
        scaner.scan_ip_in_range_port(ip=sys.argv[1], begin_port=int(sys.argv[2]), end_port=int(sys.argv[3]))
    else:
        scaner.scan_ip_in_range_port(ip='127.0.0.1', begin_port=1, end_port=10000)
    ends = datetime.now()
    print('Скан завершился... времени прошло : {}'.format(ends - start))
    input()
