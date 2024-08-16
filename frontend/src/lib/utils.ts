import { type ClassValue, clsx } from "clsx"
import { twMerge } from "tailwind-merge"

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