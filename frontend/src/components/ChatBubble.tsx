'use client';

import { useTypewriter } from '@/hooks/useTypewriter';
import ModelAvatar from './ModelAvatar';
import { MODEL_CONFIG, getModelClass } from '@/lib/models';

interface ChatBubbleProps {
    modelName: string;
    message: string;
    isLatest?: boolean;
    delay?: number;
}

export default function ChatBubble({ modelName, message, isLatest = false, delay = 0 }: ChatBubbleProps) {
    const { displayText, isComplete } = useTypewriter(
        isLatest ? message : '',
        30
    );

    const config = MODEL_CONFIG[modelName];
    const displayMessage = isLatest ? displayText : message;

    return (
        <div
            className="flex items-start gap-3 animate-slide-up"
            style={{ animationDelay: `${delay}ms` }}
        >
            <ModelAvatar modelName={modelName} size="md" />

            <div className="flex-1">
                <div className="flex items-center gap-2 mb-1">
                    <span
                        className="font-semibold text-sm"
                        style={{ color: config?.color || '#fff' }}
                    >
                        {modelName}
                    </span>
                    <span className="text-xs text-gray-500">{config?.emoji}</span>
                </div>

                <div
                    className={`chat-bubble ${getModelClass(modelName)}`}
                    style={{
                        background: `linear-gradient(135deg, ${config?.color}22 0%, ${config?.color}11 100%)`,
                        border: `1px solid ${config?.color}33`,
                    }}
                >
                    <p className="text-white/90 text-sm leading-relaxed">
                        {displayMessage}
                        {isLatest && !isComplete && (
                            <span className="typewriter-cursor" />
                        )}
                    </p>
                </div>
            </div>
        </div>
    );
}
