#pylint: disable=E0401,E0611
"""Module for multithreading in Exchange"""

import socket
import threading as th
from datetime import datetime
from burse import Exchange, Commodity

COLORS = {
    'HEADER': '\033[95m',
    'OK_BLUE': '\033[94m',
    'OK_CYAN': '\033[96m',
    'OK_GREEN': '\033[92m',
    'WARNING': '\033[93m',
    'FAIL': '\033[91m',
    'NORMAL': '\033[0m',
    'BOLD': '\033[1m',
    'UNDERLINE': '\033[4m',
}

REQUESTS = {
    "BUY": (lambda x, com: x[com].buy_price, (str,), float),
    "SELL": (lambda x, com: x[com].sell_price, (str,), float),
    "UPDATE": (lambda x, com, buy, sell: x[com].update(buy, sell), (str, float, float), None),
    "LOG": (lambda x, com: x[com].add_log(datetime.now()), (str,), None),
    "HISTORY": (lambda x, com: x[com].history, (str,), dict),
    "COMMODITIES": (lambda x: x.commodity_names, (), list),
    "ALL_PRICES": (lambda x: x.current_prices, (), dict),
    "ADD_COMMODITY": (lambda x, com, buy, sell: x.add_commodity(Commodity(com, buy, sell)),
                      (str, float, float), None),
    "ADD_TRADE": (lambda x, com, amount: x.add_trade(com, amount < 0, amount), (str, int), float)
}

def _time_print(sender, mes, color, *args, **kwargs):
    """
    Converts current time to format HH:MM:SS
    :return: converted time
    """
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(f"[{current_time}]\t{COLORS[color]}{sender}: {mes}{COLORS['NORMAL']}", *args, **kwargs)

def _resolve_request(exchange: Exchange, request: str) -> str:
    request_array = request.split(" ")
    if request_array[0] in REQUESTS:
        if len(request_array)-1 != len(REQUESTS[request_array[0]][1]):
            _time_print("Server", "ERROR", 'FAIL')
            return "ERROR"
        params = [REQUESTS[request_array[0]][1][i](request_array[i + 1]) for i in
                  range(len(REQUESTS[request_array[0]][1]))]
        if REQUESTS[request_array[0]][2] is None:
            REQUESTS[request_array[0]][0](exchange, *params)
            _time_print("Server", "NONE", 'WARNING')
            return "NONE"
        rt =  repr(REQUESTS[request_array[0]][0](exchange, *params))
        _time_print("Server", rt, 'OK_CYAN')
        return rt
    _time_print("Server", "MISSING", 'FAIL')
    return "MISSING"


def _thread_function(client_socket: socket.socket, client_id: int, exchange: Exchange) -> None:
    try:
        _time_print("Server", f"Thread for client {client_id} created.",'OK_BLUE')
        buffer = ""
        end = False
        while True:
            data = client_socket.recv(1024)
            buffer += data.decode()
            while "@" in buffer:
                mes = buffer.split("@")[0]
                buffer = "@".join(buffer.split("@")[1:])
                if mes == "END":
                    end = True
                    break
                _time_print(f"Client {client_id}",  mes, 'OK_CYAN', end = " -> ")
                client_socket.sendall((_resolve_request(exchange, mes) + "@").encode())
            if end:
                _time_print(f"Client {client_id}", "Connection closed.", 'OK_BLUE')
                break
        client_socket.close()
    except ConnectionResetError:
        _time_print(f"Client {client_id}",  "Connection lost.", 'FAIL')

def server_loop(address: str, port: int, exchange: Exchange) -> None:
    """
    Function that creates burse server
    :param address: server address
    :param port: server port
    :param exchange: exchange to use accross the server
    """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((address, port))
    server_socket.listen()
    _time_print("Server",  f"Server bind on {address}:{port}", 'OK_GREEN')
    thread_id = 1
    threads = []
    try:
        while True:
            _time_print("Server", "Waiting", 'OK_BLUE')
            client_socket, client_address = server_socket.accept()
            _time_print("Server", f"Connected to {client_address[0]}:{client_address[1]}",
                        'OK_GREEN')
            thr = th.Thread(target=_thread_function, args=(client_socket, thread_id, exchange))
            threads.append(thr)
            thread_id += 1
            thr.start()
    except KeyboardInterrupt:
        # Wait for threads to be finished, prevent the server from accepting new clients
        _time_print("Server", "Closing, waiting for all clients to disconnect.", 'WARNING')
        try:
            for thr in threads:
                thr.join()
            server_socket.close()
            _time_print("Server", "Properly closed.", 'OK_GREEN')
        except KeyboardInterrupt:
            _time_print("Server","Not closed properly, ghost clients probably remained.", 'FAIL')
