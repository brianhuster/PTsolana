# blockchain
# Built with Seahorse v0.2.7

from seahorse.prelude import *

declare_id('4Bprhf44eKn2hm8WiHZZnbHbvUjeb9NKmrseBtYKY8te')
class User(Account):
    flag: u8 # 5: Active Trainer 6: Hidden Trainer 7: Customer
    owner: Pubkey # 32 byte
    phone_u8_10_array: Array[u8, 10] # 5 characters max = 5 bytes
    name_u8_32_array: Array[u8, 32] # 32 characters max = 32 bytes
    email_u8_64_array: Array[u8, 64] # 64 characters max = 64 bytes
    location_u8_64_array: Array[u8, 64] # 64 characters max = 64 bytes # City, Nation
    info_u8_256_array: Array[u8, 256] # 256 characters max = 256 bytes
    age: u8 # 1 byte
    gender: u8 # 1 byte
    seed_random: u64 # 8 bytes

class GymClass(Account):
    flag: u8 # 0: Available 1: Unavailable 2: PT Confirmed, 3: Customer Reviewed, 4: Hidden
    company: Pubkey # 32 bytes # Program
    customer: Pubkey # 32 bytes # User
    trainer: Pubkey # 32 bytes # PT
    name_u8_32_array: Array[u8, 32] # 32 characters max = 32 bytes
    review_u8_128_array: Array[u8, 128] # 128 characters max = 128 bytes
    info_u8_256_array: Array[u8, 256] # 256 characters max = 256 bytes
    price: u64 # 8 bytes # x (sol) 
    seed_sha256: u64 # 8 bytes

# PT create a class by signing a contract with our company
@instruction
def init_gymclass(
    company: Signer,
    trainer: Signer,
    gymclass: Empty[GymClass],
    name_u8_32_array: Array[u8, 32],
    info_u8_256_array: Array[u8, 256],
    price: u64,
    seed_sha256: u64,
):
    gymclass = gymclass.init(payer = company, seeds = [company, "gymclass", seed_sha256])
    gymclass.flag = 0 # Available by default
    gymclass.company = company.key()
    gymclass.customer = gymclass.key()
    gymclass.trainer = trainer.key()
    gymclass.name_u8_32_array = name_u8_32_array
    gymclass.info_u8_256_array = info_u8_256_array
    gymclass.price = price
    gymclass.seed_sha256 = seed_sha256
    
    trainer.transfer_lamports(company, 100000000) # 0.1 sol for creating class

@instruction
def customer_join_gymclass(
    customer: Signer,
    gymclass: GymClass
):
    assert gymclass.key() == gymclass.customer, "gymclass already have customer!"
    assert gymclass.flag < 2, "gymclass already done!"

    gymclass.customer = customer.key()
    gymclass.flag = 1 # Unavailable
    customer.transfer_lamports(gymclass, gymclass.price)

@instruction
def pt_decline_customer(
    customer: Signer,
    trainer: Signer,
    gymclass: GymClass
):
    assert trainer.key() == gymclass.trainer, "gymclass trainer not same!"
    assert customer.key() == gymclass.customer, "Customer is not in gymclass!"
    gymclass.flag = 0
    gymclass.customer = gymclass.key()
    gymclass.transfer_lamports(customer, gymclass.price)   

@instruction
def update_gymclass(
    trainer: Signer,
    gymclass: GymClass,
    name_u8_32_array: Array[u8, 32],
    info_u8_256_array: Array[u8, 256],
    price: u64
):
    assert trainer.key() == gymclass.trainer, "gymclass trainer not"

    gymclass.name_u8_32_array = name_u8_32_array
    gymclass.info_u8_256_array = info_u8_256_array
    gymclass.price = price

@instruction
def pt_confirm_done(
    trainer: Signer,
    gymclass: GymClass
):
    assert trainer.key() == gymclass.trainer, "gymclass trainer not"
    assert gymclass.flag == 0, "customer cannot confirm before PT"
    gymclass.flag = 1
    
@instruction
def customer_confirm_done(
    customer: Signer,
    trainer: Signer,
    company: Signer,
    gymclass: GymClass,
    review_u8_128_array: Array[u8, 128]
):
    assert customer.key() == gymclass.customer, "gymclass student not match"
    assert gymclass.flag <= 4, "this is not a gymclass"
    assert gymclass.flag == 1, "PT not confirm yet"

    gymclass.flag = 2
    pt_money = gymclass.price // 100 * 70 
    customer_reward = gymclass.price // 100 * 20
    gymclass.review_u8_128_array = review_u8_128_array
    gymclass.transfer_lamports(customer, pt_money)
    gymclass.transfer_lamports(trainer, customer_reward)
    gymclass.transfer_lamports(company, gymclass.price - pt_money - customer_reward)

@instruction
def trainer_hide_gymclass(
    trainer: Signer,
    gymclass: GymClass
):
    assert trainer.key() == gymclass.trainer, "you are not trainer"
    gymclass.flag = 4

@instruction
def init_trainer_account(
    trainer: Signer,
    user: Empty[User],
    phone_u8_10_array: Array[u8, 10],
    name_u8_32_array: Array[u8, 32],
    email_u8_64_array: Array[u8, 64],
    location_u8_64_array: Array[u8, 64],
    info_u8_256_array: Array[u8, 256],
    age: u8,
    gender: u8,
    seed_random: u64
):
    user = user.init(payer = trainer, seeds = [trainer, "trainer", seed_random])
    user.flag = 5
    user.owner = trainer.key()
    user.name_u8_32_array = name_u8_32_array
    user.email_u8_64_array = email_u8_64_array
    user.location_u8_64_array = location_u8_64_array
    user.info_u8_256_array = info_u8_256_array
    user.phone_u8_10_array = phone_u8_10_array
    user.age = age
    user.seed_random = seed_random
    user.gender = gender
    

@instruction
def update_trainer_account(
    trainer: Signer,
    user: User,
    phone_u8_10_array: Array[u8, 10],
    name_u8_32_array: Array[u8, 32],
    email_u8_64_array: Array[u8, 64],
    location_u8_64_array: Array[u8, 64],
    info_u8_256_array: Array[u8, 256],
):
    assert user.flag == 5 or user.flag == 6, "This is not a trainer account"
    assert trainer.key() == user.owner, "you are not allowed to update this account"

    user.phone_u8_10_array = phone_u8_10_array
    user.name_u8_32_array = name_u8_32_array
    user.email_u8_64_array = email_u8_64_array
    user.location_u8_64_array = location_u8_64_array
    user.info_u8_256_array = info_u8_256_array

@instruction
def hide_trainer_account(
    trainer: Signer,
    user: User
):
    assert trainer.key() == user.owner, "you are not allowed to hide this account"
    assert user.flag == 5, "This is not a trainer account or already hidden"

    user.flag = 6

@instruction
def init_customer_account(
    customer: Signer,
    user: Empty[User],
    phone_u8_10_array: Array[u8, 10],
    name_u8_32_array: Array[u8, 32],
    email_u8_64_array: Array[u8, 64],
    location_u8_64_array: Array[u8, 64],
    info_u8_256_array: Array[u8, 256],
    age: u8,
    gender: u8,
    seed_random: u64
):
    user = user.init(payer = customer, seeds = [customer, "customer", seed_random])
    user.owner = customer.key()
    user.phone_u8_10_array = phone_u8_10_array
    user.name_u8_32_array = name_u8_32_array
    user.email_u8_64_array = email_u8_64_array
    user.location_u8_64_array = location_u8_64_array
    user.info_u8_256_array = info_u8_256_array
    user.age = age
    user.gender = gender
    user.seed_random = seed_random
    user.flag = 7
    

@instruction
def update_customer_account(
    customer: Signer,
    user: User,
    phone_u8_10_array: Array[u8, 10],
    name_u8_32_array: Array[u8, 32],
    email_u8_64_array: Array[u8, 64],
    location_u8_64_array: Array[u8, 64],
    info_u8_256_array: Array[u8, 256],
):
    assert customer.key() == user.owner , "you are not allowed to update this account"
    user.phone_u8_10_array = phone_u8_10_array
    user.name_u8_32_array = name_u8_32_array
    user.email_u8_64_array = email_u8_64_array
    user.location_u8_64_array = location_u8_64_array
    user.info_u8_256_array = info_u8_256_array
