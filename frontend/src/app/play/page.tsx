'use client';

import { useState, useEffect } from 'react';
import { getDailyInfo, playTurn, DailyInfo, ModelDialogue, PlayTurnResponse } from '@/lib/api';
import ChatBubble from '@/components/ChatBubble';
import ActionBar from '@/components/ActionBar';
import ShareResult from '@/components/ShareResult';
import ModelAvatar from '@/components/ModelAvatar';

interface GameHistory {
    round: number;
    action: 'PASS' | 'ELIMINATE';
    target?: string;
    wasCorrect?: boolean;
}

export default function PlayPage() {
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [dailyInfo, setDailyInfo] = useState<DailyInfo | null>(null);

    const [currentStateHash, setCurrentStateHash] = useState<string>('');
    const [currentRound, setCurrentRound] = useState(1);
    const [remainingModels, setRemainingModels] = useState<string[]>([]);
    const [dialogues, setDialogues] = useState<ModelDialogue[]>([]);
    const [allDialogues, setAllDialogues] = useState<ModelDialogue[][]>([]);

    const [gameOver, setGameOver] = useState(false);
    const [winner, setWinner] = useState<string | null>(null);
    const [moleModel, setMoleModel] = useState<string>('');
    const [canPass, setCanPass] = useState(true);
    const [actionLoading, setActionLoading] = useState(false);
    const [gameHistory, setGameHistory] = useState<GameHistory[]>([]);
    const [eliminatedModels, setEliminatedModels] = useState<string[]>([]);

    useEffect(() => {
        loadDailyGame();
    }, []);

    const loadDailyGame = async () => {
        try {
            setLoading(true);
            const info = await getDailyInfo();
            setDailyInfo(info);
            setCurrentStateHash(info.initial_state_hash);
            setRemainingModels(info.turn_order);
            setDialogues(info.dialogues);
            setAllDialogues([info.dialogues]);
            setCurrentRound(1);
            setCanPass(true);
        } catch (err) {
            setError(err instanceof Error ? err.message : 'Oyun yüklenemedi');
        } finally {
            setLoading(false);
        }
    };

    const handlePass = async () => {
        if (!canPass || currentRound !== 1) return;

        try {
            setActionLoading(true);
            const result = await playTurn('PASS', currentStateHash);

            setGameHistory([...gameHistory, { round: currentRound, action: 'PASS' }]);
            updateGameState(result);
            setCanPass(false);
        } catch (err) {
            setError(err instanceof Error ? err.message : 'Hata oluştu');
        } finally {
            setActionLoading(false);
        }
    };

    const handleEliminate = async (model: string) => {
        try {
            setActionLoading(true);
            const result = await playTurn('ELIMINATE', currentStateHash, model);

            const wasCorrect = result.winner === 'USER';
            setGameHistory([...gameHistory, {
                round: currentRound,
                action: 'ELIMINATE',
                target: model,
                wasCorrect
            }]);

            setEliminatedModels([...eliminatedModels, model]);
            updateGameState(result);

            if (result.game_over) {
                // Reveal the mole
                setMoleModel(model); // This is only correct if user won
            }
        } catch (err) {
            setError(err instanceof Error ? err.message : 'Hata oluştu');
        } finally {
            setActionLoading(false);
        }
    };

    const updateGameState = (result: PlayTurnResponse) => {
        setCurrentStateHash(result.state_hash);
        setCurrentRound(result.round_number);
        setRemainingModels(result.remaining_models);
        setDialogues(result.dialogues);

        if (result.dialogues.length > 0) {
            setAllDialogues([...allDialogues, result.dialogues]);
        }

        if (result.game_over) {
            setGameOver(true);
            setWinner(result.winner || null);
        }

        // Can only pass in round 1
        setCanPass(false);
    };

    if (loading) {
        return (
            <main className="min-h-screen flex items-center justify-center">
                <div className="text-center space-y-4">
                    <div className="text-6xl animate-pulse">🕵️‍♂️</div>
                    <p className="text-xl text-gray-300">Günün oyunu yükleniyor...</p>
                </div>
            </main>
        );
    }

    if (error) {
        return (
            <main className="min-h-screen flex items-center justify-center p-4">
                <div className="glass-card p-8 text-center max-w-md">
                    <div className="text-6xl mb-4">😵</div>
                    <h2 className="text-xl font-bold text-red-400 mb-2">Hata!</h2>
                    <p className="text-gray-300 mb-4">{error}</p>
                    <button
                        onClick={() => window.location.reload()}
                        className="btn-primary"
                    >
                        Tekrar Dene
                    </button>
                </div>
            </main>
        );
    }

    return (
        <main className="min-h-screen p-4 pb-32">
            {/* Header */}
            <header className="max-w-2xl mx-auto mb-6">
                <div className="flex items-center justify-between">
                    <div>
                        <h1 className="text-2xl font-bold">🕵️‍♂️ AI Köstebek</h1>
                        <p className="text-sm text-gray-400">
                            Kategori: <span className="text-mole-gold">{dailyInfo?.category}</span>
                        </p>
                    </div>
                    <div className="text-right">
                        <div className="text-lg font-bold text-mole-accent">Tur {currentRound}</div>
                        <div className="text-xs text-gray-500">
                            {remainingModels.length} AI kaldı
                        </div>
                    </div>
                </div>

                {/* Remaining Models */}
                <div className="flex gap-2 mt-4 flex-wrap">
                    {dailyInfo?.turn_order.map((model) => (
                        <ModelAvatar
                            key={model}
                            modelName={model}
                            size="sm"
                            eliminated={eliminatedModels.includes(model)}
                        />
                    ))}
                </div>
            </header>

            {/* Chat Area */}
            <div className="max-w-2xl mx-auto space-y-6">
                {allDialogues.map((roundDialogues, roundIndex) => (
                    <div key={roundIndex} className="space-y-4">
                        <div className="text-xs text-gray-500 text-center">
                            — Tur {roundIndex + 1} —
                        </div>
                        {roundDialogues.map((dialogue, idx) => (
                            <ChatBubble
                                key={`${roundIndex}-${idx}`}
                                modelName={dialogue.model_name}
                                message={dialogue.message}
                                isLatest={roundIndex === allDialogues.length - 1 && idx === roundDialogues.length - 1}
                                delay={idx * 200}
                            />
                        ))}
                    </div>
                ))}
            </div>

            {/* Action Bar - Fixed at bottom */}
            {!gameOver && (
                <div className="fixed bottom-0 left-0 right-0 p-4 bg-gradient-to-t from-mole-darker via-mole-darker to-transparent">
                    <div className="max-w-2xl mx-auto">
                        <ActionBar
                            remainingModels={remainingModels}
                            canPass={canPass && currentRound === 1}
                            onPass={handlePass}
                            onEliminate={handleEliminate}
                            isLoading={actionLoading}
                        />
                    </div>
                </div>
            )}

            {/* Game Over Overlay */}
            {gameOver && (
                <ShareResult
                    won={winner === 'USER'}
                    rounds={gameHistory}
                    moleModel={moleModel || 'Bilinmiyor'}
                />
            )}
        </main>
    );
}
