"use client";

import * as React from "react";
import Link from "next/link";

import { cn } from "@/lib/utils";
import {
    NavigationMenu,
    NavigationMenuItem,
    NavigationMenuLink,
    NavigationMenuList,
    navigationMenuTriggerStyle,
} from "@/components/ui/navigation-menu";
import { WalletMultiButton } from "@solana/wallet-adapter-react-ui";

export function Navbar() {
    return (
        <NavigationMenu className="px-10 bg-transparent">
            <NavigationMenuList>
                <div className="w-screen px-20 py-5 flex justify-between">

                    <NavigationMenuItem>
                        <Link href="/" legacyBehavior passHref>
                            <NavigationMenuLink
                                className={cn(
                                    navigationMenuTriggerStyle(),
                                    " text-2xl rounded-none py-8 bg-inherit"
                                )}
                            >
                                Home
                            </NavigationMenuLink>
                        </Link>
                    </NavigationMenuItem>
                    <NavigationMenuItem>
                        <WalletMultiButton style={{
                            backgroundColor: "white",
                            color: "black"
                        }} />
                    </NavigationMenuItem>
                </div>
            </NavigationMenuList>
        </NavigationMenu>
    );
}
