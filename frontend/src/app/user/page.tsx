"use client";
import { useConnection, useWallet } from "@solana/wallet-adapter-react";
import { useMemo, useState } from "react";
import { getAccountRole } from "@/lib/utils";

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