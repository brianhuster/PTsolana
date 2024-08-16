"use client";
import { useConnection, useWallet } from "@solana/wallet-adapter-react";
import { PublicKey } from "@solana/web3.js";
import { useEffect, useState } from "react";
import { getJSON } from "@/lib/utils";

import { useMemo } from "react";
import { getAccountRole } from "@/lib/utils";

export default function Page() {
    const { publicKey } = useWallet();
    const { connection } = useConnection();
    const [role, setRole] = useState<string>("");

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