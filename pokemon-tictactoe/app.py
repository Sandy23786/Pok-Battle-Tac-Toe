from flask import Flask, render_template, jsonify, request
import random
import json
import urllib.request
import urllib.parse

app = Flask(__name__)

# Pokemon pairs for matchups
POKEMON_PAIRS = [
    {"p1": {"name": "Pikachu", "id": 25}, "p2": {"name": "Eevee", "id": 133}},
    {"p1": {"name": "Charmander", "id": 4}, "p2": {"name": "Squirtle", "id": 7}},
    {"p1": {"name": "Bulbasaur", "id": 1}, "p2": {"name": "Jigglypuff", "id": 39}},
    {"p1": {"name": "Mewtwo", "id": 150}, "p2": {"name": "Gengar", "id": 94}},
    {"p1": {"name": "Snorlax", "id": 143}, "p2": {"name": "Charizard", "id": 6}},
    {"p1": {"name": "Lucario", "id": 448}, "p2": {"name": "Gardevoir", "id": 282}},
]

def check_winner(board):
    wins = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
    for a,b,c in wins:
        if board[a] and board[a] == board[b] == board[c]:
            return board[a], [a,b,c]
    return None, None

def minimax(board, is_maximizing, ai_mark, human_mark):
    winner, _ = check_winner(board)
    if winner == ai_mark: return 10
    if winner == human_mark: return -10
    if all(c for c in board): return 0

    if is_maximizing:
        best = -1000
        for i in range(9):
            if not board[i]:
                board[i] = ai_mark
                best = max(best, minimax(board, False, ai_mark, human_mark))
                board[i] = None
        return best
    else:
        best = 1000
        for i in range(9):
            if not board[i]:
                board[i] = human_mark
                best = min(best, minimax(board, True, ai_mark, human_mark))
                board[i] = None
        return best

def get_ai_move(board, difficulty, ai_mark, human_mark):
    empty = [i for i in range(9) if not board[i]]
    if not empty:
        return None

    if difficulty == 'easy':
        # 70% random, 30% smart
        if random.random() < 0.7:
            return random.choice(empty)

    if difficulty == 'medium':
        # Check win
        for i in empty:
            board[i] = ai_mark
            if check_winner(board)[0]:
                board[i] = None
                return i
            board[i] = None
        # Block
        for i in empty:
            board[i] = human_mark
            if check_winner(board)[0]:
                board[i] = None
                return i
            board[i] = None
        # Center or random
        if 4 in empty:
            return 4
        return random.choice(empty)

    if difficulty == 'hard':
        best_score = -1000
        best_move = empty[0]
        for i in empty:
            board[i] = ai_mark
            score = minimax(board, False, ai_mark, human_mark)
            board[i] = None
            if score > best_score:
                best_score = score
                best_move = i
        return best_move

    return random.choice(empty)

def get_pollinations_commentary(situation, pokemon1, pokemon2):
    try:
        prompt = f"You are a Pokemon battle narrator. In 1-2 short sentences, narrate this Tic-Tac-Toe moment: {situation}. {pokemon1} vs {pokemon2}. Be dramatic, fun, and Pokemon-themed!"
        encoded = urllib.parse.quote(prompt)
        url = f"https://text.pollinations.ai/{encoded}"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as response:
            return response.read().decode('utf-8').strip()[:200]
    except:
        comments = [
            f"⚡ {pokemon1} strikes with precision!",
            f"🌟 An incredible move! The battle intensifies!",
            f"🔥 {pokemon2} is fighting back! What a match!",
            f"💫 The arena shakes with each powerful move!",
        ]
        return random.choice(comments)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/random-matchup')
def random_matchup():
    pair = random.choice(POKEMON_PAIRS)
    return jsonify(pair)

@app.route('/api/ai-move', methods=['POST'])
def ai_move():
    data = request.json
    board = data.get('board', [None]*9)
    difficulty = data.get('difficulty', 'medium')
    ai_mark = data.get('ai_mark', 'O')
    human_mark = data.get('human_mark', 'X')

    move = get_ai_move(board[:], difficulty, ai_mark, human_mark)
    return jsonify({"move": move})

@app.route('/api/commentary', methods=['POST'])
def commentary():
    data = request.json
    situation = data.get('situation', 'A move was made')
    p1 = data.get('pokemon1', 'Pikachu')
    p2 = data.get('pokemon2', 'Eevee')
    text = get_pollinations_commentary(situation, p1, p2)
    return jsonify({"commentary": text})

@app.route('/api/check-winner', methods=['POST'])
def check_winner_route():
    data = request.json
    board = data.get('board', [None]*9)
    winner, line = check_winner(board)
    return jsonify({"winner": winner, "line": line})

if __name__ == '__main__':
    app.run()
