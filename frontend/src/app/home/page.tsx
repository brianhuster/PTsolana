"use client";

import GymClassItem from "@/components/custom/gym-class-item";
import { GymClass, GymData } from "@/lib/models";
import { useEffect, useState } from "react";

export default function Home() {
    const [gymClasses, setGymClasses] = useState<GymData[]>([]);

    useEffect(() => {
        // Fetch data from an external API
        const fetchData = async () => {
            const res = await fetch(
                "http://localhost:8000/get-all-gym-classes-data"
            );
            const json = await res.json();
            setGymClasses(json.data);
        };

        fetchData();
    }, []);
    return (
        <main className="grid grid-flow-row grid-cols-4 gap-10 px-40">
            {gymClasses.map((item, index) => (
                <GymClassItem key={index} {...item} />
            ))}
        </main>
    );
}
