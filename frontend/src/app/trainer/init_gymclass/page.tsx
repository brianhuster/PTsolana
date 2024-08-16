"use client";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { z } from "zod";

import { Button } from "@/components/ui/button";
import {
    Form,
    FormControl,
    FormDescription,
    FormField,
    FormItem,
    FormLabel,
    FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { useConnection, useWallet } from "@solana/wallet-adapter-react";
import { PublicKey, sendAndConfirmRawTransaction } from "@solana/web3.js";
import initGymclass from "@/lib/blockchain/initGymclass";
import { COMPANY_PUBLIC_KEY } from "@/config";

const formSchema = z.object({
    name: z.string().min(2, {
        message: "Name must be at least 2 characters.",
    }),
    info: z.string().min(5, {
        message: "Info must be at least 5 characters.",
    }),
    price: z
        .string()
        .min(1, {
            message: "Price is required.",
        })
        .transform((val) => parseInt(val))
        .refine((val) => !isNaN(val) && val >= 0, {
            message: "Price must be a valid number and at least 0.",
        }),
});

export default function TrainerForm() {
    const form = useForm<z.infer<typeof formSchema>>({
        resolver: zodResolver(formSchema),
        defaultValues: {
            name: "",
            info: "",
            price: 0,
        },
    });
    const { connection } = useConnection();
    const { publicKey, signTransaction } = useWallet();

    async function onSubmit(values: z.infer<typeof formSchema>) {
        if (!publicKey || !signTransaction) {
            console.error("Wallet not connected");
            return;
        }

        const trainerPublicKey = publicKey; // Assuming the trainer is the currently connected wallet
        const companyPublicKey = new PublicKey(COMPANY_PUBLIC_KEY)

        const name = values.name;
        const info = values.info;
        const price = values.price; // 1 SOL, in lamports (1 SOL = 1,000,000,000 lamports)

        try {
            const transaction = await initGymclass(
                connection,
                companyPublicKey,
                trainerPublicKey,
                name,
                info,
                price
            );

            const signedTransaction = await signTransaction(transaction);
            const signature = await sendAndConfirmRawTransaction(connection, signedTransaction.serialize());

            console.log("Transaction signature:", signature);
            alert("Transaction successful");
        } catch (error) {
            console.error("Transaction failed", error);
        }
    }

    return (
        <Form {...form}>
            <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-8">
                <FormField
                    control={form.control}
                    name="name"
                    render={({ field }) => (
                        <FormItem>
                            <FormLabel>Class name</FormLabel>
                            <FormControl>
                                <Input placeholder="class name" {...field} />
                            </FormControl>
                            <FormDescription>
                                This is your gym class name.
                            </FormDescription>
                            <FormMessage />
                        </FormItem>
                    )}
                />
                <FormField
                    control={form.control}
                    name="info"
                    render={({ field }) => (
                        <FormItem>
                            <FormLabel>Info</FormLabel>
                            <FormControl>
                                <Input placeholder="info" {...field} />
                            </FormControl>
                            <FormDescription>
                                This is your gym class info.
                            </FormDescription>
                            <FormMessage />
                        </FormItem>
                    )}
                />

                <FormField
                    control={form.control}
                    name="price"
                    render={({ field }) => (
                        <FormItem>
                            <FormLabel>Price</FormLabel>
                            <FormControl>
                                <Input
                                    placeholder="price"
                                    type="number"
                                    {...field}
                                />
                            </FormControl>
                            <FormDescription>
                                This is your gym class price.
                            </FormDescription>
                            <FormMessage />
                        </FormItem>
                    )}
                />
                <Button type="submit">Add class</Button>
            </form>
        </Form>
    );
}
