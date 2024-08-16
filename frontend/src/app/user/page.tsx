"use client";
import { useConnection, useWallet } from "@solana/wallet-adapter-react";
import { PublicKey } from "@solana/web3.js";
import { useEffect, useMemo, useState } from "react";

async function getAccountRole(publicKey: PublicKey | null): Promise<string> {
    const resp = await fetch("http://localhost:8000/get-account-data?public_key=" + publicKey?.toString());
    const json = await resp.json();
    const data = json.data;
    if (data === "Not found") {
        return "no account";
    } else {
        return data.role ?? "no account";
    }
}
export default function Page() {
    const [role, setRole] = useState("no account");
    const { publicKey } = useWallet();
    const { connection } = useConnection();


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