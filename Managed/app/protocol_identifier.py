from abc import ABC, abstractmethod

class identifier(ABC):
    @abstractmethod
    def verify(self, data):
        pass

class BLE_5_2_Identifier(identifier):
    def verify(self, data):
        if data[10:12] != '01':
            print(data[10:12])
            return False
        if data[12:14] != '06':
            print(data[10:12])
            return False
        if data[2:10]!= '8E89BED6'.lower():
            return False
        return True
    
class Custom_1_0_Identifier(identifier):
    def verify(self, data):
        if data[0:2] != '60':
            print(data[0:2])
            return False
        if data[2:4] != 'C3'.lower() or data[28:30] != 'C3'.lower():
            print(data[2:4] + " " + data[28:30])
            return False
        if data[4:16] != '081314A74B5B'.lower():
            print(data[-2:])
            return False
        if data[16:28]!= '010203040506':
            return False
        return True