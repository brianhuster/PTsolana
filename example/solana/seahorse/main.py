# Built with Seahorse v0.2.0

from seahorse.prelude import *

# This is your program's public key and it will update
# automatically when you build the project.
declare_id('BgXa2B5G45eCm7WffVPCj5hVhy3kV9cgfWafpFdiW6m4')

class Coordinates:
    lat: f64 # 8 bytes
    long: f64 # 8 bytes

class GymClass(Account):
    owner: Pubkey # 32 bytes
    user: Pubkey # 32 bytes
    coordinates_Coordinates_class: Coordinates
    name_u16_32_array: Array[u16, 32] # 32 characters max = 64 bytes
    address_u16_64_array: Array[u16, 64] # 64 characters max = 128 bytes
    info_u16_256_array: Array[u16, 256] # 256 characters max = 512 bytes
    price: u32 # 4 bytes
    expired_time: i64 # 8 bytes
    secret_key_u8_32_array: Array[u8, 32] # 32 bytes
    # 32 + 32 + 8 + 8 + 64 + 128 + 512 + 4 + 8 + 32 = 828 bytes

@instruction
def init_gym_class(
    clock: Clock,
    payer: Signer,
    owner: Signer,
    gym_class: Empty[GymClass],
    coordinates_Coordinates_class: Coordinates,
    name_u16_32_array: Array[u16, 32],
    address_u16_64_array: Array[u16, 64],
    info_u16_256_array: Array[u16, 256],
    price: u32,
    secret_key_u8_32_array: Array[u8, 32],
    seed_random: u64
):
    time: i64 = clock.unix_timestamp()
    gym_class = gym_class.init(payer = payer, seeds = [owner, "gym_class", seed_random])
    gym_class.owner = owner.key()
    gym_class.coordinates_Coordinates_class = coordinates_Coordinates_class
    gym_class.name_u16_32_array = name_u16_32_array
    gym_class.address_u16_64_array = address_u16_64_array
    gym_class.info_u16_256_array = info_u16_256_array
    gym_class.price = price
    gym_class.expired_time = time
    gym_class.secret_key_u8_32_array = secret_key_u8_32_array

@instruction
def update_gym_class(
    clock: Clock,
    payer: Signer,
    owner: Signer,
    gym_class: GymClass,
    address_u16_64_array: Array[u16, 64],
    info_u16_256_array: Array[u16, 256],
    price: u32,
    secret_key_u8_32_array: Array[u8, 32]
):
    time: i64 = clock.unix_timestamp()
    assert gym_class.owner == owner.key(), "The owner is not the same"

    gym_class.address_u16_64_array = address_u16_64_array
    gym_class.info_u16_256_array = info_u16_256_array
    gym_class.price = price
    gym_class.expired_time = time
    gym_class.secret_key_u8_32_array = secret_key_u8_32_array

@instruction
def hide_gym_class(
    clock: Clock,
    payer: Signer,
    user: Signer,
    gym_class: GymClass,
    secret_key_u8_32_array: Array[u8, 32],
    time_to_hide: u32,
):
    time: i64 = clock.unix_timestamp()
    assert time_to_hide > 0, "The time to hide is not valid"
    if gym_class.user != user.key():
        assert gym_class.expired_time <= time, "The GymClass area is not expired"

    is_secret_key_ok: bool = True
    secret_key_mut_u8_32_array = secret_key_u8_32_array
    for i in range(len(secret_key_mut_u8_32_array)):
        if secret_key_mut_u8_32_array[i] != gym_class.secret_key_u8_32_array[i]:
            is_secret_key_ok = False
            break
    assert is_secret_key_ok, "The secret key is not valid"

    # Check if user have enough money
    # Transfer money to owner
    user.transfer_lamports(gym_class, u64(gym_class.price*time_to_hide))

    # Hide the GymClass area
    if gym_class.user != user.key():
        gym_class.user = user.key()
    if gym_class.expired_time > time:
        gym_class.expired_time = gym_class.expired_time + time_to_hide
    else:
        gym_class.expired_time = time + time_to_hide