#!/usr/bin/env python3
"""
Hangman Bot Success Rate Tester

This script allows you to test your HangmanBot's success rate directly via code
without needing to use the web interface. Perfect for quick testing and validation.

Usage:
    python test_bot.py

The script will:
1. Load your HangmanBot from user_template.py
2. Test it on sample words
3. Calculate win rate and performance metrics
4. Display detailed results
"""

import sys
import random
from pathlib import Path

# Import the HangmanBot from user_template
try:
    from user_template import HangmanBot
except ImportError:
    print("Error: Could not import HangmanBot from user_template.py")
    print("Make sure user_template.py is in the same directory.")
    sys.exit(1)

def load_test_words():
    """Load words for testing"""
    # Try to load sample words first (smaller set for quick testing)
    try:
        with open('sample_words.txt', 'r') as f:
            words = [line.strip().lower() for line in f if line.strip()]
        print(f"Loaded {len(words)} sample words for testing")
        return words
    except FileNotFoundError:
        print("sample_words.txt not found, using default test words")
        return ['python', 'machine', 'learning', 'algorithm', 'computer', 'hangman', 
                'programming', 'artificial', 'intelligence', 'neural', 'network']

def simulate_hangman_game(bot, word, max_lives=6):
    """
    Simulate a single Hangman game
    
    Args:
        bot: HangmanBot instance
        word: Word to guess
        max_lives: Maximum number of wrong guesses allowed
    
    Returns:
        dict: Game results
    """
    masked_word = '_' * len(word)
    wrong_guesses = set()
    lives = max_lives
    guesses = 0
    
    while lives > 0 and '_' in masked_word:
        # Get bot's prediction
        guess = bot.predict_next_letter(masked_word, wrong_guesses)
        guesses += 1
        
        # Check if guess is correct
        if guess in word:
            # Update masked word
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
    
    # Determine result
    won = '_' not in masked_word
    lives_left = lives
    
    return {
        'word': word,
        'won': won,
        'guesses': guesses,
        'lives_left': lives_left,
        'final_masked': masked_word
    }

def test_bot_performance(bot, test_words, num_tests=None):
    """
    Test bot performance on a set of words
    
    Args:
        bot: HangmanBot instance
        test_words: List of words to test
        num_tests: Number of tests to run (None for all words)
    
    Returns:
        dict: Performance statistics
    """
    if num_tests:
        test_words = random.sample(test_words, min(num_tests, len(test_words)))
    
    results = []
    wins = 0
    total_guesses = 0
    
    print(f"\nTesting bot on {len(test_words)} words...")
    print("=" * 50)
    
    for i, word in enumerate(test_words, 1):
        result = simulate_hangman_game(bot, word)
        results.append(result)
        
        if result['won']:
            wins += 1
        total_guesses += result['guesses']
        
        # Show progress for every 50th word (less verbose)
        if i % 50 == 0 or i == len(test_words):
            current_win_rate = (wins / i) * 100
            print(f"Progress: {i}/{len(test_words)} | Win Rate: {current_win_rate:.1f}%")
    
    # Calculate final statistics
    win_rate = (wins / len(test_words)) * 100
    avg_guesses = total_guesses / len(test_words)
    
    return {
        'total_tests': len(test_words),
        'wins': wins,
        'losses': len(test_words) - wins,
        'win_rate': win_rate,
        'avg_guesses': avg_guesses,
        'total_guesses': total_guesses,
        'results': results
    }

def print_detailed_results(stats):
    """Print detailed test results"""
    print("\n" + "=" * 60)
    print("HANGMAN BOT PERFORMANCE RESULTS")
    print("=" * 60)
    
    print(f"Total Tests: {stats['total_tests']}")
    print(f"Wins: {stats['wins']}")
    print(f"Losses: {stats['losses']}")
    print(f"Win Rate: {stats['win_rate']:.1f}%")
    print(f"Average Guesses: {stats['avg_guesses']:.1f}")
    print(f"Total Guesses: {stats['total_guesses']}")
    
    # Performance by word length
    print("\nPerformance by Word Length:")
    print("-" * 30)
    length_stats = {}
    for result in stats['results']:
        length = len(result['word'])
        if length not in length_stats:
            length_stats[length] = {'total': 0, 'wins': 0}
        length_stats[length]['total'] += 1
        if result['won']:
            length_stats[length]['wins'] += 1
    
    for length in sorted(length_stats.keys()):
        data = length_stats[length]
        win_rate = (data['wins'] / data['total']) * 100
        print(f"Length {length}: {data['wins']}/{data['total']} ({win_rate:.1f}%)")
    
    # Show some example results
    print("\nExample Results:")
    print("-" * 20)
    for result in stats['results'][:5]:  # Show first 5 results
        status = "WON" if result['won'] else "LOST"
        print(f"{result['word']}: {status} ({result['guesses']} guesses, {result['lives_left']} lives left)")

def main():
    """Main testing function"""
    print("Hangman Bot Success Rate Tester")
    print("=" * 40)
    
    # Load training data
    try:
        with open('training_words.txt', 'r') as f:
            training_words = [line.strip() for line in f if line.strip()]
        print(f"Loaded {len(training_words)} training words")
    except FileNotFoundError:
        print("training_words.txt not found. Using sample words.")
        training_words = ['python', 'machine', 'learning', 'algorithm', 'computer'] * 1000
    
    # Create bot
    print("Initializing HangmanBot...")
    bot = HangmanBot(training_words)
    
    # Load test words
    test_words = load_test_words()
    
    # Test configuration (production-ready defaults)
    print(f"\nTest Configuration:")
    print(f"Available test words: {len(test_words)}")
    
    # Use reasonable default for production
    num_tests = min(100, len(test_words))  # Test up to 100 words by default
    print(f"Testing {num_tests} words (production default)")
    
    # Run tests
    stats = test_bot_performance(bot, test_words, num_tests)
    
    # Print results
    print_detailed_results(stats)
    
    # Success criteria
    print("\n" + "=" * 60)
    print("SUCCESS CRITERIA")
    print("=" * 60)
    
    if stats['win_rate'] >= 70:
        print(" EXCELLENT! Your bot meets the advanced target (70%+)")
    elif stats['win_rate'] >= 60:
        print(" GOOD! Your bot meets the intermediate target (60-70%)")
    elif stats['win_rate'] >= 50:
        print(" FAIR! Your bot meets the beginner target (50-60%)")
    else:
        print("  NEEDS IMPROVEMENT! Consider enhancing your bot's algorithm")
    
    print(f"\nYour bot achieved {stats['win_rate']:.1f}% win rate")
    
    if stats['win_rate'] >= 50:
        print("\n Your bot is ready for API submission!")
    else:
        print("\n Improve your bot before submitting to the API")

if __name__ == "__main__":
    main()
