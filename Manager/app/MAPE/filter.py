from util import checkAttributesAndGet, checkAttributesAndSave
import re
from datetime import datetime

class filterMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class filter(metaclass=filterMeta):

    def isValid (self,data) :
        self= checkAttributesAndGet(self,['context', 'pattern', 'history'])
        valid = True
        valid = "ID" in data
        valid = "TAG" in data
        if hasattr(data,"MESURES"):
            for m in data.MESURES :
                if isinstance(m,dict):
                    for key,value in m.items():
                        if key == "" or value == "":
                            valid = False
                else:
                    valid = False
        if valid :
            self.extractContext(data)
            self.extractPattern(data)
            checkAttributesAndSave(self,['context', 'pattern', 'history'])

        return valid, self.finalize(data)


    def extractContext(self,data):
        id_str = str(data['ID'])
        tag_str = str(data['TAG'])
        id_array = id_str.split("_")
        tag_array = tag_str.split("_")

        if id_str in self.context.keys():
            id_context = self.context[id_str]
        else:
            id_context = {'Context':[]}

        if tag_str in self.context.keys():
            tag_context = self.context[tag_str]
        else:
            tag_context = {'Context':[]}

        for i in id_array:
            if i not in id_context['Context']:
                id_context['Context'].append(str(i))

        for i in tag_array:
            if i not in tag_context['Context']:
                tag_context['Context'].append(str(i))

        self.context[id_str] = id_context
        self.context[tag_str] = tag_context

    def extractPattern(self,data):
        id_str = str(data['ID'])
        tag_str = str(data['TAG'])

        measures = data['MESURES']

        if id_str in self.pattern.keys():
            id_pattern = self.pattern[id_str]
        else:
            id_pattern = {}

        if tag_str in self.pattern.keys():
            tag_pattern = self.pattern[tag_str]
        else:
            tag_pattern = {}

        for key, value in measures.items():
            self.history.loc[len(self.history.index)] = [id_str, tag_str, key, str(value), data['DATE']]
            if key not in id_pattern.keys():
                id_pattern[key] = []
            if key not in tag_pattern.keys():
                tag_pattern[key] = []

            df_ID = self.history.loc[((self.history['ID'] == id_str) & (self.history['Mesure'] == key))]
            df_TAG = self.history.loc[((self.history['Tag'] == id_str) & (self.history['Mesure'] == key))]

            df_ID_min = df_ID['valeur'].min()
            df_ID_max = df_ID['valeur'].max()
            df_TAG_min = df_TAG['valeur'].min()
            df_TAG_max = df_TAG['valeur'].max()

            df_ID_date_min = df_ID['TimeStamp'].min()
            df_ID_date_max = df_ID['TimeStamp'].max()

            df_TAG_date_min = df_TAG['TimeStamp'].min()
            df_TAG_date_max = df_TAG['TimeStamp'].max()

            df_ID_len = len(df_ID.index)
            df_TAG_len = len(df_TAG.index)


            # TYPE
            value = str(value)
            if re.search("[A-Za-z]+", value) == None :
                if re.search("[.,]+", value) != None: # Float          
                    statement = "Type is Float"
                else : # INT
                    statement = "Type is Int"

            elif value.lower() == "true" or value.lower() == "false": # Bool
                statement = "Type is Bool"

            else: # String
                statement = "Type is String"
                
            if len(id_pattern[key]) == 0:
                id_pattern[key].append(statement)
            else:
                for i in range(len(id_pattern[key])):
                    if "Type" in id_pattern[key][i]:
                        break
                    if i == len(id_pattern[key]) -1 :
                        id_pattern[key].append(statement)
            if len(tag_pattern[key]) == 0:
                tag_pattern[key].append(statement)
            else:
                for i in range(len(tag_pattern[key])):
                    if "Type" in tag_pattern[key][i]:
                        break
                    if i == len(tag_pattern[key]) -1 :
                        tag_pattern[key].append(statement)    

            # Interval
            if str(df_ID_min) != 'nan' and str(df_ID_max) != 'nan':
                statement = "Interval between " + str(df_ID_min) + " and " + str(df_ID_max)
                for i in range(len(id_pattern[key])):
                    if "Interval" in id_pattern[key][i]:
                        id_pattern[key].pop(i)
                        break
                id_pattern[key].append(statement)
                
            if str(df_TAG_min) != 'nan' and str(df_TAG_max) != 'nan':
                statement = "Interval between " + str(df_TAG_min) + " and " + str(df_TAG_max)
                for i in range(len(tag_pattern[key])):
                    if "Interval" in tag_pattern[key][i]:
                        tag_pattern['Pattern'].pop(i)
                        break
                tag_pattern[key].append(statement)

            # FREQUENCY
            if df_ID_len == 0:
                frequency_ID = '0:00:00'
            else:
                frequency_ID = (datetime.fromisoformat(df_ID_date_max) - datetime.fromisoformat(df_ID_date_min)) / df_ID_len
            statement = "Frequency is " + str(frequency_ID)
            for i in range(len(id_pattern[key])):
                    if "Frequency" in id_pattern[key][i]:
                        id_pattern[key].pop(i)
                        break
            id_pattern[key].append(statement)
                
            if df_TAG_len == 0:
                frequency_TAG = '0:00:00'
            else:
                frequency_TAG = (datetime.fromisoformat(df_TAG_date_max) - datetime.fromisoformat(df_TAG_date_min)) / df_TAG_len
            statement = "Frequency is " + str(frequency_TAG)
            for i in range(len(tag_pattern[key])):
                    if "Frequency" in tag_pattern[key][i]:
                        tag_pattern[key].pop(i)
                        break
            tag_pattern[key].append(statement)

        self.pattern[id_str] = id_pattern
        self.pattern[tag_str] = tag_pattern

    def finalize(self, data):
        data.pop('SOURCE')
        data.pop('DESTINATION')
        dest = data.pop('THREADID')
        data["Object_name"] = dest
        data["DB"] = "Influx"
        return data