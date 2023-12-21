from crc import Calculator, Configuration
from random import randbytes
from multipledispatch import dispatch

class BLE:
    def get_new_Advertisement(self):
        return self.Advertisement_Paquet()
    
    def get_new_Connection_Request(self, adv):
        adv_obj = self.Advertisement_Paquet(adv)
        req_obj = self.Connection_Request_Paquet(adv_obj)
        self.sourceAddr = req_obj.InitA
        self.targetAddr = req_obj.AdvA
        return req_obj
    
    def get_new_Connection_Response(self, req):
        req_obj = self.Connection_Request_Paquet(req)
        res_obj = self.Connection_Response_Paquet(req_obj)
        self.sourceAddr = res_obj.AdvA
        self.targetAddr = res_obj.TargetA
        return res_obj
    
    def get_data_package(self, data):
        result = data
        result["source"] = self.sourceAddr.hex()
        result["destination"] = self.targetAddr.hex()
        return result
    
    class Base_paquet:
        @dispatch()
        def __init__(self):
            self.access_address = randbytes(1)
            self.preamble = self.get_preamble()
            self.pdu = randbytes(2)
            self.crc = self.get_CRC()

        def __repr__(self):
            return "".join([self.preamble.hex(), self.access_address.hex(), self.pdu.hex(),hex(self.crc)[2:]])
        
        def get_preamble(self):
            if int(self.access_address.hex(),16)&8 != 0:
                return bytes.fromhex('55')
            else:
                return bytes.fromhex('AA')

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
            self.access_address = bytes.fromhex('8E 89 BE D6') # 4 byte (AA changes for each connection)
            self.preamble = self.get_preamble()

            # PDU Preparation
            header_ = bytes.fromhex('01') # PDU_type = 0000, RFU = 0, ChSel= 0, TxAdd=0, RxAdd=1 # 1 byte
            payload = randbytes(6) # 6 byte source addr
            header_len = bytes.fromhex('06') # 1 byte

            self.pdu = header_ + header_len + payload  # 2-258 byte
            self.crc = self.get_CRC()# 3 byte
        
        @dispatch(str)
        def __init__(self, str_:str):
            super().__init__()
            self.preamble = str_[0:2] 
            self.access_address = str_[2:10]

            self.header_ = str_[10:12] 
            self.payload = str_[14:26] 
            self.header_len = str_[12:14] 

            self.pdu = str_[10:26]
            self.crc = str_[26:32]
        
    class Connection_Request_Paquet(Base_paquet):
        @dispatch(object)
        def __init__(self, adv_obj):
            super().__init__()
            self.access_address = bytes.fromhex(adv_obj.access_address) # 4 byte
            self.preamble = self.get_preamble()

            # PDU Preparation
            header_ = bytes.fromhex('53') # PDU_type = 0101, RFU = 0, ChSel= 0, TxAdd=1, RxAdd=1 # 1 byte
                #Payload Preparation
            self.InitA = bytes.fromhex('11 22 33 44 55 66') # 6 byte
            self.AdvA = bytes.fromhex(adv_obj.payload) # 6 byte
            
                    # LLDATA Preparation
            aa = randbytes(4) # 4 byte
            CRCInit = randbytes(3)  # 3 byte
            WinSize = bytes.fromhex('05') # 1 byte 1.25-10 /1.25
            WinOffset = bytes.fromhex('00 0A')  # 2 byte 0-interval /1.25
            Interval = bytes.fromhex('00 14') # 2 byte 7.5-40 / 1.25
            Latency = bytes.fromhex('00 07') # 2 byte 0 - (Timeout / (Interval*2)) - 1
            Timeout = bytes.fromhex('01 90')  # 2 byte 100 - 3200 /10
            ChM = randbytes(5) # 5 byte
            Hop = randbytes(5)  # 5 byte random 5-16
            sca = randbytes(3)  # 3 byte random 0-7
            LLData = aa+CRCInit+WinSize+WinOffset+Interval+Latency+Timeout+ChM+Hop+sca # 22 byte

            payload = self.InitA + self.AdvA + LLData  # [12:24] 34 byte
            header_len = bytes.fromhex('22') #  1 byte

            self.pdu = header_ + header_len + payload  # [10:26] 8 byte
            self.crc = self.get_CRC() # 3 byte

        @dispatch(str)
        def __init__(self, str_:str):
            super().__init__()
            self.preamble = str_[0:2] 
            self.access_address = str_[2:10]

            self.header_ = str_[10:12] 
            self.InitA = str_[14:26]
            self.AdvA = str_[26:38]
            
                    # LLDATA Preparation
            self.aa = str_[38:46]
            self.CRCInit = str_[46:53]
            self.WinSize = str_[52:54] 
            self.WinOffset = str_[54:58] 
            self.Interval = str_[58:62] 
            self.Latency = str_[62:66] 
            self.Timeout = str_[66:70]  
            self.ChM = str_[70:80] 
            self.Hop = str_[80:90] 
            self.sca = str_[90:96] 
            self.LLData = str_[38:96] 

            self.payload = str_[14:96]  
            self.header_len = str_[12:14]

            self.pdu = str_[10:96]
            self.crc = str_[96:102]


    class Connection_Response_Paquet(Base_paquet):
        @dispatch(object)
        def __init__(self, req_obj):
            super().__init__()
            self.access_address = bytes.fromhex(req_obj.aa)
            self.preamble = self.get_preamble()

            # PDU Preparation
            header_ = bytes.fromhex('83') # PDU_type = 1000, RFU = 0, ChSel= 0, TxAdd=1, RxAdd=1 # 1 byte
            
                #Payload Preparation
            EHLength_AdvMode = bytes.fromhex('30') # 1 byte 0011 00 + 00
            
                    # Extended Header
            flags= bytes.fromhex('C0') # 1 byte 1100 0000
            self.AdvA = bytes.fromhex(req_obj.InitA) # 6 byte
            self.TargetA = bytes.fromhex(req_obj.AdvA) # 6 byte

            Extended_Header  = flags+self.AdvA+self.TargetA # 13 byte
                   
            payload = EHLength_AdvMode + Extended_Header # 14 byte
            header_len = bytes.fromhex('0E') # 1 byte

            self.pdu = header_ + header_len + payload
            self.get_CRC()

        @dispatch(str)
        def __init__(self, str_:str):
            super().__init__()
            self.preamble = str_[0:2] 
            self.access_address = str_[2:10]

            self.header_ = str_[10:12] 
            self.EHLength_AdvMode = str_[14:16] 
            
                    # Extended Header
            self.flags= str_[16:18] # 1 byte 1100 0000
            self.AdvA = str_[18:30] # 6 byte
            self.TargetA = str_[30:42] # 6 byte

            self.Extended_Header  = str_[16:42] # 13 byte

            self.payload = str_[14:42] 
            self.header_len = str_[12:14]

            self.pdu = str_[10:42]
            self.crc = str_[42:48]