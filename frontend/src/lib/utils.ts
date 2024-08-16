import { type ClassValue, clsx } from "clsx"
import { twMerge } from "tailwind-merge"
import { PublicKey } from "@solana/web3.js";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export async function getJSON(link: string){
  try {
      const response = await fetch(link);
      if (response.status !== 200) {
          alert("Error");
      } else {
          const x = await response.json();
          return x;
      }
  }
  catch (error) {
      throw new Error("Cannot connect to " + link);
  }
}     
export async function getAccountRole(publicKey: PublicKey | null): Promise<string> {
  const resp = await fetch("http://localhost:8000/get-account-data?public_key=" + publicKey?.toString());
  const json = await resp.json();
  const data = json.data;
  if (data === "Not found") {
      return "no account";
  } else {
      return data.role ?? "no account";
  }
}
