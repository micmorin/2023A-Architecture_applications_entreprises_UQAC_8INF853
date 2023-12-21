from util import checkAttributesAndGet, checkAttributesAndSave
import pandas as pd
import operator

class analyserMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class analyser(metaclass=analyserMeta):

    def hasError (self, data, valid) :
        if not valid:
            return ["NotValid"]
        else:
            checkAttributesAndGet(self,['pattern', 'policy'])
            
            errors = []
            errors.extend(self.checkPattern(data))
            errors.extend(self.checkPolicy(data))

            return errors

    def checkPattern(self, data):
        id_str = str(data['ID'])
        tag_str = str(data['TAG'])

        patterns = []
        if id_str in self.pattern.keys():
            patterns.append(self.pattern[id_str])
        if tag_str in self.pattern.keys():
            patterns.append(self.pattern[tag_str])

        pattern_errors = []

        patterns = pd.DataFrame(patterns).max().to_dict()

        for k,v in data['MESURES'].items():
            for kp,vp in patterns.items():
                if k == kp:
                    for p in vp:
                        if 'Type' in p: 
                            err = self.verifyType(v, p.split()[2])
                            if err is not None:
                                pattern_errors.append(err)
                        elif 'Interval' in p: 
                            err = self.verifyInterval(v,p.split()[2],p.split()[4])
                            if err is not None:
                                pattern_errors.append(err)
                        elif 'Frequency' in p:
                            err =  self.verifyFrequency(v,p.split()[2])
                            if err is not None:
                                pattern_errors.append(err)
                        else: pass

        return pattern_errors
    
    def verifyFrequency(self, value, frequency):
        pass

    def verifyInterval(self, value, min, max):
        pass

    def verifyType(self, value, type):
        if type == "Int":
            try: 
                int(value)
                return None
            except:
                return "WrongType"
        elif type == "Float":
            try: 
                if isinstance(value,str):
                    value.replace(',','.')
                float(value)
                return None
            except:
                return "WrongType" 
        elif type == "Bool":
            if value == "True" or value == "False":
                return None
            else:
                return "WrongType" 
        elif type == "String":
            if not isinstance(value,str):
                return "WrongType"  
            else:
                return None 
        else:
            return "ProblemCheckingType"

    def checkPolicy(self, data):
        policy_errors = []
        
        ops = {
            '<': operator.lt,
            '<=': operator.le,
            '==': operator.eq,
            '!=': operator.ne,
            '>=': operator.ge,
            '>': operator.gt
        }
        
        for rule_key, rule_value in self.policy.items():
            if rule_value['scope'] == 'ALL' or rule_value['scope'] == data['ID'] or rule_value['scope'] == data['TAG']:
                if rule_value['if']['subject'][0] != 'E':
                    if rule_value['if']['subject'][2:] in data['MESURES'].keys():
                        subject = data['MESURES'][rule_value['if']['subject'][2:]]
                        if rule_value['if']['object'][0] == 'L':
                            object = rule_value['if']['object'][2:]
                            if ops.get(rule_value['if']['comparison'])(subject, object):
                                policy_errors.append(rule_key)
                        elif rule_value['if']['object'][2:] in data['MESURES'].keys():
                            object = data['MESURES'][rule_value['if']['object'][2:]]
                            if ops.get(rule_value['if']['comparison'])(subject, object):
                                policy_errors.append(rule_key)
                            
        return policy_errors
        """
        {rule:{
            scope: [ALL, ID, Tag]
            if:{
                subject: [M_%Mesure, E_%Erreur]
                object:  [L_Literal, M_%Mesure]
                comparison: [<, >, <=, >=, ==, !=]
                }
            then:{
                subject: [Data, %Mesure, System]
                object: [_%Objet, Data, %Mesure, Literal, User]
                action: [Contact, Change to, Remove]
                notes: [Literal]
                }
            }
        }
        """
        

        


