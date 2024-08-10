from solathon.core.instructions import transfer, create_account, Instruction, AccountMeta
from solathon import Client, Transaction, PublicKey, Keypair
import random
from hotaSolana.hotaSolanaDataBase import *
from hotaSolana.hotaSolanaMeathod import *
from nacl.public import PrivateKey as NaclPrivateKey
import base64
from nacl.signing import SigningKey

class HotaSolanaRPC:
    def __init__(self, program_id: str, localhost=False, namenet="devnet"):
        self.program_id = PublicKey(program_id)
        self.localhost = localhost
        self.namenet = namenet
        self.urlNetSolana = ""

        if localhost:
            self.connection = Client(
                "http://localhost:8899")
            self.urlNetSolana = "http://localhost:8899"
            print("Connected to localhost")
        else:
            self.connection = Client(
                f"https://api.{namenet}.solana.com")
            self.urlNetSolana = f"https://api.{namenet}.solana.com"
            print(f"Connected to {namenet}")
    
    def get_account_info(self, public_key: PublicKey):
        account_info = self.connection.get_account_info(
            public_key, commitment={
                "encoding": "base64"
            })
        return account_info

    def get_account_data(self, public_key: PublicKey, AccountDataClass: BaseStruct, shift_bytes = [8, 0]):
        account_info = self.get_account_info(public_key)
        account_data_bytes = base64.b64decode(account_info.data[0])
        print("Account data len: ", len(account_data_bytes))
        account_data = AccountDataClass()
        print("Local account data len: ", account_data.size())
        if shift_bytes[0] > 0:
            print("shift_left: ", account_data_bytes[:shift_bytes[0]].hex())
            account_data_bytes = account_data_bytes[shift_bytes[0]:]
        if shift_bytes[1] > 0:
            print("shift_right: ", account_data_bytes[-shift_bytes[1]:].hex())
            account_data_bytes = account_data_bytes[:-shift_bytes[1]]
            
        account_data.deserialize(account_data_bytes)
        return account_data.struct2object()

    def send_transaction(self, instruction_data: BaseStruct, pubkeys=[], keypairs=[], fee_payer: PublicKey = None):
        is_signers = [False] * len(pubkeys)
        for keypair in keypairs:
            for i in range(len(pubkeys)):
                if keypair.public_key == pubkeys[i]:
                    is_signers[i] = True

        keys = [AccountMeta(public_key=pubkeys[i],
                            is_signer=is_signers[i], is_writable=True)
                for i in range(len(pubkeys))]

        instruction = Instruction(
            keys=keys,
            program_id=self.program_id,
            data=bytes(instruction_data.serialize()),
        )

        print("Instruction data len: ", len(instruction_data.serialize()))

        transaction = Transaction(
            instructions=[
                instruction
            ],
            signers=keypairs, fee_payer=fee_payer
        )

        signature = self.connection.send_transaction(transaction)
        print(f"Transaction sent with signature {signature}")
        return signature
    
    def get_balance(self, public_key: PublicKey):
        balance = self.connection.get_balance(public_key)
        return balance
    
    def drop_sol(self, public_key: PublicKey, amount):
        sig = self.connection.request_airdrop(
            public_key, amount
        )
        print(f"Dropped {amount} SOL with signature {sig}")
        return sig

class HotaSolanaClient(HotaSolanaRPC):
    def __init__(self, program_id: str, localhost=False, namenet="devnet"):
        super().__init__(program_id, localhost, namenet)

    def make_key_pair(self, secret_key: str, seed = "hotaNFT"):
        self.keypair = Keypair.from_private_key(secret_key)
        print(f"Logged in with keypair {self.keypair.public_key}")

        self.public_key_seed = findProgramAddress(self.keypair.public_key, seed, self.program_id)

        print(
            f"Logged in with public_key_seed: {self.public_key_seed}")

        # Check if account is created
        try:
            self.connection.get_account_info(
                self.public_key_seed, commitment={
                    "encoding": "base64"
                })
            return {"public_key_with_seed": self.public_key_seed.__str__()}
        except Exception as e:
            raise Exception("Account not created")

    def drop_sol(self, amount):
        sig = self.connection.request_airdrop(
            self.keypair.public_key, amount
        )
        print(f"Dropped {amount} SOL with signature {sig}")
        return sig

    def get_balance(self):
        balance = self.connection.get_balance(self.keypair.public_key)
        return balance

    def get_account_info(self):
        return super().get_account_info(self.public_key_seed)

    def get_account_data(self, AccountDataClass: BaseStruct):
        return super().get_account_data(self.public_key_seed, AccountDataClass)

# Def filter BaseStruct
def FilterBaseStruct(dict_object):
    dict_object_copy = {}
    for key, value in dict_object.items():
        if isinstance(value, BaseStruct):
            dict_object_copy[key] = value
    return dict_object_copy

# @BaseStructClass
def BaseStructClass(object):
    dict_object = FilterBaseStruct(object.__dict__)
    class BaseStructClass(BaseStruct):
        def __init__(self, **kwargs):
            # Update kwargs to dict_object
            for key, value in kwargs.items():
                if key in dict_object:
                    dict_object[key] = value
            super().__init__(GenBaseEleList(dict_object))

    return BaseStructClass

# @BaseInstructionDataClass
def BaseInstructionDataClass(name: str):
    def inner_BaseInstructionDataClass(object):
        dict_object = FilterBaseStruct(object.__dict__)
        class BaseInstructionDataClass(BaseStruct):
            def __init__(self, **kwargs):
                nameHash = HotaUint64(0)
                nameHash.deserialize(convertNameToHash8Bytes(name))
                # Update kwargs to dict_object
                for key, value in kwargs.items():
                    if key in dict_object:
                        dict_object[key] = value
                super().__init__(GenBaseEleList({
                    "typeInstruction": nameHash,
                    **dict_object
                }))

        return BaseInstructionDataClass
    return inner_BaseInstructionDataClass