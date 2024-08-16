"use client";
import { useConnection, useWallet } from "@solana/wallet-adapter-react";
import { PublicKey } from "@solana/web3.js";
import { useEffect, useMemo, useState } from "react";
import { getJSON } from "@/lib/utils";

async function getAccountRole(publicKey: PublicKey | null): Promise<string> {
    const json = await getJSON(`http://localhost:8000/get-account-data?public_key=${publicKey?.toString}`);
    const data = json.data;
    if (data === "Not found") {
        return "no account";
    } else {
        return data.role ?? "no account";
    }
}
export default async function Page() {
    const { publicKey } = useWallet();
    const { connection } = useConnection();
    const role = await getAccountRole(publicKey);


    useMemo(() => {
        getAccountRole(publicKey).then((role) => {
            if (role === "no account") {
                window.location.href = "/user/create-account";
            }
        })
    }, [publicKey]);

    return (
        <div>{role}</div>
    );
}