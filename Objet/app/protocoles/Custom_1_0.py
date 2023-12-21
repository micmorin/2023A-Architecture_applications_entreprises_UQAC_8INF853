from crc import Calculator, Configuration
from random import randbytes
from multipledispatch import dispatch

class Custom:
    def get_new_Advertisement(self):
        return self.Advertisement_Paquet()
    
    def get_new_Connection_Request(self, adv):
        adv_obj = self.Advertisement_Paquet(adv)
        req_obj = self.Connection_Request_Paquet(adv_obj)
        self.sourceAddr = req_obj.src_addr
        self.targetAddr = req_obj.dst_addr
        return req_obj
    
    def get_new_Connection_Response(self, req):
        req_obj = self.Connection_Request_Paquet(req)
        res_obj = self.Connection_Response_Paquet(req_obj)
        self.sourceAddr = res_obj.src_addr
        self.targetAddr = res_obj.dst_addr
        return res_obj
    
    def get_data_package(self, data):
        result = data
        result["source"] = self.sourceAddr.hex()
        result["destination"] = self.targetAddr.hex()
        return result
    
    class Base_paquet:
        @dispatch()
        def __init__(self):
            self.header = randbytes(1)
            self.sync = bytes.fromhex('C3') # 1100 0011
            self.pdu = randbytes(12)
            self.crc = self.get_CRC()

        def __repr__(self):
            return "".join([self.header.hex(), self.pdu.hex(),hex(self.crc)[2:]])

        def get_CRC(self, init_value=0x555555):
            return (Calculator(Configuration(
                width=24,
                polynomial=0x00065b, 
                init_value=init_value, 
                reverse_input=True, 
                reverse_output=True, 
                final_xor_value=0x000000
            )).checksum(self.pdu))

    class Advertisement_Paquet(Base_paquet):
        @dispatch()
        def __init__(self):
            super().__init__()
            self.header = bytes.fromhex('60') # SRC + DST = 0110 0000

            # PDU Preparation
            self.src_addr = bytes.fromhex('08 13 14 A7 4B 5B') # 8 19 20 167 75 91
            self.dst_addr = bytes.fromhex('01 02 03 04 05 06') 
            payload = self.src_addr+self.dst_addr 

            self.pdu = self.sync + payload + self.sync 
            self.crc = self.get_CRC() # 3 byte
        
        @dispatch(str)
        def __init__(self, str_:str):
            super().__init__()
            self.header = str_[0:2]

            # PDU Preparation
            self.src_addr = str_[4:16]
            self.dst_addr = str_[16:28]
            self.payload = str_[4:28]

            self.pdu = str_[2:30] 
            self.crc = str_[30:36]
        
    class Connection_Request_Paquet(Base_paquet):
        @dispatch(object)
        def __init__(self, adv_obj):
            super().__init__()
            self.header = bytes.fromhex('66') # SRC + DST = 0110 0110

            # PDU Preparation
            self.src_addr = bytes.fromhex('20 47 DE BE 4F B5') # 32 71 222 190 79 181
            self.dst_addr = bytes.fromhex(adv_obj.src_addr)
            request = bytes("Connection", "ASCII")
            payload = self.src_addr+self.dst_addr+request 

            self.pdu = self.sync + payload + self.sync 
            self.crc = self.get_CRC() # 3 byte

        @dispatch(str)
        def __init__(self, str_:str):
            super().__init__()
            self.header = str_[0:2]

            # PDU Preparation
            self.src_addr = str_[4:16]
            self.dst_addr = str_[16:28]
            self.request = str_[28:48]
            self.payload = str_[4:48]

            self.pdu = str_[2:50] 
            self.crc = str_[50:56]


    class Connection_Response_Paquet(Base_paquet):
        @dispatch(object)
        def __init__(self, req_obj):
            super().__init__()
            self.header = bytes.fromhex('66') # SRC + DST = 0110 0110

            # PDU Preparation
            self.src_addr = bytes.fromhex(req_obj.dst_addr)
            self.dst_addr = bytes.fromhex(req_obj.src_addr)
            request = bytes("Connected", "ASCII")
            payload = self.src_addr+self.dst_addr+request 

            self.pdu = self.sync + payload + self.sync 
            self.crc = self.get_CRC() # 3 byte

        @dispatch(str)
        def __init__(self, str_:str):
            super().__init__()
            self.header = str_[0:2]

            # PDU Preparation
            self.src_addr = str_[4:16]
            self.dst_addr = str_[16:28]
            self.request = str_[28:46]
            self.payload = str_[4:46]

            self.pdu = str_[2:48] 
            self.crc = str_[48:54]