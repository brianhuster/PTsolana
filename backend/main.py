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
@BaseInstructionDataClass(name="update_gymclass")
class GymClassUpdateInstruction:
    name=HotaStringUTF8(lenArr=32)
    info=HotaStringUTF8(lenArr=256)
    price=HotaUint64()

@BaseInstructionDataClass(name="customer_confirm_done")
class CustomerConfirmDoneInstruction:
    review=HotaStringUTF8(128)

@BaseInstructionDataClass(name="update_trainer_account")
class TrainerUpdateInstruction:
    phone=HotaStringUTF8(10)
    name=HotaStringUTF8(32)
    email=HotaStringUTF8(64)
    location=HotaStringUTF8(64)
    info=HotaStringUTF8(256)

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

def normalize_gym_class_data(account_data: dict):
    account_data["gym_class_public_key"] = str(getPubkeyFromSeed(PublicKey(account_data.get("company")), "gymclass", account_data.get("seed_sha256")))
    account_data["price"] = account_data.get("price") / LAMPORTS_PER_SOL
    account_data.pop("seed_sha256")
    return account_data

def normalize_user_data(account_data: dict, secret_key: str):
    account_data["user_account_public_key"] = str(getPubkeyFromSeed(PublicKey(account_data.get("owner")), secret_key, account_data.get("seed_random")))
    if account_data.get("flag") == 5:
        account_data["role"] = "trainer"
    elif account_data.get("flag") == 6:
        account_data["role"] = "customer"
    if account_data.get("gender") == 0:
        account_data["gender"] = "male"
    elif account_data.get("gender") == 1:
        account_data["gender"] = "female"
    else:
        account_data["gender"] = "other"
    account_data.pop("seed_random")
    return account_data

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
                account_data = client.get_account_data(accounts[i].pubkey, UserData, [8, 0])
                if account_data.get("flag") == 5 or account_data.get("flag") == 6:
                    account_data = normalize_user_data(account_data, "trainer")
                    data.append(account_data)
            except Exception as e:
                print(e)
        return data
    return make_response_auto_catch(fun)

# Still in process
@app.get("/get-pending-request")
async def get_customer_request(
    gymClassPubkey: str
):
    def fun():
        accounts = client.get_program_accounts()
        data = []
        for i in range(len(accounts)):
            try:
                account = client.get_account_data(accounts[i].pubkey, GymClassData, [8, 4])
                pubkey =  getPubkeyFromSeed(PublicKey(account.get("company")), "gymclass", account.get("seed_sha256"))
                print(str(pubkey))
                if account.get("flag") == 1 and str(pubkey) == gymClassPubkey:
                    account = normalize_gym_class_data(account)
                    data.append(account)

            except Exception as e:
                if str(e) != "index out of range":
                    data.append(
                        {
                            "error": str(e),
                            "pubkey": str(accounts[i].pubkey),
                        }
                    )
        return data
    return make_response_auto_catch(fun)

# Todo: need to test
@app.get("/get-account-data")
async def get_account_data(public_key: str):
    def fun():
        accounts = client.get_program_accounts()
        account_data = None
        for i in range(len(accounts)):
            try:
                account_data = client.get_account_data(accounts[i].pubkey, UserData, [8, 0])
                if (account_data.get("flag") == 5 or account_data.get("flag") == 6) and account_data.get("owner") == public_key:
                        return normalize_user_data(account_data, "trainer")
            except Exception as e:
                print(e)
        return "Not found"
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
                    account_data = normalize_gym_class_data(account_data)
                    data.append(account_data)
            except Exception as e:
                pass
        return data
    return make_response_auto_catch(fun)

@app.get("/get-all-gym-classes-data-by-trainer")
async def get_all_gym_classes_data(
    trainerPubkey: str
):
    def fun():
        accounts = client.get_program_accounts()
        data = []
        for i in range(len(accounts)):
            try:
                account_data = client.get_account_data(accounts[i].pubkey, GymClassData, [8, 4])
                if account_data.get("flag") <= 4 and account_data.get("trainer") == trainerPubkey:
                    account_data = normalize_gym_class_data(account_data)
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

@BaseInstructionDataClass(name="trainer_hide_gymclass")
class TrainerHideGymclassInstruction:
    pass

@app.get("/trainer-hide-gymclass")
async def trainer_hide_gym_class(
    trainerPubkey: str,
    gymclassPubkey: str
):
    def fun():
        instruction_data = TrainerHideGymclassInstruction()

        transaction = client.create_transaction(
            instruction_data = instruction_data,
            pubkeys=[
                PublicKey(trainerPubkey),
                PublicKey(gymclassPubkey)
            ],
            is_signers=[True, False]
        )

        return {"transaction": transaction}
    return make_response_auto_catch(fun)

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)