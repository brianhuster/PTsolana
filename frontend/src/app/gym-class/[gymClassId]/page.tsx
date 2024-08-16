"use client";
import { GymData } from "@/lib/models";
import { useEffect, useState } from "react";
import { getJSON } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import customerJoinClass from "@/lib/blockchain/customerJoinClass";
import { useConnection, useWallet } from "@solana/wallet-adapter-react";
import { PublicKey } from "@solana/web3.js";
import { sendAndConfirmRawTransaction } from "@solana/web3.js";

export default function Page({ params }: { params: { gymClassId: string } }) {
    const [gymClass, setGymClass] = useState<GymData>();
    useEffect(() => {
        const fetchData = async () => {
            const json = await getJSON(`http://localhost:8000/get-gym-class-data?public_key=${params.gymClassId}`);
            setGymClass(json.data);
        };
        fetchData();
    }, [params.gymClassId]);

    const { connection } = useConnection();
    const { publicKey, signTransaction } = useWallet();

    return (
        <div className="py-20 flex flex-col bg-slate-500 items-center px-10">
            <div className="border border-slate-500 border-b-white border-t-white w-full h-[200px] flex flex-col items-center">
                <div className="h-full bg-slate-500 w-[200px] flex justify-center -translate-y-14">
                    <img
                        src="https://picsum.photos/200/300"
                        alt="placeholder"
                        className="h-full w-9/12 object-cover"
                    />
                </div>
                <div className="-translate-y-5 bg-slate-500 px-4 flex flex-col items-center">
                    <div className="text-4xl">{gymClass?.name}</div>
                    <div className="text-xl"> {gymClass?.location}</div>
                </div>
                <h1>About</h1>
                <div>{gymClass?.info}</div>
            </div>
            <div className="fixed bottom-10">
                <Button onClick={
                    async () => {
                        if (publicKey && signTransaction) {
                            try {
                                const transaction = await customerJoinClass(
                                    connection,
                                    publicKey,
                                    new PublicKey(params.gymClassId)
                                );
                                const signedTransaction = await signTransaction(transaction);
                                const signature = await sendAndConfirmRawTransaction(connection, signedTransaction.serialize());

                                console.log("Transaction signature:", signature);
                            } catch (error) {
                                console.error("Transaction failed", error);
                            }
                        }
                    }
                }>Join this class</Button>
            </div>
        </div>
    );
}
