import {
    Connection,
    Transaction,
    TransactionInstruction,
    PublicKey,
    Keypair,
} from "@solana/web3.js";
import bs58 from "bs58";

import { encode, generateRandomSeed, convertNameToHash8Bytes } from "./utils";
import { MY_PROGRAM_ID, SystemProgram } from "@/config";

export default async function initGymclass(
    connection: Connection,
    customerPublicKey: PublicKey,
    gymClassAddress: PublicKey
) {
    const programId = new PublicKey(MY_PROGRAM_ID);

    const instruction = new TransactionInstruction({
        keys: [
            { pubkey: customerPublicKey, isSigner: true, isWritable: true },
            { pubkey: gymClassAddress, isSigner: false, isWritable: true },
            {
                pubkey: new PublicKey(SystemProgram),
                isSigner: false,
                isWritable: false,
            },
        ],
        programId,
        data: convertNameToHash8Bytes("customer_join_gymclass"),
    });

    const transaction = new Transaction().add(instruction);
    transaction.feePayer = customerPublicKey;

    try {
        transaction.recentBlockhash = (
            await connection.getLatestBlockhash()
        ).blockhash;
    } catch (error) {
        console.error("Cannot get blockhash", error);
    }

    return transaction;
}
