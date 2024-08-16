import { type ClassValue, clsx } from "clsx"
import { twMerge } from "tailwind-merge"
import { useConnection, useWallet } from "@solana/wallet-adapter-react";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export async function getJSON(link: string){
    try {
        const response = await fetch(link);
        if (response.status !== 200) {
            console.log(response);
        } else {
            const x = await response.json();
            return x;
        }
    }
    catch (error) {
        throw new Error("Cannot connect to " + link);
    }
}   

export async function isATrainer() {
    const { publicKey } = useWallet();
    if (!publicKey) {
        alert("Please connect your wallet first.");
        return;
    }
    const json = await getJSON("http://localhost:8000/get-trainer-account-data")
    if (json.message === "ok") {
        return true;
    }
    return false;
}