from hotaSolana.hotaSolanaData import *
from hotaSolana.hotaSolanaMeathod import *
import os

name = HotaStringUTF16(lenArr=32)
location = HotaStringUTF16(lenArr=64)
info = HotaStringUTF16(lenArr=256)

name.object2struct("My Gym")
location.object2struct("My Location")
info.object2struct("My Info is here abcxyz")

def convertToString(data:HotaStringUTF16, lenArr) -> str:
    string = "["
    for i in range(lenArr):
        num:HotaUint16 = data.get(i)
        string += str(num.value())+","
    string = string[:-1]
    return string+"]"

# print(convertToString(name, 32))
# print(convertToString(location,64))
# print(convertToString(info,256))

""" seed = HotaUint64(11894801560357025724)
print("seed: " + str(seed.value()))
print("serial seed: " + str(seed.serialize()))
company_pubkey = PublicKey("6zahakYqx6d6SsyA6E9QdPcetQSwt1APify4Z5bDSrjB")
mystr="gymclass"

print(findProgramAddress(createBytesFromArrayBytes(
    company_pubkey.byte_value,
    "gymclass".encode("utf-8"),
    bytes(seed.serialize())
), PublicKey("poTfdHjWbSsodLv1npNwAAtN4Cpa1hHTwHJJ9jXbvad")))
 """

phone_num = HotaStringUTF8(30) 
phone_num.object2struct("")
print(phone_num.struct2object())