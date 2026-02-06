'use client';

import ModelAvatar from './ModelAvatar';

interface ActionBarProps {
    remainingModels: string[];
    canPass: boolean;
    onPass: () => void;
    onEliminate: (model: string) => void;
    isLoading: boolean;
}

export default function ActionBar({
    remainingModels,
    canPass,
    onPass,
    onEliminate,
    isLoading
}: ActionBarProps) {
    return (
        <div className="glass-card p-4 mt-4">
            <div className="flex flex-col gap-4">
                {/* Pass Button */}
                {canPass && (
                    <button
                        onClick={onPass}
                        disabled={isLoading}
                        className="btn-secondary w-full flex items-center justify-center gap-2"
                    >
                        <span>⏭️</span>
                        <span>PAS (Sadece 1. Turda)</span>
                    </button>
                )}

                {/* Eliminate Buttons */}
                <div className="space-y-2">
                    <p className="text-sm text-gray-400 font-medium">🎯 Köstebeği Seç:</p>
                    <div className="grid grid-cols-2 sm:grid-cols-3 gap-2">
                        {remainingModels.map((model) => (
                            <button
                                key={model}
                                onClick={() => onEliminate(model)}
                                disabled={isLoading}
                                className="btn-eliminate flex items-center justify-center gap-2 py-3"
                            >
                                <ModelAvatar modelName={model} size="sm" />
                                <span>{model}</span>
                            </button>
                        ))}
                    </div>
                </div>
            </div>

            {isLoading && (
                <div className="mt-4 text-center">
                    <div className="inline-flex items-center gap-2 text-mole-accent">
                        <svg className="animate-spin h-5 w-5" fill="none" viewBox="0 0 24 24">
                            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                        </svg>
                        <span>AI yanıtları üretiliyor...</span>
                    </div>
                </div>
            )}
        </div>
    );
}
