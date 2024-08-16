"use client";
import { useEffect, useState } from "react";

declare const window: WindowWithSolana;

export default function ConnectWallet() {
    const [walletAddress, setWalletAddress] = useState<string | null>(null);

    // Check if Phantom is installed
    const checkIfWalletIsConnected = async () => {
        try {
            const { solana } = window;
            if (solana && solana.isPhantom) {
                console.log("Phantom wallet found!");

                // Automatically connect if already authorized
                const response = await solana.connect({ onlyIfTrusted: true });
                setWalletAddress(response.publicKey.toString());
                console.log(
                    "Connected with Public Key:",
                    response.publicKey.toString()
                );
            } else {
                alert("Solana object not found! Get a Phantom Wallet 👻");
            }
        } catch (error) {
            console.error(error);
        }
    };

    const connectWallet = async () => {
        try {
            const { solana } = window;
            if (solana) {
                const response = await solana.connect();
                setWalletAddress(response.publicKey.toString());
                console.log(
                    "Connected with Public Key:",
                    response.publicKey.toString()
                );
            }
        } catch (error) {
            console.error(error);
        }
    };

    const renderNotConnectedContainer = () => (
        <button onClick={connectWallet}>Connect to Phantom Wallet</button>
    );

    useEffect(() => {
        const onLoad = async () => {
            await checkIfWalletIsConnected();
        };
        window.addEventListener("load", onLoad);
        return () => window.removeEventListener("load", onLoad);
    }, []);

    return (
        <div>
            {!walletAddress && renderNotConnectedContainer()}
            {walletAddress && <p>Connected: {walletAddress}</p>}
        </div>
    );
}
