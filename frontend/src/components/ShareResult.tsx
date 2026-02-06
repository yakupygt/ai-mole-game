'use client';

import { useState } from 'react';

interface GameHistory {
    round: number;
    action: 'PASS' | 'ELIMINATE';
    target?: string;
    wasCorrect?: boolean;
}

interface ShareResultProps {
    won: boolean;
    rounds: GameHistory[];
    moleModel: string;
}

export default function ShareResult({ won, rounds, moleModel }: ShareResultProps) {
    const [copied, setCopied] = useState(false);

    const generateShareText = () => {
        const today = new Date().toLocaleDateString('tr-TR');
        const emoji = won ? '🎉' : '😭';

        const roundEmojis = rounds.map((r) => {
            if (r.action === 'PASS') return '⏩';
            if (r.wasCorrect) return '🕵️‍♂️';
            return '❌';
        }).join(' ');

        return `AI Köstebek Oyunu ${today} ${emoji}

${roundEmojis}

${won ? 'Köstebeği buldum!' : 'Köstebek kazandı...'}

🎮 Sen de oyna: https://ai-mole-game.vercel.app`;
    };

    const handleCopy = async () => {
        const text = generateShareText();
        await navigator.clipboard.writeText(text);
        setCopied(true);
        setTimeout(() => setCopied(false), 2000);
    };

    return (
        <div className="result-overlay">
            <div className="glass-card p-8 max-w-md mx-4 text-center">
                <div className="text-6xl mb-4">
                    {won ? '🎉' : '😭'}
                </div>

                <h2 className="text-2xl font-bold mb-2">
                    {won ? 'Tebrikler!' : 'Kaybettin!'}
                </h2>

                <p className="text-gray-300 mb-4">
                    {won
                        ? 'Köstebeği buldun!'
                        : `Köstebek "${moleModel}" seni alt etti!`
                    }
                </p>

                <div className="bg-black/30 rounded-lg p-4 mb-6">
                    <p className="font-mono text-lg">
                        {rounds.map((r, i) => (
                            <span key={i} className="mx-1">
                                {r.action === 'PASS' ? '⏩' : r.wasCorrect ? '🕵️‍♂️' : '❌'}
                            </span>
                        ))}
                    </p>
                </div>

                <button
                    onClick={handleCopy}
                    className="btn-primary w-full"
                >
                    {copied ? '✅ Kopyalandı!' : '📋 Sonucu Paylaş'}
                </button>

                <p className="text-xs text-gray-500 mt-4">
                    Yarın yeni bir oyun için geri gel!
                </p>
            </div>
        </div>
    );
}
