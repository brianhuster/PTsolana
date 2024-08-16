<<<<<<< HEAD
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

async function getClassesByTrainer(publicKey: string) {
    const gymClasses = await getJSON("http://localhost:8000/get-all-gym-classes-data")
    if (!gymClasses){
        return [];
    }
    const result = gymClasses.data.filter((gymClass: any) => gymClass.trainer === publicKey);
    return result;
}

export default function trainer() {
    const [gymClasses, setGymClasses] = useState<GymData[]>([]);

    return (
        <div>
            <div><a href="/trainer/init_gymclass">
                <Button className="px-10 py-10 text-3xl">
                    Add class
                </Button>
            </a></div>

            <h2>Your classes</h2>
            
        </div>
    );
}


=======
export default function Page() {
    return (
        <div>Trainer</div>
    );
}
>>>>>>> c8dfaf32bb0c08bf5e3dd3a822d9d8c5f84a2528
