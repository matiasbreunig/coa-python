from fastapi import FastAPI, Header
from pyrad.client import Client
from pyrad.dictionary import Dictionary
from pyrad import packet
import socket
import os

app = FastAPI()

nas_server = os.environ.get("NAS_SERVER")
nas_secret = os.environ.get("NAS_SECRET")
nas_port = os.environ.get("NAS_PORT")


# Fixed authentication token
authentication_token = "b8e8251c-319d-4f87-b9f0-d53e2f2d5093"

@app.post("/coa/")
def send_coa_request(
    data: dict,
    authorization: str = Header(...)
):
    # Check authorization token
    if authorization != authentication_token:
        return {"error": "Invalid authorization token"}

    if "attributes" not in data or not isinstance(data["attributes"], dict):
        return {"error": "Missing or invalid 'attributes' field"}

    if "nas_server" not in data or "nas_secret" not in data or "nas_port" not in data:
        return {"error": "Missing required parameters"}

    # Extract parameters from data
    attributes = data["attributes"]

    # Create RADIUS client
    client = Client(server=nas_server, secret=nas_secret.encode(), coaport=nas_port)
    client.dict = Dictionary("dictionary")
    client.timeout = 1
    client.retries = 1

    # Create CoA request
    request = client.CreateCoAPacket(code=packet.CoARequest, **attributes)

    try:
        reply = client.SendPacket(request)
    except client.Timeout:
        return {"error": "RADIUS server does not reply"}
    except socket.error as error:
        return {"error": f"Network error: {error[1]}"}

    response = {
        "result": "ACK" if reply.code == packet.CoAACK else "NAK",
        "attributes": {str(i): str(reply[i]) for i in reply.keys()}
    }
    return response
