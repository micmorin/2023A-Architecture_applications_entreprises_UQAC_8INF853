from collections.abc import Callable, Iterable, Mapping
from threading import Thread
from random import randint
from glob import glob, escape
import pandas as pd
from sys import stderr
from importlib import import_module
from time import sleep
import requests


def getDataset():
    data = glob("*.csv", root_dir=escape('./dataset'))
    setid = randint(0, len(data)-1)
    return pd.read_csv('./dataset/'+data[setid],index_col=0)

def getProtocole():
    data = glob("*.py", root_dir=escape('./protocoles'))
    setid = randint(0, len(data)-1)
    
    module = import_module('protocoles.'+data[setid][:-3])
    class_ = getattr(module, data[setid].split(sep='_',maxsplit=1)[0])
    return class_()

class Object(Thread):

    def __init__(self, group= None, target= None, name =  None, args = ..., kwargs = None, *, daemon = None):
        super().__init__(group, target, name, args, kwargs, daemon=daemon)
        self.data = getDataset()
        self.protocole = getProtocole()

    def run(self):
        sleep(randint(10,60))
        response = requests.post('http://managed:5000/connect', json={
            "text":str(self.protocole.get_new_Advertisement()),
            "ID": str(self.name)})
        
        if response.status_code == 200:
            response = requests.post('http://managed:5000/connected', json={
                "text":str(self.protocole.get_new_Connection_Response(response.json()["text"])),
                "ID": str(self.name)})
        
        if response.json()["text"] == 'ACK':
            timeout = randint(10,60)
            for data in getDataset().iterrows(): 
                j = data[1].to_dict()
                j['ThreadID'] = self.name
                self.protocole.get_data_package(j)
                response = requests.post('http://managed:5000/data', json=j)
                sleep(timeout)

        return super().run()

