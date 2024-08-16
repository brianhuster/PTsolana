"use client";
import { getAccountRole } from "@/lib/utils";
import { useWallet } from "@solana/wallet-adapter-react";
import { useMemo, useState } from "react";
import TrainerView from "@/components/custom/TrainerView";
import { Button } from "@/components/ui/button";

export default function Page() {
    const { publicKey } = useWallet()
    const [role, setRole] = useState("loading");

    useMemo(async () => {
        let newRole = await getAccountRole(publicKey)
        await setRole(newRole);
    }, [publicKey])


    if (role === "trainer") {
        return <TrainerView />
    }
    else if (role === "loading") {
        return <div>Loading....</div>
    }
    return (
        <div>
            <div>
                You do not own a trainer account, please create your account
            </div>
            <a href="/user/create-account">
                <Button>Create Account</Button>
            </a>
        </div>
    );
}