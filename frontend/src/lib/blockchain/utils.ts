import { createHash, randomBytes } from "crypto";

export {};

export function convertNameToHash8Bytes(name: string): Buffer {
    const hash = createHash("sha256").update(`global:${name}`).digest();
    return hash.subarray(0, 8); // Take the first 8 bytes
}

export function encode(str: string) {
    const encoder = new TextEncoder();
    let buf = encoder.encode(str);
    for (let i = 0; i < buf.length; i++) {
        buf[i]++;
    }
    return buf;
}

export function generateRandomSeed(): Buffer {
    const random = randomBytes(8); // Generates 8 random bytes (u64)
    return random; // This will be used directly as the u64 seed
}

export function bigintToBytes(bigint: bigint, byteLength: number): Uint8Array {
    const buffer = Buffer.alloc(byteLength);

    for (let i = 0; i < byteLength; i++) {
        buffer[byteLength - 1 - i] = Number(bigint >> BigInt(i * 8)) & 0xff;
    }

    return new Uint8Array(buffer);
}
