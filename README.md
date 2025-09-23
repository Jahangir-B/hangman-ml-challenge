# Hangman ML Challenge - User Package

A machine learning challenge where you build an intelligent Hangman bot and web interface using Python.

## Challenge Overview

You will implement a machine learning algorithm to create an intelligent Hangman bot, then build a web interface using Flask or Dash to showcase your work. The challenge includes:

- Machine Learning: Train models on 300k+ training words
- Web Development: Build interactive interfaces using Python frameworks
- Competition: Submit your bot for evaluation on hidden test words

## What You Need to Do

**Simple**: Create a Python class that can guess letters in Hangman games AND build a web interface to showcase it!

## Step-by-Step Instructions

### Step 1: Setup Environment

**Clone the Repository**
```bash
# Clone the repository
git clone https://github.com/Dante-of-Chess/hangman-ml-challenge.git

# Install Python dependencies
pip install -r requirements.txt
```

**IMPORTANT**: Before proceeding, **contact the admin to request API access** for project submission. You'll need this access to submit your completed project.


### Step 2: Implement Your Bot
1. Open `user_template.py`
2. Find the `HangmanBot` class
3. Implement these methods:

```python
class HangmanBot:
    def __init__(self, training_words):
        # TODO: Train your model here
        # Load training_words.txt (300K words)
        pass
    
    def predict_next_letter(self, masked_word, wrong_guesses):
        # TODO: Implement your prediction logic here
        # masked_word: "h_ll_" 
        # wrong_guesses: {"x", "y"}
        # return: "o"
        pass
```

### Step 3: Build Web Interface
The starter code includes TWO web interface options:

#### Option A: Flask (Traditional Web App)
- HTML templates embedded in Python
- No separate HTML/CSS/JS files needed
- Interactive game interface
- Performance dashboard

#### Option B: Dash (Pure Python)
- 100% Python - no HTML/CSS/JS at all
- Built-in interactive components
- Automatic charts and graphs
- Modern web interface

**Run the starter:**
```bash
python user_template.py
```

Choose your preferred interface (Flask or Dash) and you'll get:
- Interactive Hangman game
- Performance statistics
- Simulation results

### Step 4: Test Your Bot Thoroughly

**Option A: Quick Success Rate Test (Recommended)**
```bash
python test_bot.py
```
This will:
- Test your bot on sample words automatically
- Calculate win rate and performance metrics
- Show detailed results and success criteria
- Tell you if your bot is ready for API submission

**Option B: Test via Official API (After getting API access)**
```bash
python test_api.py
```
This will:
- Submit your bot to the official API for evaluation
- Monitor evaluation progress in real-time
- Show official results and performance metrics
- Compare against official success criteria

**Option C: Interactive Web Interface**
```bash
python user_template.py
```
This will:
- Launch web interface (Flask or Dash)
- Provide interactive gameplay
- Run simulations through the web UI

**CRITICAL**: Test your bot thoroughly before submission! Use `test_bot.py` for quick validation, then `test_api.py` for official evaluation.

**Only proceed to submission after confirming your bot works correctly!**

### Step 5: Submit Your Project
**Prerequisites**: Your bot must be fully tested and working correctly!

1. Save your complete project (bot + web interface)
2. **Use the API access you requested in Step 1** to submit your project
3. Follow the admin's instructions for checking your results
4. Monitor your performance and rankings

## Machine Learning Approach Ideas

### Beginner (Target: 50-60% hit rate)
```python
# Simple frequency analysis
def predict_next_letter(self, masked_word, wrong_guesses):
    # Count letter frequencies in training data
    # Return most frequent available letter
    pass
```

### Intermediate (Target: 60-70% hit rate)
```python
# Pattern matching + frequency
def predict_next_letter(self, masked_word, wrong_guesses):
    # Find words matching current pattern
    # Use letter frequency within those words
    # Consider word length and position
    pass
```

### Advanced (Target: 70%+ hit rate)
```python
# Machine learning models
def predict_next_letter(self, masked_word, wrong_guesses):
    # Extract features: word length, revealed letters, position patterns
    # Train scikit-learn models (Random Forest, SVM, etc.)
    # Use ensemble methods for better predictions
    pass
```

## Success Metrics

| Component | Points | Target |
|-----------|--------|--------|
| **ML Performance** | 40 | >=70% hit rate |
| **Web Interface** | 30 | Interactive Flask/Dash app |
| **Testing & Validation** | 20 | Comprehensive testing |
| **Code Quality** | 10 | Clean, documented code |

## Files Included

- `user_template.py` - Complete starter template with ML + web interface
- `test_bot.py` - Standalone script to test bot success rate via code
- `test_api.py` - Script to test bot via official API (requires API access)
- `training_words.txt` - Training dataset (300K words)
- `sample_words.txt` - Sample dataset for quick testing (1K words)
- `requirements.txt` - Python dependencies
- `README.md` - This file

## Important Notes

- **Training Data Only**: You can only use the provided training words
- **Hidden Evaluation**: Test words are never revealed to you
- **Fair Competition**: Consistent evaluation for all participants
- **Python Only**: No external languages or frameworks required

## Project Submission

**IMPORTANT**: Contact the admin **from the start** to request API access for project submission.

**Workflow**:
1. **Request API access** before beginning development
2. **Develop and test** your bot thoroughly
3. **Submit** using the provided API access
4. **Monitor** your results and rankings

**Note**: API access is required for submission. Contact the admin early to avoid delays.

## Security & Safety

This repository is designed to be safe and self-contained:
- No hardcoded credentials or keys
- Protected by `.gitignore` to prevent sensitive file commits
- Contact admin for submission access

## Getting Help

- **Request API access from the admin first** - don't wait until the end!
- Check the starter template for examples
- Test your bot thoroughly before submitting
- Use the sample words for quick testing
- Ensure your bot works correctly before submission
- Follow security best practices when working with the repository

Good luck with your Hangman ML Challenge!
