"""
Hangman ML Challenge - User Template
Complete starter template for ML bot + web interface development.

This template provides:
- HangmanBot class for ML implementation
- Flask web interface option
- Dash web interface option
- Complete game simulation
- Performance evaluation

Users need to implement the HangmanBot class and choose a web framework.
"""

import random
from collections import Counter
from typing import List, Set
import pickle

# Flask imports
from flask import Flask, render_template_string, request, jsonify, session
import json

# Dash imports (alternative to Flask)
try:
    import dash
    from dash import dcc, html, Input, Output, State, callback
    import plotly.graph_objs as go
    import plotly.express as px
    DASH_AVAILABLE = True
except ImportError:
    DASH_AVAILABLE = False
    print("Dash not available. Install with: pip install dash plotly")

class HangmanBot:
    """
    Your Hangman Bot Implementation
    
    This is the core ML component users need to implement!
    """
    
    def __init__(self, training_words: List[str]):
        """Initialize your bot with training words"""
        self.training_words = [word.lower() for word in training_words]
        
        # TODO: Add your training logic here
        # Examples:
        # - Build letter frequency models
        # - Train machine learning models
        # - Create pattern matching systems
        
        print(f"Bot initialized with {len(self.training_words)} training words")
        self._train_model()
    
    def _train_model(self):
        """Train your model on the training words"""
        # TODO: Implement your training logic here
        
        # Example: Simple frequency analysis
        self.letter_freq = Counter()
        for word in self.training_words:
            self.letter_freq.update(word)
        
        print("Model training completed")
    
    def predict_next_letter(self, masked_word: str, wrong_guesses: Set[str]) -> str:
        """
        Predict the next letter to guess
        
        Args:
            masked_word: Current state like "h_ll_" 
            wrong_guesses: Set of already guessed wrong letters like {"x", "y"}
            
        Returns:
            Next letter to guess (single character)
        """
        # TODO: Implement your prediction logic here
        
        # Example: Simple frequency-based approach
        revealed_letters = set(masked_word.replace('_', ''))
        available_letters = set('abcdefghijklmnopqrstuvwxyz') - revealed_letters - wrong_guesses
        
        if not available_letters:
            return 'a'  # Fallback
        
        # Return most frequent available letter
        for letter, count in self.letter_freq.most_common():
            if letter in available_letters:
                return letter
        
        return list(available_letters)[0]  # Fallback

# =============================================================================
# FLASK WEB INTERFACE
# =============================================================================

def create_flask_app(bot):
    """Create Flask web interface"""
    
    app = Flask(__name__)
    app.secret_key = 'hangman_secret_key'
    
    # HTML template embedded in Python (no separate HTML files needed!)
    HTML_TEMPLATE = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Hangman Bot Challenge</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
            .game-container { background: #f5f5f5; padding: 20px; border-radius: 10px; margin: 20px 0; }
            .word-display { font-size: 2em; letter-spacing: 0.5em; margin: 20px 0; }
            .controls { margin: 20px 0; }
            button { padding: 10px 20px; margin: 5px; font-size: 16px; cursor: pointer; }
            .stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin: 20px 0; }
            .stat-card { background: white; padding: 15px; border-radius: 5px; text-align: center; }
            .stat-value { font-size: 2em; font-weight: bold; color: #007bff; }
            .stat-label { color: #666; margin-top: 5px; }
        </style>
    </head>
    <body>
        <h1>Hangman Bot Challenge</h1>
        
        <div class="game-container">
            <h2>Current Game</h2>
            <div class="word-display" id="word-display">{{ masked_word }}</div>
            <div>
                <strong>Lives:</strong> <span id="lives">{{ lives }}</span> | 
                <strong>Wrong Guesses:</strong> <span id="wrong">{{ wrong_guesses }}</span>
            </div>
            
            <div class="controls">
                <button onclick="getBotGuess()">Get Bot Guess</button>
                <button onclick="newGame()">New Game</button>
                <button onclick="runSimulation()">Run Simulation</button>
            </div>
        </div>
        
        <div class="stats">
            <div class="stat-card">
                <div class="stat-value" id="win-rate">0%</div>
                <div class="stat-label">Win Rate</div>
            </div>
            <div class="stat-card">
                <div class="stat-value" id="games-played">0</div>
                <div class="stat-label">Games Played</div>
            </div>
            <div class="stat-card">
                <div class="stat-value" id="avg-guesses">0</div>
                <div class="stat-label">Avg Guesses</div>
            </div>
        </div>
        
        <div id="simulation-results" style="display: none;">
            <h3>Simulation Results</h3>
            <div id="results-content"></div>
        </div>
        
        <script>
            let currentGame = null;
            
            function getBotGuess() {
                fetch('/api/guess', {method: 'POST'})
                    .then(r => r.json())
                    .then(data => {
                        if (data.success) {
                            updateGameState(data.game_state);
                            alert('Bot guesses: ' + data.guess);
                        } else {
                            alert('Error: ' + data.error);
                        }
                    });
            }
            
            function newGame() {
                fetch('/api/new_game', {method: 'POST'})
                    .then(r => r.json())
                    .then(data => {
                        if (data.success) {
                            updateGameState(data.game_state);
                        } else {
                            alert('Error: ' + data.error);
                        }
                    });
            }
            
            function runSimulation() {
                fetch('/api/simulate', {method: 'POST'})
                    .then(r => r.json())
                    .then(data => {
                        if (data.success) {
                            showSimulationResults(data.results);
                        } else {
                            alert('Error: ' + data.error);
                        }
                    });
            }
            
            function updateGameState(gameState) {
                document.getElementById('word-display').textContent = gameState.masked_word;
                document.getElementById('lives').textContent = gameState.lives;
                document.getElementById('wrong').textContent = gameState.wrong_guesses.join(', ');
            }
            
            function showSimulationResults(results) {
                document.getElementById('win-rate').textContent = results.win_rate + '%';
                document.getElementById('games-played').textContent = results.games_played;
                document.getElementById('avg-guesses').textContent = results.avg_guesses.toFixed(1);
                
                const content = `
                    <p><strong>Games Played:</strong> ${results.games_played}</p>
                    <p><strong>Wins:</strong> ${results.wins}</p>
                    <p><strong>Losses:</strong> ${results.losses}</p>
                    <p><strong>Win Rate:</strong> ${results.win_rate}%</p>
                    <p><strong>Average Guesses:</strong> ${results.avg_guesses.toFixed(1)}</p>
                `;
                document.getElementById('results-content').innerHTML = content;
                document.getElementById('simulation-results').style.display = 'block';
            }
        </script>
    </body>
    </html>
    """
    
    @app.route('/')
    def index():
        """Main game page"""
        if 'game_state' not in session:
            session['game_state'] = {
                'word': '',
                'masked_word': '_____',
                'lives': 6,
                'wrong_guesses': [],
                'game_over': False
            }
        
        game_state = session['game_state']
        return render_template_string(HTML_TEMPLATE, 
                                    masked_word=game_state['masked_word'],
                                    lives=game_state['lives'],
                                    wrong_guesses=', '.join(game_state['wrong_guesses']))
    
    @app.route('/api/new_game', methods=['POST'])
    def new_game():
        """Start a new game"""
        try:
            # Choose random word (in real implementation, use your word list)
            words = ['python', 'machine', 'learning', 'algorithm', 'computer', 'hangman']
            word = random.choice(words)
            
            session['game_state'] = {
                'word': word,
                'masked_word': '_' * len(word),
                'lives': 6,
                'wrong_guesses': [],
                'game_over': False
            }
            
            return jsonify({
                'success': True,
                'game_state': session['game_state']
            })
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)})
    
    @app.route('/api/guess', methods=['POST'])
    def get_guess():
        """Get bot's next guess"""
        try:
            game_state = session.get('game_state', {})
            if not game_state or game_state.get('game_over', False):
                return jsonify({'success': False, 'error': 'No active game'})
            
            # Get bot's prediction
            guess = bot.predict_next_letter(
                game_state['masked_word'], 
                set(game_state['wrong_guesses'])
            )
            
            # Update game state
            word = game_state['word']
            if guess in word:
                # Update masked word
                new_masked = ""
                for i, char in enumerate(word):
                    if char == guess:
                        new_masked += char
                    else:
                        new_masked += game_state['masked_word'][i]
                game_state['masked_word'] = new_masked
            else:
                game_state['wrong_guesses'].append(guess)
                game_state['lives'] -= 1
            
            # Check game over
            if '_' not in game_state['masked_word']:
                game_state['game_over'] = True
            elif game_state['lives'] <= 0:
                game_state['game_over'] = True
            
            session['game_state'] = game_state
            
            return jsonify({
                'success': True,
                'guess': guess,
                'game_state': game_state
            })
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)})
    
    @app.route('/api/simulate', methods=['POST'])
    def run_simulation():
        """Run bot simulation"""
        try:
            words = ['python', 'machine', 'learning', 'algorithm', 'computer']
            wins = 0
            total_guesses = 0
            
            for word in words:
                masked_word = '_' * len(word)
                wrong_guesses = set()
                lives = 6
                guesses = 0
                
                while lives > 0 and '_' in masked_word:
                    guess = bot.predict_next_letter(masked_word, wrong_guesses)
                    guesses += 1
                    
                    if guess in word:
                        new_masked = ""
                        for i, char in enumerate(word):
                            if char == guess:
                                new_masked += char
                            else:
                                new_masked += masked_word[i]
                        masked_word = new_masked
                    else:
                        wrong_guesses.add(guess)
                        lives -= 1
                
                if '_' not in masked_word:
                    wins += 1
                total_guesses += guesses
            
            results = {
                'games_played': len(words),
                'wins': wins,
                'losses': len(words) - wins,
                'win_rate': round((wins / len(words)) * 100, 1),
                'avg_guesses': round(total_guesses / len(words), 1)
            }
            
            return jsonify({'success': True, 'results': results})
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)})
    
    return app

# =============================================================================
# DASH WEB INTERFACE (Alternative to Flask)
# =============================================================================

def create_dash_app(bot):
    """Create Dash web interface (pure Python, no HTML/CSS/JS needed!)"""
    
    if not DASH_AVAILABLE:
        print("Dash not available. Install with: pip install dash plotly")
        return None
    
    app = dash.Dash(__name__)
    
    # Define layout using Python components
    app.layout = html.Div([
        html.H1("Hangman Bot Challenge", style={'textAlign': 'center'}),
        
        # Game state display
        html.Div([
            html.H2("Current Game"),
            html.Div(id="word-display", style={'fontSize': '2em', 'letterSpacing': '0.5em', 'textAlign': 'center', 'margin': '20px'}),
            html.Div([
                html.Span("Lives: "),
                html.Span(id="lives-display"),
                html.Span(" | Wrong Guesses: "),
                html.Span(id="wrong-display")
            ], style={'textAlign': 'center', 'margin': '20px'}),
        ], style={'backgroundColor': '#f5f5f5', 'padding': '20px', 'borderRadius': '10px', 'margin': '20px'}),
        
        # Controls
        html.Div([
            html.Button("Get Bot Guess", id="guess-btn", n_clicks=0, style={'margin': '5px'}),
            html.Button("New Game", id="new-game-btn", n_clicks=0, style={'margin': '5px'}),
            html.Button("Run Simulation", id="simulate-btn", n_clicks=0, style={'margin': '5px'}),
        ], style={'textAlign': 'center', 'margin': '20px'}),
        
        # Statistics
        html.Div([
            html.Div([
                html.Div(id="win-rate", className="stat-value"),
                html.Div("Win Rate", className="stat-label")
            ], className="stat-card"),
            html.Div([
                html.Div(id="games-played", className="stat-value"),
                html.Div("Games Played", className="stat-label")
            ], className="stat-card"),
            html.Div([
                html.Div(id="avg-guesses", className="stat-value"),
                html.Div("Avg Guesses", className="stat-label")
            ], className="stat-card"),
        ], className="stats"),
        
        # Results
        html.Div(id="simulation-results"),
        
        # Hidden div to store game state
        html.Div(id="game-state", style={'display': 'none'}),
    ], style={'maxWidth': '800px', 'margin': '0 auto', 'padding': '20px'})
    
    # Add CSS styles
    app.index_string = '''
    <!DOCTYPE html>
    <html>
        <head>
            {%metas%}
            <title>{%title%}</title>
            {%favicon%}
            {%css%}
            <style>
                .stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin: 20px 0; }
                .stat-card { background: white; padding: 15px; border-radius: 5px; text-align: center; border: 1px solid #ddd; }
                .stat-value { font-size: 2em; font-weight: bold; color: #007bff; }
                .stat-label { color: #666; margin-top: 5px; }
            </style>
        </head>
        <body>
            {%app_entry%}
            <footer>
                {%config%}
                {%scripts%}
                {%renderer%}
            </footer>
        </body>
    </html>
    '''
    
    # Callbacks for interactivity
    @app.callback(
        [Output("word-display", "children"),
         Output("lives-display", "children"),
         Output("wrong-display", "children"),
         Output("game-state", "children")],
        [Input("new-game-btn", "n_clicks"),
         Input("guess-btn", "n_clicks")],
        [State("game-state", "children")]
    )
    def update_game(new_clicks, guess_clicks, game_state_json):
        """Update game state based on button clicks"""
        ctx = dash.callback_context
        if not ctx.triggered:
            return "_____", 6, "", '{"word": "", "masked_word": "_____", "lives": 6, "wrong_guesses": [], "game_over": false}'
        
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        
        if game_state_json:
            game_state = json.loads(game_state_json)
        else:
            game_state = {"word": "", "masked_word": "_____", "lives": 6, "wrong_guesses": [], "game_over": False}
        
        if button_id == "new-game-btn":
            # Start new game
            words = ['python', 'machine', 'learning', 'algorithm', 'computer']
            word = random.choice(words)
            game_state = {
                "word": word,
                "masked_word": '_' * len(word),
                "lives": 6,
                "wrong_guesses": [],
                "game_over": False
            }
        elif button_id == "guess-btn" and not game_state.get("game_over", False):
            # Get bot guess
            guess = bot.predict_next_letter(
                game_state['masked_word'], 
                set(game_state['wrong_guesses'])
            )
            
            # Update game state
            word = game_state['word']
            if guess in word:
                new_masked = ""
                for i, char in enumerate(word):
                    if char == guess:
                        new_masked += char
                    else:
                        new_masked += game_state['masked_word'][i]
                game_state['masked_word'] = new_masked
            else:
                game_state['wrong_guesses'].append(guess)
                game_state['lives'] -= 1
            
            # Check game over
            if '_' not in game_state['masked_word']:
                game_state['game_over'] = True
            elif game_state['lives'] <= 0:
                game_state['game_over'] = True
        
        return (game_state['masked_word'], 
                game_state['lives'], 
                ', '.join(game_state['wrong_guesses']),
                json.dumps(game_state))
    
    @app.callback(
        [Output("win-rate", "children"),
         Output("games-played", "children"),
         Output("avg-guesses", "children"),
         Output("simulation-results", "children")],
        [Input("simulate-btn", "n_clicks")]
    )
    def run_simulation(n_clicks):
        """Run bot simulation"""
        if n_clicks == 0:
            return "0%", "0", "0", ""
        
        words = ['python', 'machine', 'learning', 'algorithm', 'computer']
        wins = 0
        total_guesses = 0
        
        for word in words:
            masked_word = '_' * len(word)
            wrong_guesses = set()
            lives = 6
            guesses = 0
            
            while lives > 0 and '_' in masked_word:
                guess = bot.predict_next_letter(masked_word, wrong_guesses)
                guesses += 1
                
                if guess in word:
                    new_masked = ""
                    for i, char in enumerate(word):
                        if char == guess:
                            new_masked += char
                        else:
                            new_masked += masked_word[i]
                    masked_word = new_masked
                else:
                    wrong_guesses.add(guess)
                    lives -= 1
            
            if '_' not in masked_word:
                wins += 1
            total_guesses += guesses
        
        win_rate = round((wins / len(words)) * 100, 1)
        avg_guesses = round(total_guesses / len(words), 1)
        
        results = html.Div([
            html.H3("Simulation Results"),
            html.P(f"Games Played: {len(words)}"),
            html.P(f"Wins: {wins}"),
            html.P(f"Losses: {len(words) - wins}"),
            html.P(f"Win Rate: {win_rate}%"),
            html.P(f"Average Guesses: {avg_guesses}")
        ], style={'backgroundColor': '#f0f8ff', 'padding': '20px', 'borderRadius': '10px', 'margin': '20px'})
        
        return f"{win_rate}%", str(len(words)), str(avg_guesses), results
    
    return app

# =============================================================================
# MAIN EXECUTION
# =============================================================================

def main():
    """Main function to run the web interface"""
    print("Hangman ML Challenge - Web Interface")
    print("=" * 50)
    
    # Load training data
    try:
        with open('training_words.txt', 'r') as f:
            training_words = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print("training_words.txt not found. Using sample words.")
        training_words = ['python', 'machine', 'learning', 'algorithm', 'computer'] * 1000
    
    # Create bot
    bot = HangmanBot(training_words)
    
    # Start Flask app by default (production-ready)
    print("Starting Flask web interface...")
    app = create_flask_app(bot)
    app.run(debug=False, host='0.0.0.0', port=5000)

if __name__ == "__main__":
    main()
