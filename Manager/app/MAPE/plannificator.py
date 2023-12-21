from util import checkAttributesAndGet
import operator

class planificatorMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class planificator(metaclass=planificatorMeta):

    def get_plan(self,data,errors):
        checkAttributesAndGet(self,['pattern', 'policy'])

        plan = []
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
                if rule_value['if']['subject'][0] == 'E':
                    if rule_value['if']['subject'][2:] in errors:
                        subject = rule_value['if']['subject'][2:]
                        if rule_value['if']['object'][0] == 'L':
                            object = rule_value['if']['object'][2:]
                            if ops.get(rule_value['if']['comparison'])(subject, object):
                                statement =  rule_value['then']['subject'] + " "
                                statement = statement + rule_value['then']['action'] + " "
                                if rule_value['then']['object'][0] == '_':
                                    if rule_value['then']['object'][1:] == data['Object_name']:
                                        statement = statement + rule_value['then']['object'][1:]
                                    else: break
                                else:
                                    statement = statement + rule_value['then']['object']
                                plan.append(statement)
                                errors.remove(rule_value['if']['subject'][2:])
                        elif rule_value['if']['object'][2:] in data['MESURES'].keys():
                            object = data['MESURES'][rule_value['if']['object'][2:]]
                            if ops.get(rule_value['if']['comparison'])(subject, object):
                                statement =  rule_value['then']['subject'] + " "
                                statement = statement + rule_value['then']['action'] + " "
                                if rule_value['then']['object'][0] == '_':
                                    if rule_value['then']['object'][1:] == data['Object_name']:
                                        statement = statement + rule_value['then']['object'][1:]
                                    else: break
                                else:
                                    statement = statement + rule_value['then']['object']
                                plan.append(statement)
                                errors.remove(rule_value['if']['subject'][2:])
                        
        for err in errors:
            plan.append("System Contact User " + str(err))
            
        return plan