'use client';

import { MODEL_CONFIG, getModelClass } from '@/lib/models';

interface ModelAvatarProps {
    modelName: string;
    size?: 'sm' | 'md' | 'lg';
    eliminated?: boolean;
}

export default function ModelAvatar({ modelName, size = 'md', eliminated = false }: ModelAvatarProps) {
    const config = MODEL_CONFIG[modelName];

    const sizeClasses = {
        sm: 'w-8 h-8 text-xs',
        md: 'w-12 h-12 text-sm',
        lg: 'w-16 h-16 text-base',
    };

    if (!config) {
        return (
            <div className={`avatar ${sizeClasses[size]} bg-gray-500`}>
                ?
            </div>
        );
    }

    return (
        <div
            className={`avatar ${sizeClasses[size]} ${getModelClass(modelName)} ${eliminated ? 'eliminated' : ''}`}
            style={{ background: config.gradient }}
            title={config.name}
        >
            {config.shortName}
        </div>
    );
}
