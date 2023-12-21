from yaml import dump, safe_load
import pandas as pd
from os.path import isfile, getsize

def checkAttributesAndGet(self:object, attList:list):
        if isinstance(attList, list):
               for att in attList:
                    try:
                        att_s = str(att)
                        if not hasattr(self, att_s):
                            
                            if att_s == 'history':
                                file_path = "./knowledge/" + att_s + ".csv"
                                if isfile(file_path) and getsize(file_path) > 0:
                                    setattr(self, att_s, pd.read_csv(file_path, index_col=0))
                                else:
                                    setattr(self, att_s, pd.DataFrame( {'ID': pd.Series([],dtype='str'),
                                                                        'Tag': pd.Series([],dtype='str'),
                                                                        'Mesure': pd.Series([],dtype='str'),
                                                                        'valeur': pd.Series([],dtype='str'),
                                                                        'TimeStamp': pd.Series([])}))
                            else:
                                file_path = "./knowledge/" + att_s + ".yml"
                                if isfile(file_path) and getsize(file_path) > 0:
                                    setattr(self, att_s, safe_load(open(file_path, 'r')))
                                else:
                                    setattr(self, att_s, {})
                    except:
                        pass
        return self

def checkAttributesAndSave(self:object, attList:list):
        if isinstance(attList, list):
               for att in attList:
                    try:
                        att_s = str(att)
                        if hasattr(self, att_s):
                            if att_s == 'history':
                                file_path = "./knowledge/" + att_s + ".csv"
                                if isfile(file_path):
                                    getattr(self, att_s).to_csv(file_path)
                            else:
                                file_path = "./knowledge/" + att_s + ".yml"
                                if isfile(file_path):
                                    dump(getattr(self, att_s),open(file_path, 'w'))
                    except:
                        pass

def getAttributes(attList:list):
        if isinstance(attList, list):
               for att in attList:
                    try:
                        att_s = str(att)
                        if att_s == 'history':
                            file_path = "./knowledge/" + att_s + ".csv"
                            if isfile(file_path) and getsize(file_path) > 0:
                                obj = pd.read_csv(file_path, index_col=0)
                            else:
                                obj = pd.DataFrame( {'ID': pd.Series([],dtype='str'),
                                                                    'Tag': pd.Series([],dtype='str'),
                                                                    'Mesure': pd.Series([],dtype='str'),
                                                                    'valeur': pd.Series([],dtype='str'),
                                                                    'TimeStamp': pd.Series([])})
                        else:
                            file_path = "./knowledge/" + att_s + ".yml"
                            if isfile(file_path) and getsize(file_path) > 0:
                                obj = safe_load(open(file_path, 'r'))
                            else:
                                obj = {}
                    except:
                        pass
        return obj

def saveAttribute(att_s:str, obj:object):
        if isinstance(att_s, str):
            try:
                if att_s == 'history':
                    file_path = "./knowledge/" + att_s + ".csv"
                    if isfile(file_path):
                        obj.to_csv(file_path)
                else:
                    file_path = "./knowledge/" + att_s + ".yml"
                    if isfile(file_path):
                        dump(obj,open(file_path, 'w'))
            except:
                pass