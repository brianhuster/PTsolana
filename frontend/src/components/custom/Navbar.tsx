import { cn } from "@/lib/utils";
import {
    NavigationMenu,
    NavigationMenuItem,
    NavigationMenuList,
    navigationMenuTriggerStyle,
} from "@/components/ui/navigation-menu";
import { WalletMultiButton } from "@solana/wallet-adapter-react-ui";

export default function Navbar() {
    return (
        <NavigationMenu className="max-w-full w-full px-10 bg-transparent text-primary flex justify-between">
            <NavigationMenuList className="">
                <NavigationMenuItem>
                    <a
                        href="/"
                        className={cn(
                            navigationMenuTriggerStyle(),
                            " text-2xl rounded-none py-8 bg-inherit"
                        )}
                    >
                        BlockGym
                    </a>
                </NavigationMenuItem>
                <NavigationMenuItem>
                    <a
                        href="/user"
                        className={cn(
                            navigationMenuTriggerStyle(),
                            " text-2xl rounded-none py-8 bg-inherit"
                        )}
                    >
                        Account
                    </a>
                </NavigationMenuItem>
                <NavigationMenuItem>
                    <a
                        href="/view-gym-class"
                        className={cn(
                            navigationMenuTriggerStyle(),
                            " text-2xl rounded-none py-8 bg-inherit"
                        )}
                    >
                        Classes
                    </a>
                </NavigationMenuItem>
            </NavigationMenuList>
            <NavigationMenuList className="">
                <NavigationMenuItem>
                    <WalletMultiButton className="" style={
                        { backgroundColor: "white", color: "black" }
                    } />
                </NavigationMenuItem>
            </NavigationMenuList>
        </NavigationMenu >
    )
}