"use client";

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
import GymClassItem from "@/components/custom/gym-class-item";
import { GymClass, GymData } from "@/lib/models";
import { useEffect, useState } from "react";
import { getJSON } from "@/lib/utils";

declare const window: WindowWithSolana;

export default function trainer() {
    const [gymClasses, setGymClasses] = useState<GymData[]>([]);

    return (
        <div><a href="/trainer/init_gymclass">
            <Button className="px-10 py-10 text-3xl">
                Add class
            </Button>
        </a></div>
    );
}


