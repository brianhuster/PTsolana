#![allow(unused_imports)]
#![allow(unused_variables)]
#![allow(unused_mut)]

pub mod dot;

use anchor_lang::prelude::*;
use anchor_spl::{
    associated_token::{self, AssociatedToken},
    token::{self, Mint, Token, TokenAccount},
};

use dot::program::*;
use std::{cell::RefCell, rc::Rc};

declare_id!("FwrxzVAS7hdsWmnGmm1isX9u24wRpNiKiKR3RTaBbSDx");

pub mod seahorse_util {
    use super::*;

    #[cfg(feature = "pyth-sdk-solana")]
    pub use pyth_sdk_solana::{load_price_feed_from_account_info, PriceFeed};
    use std::{collections::HashMap, fmt::Debug, ops::Deref};

    pub struct Mutable<T>(Rc<RefCell<T>>);

    impl<T> Mutable<T> {
        pub fn new(obj: T) -> Self {
            Self(Rc::new(RefCell::new(obj)))
        }
    }

    impl<T> Clone for Mutable<T> {
        fn clone(&self) -> Self {
            Self(self.0.clone())
        }
    }

    impl<T> Deref for Mutable<T> {
        type Target = Rc<RefCell<T>>;

        fn deref(&self) -> &Self::Target {
            &self.0
        }
    }

    impl<T: Debug> Debug for Mutable<T> {
        fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
            write!(f, "{:?}", self.0)
        }
    }

    impl<T: Default> Default for Mutable<T> {
        fn default() -> Self {
            Self::new(T::default())
        }
    }

    impl<T: Clone> Mutable<Vec<T>> {
        pub fn wrapped_index(&self, mut index: i128) -> usize {
            if index >= 0 {
                return index.try_into().unwrap();
            }

            index += self.borrow().len() as i128;

            return index.try_into().unwrap();
        }
    }

    impl<T: Clone, const N: usize> Mutable<[T; N]> {
        pub fn wrapped_index(&self, mut index: i128) -> usize {
            if index >= 0 {
                return index.try_into().unwrap();
            }

            index += self.borrow().len() as i128;

            return index.try_into().unwrap();
        }
    }

    #[derive(Clone)]
    pub struct Empty<T: Clone> {
        pub account: T,
        pub bump: Option<u8>,
    }

    #[derive(Clone, Debug)]
    pub struct ProgramsMap<'info>(pub HashMap<&'static str, AccountInfo<'info>>);

    impl<'info> ProgramsMap<'info> {
        pub fn get(&self, name: &'static str) -> AccountInfo<'info> {
            self.0.get(name).unwrap().clone()
        }
    }

    #[derive(Clone, Debug)]
    pub struct WithPrograms<'info, 'entrypoint, A> {
        pub account: &'entrypoint A,
        pub programs: &'entrypoint ProgramsMap<'info>,
    }

    impl<'info, 'entrypoint, A> Deref for WithPrograms<'info, 'entrypoint, A> {
        type Target = A;

        fn deref(&self) -> &Self::Target {
            &self.account
        }
    }

    pub type SeahorseAccount<'info, 'entrypoint, A> =
        WithPrograms<'info, 'entrypoint, Box<Account<'info, A>>>;

    pub type SeahorseSigner<'info, 'entrypoint> = WithPrograms<'info, 'entrypoint, Signer<'info>>;

    #[derive(Clone, Debug)]
    pub struct CpiAccount<'info> {
        #[doc = "CHECK: CpiAccounts temporarily store AccountInfos."]
        pub account_info: AccountInfo<'info>,
        pub is_writable: bool,
        pub is_signer: bool,
        pub seeds: Option<Vec<Vec<u8>>>,
    }

    #[macro_export]
    macro_rules! seahorse_const {
        ($ name : ident , $ value : expr) => {
            macro_rules! $name {
                () => {
                    $value
                };
            }

            pub(crate) use $name;
        };
    }

    #[macro_export]
    macro_rules! assign {
        ($ lval : expr , $ rval : expr) => {{
            let temp = $rval;

            $lval = temp;
        }};
    }

    #[macro_export]
    macro_rules! index_assign {
        ($ lval : expr , $ idx : expr , $ rval : expr) => {
            let temp_rval = $rval;
            let temp_idx = $idx;

            $lval[temp_idx] = temp_rval;
        };
    }

    pub(crate) use assign;

    pub(crate) use index_assign;

    pub(crate) use seahorse_const;
}

#[program]
mod blockchain {
    use super::*;
    use seahorse_util::*;
    use std::collections::HashMap;

    #[derive(Accounts)]
    # [instruction (review_array: [u16; 128])]
    pub struct CustomerConfirmDone<'info> {
        #[account(mut)]
        pub customer: Signer<'info>,
        #[account(mut)]
        pub trainer: Signer<'info>,
        #[account(mut)]
        pub company: Signer<'info>,
        #[account(mut)]
        pub gymclass: Box<Account<'info, dot::program::GymClass>>,
    }

    pub fn customer_confirm_done(
        ctx: Context<CustomerConfirmDone>,
        review_array: [u16; 128],
    ) -> Result<()> {
        let mut programs = HashMap::new();
        let programs_map = ProgramsMap(programs);
        let customer = SeahorseSigner {
            account: &ctx.accounts.customer,
            programs: &programs_map,
        };

        let trainer = SeahorseSigner {
            account: &ctx.accounts.trainer,
            programs: &programs_map,
        };

        let company = SeahorseSigner {
            account: &ctx.accounts.company,
            programs: &programs_map,
        };

        let gymclass = dot::program::GymClass::load(&mut ctx.accounts.gymclass, &programs_map);

        customer_confirm_done_handler(
            customer.clone(),
            trainer.clone(),
            company.clone(),
            gymclass.clone(),
            review_array,
        );

        dot::program::GymClass::store(gymclass);

        return Ok(());
    }

    #[derive(Accounts)]
    pub struct CustomerJoinGymclass<'info> {
        #[account(mut)]
        pub customer: Signer<'info>,
        #[account(mut)]
        pub gymclass: Box<Account<'info, dot::program::GymClass>>,
        pub system_program: Program<'info, System>,
    }

    pub fn customer_join_gymclass(ctx: Context<CustomerJoinGymclass>) -> Result<()> {
        let mut programs = HashMap::new();

        programs.insert(
            "system_program",
            ctx.accounts.system_program.to_account_info(),
        );

        let programs_map = ProgramsMap(programs);
        let customer = SeahorseSigner {
            account: &ctx.accounts.customer,
            programs: &programs_map,
        };

        let gymclass = dot::program::GymClass::load(&mut ctx.accounts.gymclass, &programs_map);

        customer_join_gymclass_handler(customer.clone(), gymclass.clone());

        dot::program::GymClass::store(gymclass);

        return Ok(());
    }

    #[derive(Accounts)]
    pub struct HideTrainerAccount<'info> {
        #[account(mut)]
        pub trainer: Signer<'info>,
        #[account(mut)]
        pub trainer_account: Box<Account<'info, dot::program::Trainer>>,
    }

    pub fn hide_trainer_account(ctx: Context<HideTrainerAccount>) -> Result<()> {
        let mut programs = HashMap::new();
        let programs_map = ProgramsMap(programs);
        let trainer = SeahorseSigner {
            account: &ctx.accounts.trainer,
            programs: &programs_map,
        };

        let trainer_account =
            dot::program::Trainer::load(&mut ctx.accounts.trainer_account, &programs_map);

        hide_trainer_account_handler(trainer.clone(), trainer_account.clone());

        dot::program::Trainer::store(trainer_account);

        return Ok(());
    }

    #[derive(Accounts)]
    # [instruction (seed_random : u64 , name_array: [u16; 32] , location_array: [u16; 64] , info_array: [u16; 256] , phone_array: [u8; 10] , gender : u8)]
    pub struct InitCustomerAccount<'info> {
        #[account(mut)]
        pub customer: Signer<'info>,
        # [account (init , space = std :: mem :: size_of :: < dot :: program :: Customer > () + 8 , payer = customer , seeds = [customer . key () . as_ref () , "customer" . as_bytes () . as_ref () , seed_random . to_le_bytes () . as_ref ()] , bump)]
        pub customer_account: Box<Account<'info, dot::program::Customer>>,
        pub rent: Sysvar<'info, Rent>,
        pub system_program: Program<'info, System>,
    }

    pub fn init_customer_account(
        ctx: Context<InitCustomerAccount>,
        seed_random: u64,
        name_array: [u16; 32],
        location_array: [u16; 64],
        info_array: [u16; 256],
        phone_array: [u8; 10],
        gender: u8,
    ) -> Result<()> {
        let mut programs = HashMap::new();

        programs.insert(
            "system_program",
            ctx.accounts.system_program.to_account_info(),
        );

        let programs_map = ProgramsMap(programs);
        let customer = SeahorseSigner {
            account: &ctx.accounts.customer,
            programs: &programs_map,
        };

        let customer_account = Empty {
            account: dot::program::Customer::load(
                &mut ctx.accounts.customer_account,
                &programs_map,
            ),
            bump: Some(ctx.bumps.customer_account),
        };

        init_customer_account_handler(
            customer.clone(),
            customer_account.clone(),
            seed_random,
            name_array,
            location_array,
            info_array,
            phone_array,
            gender,
        );

        dot::program::Customer::store(customer_account.account);

        return Ok(());
    }

    #[derive(Accounts)]
    # [instruction (seed_sha256 : u64 , price : u64 , name_array: [u16; 32] , info_array: [u16; 256])]
    pub struct InitGymclass<'info> {
        #[account(mut)]
        pub trainer: Signer<'info>,
        #[account(mut)]
        pub company: Signer<'info>,
        # [account (init , space = std :: mem :: size_of :: < dot :: program :: GymClass > () + 8 , payer = company , seeds = [company . key () . as_ref () , "gymclass" . as_bytes () . as_ref () , seed_sha256 . to_le_bytes () . as_ref ()] , bump)]
        pub gymclass: Box<Account<'info, dot::program::GymClass>>,
        pub rent: Sysvar<'info, Rent>,
        pub system_program: Program<'info, System>,
    }

    pub fn init_gymclass(
        ctx: Context<InitGymclass>,
        seed_sha256: u64,
        price: u64,
        name_array: [u16; 32],
        info_array: [u16; 256],
    ) -> Result<()> {
        let mut programs = HashMap::new();

        programs.insert(
            "system_program",
            ctx.accounts.system_program.to_account_info(),
        );

        let programs_map = ProgramsMap(programs);
        let trainer = SeahorseSigner {
            account: &ctx.accounts.trainer,
            programs: &programs_map,
        };

        let company = SeahorseSigner {
            account: &ctx.accounts.company,
            programs: &programs_map,
        };

        let gymclass = Empty {
            account: dot::program::GymClass::load(&mut ctx.accounts.gymclass, &programs_map),
            bump: Some(ctx.bumps.gymclass),
        };

        init_gymclass_handler(
            trainer.clone(),
            company.clone(),
            gymclass.clone(),
            seed_sha256,
            price,
            name_array,
            info_array,
        );

        dot::program::GymClass::store(gymclass.account);

        return Ok(());
    }

    #[derive(Accounts)]
    # [instruction (seed_random : u64 , name_array: [u16; 32] , location_array: [u16; 64] , info_array: [u16; 256] , phone_array: [u8; 10] , age : u8 , gender : u8)]
    pub struct InitTrainerAccount<'info> {
        #[account(mut)]
        pub trainer: Signer<'info>,
        # [account (init , space = std :: mem :: size_of :: < dot :: program :: Trainer > () + 8 , payer = trainer , seeds = [trainer . key () . as_ref () , "trainer" . as_bytes () . as_ref () , seed_random . to_le_bytes () . as_ref ()] , bump)]
        pub trainer_account: Box<Account<'info, dot::program::Trainer>>,
        pub rent: Sysvar<'info, Rent>,
        pub system_program: Program<'info, System>,
    }

    pub fn init_trainer_account(
        ctx: Context<InitTrainerAccount>,
        seed_random: u64,
        name_array: [u16; 32],
        location_array: [u16; 64],
        info_array: [u16; 256],
        phone_array: [u8; 10],
        age: u8,
        gender: u8,
    ) -> Result<()> {
        let mut programs = HashMap::new();

        programs.insert(
            "system_program",
            ctx.accounts.system_program.to_account_info(),
        );

        let programs_map = ProgramsMap(programs);
        let trainer = SeahorseSigner {
            account: &ctx.accounts.trainer,
            programs: &programs_map,
        };

        let trainer_account = Empty {
            account: dot::program::Trainer::load(&mut ctx.accounts.trainer_account, &programs_map),
            bump: Some(ctx.bumps.trainer_account),
        };

        init_trainer_account_handler(
            trainer.clone(),
            trainer_account.clone(),
            seed_random,
            name_array,
            location_array,
            info_array,
            phone_array,
            age,
            gender,
        );

        dot::program::Trainer::store(trainer_account.account);

        return Ok(());
    }

    #[derive(Accounts)]
    pub struct PtConfirmDone<'info> {
        #[account(mut)]
        pub trainer: Signer<'info>,
        #[account(mut)]
        pub gymclass: Box<Account<'info, dot::program::GymClass>>,
    }

    pub fn pt_confirm_done(ctx: Context<PtConfirmDone>) -> Result<()> {
        let mut programs = HashMap::new();
        let programs_map = ProgramsMap(programs);
        let trainer = SeahorseSigner {
            account: &ctx.accounts.trainer,
            programs: &programs_map,
        };

        let gymclass = dot::program::GymClass::load(&mut ctx.accounts.gymclass, &programs_map);

        pt_confirm_done_handler(trainer.clone(), gymclass.clone());

        dot::program::GymClass::store(gymclass);

        return Ok(());
    }

    #[derive(Accounts)]
    pub struct PtDeclineCustomer<'info> {
        #[account(mut)]
        pub trainer: Signer<'info>,
        #[account(mut)]
        pub customer: Signer<'info>,
        #[account(mut)]
        pub gymclass: Box<Account<'info, dot::program::GymClass>>,
    }

    pub fn pt_decline_customer(ctx: Context<PtDeclineCustomer>) -> Result<()> {
        let mut programs = HashMap::new();
        let programs_map = ProgramsMap(programs);
        let trainer = SeahorseSigner {
            account: &ctx.accounts.trainer,
            programs: &programs_map,
        };

        let customer = SeahorseSigner {
            account: &ctx.accounts.customer,
            programs: &programs_map,
        };

        let gymclass = dot::program::GymClass::load(&mut ctx.accounts.gymclass, &programs_map);

        pt_decline_customer_handler(trainer.clone(), customer.clone(), gymclass.clone());

        dot::program::GymClass::store(gymclass);

        return Ok(());
    }

    #[derive(Accounts)]
    pub struct TrainerHideGymclass<'info> {
        #[account(mut)]
        pub trainer: Signer<'info>,
        #[account(mut)]
        pub gymclass: Box<Account<'info, dot::program::GymClass>>,
    }

    pub fn trainer_hide_gymclass(ctx: Context<TrainerHideGymclass>) -> Result<()> {
        let mut programs = HashMap::new();
        let programs_map = ProgramsMap(programs);
        let trainer = SeahorseSigner {
            account: &ctx.accounts.trainer,
            programs: &programs_map,
        };

        let gymclass = dot::program::GymClass::load(&mut ctx.accounts.gymclass, &programs_map);

        trainer_hide_gymclass_handler(trainer.clone(), gymclass.clone());

        dot::program::GymClass::store(gymclass);

        return Ok(());
    }

    #[derive(Accounts)]
    # [instruction (name_array: [u16; 32] , location_array: [u16; 64] , info_array: [u16; 256] , phone_array: [u8; 10])]
    pub struct UpdateCustomerAccount<'info> {
        #[account(mut)]
        pub customer: Signer<'info>,
        #[account(mut)]
        pub customer_account: Box<Account<'info, dot::program::Customer>>,
    }

    pub fn update_customer_account(
        ctx: Context<UpdateCustomerAccount>,
        name_array: [u16; 32],
        location_array: [u16; 64],
        info_array: [u16; 256],
        phone_array: [u8; 10],
    ) -> Result<()> {
        let mut programs = HashMap::new();
        let programs_map = ProgramsMap(programs);
        let customer = SeahorseSigner {
            account: &ctx.accounts.customer,
            programs: &programs_map,
        };

        let customer_account =
            dot::program::Customer::load(&mut ctx.accounts.customer_account, &programs_map);

        update_customer_account_handler(
            customer.clone(),
            customer_account.clone(),
            name_array,
            location_array,
            info_array,
            phone_array,
        );

        dot::program::Customer::store(customer_account);

        return Ok(());
    }

    #[derive(Accounts)]
    # [instruction (price : u64 , name_array: [u16; 32] , info_array: [u16; 256] , flag : u8)]
    pub struct UpdateGymclass<'info> {
        #[account(mut)]
        pub trainer: Signer<'info>,
        #[account(mut)]
        pub gymclass: Box<Account<'info, dot::program::GymClass>>,
    }

    pub fn update_gymclass(
        ctx: Context<UpdateGymclass>,
        price: u64,
        name_array: [u16; 32],
        info_array: [u16; 256],
        flag: u8,
    ) -> Result<()> {
        let mut programs = HashMap::new();
        let programs_map = ProgramsMap(programs);
        let trainer = SeahorseSigner {
            account: &ctx.accounts.trainer,
            programs: &programs_map,
        };

        let gymclass = dot::program::GymClass::load(&mut ctx.accounts.gymclass, &programs_map);

        update_gymclass_handler(
            trainer.clone(),
            gymclass.clone(),
            price,
            name_array,
            info_array,
            flag,
        );

        dot::program::GymClass::store(gymclass);

        return Ok(());
    }

    #[derive(Accounts)]
    # [instruction (name_array: [u16; 32] , location_array: [u16; 64] , info_array: [u16; 256] , phone_array: [u8; 10])]
    pub struct UpdateTrainerAccount<'info> {
        #[account(mut)]
        pub trainer: Signer<'info>,
        #[account(mut)]
        pub trainer_account: Box<Account<'info, dot::program::Trainer>>,
    }

    pub fn update_trainer_account(
        ctx: Context<UpdateTrainerAccount>,
        name_array: [u16; 32],
        location_array: [u16; 64],
        info_array: [u16; 256],
        phone_array: [u8; 10],
    ) -> Result<()> {
        let mut programs = HashMap::new();
        let programs_map = ProgramsMap(programs);
        let trainer = SeahorseSigner {
            account: &ctx.accounts.trainer,
            programs: &programs_map,
        };

        let trainer_account =
            dot::program::Trainer::load(&mut ctx.accounts.trainer_account, &programs_map);

        update_trainer_account_handler(
            trainer.clone(),
            trainer_account.clone(),
            name_array,
            location_array,
            info_array,
            phone_array,
        );

        dot::program::Trainer::store(trainer_account);

        return Ok(());
    }
}