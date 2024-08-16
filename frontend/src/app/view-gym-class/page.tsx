"use client";

import GymClassItem from "@/components/custom/gym-class-item";
import { GymData, GymClassItemBtn, GymClass } from "@/lib/models";
import { useEffect, useState } from "react";
import { getJSON } from "@/lib/utils";

export default function ViewGymClass() {
    const [gymClasses, setGymClasses] = useState<GymData[]>([]);
    useEffect(() => {
        const fetchData = async () => {
            const json = await getJSON("http://localhost:8000/get-all-gym-classes-data");
            setGymClasses(json.data);
        };

        fetchData();
    }, []);
    return (
        <main className="grid grid-flow-row grid-cols-4 gap-10 px-40">
            {gymClasses.map((item, index) => (
                <GymClassItem key={index} gymclass={item}
                    buttons={[{
                        text: "Book",
                        link: "/gym-class/" + item.customer
                    }]}
                />
            ))}
        </main>
    );
}
