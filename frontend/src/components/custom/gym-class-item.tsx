import { GymClass, GymData } from "@/lib/models";
import * as React from "react";

import { Button } from "@/components/ui/button";
import { Card, CardContent, CardFooter } from "@/components/ui/card";
export default function GymClassItem(gymclass: GymData) {
    return (
        <Card className="w-[350px]">
            <div className="w-full">
                <img
                    src="https://swequity.vn/wp-content/uploads/2019/12/bai-tap-leanbody-1024x683.png"
                    alt="placeholder"
                    className="w-full h-[300px] object-cover"
                />
            </div>
            <CardContent className="mt-2">
                <div className="text-3xl">{gymclass.name}</div>
                <div className="mt-2">
                    <div>Location: {gymclass.location}</div>
                </div>
            </CardContent>
            <CardFooter className="flex justify-between">
                <div className="font-bold">{gymclass.price}</div>
                <a href={"/gym-class/" + gymclass.customer}>
                    <Button>Book</Button>
                </a>
            </CardFooter>
        </Card>
    );
}
