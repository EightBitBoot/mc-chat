import sys
import os
import copy

import getpass
import uuid
from uuid import UUID
import json
import requests

CLIENT_ID_FILENAME = "clientId.txt"

AUTHENTICATION_URL = "https://authserver.mojang.com/authenticate"

def lshift(value, n):
    return (value & 0xFFFFFFFF) << n

def rshift(value, n):
    return (value & 0xFFFFFFFF) >> n

def encodeVarint(value):
    val = copy.deepcopy(value)
    buffer = bytearray()

    # JUST ADD A DO WHILE LOOP PYTHON COME ON
    while True:
        temp = val & 0b01111111
        val = rshift(val, 7)

        if val != 0:
            temp |= 0b10000000

        buffer.append(temp)
        
        if val == 0:
            break

    return bytes(buffer)


def decodeVarint(varint):
    # TODO(Adin): Finish me
    pass


def getClientId():
    result = None

    if os.path.exists(CLIENT_ID_FILENAME):
        with open(CLIENT_ID_FILENAME, "r") as idFile:
            idStr = idFile.read()
            result = UUID(idStr)
    else:
        result = uuid.uuid4()

    return result


def buildRequestPayload(uname, passwd, clientId):
    payloadDict = {"agent": {"name": "Minecraft", "version": 1}, "username": uname, "password": passwd, "clientToken": str(clientId), "requestUser": True}

    return json.dumps(payloadDict)


def main(argv):
    print("Make sure no one is looking over your shoulder: this prints sensitive information to the console\n")
    
    uname = input("username> ")
    passwd = getpass.getpass("password> ")
    clientId = getClientId()

    if not os.path.exists(CLIENT_ID_FILENAME):
        with open(CLIENT_ID_FILENAME, "w+") as idFile:
            idFile.write(str(clientId))

    requestPayload = buildRequestPayload(uname, passwd, clientId)
    print(requestPayload)

    response = requests.post(AUTHENTICATION_URL, headers={"Content-Type": "application/json"}, data=requestPayload)
    print(response.text)


if __name__ == "__main__":
    main(sys.argv)
