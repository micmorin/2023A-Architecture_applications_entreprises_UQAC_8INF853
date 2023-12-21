import os
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

class executorMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class executor(metaclass=executorMeta):
    def execute(self, data, plan):
        for action in plan:
            components = action.split()
            if components[0] == 'Data':
                if components[1] == 'Change to':
                    data = components[2]
            elif components[0] == 'System':
                if components[1] == 'Contact':
                    if components[2] == 'User':
                        pass
                    elif components[1][0] == '_':
                        pass
                elif components[1] == 'Remove':
                    if components[2] == 'Data':
                        data = None
                    elif components[1][0] == '_':
                        pass
                    else:
                        data[components[0]] = None
            else:
                if components[1] == 'Change to':
                    data[components[0]] = components[2]

        if data != None:
            write_api = self.getClient().write_api(write_options=SYNCHRONOUS)
            dict_structure = {
                "measurement": data['Object_name'],
                "tags": {"ID":data['ID'],"Tag": data['TAG']},
                "fields": {}
            }

            for k,v in data['MESURES'].items():
                dict_structure['fields'][k] = v

            write_api.write(bucket=self.getBucket(), org=self.getOrg(), 
                            record=Point.from_dict(dict_structure))

        return {"msg":"Completed"}
    
    def getClient(self):
        token = os.environ.get("INFLUXDB_TOKEN")
        org = "my-org"
        url = "http://db:8086"
        return InfluxDBClient(url=url, token=token, org=org)

    def getOrg(self):
        return "my-org"

    def getBucket(self):
        return "my-bucket"
