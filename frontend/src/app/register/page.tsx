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
import { Connection } from "@solana/web3.js";

const formSchema = z.object({
    classname: z.string().min(2, {
        message: "Classname must be at least 2 characters.",
    }),
    Phone: z.string().min(1, { message: "Phone is required." }),
    Name: z.string().min(1, { message: "Name is required." }),
    Email: z.string().email({ message: "Invalid email address." }),
    Location: z.string().min(1, { message: "Location is required." }),
    Info: z.string().optional(),
    Age: z.number().min(0, { message: "Age must be a positive number." }),
    Gender: z.string().min(1, { message: "Gender is required." }),
});

export default function TrainerForm() {
    const form = useForm<z.infer<typeof formSchema>>({
        resolver: zodResolver(formSchema),
        defaultValues: {
            classname: "",
        },
    });

    async function onSubmit(values: z.infer<typeof formSchema>) {
        try {
            const response = await fetch('/init-trainer-account', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(values),
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const data = await response.json();
            console.log(data);
            // Handle success (e.g., redirect to another page or show a success message)
        } catch (error) {
            console.error('There was a problem with the fetch operation:', error);
            // Handle error (e.g., show an error message)
        }
    }

    const listOfFields = ["Phone", "Name", "Email", "Location", "Info", "Age", "Gender"]

    return (
        <Form {...form}>
            <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-8">
                {listOfFields.map((field) => (
                    <FormField
                        key={field} 
                        control={form.control}
                        name={field.toLowerCase() as keyof z.infer<typeof formSchema>} // Ensures the field name matches the schema
                        render={({ field: formField }) => (
                            <FormItem>
                                <FormLabel>{field}</FormLabel>
                                <FormControl>
                                    <Input placeholder="Input" {...formField} />
                                </FormControl>
                                <FormMessage />
                            </FormItem>
                        )}
                    />
                ))}
                <Button type="submit">Submit</Button>
            </form>
        </Form>
    );
}
