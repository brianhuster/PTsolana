export default function Layout({children}: {children: React.ReactNode}) {
    return (
        <section className="bg-red-500">
            {children}
        </section>
    );
}