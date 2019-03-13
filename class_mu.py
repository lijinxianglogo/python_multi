#_*_ coding:utf-8 _*_
import struct
class BS_Father(object):
    def __init__(self, data=None):
        if type(data) is dict and "bs_x" in data:
            self.bs_x = data["bs_x"]
            self.bs_y = data["bs_y"]
            self.bs_z = data["bs_z"]
            self.bs_buid = data["bs_buid"]
            self.bs_floor = data["bs_floor"]
            self.bs_sence = data["bs_sence"]
        else:
            self.bs_x = 0
            self.bs_y = 0
            self.bs_z = 0
            self.bs_buid = 0
            self.bs_floor = 0
            self.bs_sence = 0
    def bin_fdata(self):
        msg = struct.pack("<6B", self.bs_x, self.bs_y, self.bs_z, self.bs_buid, self.bs_floor, self.bs_sence)
        return msg

    def update_sql(self):
        pass

class BS_UWB(BS_Father):
    def __init__(self, data=None):
        super(BS_UWB, self).__init__(data)
        if type(data) is dict and "uwb_chan" in data:
            self.uwb_chan = data["uwb_chan"]
            self.PRF = data["PRF"]
            self.data_rate = data["data_rate"]
            self.NTM = data["NTM"]
        else:
            self.uwb_chan = 0
            self.PRF = 0
            self.data_rate = 0
            self.NTM = 0
    def bin_uwb(self):
        msg = super(BS_UWB, self).bin_fdata()
        msg += struct.pack("<4B", self.uwb_chan, self.PRF, self.data_rate, self.NTM)
        return msg



bs_1105 = BS_UWB({"bs_x": 23, "bs_y": 3, "bs_z": 12, "bs_buid": 1, "bs_floor": 2, "bs_sence": 3})

print struct.unpack("<10B", bs_1105.bin_uwb())
print bs_1105.bs_x, bs_1105.uwb_chan

