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

declare const window: WindowWithSolana;

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

    async function onsubmit(values: z.infer<typeof formSchema>) {
        const { solana } = window;
        if (solana?.publicKey === null) {
            alert("Please connect your wallet first.");
            return;
        }
        const res = await fetch(
            `http://localhost:8000/init-gymclass?trainerPubkey=${solana?.publicKey.toString()}`,
            {
                method: "post",
                headers: {
                    "content-type": "application/json",
                },
                body: JSON.stringify(values),
            }
        );
        const json = await res.json();
        const transaction = await json.transaction;
        const solana_resp = await solana?.signTransaction(transaction);
    }

    return (
        <Form {...form}>
            <form onSubmit={form.handleSubmit(onsubmit)} className="space-y-8">
                <FormField
                    control={form.control}
                    name="name"
                    render={({ field }) => (
                        <FormItem>
                            <FormLabel>Class name</FormLabel>
                            <FormControl>
                                <Input placeholder="shadcn" {...field} />
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
