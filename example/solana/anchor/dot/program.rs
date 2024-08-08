#![allow(unused_imports)]
#![allow(unused_variables)]
#![allow(unused_mut)]
use crate::{id, seahorse_util::*};
use anchor_lang::{prelude::*, solana_program};
use anchor_spl::token::{self, Mint, Token, TokenAccount};
use std::{cell::RefCell, rc::Rc};

#[derive(Clone, AnchorSerialize, AnchorDeserialize, Debug, Default)]
pub struct Coordinates {
    pub lat: f64,
    pub long: f64,
}

#[account]
#[derive(Debug)]
pub struct GymClass {
    pub owner: Pubkey,
    pub user: Pubkey,
    pub coordinates_class: Coordinates,
    pub name_array: [u16; 32],
    pub address_array: [u16; 64],
    pub info_array: [u16; 256],
    pub price: u32,
    pub expired_time: i64,
    pub secret_key_array: [u8; 32],
}

impl<'info, 'entrypoint> GymClass {
    pub fn load(
        account: &'entrypoint mut Box<Account<'info, Self>>,
        programs_map: &'entrypoint ProgramsMap<'info>,
    ) -> Mutable<LoadedGymClass<'info, 'entrypoint>> {
        let owner = account.owner.clone();
        let user = account.user.clone();
        let coordinates_class =
            Mutable::new(account.coordinates_class.clone());

        let name_array = Mutable::new(account.name_array.clone());
        let address_array = Mutable::new(account.address_array.clone());
        let info_array = Mutable::new(account.info_array.clone());
        let price = account.price;
        let expired_time = account.expired_time;
        let secret_key_array = Mutable::new(account.secret_key_array.clone());

        Mutable::new(LoadedGymClass {
            __account__: account,
            __programs__: programs_map,
            owner,
            user,
            coordinates_class,
            name_array,
            address_array,
            info_array,
            price,
            expired_time,
            secret_key_array,
        })
    }

    pub fn store(loaded: Mutable<LoadedGymClass>) {
        let mut loaded = loaded.borrow_mut();
        let owner = loaded.owner.clone();

        loaded.__account__.owner = owner;

        let user = loaded.user.clone();

        loaded.__account__.user = user;

        let coordinates_class = loaded.coordinates_class.borrow().clone();

        loaded.__account__.coordinates_class = coordinates_class;

        let name_array = loaded.name_array.borrow().clone();

        loaded.__account__.name_array = name_array;

        let address_array = loaded.address_array.borrow().clone();

        loaded.__account__.address_array = address_array;

        let info_array = loaded.info_array.borrow().clone();

        loaded.__account__.info_array = info_array;

        let price = loaded.price;

        loaded.__account__.price = price;

        let expired_time = loaded.expired_time;

        loaded.__account__.expired_time = expired_time;

        let secret_key_array = loaded.secret_key_array.borrow().clone();

        loaded.__account__.secret_key_array = secret_key_array;
    }
}

#[derive(Debug)]
pub struct LoadedGymClass<'info, 'entrypoint> {
    pub __account__: &'entrypoint mut Box<Account<'info, GymClass>>,
    pub __programs__: &'entrypoint ProgramsMap<'info>,
    pub owner: Pubkey,
    pub user: Pubkey,
    pub coordinates_class: Mutable<Coordinates>,
    pub name_array: Mutable<[u16; 32]>,
    pub address_array: Mutable<[u16; 64]>,
    pub info_array: Mutable<[u16; 256]>,
    pub price: u32,
    pub expired_time: i64,
    pub secret_key_array: Mutable<[u8; 32]>,
}

pub fn hide_gym_class_handler<'info>(
    mut clock: Sysvar<'info, Clock>,
    mut payer: SeahorseSigner<'info, '_>,
    mut user: SeahorseSigner<'info, '_>,
    mut gym_class: Mutable<LoadedGymClass<'info, '_>>,
    mut secret_key_array: [u8; 32],
    mut time_to_hide: u32,
) -> () {
    let mut time = clock.unix_timestamp;

    if !(time_to_hide > 0) {
        panic!("The time to hide is not valid");
    }

    if gym_class.borrow().user != user.key() {
        if !(gym_class.borrow().expired_time <= time) {
            panic!("The GymClass area is not expired");
        }
    }

    let mut is_secret_key_ok = true;
    let mut secret_key_mut_array = Mutable::<[u8; 32]>::new(secret_key_array);

    for mut i in 0..(secret_key_mut_array.borrow().len() as u64) {
        if secret_key_mut_array.borrow()
            [secret_key_mut_array.wrapped_index((i as i128) as i128)]
            != gym_class.borrow().secret_key_array.borrow()[gym_class
                .borrow()
                .secret_key_array
                .wrapped_index((i as i128) as i128)]
        {
            is_secret_key_ok = false;

            break;
        }
    }

    if !is_secret_key_ok {
        panic!("The secret key is not valid");
    }

    solana_program::program::invoke(
        &solana_program::system_instruction::transfer(
            &user.key(),
            &gym_class.borrow().__account__.key(),
            <u64 as TryFrom<_>>::try_from((gym_class.borrow().price * time_to_hide)).unwrap(),
        ),
        &[
            user.to_account_info(),
            gym_class.borrow().__account__.to_account_info(),
            user.programs.get("system_program").clone(),
        ],
    )
    .unwrap();

    if gym_class.borrow().user != user.key() {
        assign!(gym_class.borrow_mut().user, user.key());
    }

    if gym_class.borrow().expired_time > time {
        assign!(
            gym_class.borrow_mut().expired_time,
            gym_class.borrow().expired_time + (time_to_hide as i64)
        );
    } else {
        assign!(
            gym_class.borrow_mut().expired_time,
            time + (time_to_hide as i64)
        );
    }
}

pub fn init_gym_class_handler<'info>(
    mut clock: Sysvar<'info, Clock>,
    mut payer: SeahorseSigner<'info, '_>,
    mut owner: SeahorseSigner<'info, '_>,
    mut gym_class: Empty<Mutable<LoadedGymClass<'info, '_>>>,
    mut coordinates_class: Coordinates,
    mut name_array: [u16; 32],
    mut address_array: [u16; 64],
    mut info_array: [u16; 256],
    mut price: u32,
    mut secret_key_array: [u8; 32],
    mut seed_random: u64,
) -> () {
    let mut time = clock.unix_timestamp;
    let mut gym_class = gym_class.account.clone();

    assign!(gym_class.borrow_mut().owner, owner.key());

    assign!(gym_class.borrow_mut().coordinates_class, Mutable::<Coordinates>::new(coordinates_class));

    assign!(gym_class.borrow_mut().name_array, Mutable::<[u16; 32]>::new(name_array));

    assign!(gym_class.borrow_mut().address_array, Mutable::<[u16; 64]>::new(address_array));

    assign!(gym_class.borrow_mut().info_array, Mutable::<[u16; 256]>::new(info_array));

    assign!(gym_class.borrow_mut().price, price);

    assign!(gym_class.borrow_mut().expired_time, time);

    assign!(gym_class.borrow_mut().secret_key_array, Mutable::<[u8; 32]>::new(secret_key_array));
}

pub fn update_gym_class_handler<'info>(
    mut clock: Sysvar<'info, Clock>,
    mut payer: SeahorseSigner<'info, '_>,
    mut owner: SeahorseSigner<'info, '_>,
    mut gym_class: Mutable<LoadedGymClass<'info, '_>>,
    mut address_array: [u16; 64],
    mut info_array: [u16; 256],
    mut price: u32,
    mut secret_key_array: [u8; 32],
) -> () {
    let mut time = clock.unix_timestamp;

    if !(gym_class.borrow().owner == owner.key()) {
        panic!("The owner is not the same");
    }

    assign!(gym_class.borrow_mut().address_array, Mutable::<[u16; 64]>::new(address_array));

    assign!(gym_class.borrow_mut().info_array, Mutable::<[u16; 256]>::new(info_array));

    assign!(gym_class.borrow_mut().price, price);

    assign!(gym_class.borrow_mut().expired_time, time);

    assign!(gym_class.borrow_mut().secret_key_array, Mutable::<[u8; 32]>::new(secret_key_array));
}
