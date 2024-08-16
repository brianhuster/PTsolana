import {
    Connection,
    Transaction,
    TransactionInstruction,
    PublicKey,
    Keypair,
} from "@solana/web3.js";
import {
    COMPANY_PUBLIC_KEY,
    MY_PROGRAM_ID,
    SystemProgram,
    SystemRent,
} from "@/config";

import {
    encode,
    generateRandomSeed,
    bigintToBytes,
    convertNameToHash8Bytes,
} from "./utils";

export default async function initUserAccount(
    connection: Connection,
    userPublickey: PublicKey,
    phone: string,
    name: string,
    info: string,
    email: string,
    location: string,
    age: number,
    gender: string,
    role: string
) {
    const programId = new PublicKey(MY_PROGRAM_ID);

    let secret_key = "";
    let flag = -1;
    let indentifier = null;
    if (role === "trainer") {
        secret_key = "trainer";
        flag = 5;
        indentifier = convertNameToHash8Bytes("init_trainer_account");
    } else if (role === "customer") {
        secret_key = "customer";
        flag = 6;
        indentifier = convertNameToHash8Bytes("init_customer_account");
    }

    let genderEncoded = -1;
    if (gender === "male") {
        genderEncoded = 0;
    } else if (gender === "female") {
        genderEncoded = 1;
    } else {
        genderEncoded = 2;
    }

    // Ensure that name and info fit into the required byte arrays
    const nameBytes = encode(name);
    const infoBytes = encode(info);
    const emailBytes = encode(email);
    const locationBytes = encode(location);
    const phoneBytes = encode(phone);

    const phoneArray = new Uint8Array(10);
    phoneArray.set(phoneBytes);

    const nameArray = new Uint8Array(32);
    nameArray.set(nameBytes);

    const emailArray = new Uint8Array(64);
    emailArray.set(emailBytes);

    const locationArray = new Uint8Array(64);
    locationArray.set(locationBytes);

    const infoArray = new Uint8Array(256);
    infoArray.set(infoBytes);

    const seedSha256 = generateRandomSeed();

    const [userAccountAddress] = await PublicKey.findProgramAddressSync(
        [userPublickey.toBuffer(), Buffer.from(secret_key), seedSha256],
        programId
    );
    console.log(`seed ${seedSha256}`);
    console.log(`user address: ${userAccountAddress}`);
    console.log(`flag: ${flag}`);

    const instruction = new TransactionInstruction({
        keys: [
            { pubkey: userPublickey, isSigner: true, isWritable: true },
            { pubkey: userAccountAddress, isSigner: false, isWritable: true },
            {
                pubkey: new PublicKey(SystemRent),
                isSigner: false,
                isWritable: false,
            },
            {
                pubkey: new PublicKey(SystemProgram),
                isSigner: false,
                isWritable: false,
            },
        ],
        programId,
        data: Buffer.concat([
            indentifier ?? Buffer.from([0]),
            phoneArray,
            nameArray,
            emailArray,
            locationArray,
            infoArray,
            Buffer.from(new Uint8Array([age]).buffer),
            Buffer.from(new Uint8Array([genderEncoded]).buffer),
            seedSha256,
        ]),
    });

    const transaction = new Transaction().add(instruction);
    transaction.feePayer = userPublickey;
    try {
        transaction.recentBlockhash = (
            await connection.getLatestBlockhash()
        ).blockhash;
    } catch (error) {
        console.error("Cannot get blockhash", error);
    }

    return transaction;
}
