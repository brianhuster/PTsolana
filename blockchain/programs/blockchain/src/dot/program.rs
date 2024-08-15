#![allow(unused_imports)]
#![allow(unused_variables)]
#![allow(unused_mut)]
use crate::{id, seahorse_util::*};
use anchor_lang::{prelude::*, solana_program};
use anchor_spl::token::{self, Mint, Token, TokenAccount};
use std::{cell::RefCell, rc::Rc};

#[account]
#[derive(Debug)]
pub struct GymClass {
    pub flag: u8,
    pub company: Pubkey,
    pub customer: Pubkey,
    pub trainer: Pubkey,
    pub name_array: [u8; 32],
    pub review_array: [u8; 128],
    pub info_array: [u8; 256],
    pub price: u64,
    pub seed_sha256: u64,
}

impl<'info, 'entrypoint> GymClass {
    pub fn load(
        account: &'entrypoint mut Box<Account<'info, Self>>,
        programs_map: &'entrypoint ProgramsMap<'info>,
    ) -> Mutable<LoadedGymClass<'info, 'entrypoint>> {
        let flag = account.flag;
        let company = account.company.clone();
        let customer = account.customer.clone();
        let trainer = account.trainer.clone();
        let name_array = Mutable::new(account.name_array.clone());
        let review_array = Mutable::new(account.review_array.clone());
        let info_array = Mutable::new(account.info_array.clone());
        let price = account.price;
        let seed_sha256 = account.seed_sha256;

        Mutable::new(LoadedGymClass {
            __account__: account,
            __programs__: programs_map,
            flag,
            company,
            customer,
            trainer,
            name_array,
            review_array,
            info_array,
            price,
            seed_sha256,
        })
    }

    pub fn store(loaded: Mutable<LoadedGymClass>) {
        let mut loaded = loaded.borrow_mut();
        let flag = loaded.flag;

        loaded.__account__.flag = flag;

        let company = loaded.company.clone();

        loaded.__account__.company = company;

        let customer = loaded.customer.clone();

        loaded.__account__.customer = customer;

        let trainer = loaded.trainer.clone();

        loaded.__account__.trainer = trainer;

        let name_array = loaded.name_array.borrow().clone();

        loaded.__account__.name_array = name_array;

        let review_array = loaded.review_array.borrow().clone();

        loaded.__account__.review_array = review_array;

        let info_array = loaded.info_array.borrow().clone();

        loaded.__account__.info_array = info_array;

        let price = loaded.price;

        loaded.__account__.price = price;

        let seed_sha256 = loaded.seed_sha256;

        loaded.__account__.seed_sha256 = seed_sha256;
    }
}

#[derive(Debug)]
pub struct LoadedGymClass<'info, 'entrypoint> {
    pub __account__: &'entrypoint mut Box<Account<'info, GymClass>>,
    pub __programs__: &'entrypoint ProgramsMap<'info>,
    pub flag: u8,
    pub company: Pubkey,
    pub customer: Pubkey,
    pub trainer: Pubkey,
    pub name_array: Mutable<[u8; 32]>,
    pub review_array: Mutable<[u8; 128]>,
    pub info_array: Mutable<[u8; 256]>,
    pub price: u64,
    pub seed_sha256: u64,
}

#[account]
#[derive(Debug)]
pub struct User {
    pub flag: u8,
    pub owner: Pubkey,
    pub phone_array: [u8; 10],
    pub name_array: [u8; 32],
    pub email_array: [u8; 64],
    pub location_array: [u8; 64],
    pub info_array: [u8; 256],
    pub age: u8,
    pub gender: u8,
    pub seed_random: u64,
}

impl<'info, 'entrypoint> User {
    pub fn load(
        account: &'entrypoint mut Box<Account<'info, Self>>,
        programs_map: &'entrypoint ProgramsMap<'info>,
    ) -> Mutable<LoadedUser<'info, 'entrypoint>> {
        let flag = account.flag;
        let owner = account.owner.clone();
        let phone_array = Mutable::new(account.phone_array.clone());
        let name_array = Mutable::new(account.name_array.clone());
        let email_array = Mutable::new(account.email_array.clone());
        let location_array = Mutable::new(account.location_array.clone());
        let info_array = Mutable::new(account.info_array.clone());
        let age = account.age;
        let gender = account.gender;
        let seed_random = account.seed_random;

        Mutable::new(LoadedUser {
            __account__: account,
            __programs__: programs_map,
            flag,
            owner,
            phone_array,
            name_array,
            email_array,
            location_array,
            info_array,
            age,
            gender,
            seed_random,
        })
    }

    pub fn store(loaded: Mutable<LoadedUser>) {
        let mut loaded = loaded.borrow_mut();
        let flag = loaded.flag;

        loaded.__account__.flag = flag;

        let owner = loaded.owner.clone();

        loaded.__account__.owner = owner;

        let phone_array = loaded.phone_array.borrow().clone();

        loaded.__account__.phone_array = phone_array;

        let name_array = loaded.name_array.borrow().clone();

        loaded.__account__.name_array = name_array;

        let email_array = loaded.email_array.borrow().clone();

        loaded.__account__.email_array = email_array;

        let location_array = loaded.location_array.borrow().clone();

        loaded.__account__.location_array = location_array;

        let info_array = loaded.info_array.borrow().clone();

        loaded.__account__.info_array = info_array;

        let age = loaded.age;

        loaded.__account__.age = age;

        let gender = loaded.gender;

        loaded.__account__.gender = gender;

        let seed_random = loaded.seed_random;

        loaded.__account__.seed_random = seed_random;
    }
}

#[derive(Debug)]
pub struct LoadedUser<'info, 'entrypoint> {
    pub __account__: &'entrypoint mut Box<Account<'info, User>>,
    pub __programs__: &'entrypoint ProgramsMap<'info>,
    pub flag: u8,
    pub owner: Pubkey,
    pub phone_array: Mutable<[u8; 10]>,
    pub name_array: Mutable<[u8; 32]>,
    pub email_array: Mutable<[u8; 64]>,
    pub location_array: Mutable<[u8; 64]>,
    pub info_array: Mutable<[u8; 256]>,
    pub age: u8,
    pub gender: u8,
    pub seed_random: u64,
}

pub fn customer_confirm_done_handler<'info>(
    mut customer: SeahorseSigner<'info, '_>,
    mut trainer: SeahorseSigner<'info, '_>,
    mut company: SeahorseSigner<'info, '_>,
    mut gymclass: Mutable<LoadedGymClass<'info, '_>>,
    mut review_array: [u8; 128],
) -> () {
    if !(customer.key() == gymclass.borrow().customer) {
        panic!("gymclass student not match");
    }

    if !(gymclass.borrow().flag <= 4) {
        panic!("this is not a gymclass");
    }

    if !(gymclass.borrow().flag == 1) {
        panic!("PT not confirm yet");
    }

    assign!(gymclass.borrow_mut().flag, 2);

    let mut pt_money = (gymclass.borrow().price / 100) * 70;
    let mut customer_reward = (gymclass.borrow().price / 100) * 20;

    assign!(gymclass.borrow_mut().review_array, Mutable::<[u8; 128]>::new(review_array));

    {
        let amount = pt_money.clone();

        **gymclass
            .borrow()
            .__account__
            .to_account_info()
            .try_borrow_mut_lamports()
            .unwrap() -= amount;

        **customer
            .clone()
            .to_account_info()
            .try_borrow_mut_lamports()
            .unwrap() += amount;
    };

    {
        let amount = customer_reward.clone();

        **gymclass
            .borrow()
            .__account__
            .to_account_info()
            .try_borrow_mut_lamports()
            .unwrap() -= amount;

        **trainer
            .clone()
            .to_account_info()
            .try_borrow_mut_lamports()
            .unwrap() += amount;
    };

    {
        let amount = ((gymclass.borrow().price - pt_money) - customer_reward);

        **gymclass
            .borrow()
            .__account__
            .to_account_info()
            .try_borrow_mut_lamports()
            .unwrap() -= amount;

        **company
            .clone()
            .to_account_info()
            .try_borrow_mut_lamports()
            .unwrap() += amount;
    };
}

pub fn customer_join_gymclass_handler<'info>(
    mut customer: SeahorseSigner<'info, '_>,
    mut gymclass: Mutable<LoadedGymClass<'info, '_>>,
) -> () {
    if !(gymclass.borrow().__account__.key() == gymclass.borrow().customer) {
        panic!("gymclass already have customer!");
    }

    if !(gymclass.borrow().flag < 2) {
        panic!("gymclass already done!");
    }

    assign!(gymclass.borrow_mut().customer, customer.key());

    assign!(gymclass.borrow_mut().flag, 1);

    solana_program::program::invoke(
        &solana_program::system_instruction::transfer(
            &customer.key(),
            &gymclass.borrow().__account__.key(),
            gymclass.borrow().price.clone(),
        ),
        &[
            customer.to_account_info(),
            gymclass.borrow().__account__.to_account_info(),
            customer.programs.get("system_program").clone(),
        ],
    )
    .unwrap();
}

pub fn hide_trainer_account_handler<'info>(
    mut trainer: SeahorseSigner<'info, '_>,
    mut user: Mutable<LoadedUser<'info, '_>>,
) -> () {
    if !(trainer.key() == user.borrow().owner) {
        panic!("you are not allowed to hide this account");
    }

    if !(user.borrow().flag == 5) {
        panic!("This is not a trainer account or already hidden");
    }

    assign!(user.borrow_mut().flag, 6);
}

pub fn init_customer_account_handler<'info>(
    mut customer: SeahorseSigner<'info, '_>,
    mut user: Empty<Mutable<LoadedUser<'info, '_>>>,
    mut phone_array: [u8; 10],
    mut name_array: [u8; 32],
    mut email_array: [u8; 64],
    mut location_array: [u8; 64],
    mut info_array: [u8; 256],
    mut age: u8,
    mut gender: u8,
    mut seed_random: u64,
) -> () {
    let mut user = user.account.clone();

    assign!(user.borrow_mut().owner, customer.key());

    assign!(user.borrow_mut().phone_array, Mutable::<[u8; 10]>::new(phone_array));

    assign!(user.borrow_mut().name_array, Mutable::<[u8; 32]>::new(name_array));

    assign!(user.borrow_mut().email_array, Mutable::<[u8; 64]>::new(email_array));

    assign!(user.borrow_mut().location_array, Mutable::<[u8; 64]>::new(location_array));

    assign!(user.borrow_mut().info_array, Mutable::<[u8; 256]>::new(info_array));

    assign!(user.borrow_mut().age, age);

    assign!(user.borrow_mut().gender, gender);

    assign!(user.borrow_mut().seed_random, seed_random);

    assign!(user.borrow_mut().flag, 7);
}

pub fn init_gymclass_handler<'info>(
    mut company: SeahorseSigner<'info, '_>,
    mut trainer: SeahorseSigner<'info, '_>,
    mut gymclass: Empty<Mutable<LoadedGymClass<'info, '_>>>,
    mut name_array: [u8; 32],
    mut info_array: [u8; 256],
    mut price: u64,
    mut seed_sha256: u64,
) -> () {
    let mut gymclass = gymclass.account.clone();

    assign!(gymclass.borrow_mut().flag, 0);

    assign!(gymclass.borrow_mut().company, company.key());

    assign!(
        gymclass.borrow_mut().customer,
        gymclass.borrow().__account__.key()
    );

    assign!(gymclass.borrow_mut().trainer, trainer.key());

    assign!(gymclass.borrow_mut().name_array, Mutable::<[u8; 32]>::new(name_array));

    assign!(gymclass.borrow_mut().info_array, Mutable::<[u8; 256]>::new(info_array));

    assign!(gymclass.borrow_mut().price, price);

    assign!(gymclass.borrow_mut().seed_sha256, seed_sha256);

    solana_program::program::invoke(
        &solana_program::system_instruction::transfer(
            &trainer.key(),
            &company.clone().key(),
            100000000,
        ),
        &[
            trainer.to_account_info(),
            company.clone().to_account_info(),
            trainer.programs.get("system_program").clone(),
        ],
    )
    .unwrap();
}

pub fn init_trainer_account_handler<'info>(
    mut trainer: SeahorseSigner<'info, '_>,
    mut user: Empty<Mutable<LoadedUser<'info, '_>>>,
    mut phone_array: [u8; 10],
    mut name_array: [u8; 32],
    mut email_array: [u8; 64],
    mut location_array: [u8; 64],
    mut info_array: [u8; 256],
    mut age: u8,
    mut gender: u8,
    mut seed_random: u64,
) -> () {
    let mut user = user.account.clone();

    assign!(user.borrow_mut().flag, 5);

    assign!(user.borrow_mut().owner, trainer.key());

    assign!(user.borrow_mut().name_array, Mutable::<[u8; 32]>::new(name_array));

    assign!(user.borrow_mut().email_array, Mutable::<[u8; 64]>::new(email_array));

    assign!(user.borrow_mut().location_array, Mutable::<[u8; 64]>::new(location_array));

    assign!(user.borrow_mut().info_array, Mutable::<[u8; 256]>::new(info_array));

    assign!(user.borrow_mut().phone_array, Mutable::<[u8; 10]>::new(phone_array));

    assign!(user.borrow_mut().age, age);

    assign!(user.borrow_mut().seed_random, seed_random);

    assign!(user.borrow_mut().gender, gender);
}

pub fn pt_confirm_done_handler<'info>(
    mut trainer: SeahorseSigner<'info, '_>,
    mut gymclass: Mutable<LoadedGymClass<'info, '_>>,
) -> () {
    if !(trainer.key() == gymclass.borrow().trainer) {
        panic!("gymclass trainer not");
    }

    if !(gymclass.borrow().flag == 0) {
        panic!("customer cannot confirm before PT");
    }

    assign!(gymclass.borrow_mut().flag, 1);
}

pub fn pt_decline_customer_handler<'info>(
    mut customer: SeahorseSigner<'info, '_>,
    mut trainer: SeahorseSigner<'info, '_>,
    mut gymclass: Mutable<LoadedGymClass<'info, '_>>,
) -> () {
    if !(trainer.key() == gymclass.borrow().trainer) {
        panic!("gymclass trainer not same!");
    }

    if !(customer.key() == gymclass.borrow().customer) {
        panic!("Customer is not in gymclass!");
    }

    assign!(gymclass.borrow_mut().flag, 0);

    assign!(
        gymclass.borrow_mut().customer,
        gymclass.borrow().__account__.key()
    );

    {
        let amount = gymclass.borrow().price.clone();

        **gymclass
            .borrow()
            .__account__
            .to_account_info()
            .try_borrow_mut_lamports()
            .unwrap() -= amount;

        **customer
            .clone()
            .to_account_info()
            .try_borrow_mut_lamports()
            .unwrap() += amount;
    };
}

pub fn trainer_hide_gymclass_handler<'info>(
    mut trainer: SeahorseSigner<'info, '_>,
    mut gymclass: Mutable<LoadedGymClass<'info, '_>>,
) -> () {
    if !(trainer.key() == gymclass.borrow().trainer) {
        panic!("you are not trainer");
    }

    assign!(gymclass.borrow_mut().flag, 4);
}

pub fn update_customer_account_handler<'info>(
    mut customer: SeahorseSigner<'info, '_>,
    mut user: Mutable<LoadedUser<'info, '_>>,
    mut phone_array: [u8; 10],
    mut name_array: [u8; 32],
    mut email_array: [u8; 64],
    mut location_array: [u8; 64],
    mut info_array: [u8; 256],
) -> () {
    if !(customer.key() == user.borrow().owner) {
        panic!("you are not allowed to update this account");
    }

    assign!(user.borrow_mut().phone_array, Mutable::<[u8; 10]>::new(phone_array));

    assign!(user.borrow_mut().name_array, Mutable::<[u8; 32]>::new(name_array));

    assign!(user.borrow_mut().email_array, Mutable::<[u8; 64]>::new(email_array));

    assign!(user.borrow_mut().location_array, Mutable::<[u8; 64]>::new(location_array));

    assign!(user.borrow_mut().info_array, Mutable::<[u8; 256]>::new(info_array));
}

pub fn update_gymclass_handler<'info>(
    mut trainer: SeahorseSigner<'info, '_>,
    mut gymclass: Mutable<LoadedGymClass<'info, '_>>,
    mut name_array: [u8; 32],
    mut info_array: [u8; 256],
    mut price: u64,
) -> () {
    if !(trainer.key() == gymclass.borrow().trainer) {
        panic!("gymclass trainer not");
    }

    assign!(gymclass.borrow_mut().name_array, Mutable::<[u8; 32]>::new(name_array));

    assign!(gymclass.borrow_mut().info_array, Mutable::<[u8; 256]>::new(info_array));

    assign!(gymclass.borrow_mut().price, price);
}

pub fn update_trainer_account_handler<'info>(
    mut trainer: SeahorseSigner<'info, '_>,
    mut user: Mutable<LoadedUser<'info, '_>>,
    mut phone_array: [u8; 10],
    mut name_array: [u8; 32],
    mut email_array: [u8; 64],
    mut location_array: [u8; 64],
    mut info_array: [u8; 256],
) -> () {
    if !((user.borrow().flag == 5) || (user.borrow().flag == 6)) {
        panic!("This is not a trainer account");
    }

    if !(trainer.key() == user.borrow().owner) {
        panic!("you are not allowed to update this account");
    }

    assign!(user.borrow_mut().phone_array, Mutable::<[u8; 10]>::new(phone_array));

    assign!(user.borrow_mut().name_array, Mutable::<[u8; 32]>::new(name_array));

    assign!(user.borrow_mut().email_array, Mutable::<[u8; 64]>::new(email_array));

    assign!(user.borrow_mut().location_array, Mutable::<[u8; 64]>::new(location_array));

    assign!(user.borrow_mut().info_array, Mutable::<[u8; 256]>::new(info_array));
}
