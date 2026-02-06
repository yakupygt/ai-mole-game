import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
    title: "AI Köstebek Oyunu - Yapay Zekaları Tanıyabilir misin?",
    description: "6 yapay zeka modeli arasındaki köstebeği bulun! Günlük sosyal çıkarım oyunu.",
    keywords: ["AI", "yapay zeka", "oyun", "köstebek", "sosyal çıkarım", "Gemini", "Claude", "ChatGPT"],
    authors: [{ name: "AI Mole Game" }],
    openGraph: {
        title: "AI Köstebek Oyunu",
        description: "6 yapay zeka modeli arasındaki köstebeği bulun!",
        type: "website",
    },
};

export default function RootLayout({
    children,
}: Readonly<{
    children: React.ReactNode;
}>) {
    return (
        <html lang="tr">
            <body className="antialiased">
                {children}
            </body>
        </html>
    );
}
