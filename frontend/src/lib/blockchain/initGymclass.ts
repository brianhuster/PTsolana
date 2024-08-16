import {
    Connection,
    Transaction,
    TransactionInstruction,
    PublicKey,
    Keypair,
} from "@solana/web3.js";
import bs58 from "bs58";

import {
    encode,
    generateRandomSeed,
    bigintToBytes,
    convertNameToHash8Bytes,
} from "./utils";
import {
    COMPANY_PRIVATE_KEY,
    MY_PROGRAM_ID,
    SystemProgram,
    SystemRent,
} from "@/config";

export default async function initGymclass(
    connection: Connection,
    companyPublicKey: PublicKey,
    trainerPublicKey: PublicKey,
    name: string,
    info: string,
    price: number
) {
    const programId = new PublicKey(MY_PROGRAM_ID);
    const companyKeypair = Keypair.fromSecretKey(
        Uint8Array.from(bs58.decode(COMPANY_PRIVATE_KEY))
    );
    // Constants and assumptions
    const SEED_PREFIX = "gymclass";

    // Ensure that name and info fit into the required byte arrays
    const nameBytes = encode(name);
    const infoBytes = encode(info);

    if (nameBytes.length > 32 || infoBytes.length > 256) {
        throw new Error("Name or info exceeds maximum length.");
    }

    const nameArray = new Uint8Array(32);
    nameArray.set(nameBytes);

    const infoArray = new Uint8Array(256);
    infoArray.set(infoBytes);

    // Generate the seed_sha256 value
    const seedSha256 = generateRandomSeed();

    const [gymClassAddress] = await PublicKey.findProgramAddressSync(
        [companyPublicKey.toBuffer(), Buffer.from(SEED_PREFIX), seedSha256],
        programId
    );
    console.log(`seed ${seedSha256}`);
    console.log(`gym class address: ${gymClassAddress}`);

    // Create the instruction
    const instruction = new TransactionInstruction({
        keys: [
            { pubkey: companyPublicKey, isSigner: true, isWritable: true },
            { pubkey: trainerPublicKey, isSigner: true, isWritable: true },
            { pubkey: gymClassAddress, isSigner: false, isWritable: true },
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
            convertNameToHash8Bytes("init_gymclass"),
            nameArray,
            infoArray,
            Buffer.from(
                new Uint8Array(new BigUint64Array([BigInt(price)]).buffer)
            ),
            seedSha256,
        ]),
    });

    // Send the transaction
    const transaction = new Transaction().add(instruction);
    transaction.feePayer = companyKeypair.publicKey;
    try {
        transaction.recentBlockhash = (
            await connection.getLatestBlockhash()
        ).blockhash;
    } catch (error) {
        console.error("Cannot get blockhash", error);
    }
    transaction.sign(companyKeypair);

    return transaction;
}
