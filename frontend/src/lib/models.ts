export class GymClass {
    id: number;
    name: string;
    location: string;
    price: number;
    flag: number;
    status: string;

    constructor(
        id: number,
        name: string,
        age: number,
        location: string,
        flag: number
    ) {
        this.id = id;
        this.name = name;
        this.price = age;
        this.location = location;
        this.flag = flag;
        if (flag === 0) {
            this.status = "Available";
        } else {
            this.status = "Unavailable";
        }
    }
}

export interface GymData {
    company: string;
    trainer: string;
    customer: string;
    name: string;
    location: string;
    info: string;
    price: number;
    flag: number;
    seed_sha256: number;
}
