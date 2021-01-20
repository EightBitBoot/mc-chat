import sys
import os

import getpass
import uuid
from uuid import UUID
import json
import requests

CLIENT_ID_FILENAME = "clientId.txt"

AUTHENTICATION_URL = "https://authserver.mojang.com/authenticate"

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