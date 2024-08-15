export {};

declare global {
    interface WindowWithSolana extends Window {
        solana?: {
            isPhantom: boolean;
            connect: (config?: {
                onlyIfTrusted: boolean;
            }) => Promise<{ publicKey: PublicKey }>;
            disconnect: () => Promise<void>;
            publicKey: PublicKey | null;
            on: (event: string, handler: (args: any) => void) => void;
            signTransaction: (transaction: Transaction) => Promise<string>;
        };
    }
}
