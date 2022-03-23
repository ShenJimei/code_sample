import socket
import os
import pickle


def save_record(data):
    content = {}

    if os.path.exists("records"):
        with open("records", "rb") as f:
            content = pickle.load(f)

    with open("records", "wb") as f:
        content[hash(data["TYPE"] + "+" + data["NAME"])] = data
        pickle.dump(content, f)


def query_record(data):
    content = {}
    if os.path.exists("records"):
        with open("records", "rb") as f:
            content = pickle.load(f)

    key = hash(data["TYPE"] + "+" + data["NAME"])
    if key in content:
        return content[key]
    else:
        return None


def parse_str(s):
    s = s.split('\n')

    result = {}
    for item in s:
        tmp = item.split('=')
        result[tmp[0]] = tmp[1]
    return result


port = 53533
address = "0.0.0.0"
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind((address, port))

while True:
    data, address = server.recvfrom(4096)
    res = parse_str(data.decode(encoding="utf-8"))

    if "VALUE" in res and "TTL" in res:
        try:
            save_record(res)
            server.sendto(b"ok", address)
        except BaseException as e:
            print(e)
            server.sendto(b"failed", address)

    else:
        r = query_record(res)
        if r is not None:
            server.sendto(
                "TYPE={}\nNAME={}\nVALUE={}\nTTL={}".format(r["TYPE"], r["NAME"], r["VALUE"], r["TTL"]).encode("utf-8"),
                address)
        else:
            server.sendto(b"None", address)
