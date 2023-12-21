from sys import stderr
from flask import  request
from MAPE.filter import filter
from MAPE.analyser import analyser
from MAPE.plannificator import planificator
from MAPE.executor import executor
from util import getAttributes, saveAttribute


def index():
    data = request.json
    data = dict(data)

    obj = filter()
    valid, data = obj.isValid(data)

    obj = analyser()
    errors = obj.hasError(data, valid)

    obj = planificator()
    plan = obj.get_plan(data, errors)

    obj = executor()
    return obj.execute(data,plan)


def add_policy():
    obj = getAttributes(['policy'])
    key = list(request.json.keys())[0]
    obj[key] = request.json[key]
    saveAttribute('policy',obj)
    return {"msg":"Completed"}


def update_policy():
    obj = getAttributes(['policy'])
    key = list(request.json.keys())[0]
    obj[key] = request.json[key]
    saveAttribute('policy',obj)
    return {"msg":"Completed"}


def delete_policy():
    obj = getAttributes(['policy'])
    key = request.json.get('name')
    obj.pop(key)
    saveAttribute('policy', obj)
    return {"msg":"Completed"}


def get_policies():
    return getAttributes(['policy'])