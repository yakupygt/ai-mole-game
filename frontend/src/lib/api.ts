const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export interface ModelDialogue {
    model_name: string;
    message: string;
    internal_thought?: string;
}

export interface DailyInfo {
    date: string;
    category: string;
    turn_order: string[];
    initial_state_hash: string;
    round_number: number;
    dialogues: ModelDialogue[];
}

export interface PlayTurnResponse {
    state_hash: string;
    round_number: number;
    remaining_models: string[];
    dialogues: ModelDialogue[];
    game_over: boolean;
    winner?: string;
    can_pass: boolean;
    eliminated_model?: string;
}

export async function getDailyInfo(): Promise<DailyInfo> {
    const response = await fetch(`${API_URL}/api/daily`, {
        cache: 'no-store',
    });

    if (!response.ok) {
        throw new Error('Failed to fetch daily info');
    }

    return response.json();
}

export async function playTurn(
    action: 'PASS' | 'ELIMINATE',
    currentStateHash?: string,
    targetModel?: string
): Promise<PlayTurnResponse> {
    const response = await fetch(`${API_URL}/api/play_turn`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            action,
            current_state_hash: currentStateHash,
            target_model: targetModel,
        }),
    });

    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Failed to play turn');
    }

    return response.json();
}
