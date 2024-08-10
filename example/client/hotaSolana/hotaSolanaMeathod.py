import requests
import json
from hotaSolana.bs58 import bs58
import hashlib
from solathon import Client, Transaction, PublicKey, Keypair
from nacl.signing import SigningKey, VerifyKey
from hotaSolana import ed25519

def send_rpc_api(url, jsonData):
    headers = {
        'Content-Type': 'application/json',
    }
    response = requests.post(url, headers=headers, data=jsonData)
    return response.json()


# def random_32bytes_with_seed(pubkey, seed, programid):
#     data = f"{pubkey}|{seed}|{programid}"
#     hashRandom = hashlib.sha256(data.encode('utf-8'))
#     return bs58.encode(hashRandom.digest())
def textEncodeASCII(text):
    # arr = []
    # for i in range(len(text)):
    #     arr.append(ord(text[i]))
    # print(arr)
    # return bytes(arr)
    return bytes(text, 'utf-8')


def random_32bytes_with_seed(pubkey, seed, programid):
    '''
    const buffer = Buffer.concat([
      fromPublicKey.toBuffer(),
      Buffer.from(seed),
      programId.toBuffer(),
    ]);
    const publicKeyBytes = sha256(buffer);
    return new PublicKey(publicKeyBytes);
    '''
    databytes = bytearray()
    databytes.extend(pubkey.byte_value)
    databytes.extend(textEncodeASCII(seed))
    databytes.extend(programid.byte_value)

    hashRandom = hashlib.sha256(bytes(databytes))
    return bytes(hashRandom.digest())


def random_64bytes_with_seed(pubkey, seed, programid):
    databytes = bytearray()
    databytes.extend(pubkey.byte_value)
    databytes.extend(seed.encode('utf-8'))
    databytes.extend(programid.byte_value)
    hashRandom32_0 = hashlib.sha256(bytes(databytes))
    hashRandom32_1 = hashlib.sha256(hashRandom32_0.digest())
    # Combine 2 hash
    hashRandom64 = bytearray()
    hashRandom64.extend(hashRandom32_0.digest())
    hashRandom64.extend(hashRandom32_1.digest())
    return bytes(hashRandom64)


def get_minimum_balance_for_rent_exmeption(url, span):
    jsonData = json.dumps({
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getMinimumBalanceForRentExemption",
        "params": [span]
    })
    response = send_rpc_api(url, jsonData)
    return response['result']


def getAccountInfo(url, pubkey):
    jsonData = json.dumps({
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getAccountInfo",
        "params": [pubkey, {"encoding": "base64"}]
    })
    response = send_rpc_api(url, jsonData)
    return response['result']

def convertNameToHash8Bytes(name):
    hashName = hashlib.sha256(f"global:{name}".encode('utf-8')).digest()
    return hashName[:8]

def hash256(data: str):
    return hashlib.sha256(data.encode('utf-8')).digest()

def makeKeyPair(secret_key: str):
    return Keypair.from_private_key(secret_key)

def makeKeyPairWithSeed(pubkey: PublicKey, seed: str, program_id: PublicKey):
    esPairKey = SigningKey(
        random_32bytes_with_seed(
            pubkey,
            seed,
            program_id
        )
    )
    return Keypair.from_private_key(bs58.encode(esPairKey.__dict__["_signing_key"]))

def makePublicKey(pubkey: str):
    return PublicKey(pubkey)

def createProblemAddress(bump: bytes, pubkey: PublicKey, seed: str, program_id: PublicKey):
    databytes = bytearray()
    databytes.extend(pubkey.byte_value)
    databytes.extend(textEncodeASCII(seed))
    databytes.extend(bump)
    databytes.extend(program_id.byte_value)
    databytes.extend(textEncodeASCII("ProgramDerivedAddress"))

    hashRandom = hashlib.sha256(bytes(databytes))

    return PublicKey(hashRandom.digest())

def findProgramAddress(pubKey: PublicKey, seed: str, program_id: PublicKey):
    for i in range(255, 0, -1):
        pubkey_seed = createProblemAddress(bytes([i]), pubKey, seed, program_id)

        if not ed25519.isOnCurve(pubkey_seed.byte_value.hex()):
            return pubkey_seed
    return None

# Only bytes
def makeKeyPairWithSeed(seed: bytes, program_id: PublicKey):
    databytes = bytearray()
    databytes.extend(seed)
    databytes.extend(program_id.byte_value)

    hashRandom = hashlib.sha256(bytes(databytes))
    
    esPairKey = SigningKey(bytes(hashRandom.digest()))
    return Keypair.from_private_key(bs58.encode(esPairKey.__dict__["_signing_key"]))

def createProblemAddress(bump: bytes, seed: bytes, program_id: PublicKey):
    databytes = bytearray()
    databytes.extend(seed)
    databytes.extend(bump)
    databytes.extend(program_id.byte_value)
    databytes.extend(textEncodeASCII("ProgramDerivedAddress"))

    hashRandom = hashlib.sha256(bytes(databytes))

    return PublicKey(hashRandom.digest())

def findProgramAddress(seed: bytes, program_id: PublicKey):
    for i in range(255, 0, -1):
        pubkey_seed = createProblemAddress(bytes([i]), seed, program_id)

        if not ed25519.isOnCurve(pubkey_seed.byte_value.hex()):
            return pubkey_seed
    return None

def createBytesFromArrayBytes(*array_bytes):
    bytes_data = bytearray()
    for byte in array_bytes:
        bytes_data.extend(byte)
    return bytes(bytes_data)