from flask import Flask
from flask import request
import json
import socket
import math as math

app = Flask(__name__)


def quick_power(x, n):
    if n == 0:
        return 1

    if n == 1:
        return x
    if n % 2 == 0:
        return quick_power(x * x, n // 2)
    else:
        return quick_power(x * x, n // 2) * x


@app.route("/register", methods=["PUT"])
def register():
    try:
        content = json.loads(request.data)

        # create udp connect to AS
        udp_conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        body = "TYPE={}\nNAME={}\nVALUE={}\nTTL={}".format('A', content["hostname"], content["ip"], 10)
        udp_conn.sendto(body.encode(encoding="utf-8"), (content["as_ip"], int(content["as_port"])))

        while True:
            data, address = udp_conn.recvfrom(4096)
            res = data.decode(encoding="utf-8")

            if res == "ok":
                udp_conn.close()
                return "", 201
            elif res == "failed":
                udp_conn.close()
                return "", 500

    except BaseException as e:
        print(e)
        return "Registration failed", 400


# start from 0, a_1 = 0, a_2 = 1
@app.route("/fibonacci", methods=["GET"])
def fibonacci():
    try:
        number = int(request.args.get("number")) - 1
    except TypeError:
        return "Type error", 400

    result = (quick_power((1 + math.sqrt(5)) / 2, number) - quick_power((1 - math.sqrt(5)) / 2, number)) / math.sqrt(5)

    return str(round(result)), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9090)
