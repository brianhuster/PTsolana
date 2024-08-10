from typing import Optional
import uvicorn
import os
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, Body, Depends, HTTPException,  File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from config import *
from pydantic import BaseModel
import json

# import data
from hotaSolana.hotaSolanaDataBase import *
from hotaSolana.hotaSolanaData import *
from hotaSolana.bs58 import bs58

from baseAPI import *

PORT = int(os.getenv("PORT", 8000))
payerPrivateKey = os.getenv("PAYER_PRIVATE_KEY")
programId = os.getenv("PROGRAM_ID")

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Solana Client
client = HotaSolanaRPC(programId, False, "devnet")

# Solana instruction data
@BaseInstructionDataClass(name="init_gym_class")
class GymClassInitInstruction:
    name=HotaStringUTF16(32)
    address=HotaStringUTF16(64)
    info=HotaStringUTF16(256)
    price=HotaUint32()
    secret_key=HotaHex(32)
    seed_random=HotaHex(8)

@BaseInstructionDataClass(name="update_gym_class")
class GymClassUpdateInstruction:
    address=HotaStringUTF16(64)
    info=HotaStringUTF16(256)
    price=HotaUint32()
    secret_key=HotaHex(32)

@BaseInstructionDataClass(name="hide_gym_class")
class HideGymClassInstruction:
    secret_key=HotaHex(32)
    time_to_hide=HotaUint32()

# Solana account data
@BaseStructClass
class GymClassData:
    owner=HotaPublicKey()
    user=HotaPublicKey()
    name=HotaStringUTF16(32)
    address=HotaStringUTF16(64)
    info=HotaStringUTF16(256)
    price=HotaUint32()
    expired_time=HotaUint64()
    secret_key=HotaHex(32)

##### Router

# init_gym_class

class InitPTModel(BaseModel):
    name: str
    address: str
    info: str
    price: int
    secret_key: str

@app.post("/init-gym-class")
async def init_gym_class(
    owner_private_key: str,
    initGymClassModel: InitPTModel,
):
    def fun():
        owner_keypair = makeKeyPair(owner_private_key)

        instruction_data = GymClassInitInstruction()
        instruction_data.get("name").object2struct(initGymClassModel.name)
        instruction_data.get("address").object2struct(initGymClassModel.address)
        instruction_data.get("info").object2struct(initGymClassModel.info)
        instruction_data.get("price").object2struct(initGymClassModel.price)
        instruction_data.get("secret_key").deserialize(hash256(initGymClassModel.secret_key))
        instruction_data.get("seed_random").random()

        gym_class_pubkey = findProgramAddress(createBytesFromArrayBytes(
            owner_keypair.public_key.byte_value,
            "gym_class".encode("utf-8"),
            bytes(instruction_data.get("seed_random").serialize()),
        ), client.program_id)

        instruction_address = client.send_transaction(
            instruction_data,
            [
                makePublicKey(sysvar_clock),
                makeKeyPair(payerPrivateKey).public_key,
                owner_keypair.public_key,
                gym_class_pubkey,
                makePublicKey(sysvar_rent),
                makePublicKey(system_program),
            ],
            [
                makeKeyPair(payerPrivateKey),
                owner_keypair,
            ],
            fee_payer=makeKeyPair(payerPrivateKey).public_key
        )

        return {
            "instruction_address": instruction_address,
            "gym_class_public_key": bs58.encode(gym_class_pubkey.byte_value),
        }

    return make_response_auto_catch(fun)

# update_gym_class
class UpdateGymClassModel(BaseModel):
    address: str
    info: str
    price: int
    secret_key: str

@app.post("/update-gym-class")
async def update_gym_class(
    owner_private_key: str,
    gym_class_public_key: str,
    updateGymClassModel: UpdateGymClassModel,
):
    def fun():
        owner_keypair = makeKeyPair(owner_private_key)
        gym_class_pubkey = PublicKey(gym_class_public_key)

        instruction_data = GymClassUpdateInstruction()
        instruction_data.get("address").object2struct(updateGymClassModel.address)
        instruction_data.get("info").object2struct(updateGymClassModel.info)
        instruction_data.get("price").object2struct(updateGymClassModel.price)
        instruction_data.get("secret_key").deserialize(hash256(updateGymClassModel.secret_key))

        instruction_address = client.send_transaction(
            instruction_data,
            [
                makePublicKey(sysvar_clock),
                makeKeyPair(payerPrivateKey).public_key,
                owner_keypair.public_key,
                gym_class_pubkey,
                makePublicKey(sysvar_rent),
                makePublicKey(system_program),
            ],
            [
                makeKeyPair(payerPrivateKey),
                owner_keypair,
            ],
            fee_payer=makeKeyPair(payerPrivateKey).public_key
        )

        return {
            "instruction_address": instruction_address,
            "gym_class_public_key": bs58.encode(gym_class_pubkey.byte_value),
        }
    
    return make_response_auto_catch(fun)

# hide_gym_class
class HideGymClassModel(BaseModel):
    secret_key: str
    time_to_hide: int

@app.post("/hide-gym-class")
async def hide_gym_class(
    owner_private_key: str,
    gym_class_public_key: str,
    hideGymClassModel: HideGymClassModel,
):
    def fun():
        owner_keypair = makeKeyPair(owner_private_key)
        gym_class_pubkey = PublicKey(gym_class_public_key)

        instruction_data = HideGymClassInstruction()
        instruction_data.get("secret_key").deserialize(hash256(hideGymClassModel.secret_key))
        instruction_data.get("time_to_hide").object2struct(hideGymClassModel.time_to_hide)

        instruction_address = client.send_transaction(
            instruction_data,
            [
                makePublicKey(sysvar_clock),
                makeKeyPair(payerPrivateKey).public_key,
                owner_keypair.public_key,
                gym_class_pubkey,
                # makePublicKey(sysvar_rent),
                makePublicKey(system_program),
            ],
            [
                makeKeyPair(payerPrivateKey),
                owner_keypair,
            ],
            fee_payer=makeKeyPair(payerPrivateKey).public_key
        )

        return {
            "instruction_address": instruction_address,
            "gym_class_public_key": bs58.encode(gym_class_pubkey.byte_value),
            "time_to_hide": hideGymClassModel.time_to_hide,
        }
    
    return make_response_auto_catch(fun)

#### Common function1
@app.post("/convert-keypair-to-private-key")
async def convert_keypair_to_private_key(file: UploadFile):
    # Bytes to string
    result = file.file.read()
    keypair_json = json.loads(result)
    keypair_bytes = bytes(keypair_json)
    return {
        "public_key": bs58.encode(keypair_bytes[32:]),
        "private_key": bs58.encode(keypair_bytes),
    }

@app.get("/get-gym-class-info")
async def get_gym_class_info(public_key: str):
    return make_response_auto_catch(lambda: client.get_account_info(PublicKey(public_key)))

@app.get("/get-gym_class-data")
async def get_gym_class_data(public_key: str):
    return make_response_auto_catch(lambda: client.get_account_data(PublicKey(public_key), GymClassData, [8, 4]))

@app.get("/get-balance")
async def get_balance(public_key: str):
    return make_response_auto_catch(client.get_balance(public_key))

@app.post("/airdrop")
async def airdrop(public_key: str, amount: int = 1):
    return make_response_auto_catch(client.drop_sol(public_key, amount))

# Run
if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=PORT)
