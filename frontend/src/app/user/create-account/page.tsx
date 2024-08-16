"use client";
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
import { Button } from "@/components/ui/button";
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form"
import initUserAccount from "@/lib/blockchain/initUserAccount";
import { useConnection, useWallet } from "@solana/wallet-adapter-react";
import { sendAndConfirmRawTransaction } from "@solana/web3.js";

const formSchema = z.object({
    phone: z.string().min(10, {
        message: "Phone number must be at least 10 digits.",
    }).max(10, {
        message: "Phone number must be at most 10 digits.",
    }),
    name: z.string().min(2, {
        message: "Name must be at least 2 characters.",
    }).max(32, {
        message: "Name must be at most 32 characters.",
    }),
    email: z.string().email({
        message: "Please enter a valid email address.",
    }).max(64, { message: "Email must be at most 64 characters." }),
    location: z.string().min(2, {
        message: "Location must be at least 2 characters.",
    }).max(64, {
        message: "Location must be at most 64 characters.",
    }),
    info: z.string().min(5, {
        message: "Info must be at least 5 characters.",
    }).max(256, {
        message: "Info must be at most 256 characters.",
    }),
    age: z.string().refine((val) => !isNaN(parseInt(val)), {
        message: "Age must be a number.",
    }),
    gender: z.enum(["male", "female", "other"], {
        errorMap: () => ({ message: "Please select a gender." }),
    }),
    role: z.enum(["trainer", "customer"], {
        errorMap: () => ({ message: "Please select a role." }),
    }),
});

export default function CreateAccount() {
    const form = useForm<z.infer<typeof formSchema>>({
        resolver: zodResolver(formSchema),
        defaultValues: {
            phone: "",
            name: "",
            email: "",
            location: "",
            info: "",
            age: '0',
        }
    });

    const { connection } = useConnection();
    const { publicKey, signTransaction } = useWallet();

    async function onSubmit(values: z.infer<typeof formSchema>) {
        if (!publicKey || !signTransaction) {
            console.error("Wallet not connected");
            return;
        }
        try {
            const transaction = await initUserAccount(
                connection,
                publicKey,
                values.phone,
                values.name,
                values.info,
                values.email,
                values.location,
                parseInt(values.age),
                values.gender,
                values.role
            )

            const signedTransaction = await signTransaction(transaction);
            const signature = await sendAndConfirmRawTransaction(connection, signedTransaction.serialize());

            console.log("Transaction signature:", signature);
        } catch (error) {
            console.error("Transaction failed", error);
        }
    }
    return (
        <Form {...form}>
            <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-8">
                <FormField
                    control={form.control}
                    name="phone"
                    render={({ field }) => (
                        <FormItem>
                            <FormLabel>Phone</FormLabel>
                            <FormControl>
                                <Input placeholder="1111111111" {...field} />
                            </FormControl>
                            <FormDescription>
                                Please enter your phone number.
                            </FormDescription>
                            <FormMessage />
                        </FormItem>
                    )}
                />

                <FormField
                    control={form.control}
                    name="name"
                    render={({ field }) => (
                        <FormItem>
                            <FormLabel>Name</FormLabel>
                            <FormControl>
                                <Input placeholder="Changed 2" {...field} />
                            </FormControl>
                            <FormDescription>
                                Please enter your full name.
                            </FormDescription>
                            <FormMessage />
                        </FormItem>
                    )}
                />

                <FormField
                    control={form.control}
                    name="email"
                    render={({ field }) => (
                        <FormItem>
                            <FormLabel>Email</FormLabel>
                            <FormControl>
                                <Input placeholder="2Trainer@gmail.com" {...field} />
                            </FormControl>
                            <FormDescription>
                                Please enter your email address.
                            </FormDescription>
                            <FormMessage />
                        </FormItem>
                    )}
                />

                <FormField
                    control={form.control}
                    name="location"
                    render={({ field }) => (
                        <FormItem>
                            <FormLabel>Location</FormLabel>
                            <FormControl>
                                <Input placeholder="Hanoi, Vietnam" {...field} />
                            </FormControl>
                            <FormDescription>
                                Please enter your location.
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
                                <Input placeholder="I have 1000 years of experience" {...field} />
                            </FormControl>
                            <FormDescription>
                                Please provide some information about your experience.
                            </FormDescription>
                            <FormMessage />
                        </FormItem>
                    )}
                />

                <FormField
                    control={form.control}
                    name="age"
                    render={({ field }) => (
                        <FormItem>
                            <FormLabel>Age</FormLabel>
                            <FormControl>
                                <Input placeholder="22" type="number" {...field} />
                            </FormControl>
                            <FormDescription>
                                Please enter your age.
                            </FormDescription>
                            <FormMessage />
                        </FormItem>
                    )}
                />

                <FormField
                    control={form.control}
                    name="gender"
                    render={({ field }) => (
                        <FormItem>
                            <FormLabel>Gender</FormLabel>
                            <FormControl>
                                <RadioGroup
                                    onValueChange={field.onChange}
                                    defaultValue={field.value}
                                    className="flex justify-evenly"
                                >
                                    <div>
                                        <RadioGroupItem value="male" id="male" />
                                        <FormLabel htmlFor="male" className="ml-2">Male</FormLabel>
                                    </div>
                                    <div>
                                        <RadioGroupItem value="female" id="female" />
                                        <FormLabel htmlFor="female" className="ml-2">Female</FormLabel>
                                    </div>
                                    <div>
                                        <RadioGroupItem value="other" id="other" />
                                        <FormLabel htmlFor="other" className="ml-2">Other</FormLabel>
                                    </div>
                                </RadioGroup>
                            </FormControl>
                            <FormDescription>
                                Please select your gender.
                            </FormDescription>
                            <FormMessage />
                        </FormItem>
                    )}
                />

                <FormField
                    control={form.control}
                    name="role"
                    render={({ field }) => (
                        <FormItem>
                            <FormLabel>Role</FormLabel>
                            <FormControl>
                                <RadioGroup
                                    onValueChange={field.onChange}
                                    defaultValue={field.value}
                                    className="flex justify-evenly"
                                >
                                    <div>

                                        <RadioGroupItem value="trainer" id="trainer" />
                                        <FormLabel htmlFor="trainer" className="ml-2">Trainer</FormLabel>
                                    </div>
                                    <div>
                                        <RadioGroupItem value="customer" id="customer" />
                                        <FormLabel htmlFor="customer" className="ml-2">Customer</FormLabel>
                                    </div>
                                </RadioGroup>
                            </FormControl>
                            <FormDescription>
                                Please select your role.
                            </FormDescription>
                            <FormMessage />
                        </FormItem>
                    )}
                />

                <Button type="submit">Add class</Button>
            </form>
        </Form >
    );
}