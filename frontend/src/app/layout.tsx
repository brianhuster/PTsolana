"use client";

import "./globals.css";
import { Navbar } from "../components/custom/navbar";
import React from "react";
import AppWalletProvider from "@/components/custom/AppWalletProvider";

require("@solana/wallet-adapter-react-ui/styles.css");

export default function RootLayout({
    children,
}: Readonly<{
    children: React.ReactNode;
}>) {

    return (
        <html lang="en" className="dark">
            <body className="w-screen h-fit">
                <AppWalletProvider>
                    <Navbar />
                    <div id="container" className="w-full h-fit">
                        {children}
                    </div>
                </AppWalletProvider>
            </body>
        </html>
    );
}
