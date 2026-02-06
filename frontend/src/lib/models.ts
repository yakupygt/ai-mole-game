export const MODEL_CONFIG: Record<string, {
    name: string;
    color: string;
    gradient: string;
    emoji: string;
    shortName: string;
}> = {
    Gemini: {
        name: 'Gemini',
        color: '#4285f4',
        gradient: 'linear-gradient(135deg, #4285f4 0%, #34a853 100%)',
        emoji: '💎',
        shortName: 'GEM',
    },
    Claude: {
        name: 'Claude',
        color: '#cc785c',
        gradient: 'linear-gradient(135deg, #cc785c 0%, #d4a574 100%)',
        emoji: '🧡',
        shortName: 'CLA',
    },
    ChatGPT: {
        name: 'ChatGPT',
        color: '#10a37f',
        gradient: 'linear-gradient(135deg, #10a37f 0%, #1a7f64 100%)',
        emoji: '💚',
        shortName: 'GPT',
    },
    Grok: {
        name: 'Grok',
        color: '#1da1f2',
        gradient: 'linear-gradient(135deg, #1da1f2 0%, #0d8bd9 100%)',
        emoji: '💙',
        shortName: 'GRK',
    },
    Llama: {
        name: 'Llama',
        color: '#7c3aed',
        gradient: 'linear-gradient(135deg, #7c3aed 0%, #a855f7 100%)',
        emoji: '🦙',
        shortName: 'LLA',
    },
    DeepSeek: {
        name: 'DeepSeek',
        color: '#3b82f6',
        gradient: 'linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%)',
        emoji: '🔵',
        shortName: 'DSK',
    },
};

export function getModelClass(modelName: string): string {
    const classMap: Record<string, string> = {
        Gemini: 'model-gemini',
        Claude: 'model-claude',
        ChatGPT: 'model-chatgpt',
        Grok: 'model-grok',
        Llama: 'model-llama',
        DeepSeek: 'model-deepseek',
    };
    return classMap[modelName] || 'model-gemini';
}
