import fastapi.middleware
import fastapi.middleware.cors
import uvicorn
from dotenv import load_dotenv
load_dotenv()
import json
from baseAPI import *
from hotaSolana.hotaSolanaData import *

from config import *
import fastapi

app = fastapi.FastAPI()
client = HotaSolanaRPC(PROGRAM_ID, False, "devnet")

origins = ["*"]

app.add_middleware(
    fastapi.middleware.cors.CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@BaseInstructionDataClass(name="init_gymclass")
class GymClassInitInstruction:
    name= HotaStringUTF8(lenArr=32)
    info=HotaStringUTF8(lenArr=256)
    price=HotaUint64()
    seed_sha256=HotaUint64()

@BaseInstructionDataClass(name="update_gymclass")
class GymClassUpdateInstruction:
    name=HotaStringUTF8(lenArr=32)
    info=HotaStringUTF8(lenArr=256)
    price=HotaUint64()

@BaseInstructionDataClass(name="customer_confirm_done")
class CustomerConfirmDoneInstruction:
    review=HotaStringUTF8(128)

@BaseInstructionDataClass(name="init_trainer_account")
class TrainerInitInstruction:
    phone=HotaStringUTF8(10)
    name=HotaStringUTF8(32)
    email=HotaStringUTF8(64)
    location=HotaStringUTF8(64)
    info=HotaStringUTF8(256)
    age=HotaUint8()
    gender=HotaUint8()
    seed_random=HotaUint64()
@BaseInstructionDataClass(name="update_trainer_account")
class TrainerUpdateInstruction:
    phone=HotaStringUTF8(10)
    name=HotaStringUTF8(32)
    email=HotaStringUTF8(64)
    location=HotaStringUTF8(64)
    info=HotaStringUTF8(256)

@BaseInstructionDataClass(name="init_customer_account")
class CustomerInitInstruction:
    phone=HotaStringUTF8(10)
    name=HotaStringUTF8(32)
    email=HotaStringUTF8(64)
    location=HotaStringUTF8(64)
    info=HotaStringUTF8(256)
    age=HotaUint8()
    gender=HotaUint8()
    seed_random=HotaUint64()

@BaseInstructionDataClass(name="update_customer_account")
class CustomerUpdateInstruction:
    phone=HotaStringUTF8(10)
    name=HotaStringUTF8(32)
    email=HotaStringUTF8(64)
    location=HotaStringUTF8(64)
    info=HotaStringUTF8(256)

@BaseStructClass
class GymClassData:
    flag=HotaUint8()
    company=HotaPublicKey() 
    customer=HotaPublicKey()
    trainer=HotaPublicKey()
    name=HotaStringUTF8(32)
    review=HotaStringUTF8(128)
    info=HotaStringUTF8(256)
    price=HotaUint64()
    seed_sha256=HotaUint64()
@BaseStructClass
class UserData:
    flag=HotaUint8()
    owner=HotaPublicKey()
    phone=HotaStringUTF8(10)
    name=HotaStringUTF8(32)
    email=HotaStringUTF8(64)
    location=HotaStringUTF8(64)
    info=HotaStringUTF8(256)
    age=HotaUint8()
    gender=HotaUint8()
    seed_random=HotaUint64()

class InitGymClassModel(BaseModel):
    name: str
    info: str
    price: int

class InitTrainerModel(BaseModel):
    phone: str
    name: str
    email:str
    location: str
    info: str
    age: int
    gender: int

class UpdateGymClassModel(BaseModel):
    name: str
    info: str
    price: int

def getPubkeyFromSeed(owner: PublicKey, secret_key: str, seed_random: int):
    return findProgramAddress(createBytesFromArrayBytes(
        owner.byte_value,
        secret_key.encode("utf-8"),
        bytes(HotaUint64(seed_random).serialize()),
    ), client.program_id)

@app.post("/init-gymclass")
async def init_gym_class(
    trainerPrivateKey: str,
    initGymClassModel: InitGymClassModel,
):
    def fun():
        company_keypair = makeKeyPair(OWNER_PRIVATE_KEY)

        instruction_data = GymClassInitInstruction()
        instruction_data.get("name").object2struct(initGymClassModel.name)
        instruction_data.get("info").object2struct(initGymClassModel.info)
        instruction_data.get("price").object2struct(initGymClassModel.price)
        instruction_data.get("seed_sha256").random()

        gym_class_pubkey = getPubkeyFromSeed(company_keypair.public_key, "gymclass", int(instruction_data.get("seed_sha256").value()))        
        print(gym_class_pubkey)

        instruction_address = client.send_transaction(
            instruction_data=instruction_data,
            pubkeys=[
                company_keypair.public_key,
                makeKeyPair(trainerPrivateKey).public_key,
                gym_class_pubkey,
                makePublicKey(sysvar_rent),
                makePublicKey(system_program),
            ],
            keypairs=[
                company_keypair,
                makeKeyPair(trainerPrivateKey),
            ],
            fee_payer=company_keypair.public_key
        )

        return {
            "instruction_address": instruction_address,
            "gym_class_public_key": bs58.encode(gym_class_pubkey.byte_value),
        }
    return make_response_auto_catch(fun)

@app.post("/update-gymclass")
async def update_gym_class(
    trainerPrivateKey: str,
    gymClassPubkey: str,
    updateGymClassModel: UpdateGymClassModel,
):
    def fun():
        trainer_keypair = makeKeyPair(trainerPrivateKey)

        instruction_data = GymClassUpdateInstruction()
        instruction_data.get("name").object2struct(updateGymClassModel.name)
        instruction_data.get("info").object2struct(updateGymClassModel.info)
        instruction_data.get("price").object2struct(updateGymClassModel.price)

        instruction_address = client.send_transaction(
            instruction_data=instruction_data,
            pubkeys=[
                trainer_keypair.public_key,
                PublicKey(gymClassPubkey),
                makePublicKey(sysvar_rent),
                makePublicKey(system_program),
            ],
            keypairs=[
                trainer_keypair,
            ],
            fee_payer=trainer_keypair.public_key
        )

        return {
            "updated_data": {
                "name": updateGymClassModel.name,
                "info": updateGymClassModel.info,
                "price": updateGymClassModel.price,
            },
            "instruction_address": instruction_address,
        }
    return make_response_auto_catch(fun)

@app.post("/init-trainer-account")
async def init_trainer_account(
    trainerPrivateKey: str,
    initTrainerModel: InitTrainerModel,
):
    def fun():
        trainer_keypair = makeKeyPair(trainerPrivateKey)

        instruction_data = TrainerInitInstruction()
        instruction_data.get("phone").object2struct(initTrainerModel.phone)
        instruction_data.get("name").object2struct(initTrainerModel.name)
        instruction_data.get("email").object2struct(initTrainerModel.email)
        instruction_data.get("location").object2struct(initTrainerModel.location)
        instruction_data.get("info").object2struct(initTrainerModel.info)
        instruction_data.get("age").object2struct(initTrainerModel.age)
        instruction_data.get("gender").object2struct(initTrainerModel.gender)
        instruction_data.get("seed_random").random()

        trainer_account_pubkey = getPubkeyFromSeed(trainer_keypair.public_key, "trainer", instruction_data.get("seed_random").value())
        
        instruction_address = client.send_transaction(
            instruction_data=instruction_data,
            pubkeys=[
                trainer_keypair.public_key,
                trainer_account_pubkey,
                makePublicKey(sysvar_rent),
                makePublicKey(system_program),
            ],
            keypairs=[
                makeKeyPair(trainerPrivateKey),
            ],
            fee_payer=trainer_keypair.public_key
        )

        return {
            "instruction_address": instruction_address,
            "trainer_account_public_key": bs58.encode(trainer_account_pubkey.byte_value),
        }
    return make_response_auto_catch(fun)

class UpdateTrainerModel(BaseModel):
    phone: str
    name: str
    email:str
    location: str
    info: str
@app.post("/update-trainer-account")
async def update_trainer_account(
    trainerPrivateKey: str,
    trainerAccountPubkey: str,
    updateTrainerModel: UpdateTrainerModel,
):
    def fun():
        trainer_keypair = makeKeyPair(trainerPrivateKey)
        
        instruction_data = TrainerUpdateInstruction()
        instruction_data.get("phone").object2struct(updateTrainerModel.phone)
        instruction_data.get("name").object2struct(updateTrainerModel.name)
        instruction_data.get("email").object2struct(updateTrainerModel.email)
        instruction_data.get("location").object2struct(updateTrainerModel.location)
        instruction_data.get("info").object2struct(updateTrainerModel.info)

        instruction_address = client.send_transaction(
            instruction_data=instruction_data,
            pubkeys=[
                trainer_keypair.public_key,
                PublicKey(trainerAccountPubkey),
                makePublicKey(sysvar_rent),
                makePublicKey(system_program),
            ],
            keypairs=[
                trainer_keypair,
            ],
            fee_payer=trainer_keypair.public_key
        )
        
        return {
            "updated_data": {
                "phone": updateTrainerModel.phone,
                "name": updateTrainerModel.name,
                "email": updateTrainerModel.email,
                "location": updateTrainerModel.location,
                "info": updateTrainerModel.info,
            },
            "instruction_address": instruction_address,
        }
    return make_response_auto_catch(fun)

@app.get("/get-all-trainer-accounts")
async def get_all_trainer_accounts_data():
    def fun():
        accounts = client.get_program_accounts()
        data = []
        for i in range(len(accounts)):
            try:
                # account_data = client.get_account_info(accounts[i].pubkey)
                account_data = client.get_account_data(accounts[i].pubkey, UserData, [8, 0])
                if account_data.get("flag") == 5 or account_data.get("flag") == 6:
                    trainerPubkey = PublicKey(account_data.get("owner"))
                    account_data["account_public_key"] = str(getPubkeyFromSeed(trainerPubkey, "trainer", account_data.get("seed_random")))
                    account_data.pop("seed_random")
                    data.append(account_data)
            except Exception as e:
                print(e)
        return data
    return make_response_auto_catch(fun)

# Todo: need to test
@app.get("/get-trainer-account-data")
async def get_trainer_account_data(public_key: str):
    def fun():
        try:
            account_data = client.get_account_data(PublicKey(public_key), UserData, [8, 4])
            if account_data.get("flag") == 5 or account_data.get("flag") == 6:
                return account_data
            else:
                return "This is not a trainer account"
        except Exception as e:
            return "cannot get to user account or the public key is invalid"
    return make_response_auto_catch(fun)

@app.get("/get-all-gym-classes-data")
async def get_all_gym_classes_data():
    def fun():
        accounts = client.get_program_accounts()
        data = []
        for i in range(len(accounts)):
            try:
                account_data = client.get_account_data(accounts[i].pubkey, GymClassData, [8, 4])
                if account_data.get("flag") <= 4:
                    gymClassPubkey = PublicKey(account_data.get("company"))
                    account_data["gym_class_public_key"] = str(getPubkeyFromSeed(gymClassPubkey, "gymclass", account_data.get("seed_sha256")))
                    account_data.pop("seed_sha256")
                    data.append(account_data)
            except Exception as e:
                pass
        return data
    return make_response_auto_catch(fun)

@app.get("/get-gym-class-data")
async def get_gym_class_data(public_key: str):
    return make_response_auto_catch(lambda: client.get_account_data(PublicKey(public_key), GymClassData, [8, 4]))

#### Common function1
@app.post("/convert-keypair-to-private-key")
async def convert_keypair_to_private_key(file: fastapi.UploadFile):
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

@app.get("/get-balance")
async def get_balance(public_key: str):
    return make_response_auto_catch(client.get_balance(public_key))

@app.post("/airdrop")
async def airdrop(public_key: str, amount: int = 1):
    return make_response_auto_catch(client.drop_sol(public_key, amount))

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)