"use client";

import AdapterWallet from "@/components/custom/AdapterWallet";
import "./globals.css";
import React, { useState, useEffect } from "react";
import Navbar from "@/components/custom/Navbar";

export default function RootLayout({
    children,
}: {
    children: React.ReactNode;
}) {
    const [isMounted, setIsMounted] = useState(false);

    useEffect(() => {
        setIsMounted(true);
    }, []);

    return (
        <html lang="en" className="dark">
            <body className="w-screen h-fit dark">
                {
                    isMounted ?
                        <AdapterWallet>
                            <Navbar />
                            <div id="container" className="w-full h-fit py-5">
                                {children}
                            </div>
                        </AdapterWallet>

                        : null
                }
            </body>
        </html>
    );
}