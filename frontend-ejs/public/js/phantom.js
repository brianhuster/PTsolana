async function connect_to_phantom() {
    const provider = await getProvider();
    if (!provider) {
        return;
    }
    try {
        const resp = await provider.connect({ onlyIfTrusted: true });
        console.log(resp.publicKey.toString());
    } catch (err) {
        console.error(err);
    }
}
const getProvider = async () => {
    if ("phantom" in window) {
        const provider = window.phantom?.solana;
        
        if (provider?.isPhantom) {
            return provider;
        }
        else {
            window.open("https://phantom.app/", "_blank");
        }
    }
};
