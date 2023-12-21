import os
from typing import Annotated
from fastapi import APIRouter, Body, Request
from glob import glob, escape
from importlib import import_module
from pydantic import BaseModel
import protocol_identifier
from yaml import safe_load, dump
import requests as rq
from sys import stderr
from fastapi.responses import JSONResponse

main = APIRouter(
    responses={404: {"description": "Not found"}},
)

class MSG(BaseModel):
    text: str
    ID: str

def protocol_verification(txt):
    for m in glob("*.py", root_dir=escape('./protocoles')):
        class_ = getattr(protocol_identifier, m[:-3]+"_Identifier")
        if class_().verify(txt):
            return m[:-3]
        
def reFormat(j):
    data = {}
    data['TAG'] = j.pop('TAG')
    data['ID'] = j.pop('ID')
    data['DATE'] = j.pop('DATE')
    data['THREADID'] = j.pop('THREADID')
    data['SOURCE'] = j.pop('SOURCE')
    data['DESTINATION'] = j.pop('DESTINATION')
    data['MESURES'] = j
    return data

@main.get("/")
def read_root():
    return {"Hello": "World"}

@main.post("/connect")
def post_connect(msg: MSG):
    if os.path.isfile("./knowledge/mapping.yml") and os.path.getsize("./knowledge/mapping.yml") > 0:
        if msg.ID not in dict(safe_load(open("./knowledge/mapping.yml","r"))).keys():
            protocol = protocol_verification(msg.text)
        else:
            protocol = dict(safe_load(open("./knowledge/mapping.yml","r")))[msg.ID]['Module']
    else:
        protocol = protocol_verification(msg.text)

    module = import_module('protocoles.'+protocol)
    class_ = getattr(module, protocol.split(sep='_',maxsplit=1)[0])
    dump({msg.ID:{"Module":protocol}},open("./knowledge/mapping.yml","a"))
    return {"text":str(class_().get_new_Connection_Request(msg.text))}

@main.post("/connected")
def post_connect(msg: MSG):
    if os.path.isfile("./knowledge/mapping.yml") and os.path.getsize("./knowledge/mapping.yml") > 0:
        if msg.ID not in dict(safe_load(open("./knowledge/mapping.yml","r"))).keys():
            return {"text":"Not Connected"}
        else:
            return {"text":"ACK"}
    else:
        return {"text":"Not Connected"}
    
@main.post("/data")
async def post_data(request: Request):
    j = await request.json()
    j = {k.upper():v for k,v in j.items()}
    response = rq.post('http://manager:5000/', json=reFormat(j))
    if response.status_code == 200:
        return JSONResponse(status_code=response.status_code, content=response.json())
    else:
        return JSONResponse(status_code=response.status_code, content={})