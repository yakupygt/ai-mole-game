import Link from 'next/link';

export default function Home() {
    return (
        <main className="min-h-screen flex flex-col items-center justify-center p-4">
            {/* Hero Section */}
            <div className="max-w-2xl text-center space-y-8">
                {/* Logo/Title */}
                <div className="space-y-4">
                    <div className="text-8xl mb-4">🕵️‍♂️</div>
                    <h1 className="text-4xl sm:text-5xl font-bold bg-gradient-to-r from-mole-accent via-mole-gold to-mole-accent bg-clip-text text-transparent">
                        AI Köstebek Oyunu
                    </h1>
                    <p className="text-xl text-gray-300">
                        6 Yapay Zeka. 1 Köstebek. Bulabilir misin?
                    </p>
                </div>

                {/* Description */}
                <div className="glass-card p-6 text-left space-y-4">
                    <h2 className="text-lg font-semibold text-mole-gold flex items-center gap-2">
                        <span>📜</span> Nasıl Oynanır?
                    </h2>
                    <ul className="space-y-3 text-gray-300">
                        <li className="flex items-start gap-3">
                            <span className="text-mole-accent">1.</span>
                            <span>6 AI modeli bir kelimeyi tarif ediyor. Ama bir tanesi <strong className="text-mole-accent">farklı bir kelime</strong> hakkında konuşuyor!</span>
                        </li>
                        <li className="flex items-start gap-3">
                            <span className="text-mole-accent">2.</span>
                            <span>Konuşmaları dikkatlice oku ve <strong className="text-mole-gold">köstebeği</strong> bulmaya çalış.</span>
                        </li>
                        <li className="flex items-start gap-3">
                            <span className="text-mole-accent">3.</span>
                            <span>Her turda bir AI'ı <strong className="text-red-400">ele</strong> veya ilk turda <strong className="text-blue-400">pas</strong> geçebilirsin.</span>
                        </li>
                        <li className="flex items-start gap-3">
                            <span className="text-mole-accent">4.</span>
                            <span>Köstebeği bul ve <strong className="text-mole-success">kazan!</strong> Yanlış elemelerde köstebek kazanır.</span>
                        </li>
                    </ul>
                </div>

                {/* AI Models */}
                <div className="glass-card p-6">
                    <h3 className="text-sm font-medium text-gray-400 mb-4">Yarışmacı AI Modelleri</h3>
                    <div className="flex flex-wrap justify-center gap-4">
                        {['Gemini', 'Claude', 'ChatGPT', 'Grok', 'Llama', 'DeepSeek'].map((model) => (
                            <div
                                key={model}
                                className="px-4 py-2 rounded-full text-sm font-medium"
                                style={{
                                    background: getGradient(model),
                                }}
                            >
                                {model}
                            </div>
                        ))}
                    </div>
                </div>

                {/* Play Button */}
                <Link href="/play" className="block">
                    <button className="btn-primary text-xl px-12 py-4 w-full sm:w-auto">
                        🎮 Oyna
                    </button>
                </Link>

                {/* Daily info */}
                <p className="text-sm text-gray-500">
                    Her gün yeni bir oyun! • Günlük sıralama yakında 🏆
                </p>
            </div>
        </main>
    );
}

function getGradient(model: string): string {
    const gradients: Record<string, string> = {
        Gemini: 'linear-gradient(135deg, #4285f4 0%, #34a853 100%)',
        Claude: 'linear-gradient(135deg, #cc785c 0%, #d4a574 100%)',
        ChatGPT: 'linear-gradient(135deg, #10a37f 0%, #1a7f64 100%)',
        Grok: 'linear-gradient(135deg, #1da1f2 0%, #0d8bd9 100%)',
        Llama: 'linear-gradient(135deg, #7c3aed 0%, #a855f7 100%)',
        DeepSeek: 'linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%)',
    };
    return gradients[model] || 'linear-gradient(135deg, #666 0%, #444 100%)';
}
