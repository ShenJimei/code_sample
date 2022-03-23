import socket

import requests
from flask import Flask
from flask import request

app = Flask(__name__)


def parse_str(s):
    s = s.split('\n')

    result = {}
    for item in s:
        tmp = item.split('=')
        result[tmp[0]] = tmp[1]
    return result


@app.route("/fibonacci", methods=["GET"])
def work():
    try:
        hostname = request.args["hostname"]
        fs_port = int(request.args["fs_port"])
        number = int(request.args["number"])
        as_ip = request.args["as_ip"]
        as_port = int(request.args["as_port"])

        udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_sock.sendto(F"TYPE=A\nNAME={hostname}".encode("utf-8"), (as_ip, as_port))
        while True:
            as_data, address = udp_sock.recvfrom(4096)
            
            if as_data is not None:
                udp_sock.close()
                break
        if as_data == b"None":
            return 'bad request!', 400
        else:
            print(as_data)
            res = parse_str(as_data.decode(encoding="utf-8"))
            print(res)
        fibonacci_data = requests.get(F"http://{res['VALUE']}:{fs_port}/fibonacci?number={number}")
        if fibonacci_data.status_code != 200:
            return fibonacci_data.text, 400
        else:
            return fibonacci_data.text, 200
    except Exception as E:
        return str(E), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)