#!/usr/bin/env python3
"""
Hangman Bot API Tester

This script allows you to test your HangmanBot via the actual API once you have
received the API URL and credentials from the admin.

Usage:
    python test_api.py

The script will:
1. Load your HangmanBot from user_template.py
2. Submit it to the API for evaluation
3. Monitor the evaluation progress
4. Display detailed results and performance metrics
"""

import sys
import time
import requests
import json
from pathlib import Path

# Import the HangmanBot from user_template
try:
    from user_template import HangmanBot
except ImportError:
    print("Error: Could not import HangmanBot from user_template.py")
    print("Make sure user_template.py is in the same directory.")
    sys.exit(1)

def get_api_config():
    """Get API configuration from user"""
    print("API Configuration")
    print("=" * 20)
    print("Enter the API details provided by the admin:")
    
    api_url = input("API URL (provided by admin): ").strip()
    if not api_url:
        print("Error: API URL is required")
        sys.exit(1)
    
    # Remove trailing slash if present
    api_url = api_url.rstrip('/')
    
    user_id = input("Your User ID: ").strip()
    if not user_id:
        user_id = "test_user"
        print(f"Using default user ID: {user_id}")
    
    model_name = input("Model Name (optional): ").strip()
    if not model_name:
        model_name = "my_hangman_bot"
        print(f"Using default model name: {model_name}")
    
    return {
        'api_url': api_url,
        'user_id': user_id,
        'model_name': model_name
    }

def submit_bot_to_api(config):
    """Submit the bot to the API for evaluation"""
    print("\nSubmitting bot to API...")
    print("=" * 30)
    
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
    
    # Prepare submission
    files = {
        'files': ('user_template.py', open('user_template.py', 'rb'), 'text/plain')
    }
    
    data = {
        'user_id': config['user_id'],
        'model_name': config['model_name']
    }
    
    try:
        # Submit to API
        response = requests.post(
            f"{config['api_url']}/api/evaluate",
            files=files,
            data=data,
            timeout=30
        )
        
        files['files'][1].close()  # Close the file
        
        if response.status_code == 200:
            result = response.json()
            print(" Submission successful!")
            print(f"Job ID: {result.get('job_id', 'N/A')}")
            print(f"Status: {result.get('status', 'N/A')}")
            print(f"Message: {result.get('message', 'N/A')}")
            print(f"Estimated Time: {result.get('estimated_time', 'N/A')}")
            print(f"Test Words: {result.get('test_words', 'N/A')}")
            return result.get('job_id')
        else:
            print(f" Submission failed!")
            print(f"Status Code: {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f" Network error: {e}")
        return None

def check_job_status(config, job_id):
    """Check the status of a job"""
    try:
        response = requests.get(
            f"{config['api_url']}/api/status/{job_id}",
            timeout=10
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f" Status check failed: {response.status_code}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f" Network error: {e}")
        return None

def wait_for_completion(config, job_id):
    """Wait for job completion and show progress"""
    print(f"\nMonitoring job {job_id}...")
    print("=" * 40)
    
    start_time = time.time()
    last_status = None
    
    while True:
        status_data = check_job_status(config, job_id)
        
        if not status_data:
            print(" Failed to check job status")
            return None
        
        current_status = status_data.get('status', 'unknown')
        
        # Show status change
        if current_status != last_status:
            print(f"Status: {current_status}")
            last_status = current_status
        
        if current_status == 'completed':
            elapsed = time.time() - start_time
            print(f" Job completed in {elapsed:.1f} seconds!")
            return status_data
        elif current_status == 'failed':
            print(" Job failed!")
            return status_data
        elif current_status in ['queued', 'running']:
            # Show progress dots
            print(".", end="", flush=True)
            time.sleep(5)  # Check every 5 seconds
        else:
            print(f"Unknown status: {current_status}")
            time.sleep(5)

def print_api_results(status_data):
    """Print detailed API results"""
    if not status_data:
        return
    
    print("\n" + "=" * 60)
    print("API EVALUATION RESULTS")
    print("=" * 60)
    
    # Basic info
    print(f"Job ID: {status_data.get('job_id', 'N/A')}")
    print(f"User ID: {status_data.get('user_id', 'N/A')}")
    print(f"Model Name: {status_data.get('model_name', 'N/A')}")
    print(f"Status: {status_data.get('status', 'N/A')}")
    
    if 'results' in status_data:
        results = status_data['results']
        
        # Overall performance
        if 'performance' in results:
            perf = results['performance']
            print(f"\nOverall Performance:")
            print(f"Games Played: {perf.get('games_played', 'N/A')}")
            print(f"Wins: {perf.get('wins', 'N/A')}")
            print(f"Losses: {perf.get('losses', 'N/A')}")
            print(f"Win Rate: {perf.get('win_rate', 'N/A')}%")
            print(f"Average Guesses: {perf.get('avg_guesses', 'N/A')}")
            print(f"Total Guesses: {perf.get('total_guesses', 'N/A')}")
        
        # Score
        if 'overall_score' in results:
            print(f"\nOverall Score: {results['overall_score']}/100")
        
        # Performance by word length
        if 'length_performance' in results:
            print(f"\nPerformance by Word Length:")
            print("-" * 30)
            length_perf = results['length_performance']
            for length in sorted(length_perf.keys()):
                data = length_perf[length]
                print(f"Length {length}: {data.get('wins', 0)}/{data.get('total', 0)} ({data.get('win_rate', 0):.1f}%)")
        
        # Sample results
        if 'word_results' in results and results['word_results']:
            print(f"\nSample Results:")
            print("-" * 20)
            for result in results['word_results'][:5]:  # Show first 5
                status = "WON" if result.get('won', False) else "LOST"
                print(f"{result.get('word', 'N/A')}: {status} ({result.get('guesses', 'N/A')} guesses, {result.get('lives_left', 'N/A')} lives left)")
    
    # Success criteria
    print("\n" + "=" * 60)
    print("SUCCESS EVALUATION")
    print("=" * 60)
    
    if 'results' in status_data and 'performance' in status_data['results']:
        win_rate = status_data['results']['performance'].get('win_rate', 0)
        
        if win_rate >= 70:
            print(" EXCELLENT! Your bot meets the advanced target (70%+)")
        elif win_rate >= 60:
            print(" GOOD! Your bot meets the intermediate target (60-70%)")
        elif win_rate >= 50:
            print(" FAIR! Your bot meets the beginner target (50-60%)")
        else:
            print("  NEEDS IMPROVEMENT! Consider enhancing your bot's algorithm")
        
        print(f"\nYour bot achieved {win_rate}% win rate on the official test set")
        
        if win_rate >= 50:
            print("\n Congratulations! Your bot performed well on the official evaluation!")
        else:
            print("\n Consider improving your bot's algorithm before resubmitting")

def main():
    """Main API testing function"""
    print("Hangman Bot API Tester")
    print("=" * 25)
    print("This script will test your bot via the official API")
    print("Make sure you have received API access from the admin first!")
    print()
    
    # Get API configuration
    config = get_api_config()
    
    # Submit bot
    job_id = submit_bot_to_api(config)
    
    if not job_id:
        print(" Failed to submit bot to API")
        sys.exit(1)
    
    # Wait for completion
    results = wait_for_completion(config, job_id)
    
    if results:
        print_api_results(results)
    else:
        print(" Failed to get results")

if __name__ == "__main__":
    main()
