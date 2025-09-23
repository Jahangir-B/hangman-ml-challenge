# Hangman ML Challenge - Student Package

A machine learning challenge where you build an intelligent Hangman bot and web interface using Python.

## Challenge Overview

You will implement a machine learning algorithm to create an intelligent Hangman bot, then build a web interface using Flask or Dash to showcase your work. The challenge includes:

- Machine Learning: Train models on 176K+ training words
- Web Development: Build interactive interfaces using Python frameworks
- Competition: Submit your bot for evaluation on hidden test words
- Leaderboard: Real-time ranking system

## What You Need to Do

**Simple**: Create a Python class that can guess letters in Hangman games AND build a web interface to showcase it!

## Step-by-Step Instructions

### Step 1: Setup Environment

**Option A: Clone the Instructor Repository**
```bash
# Clone the instructor repository
git clone https://github.com/Dante-of-Chess/hangman-ml-challenge-instructor.git
cd hangman-ml-challenge-instructor/student-package

# Install Python dependencies
pip install -r requirements.txt
```

**Option B: Download Student Package**
```bash
# Download the student package zip file
# Extract and navigate to the folder
pip install -r requirements.txt
```

### Step 2: Implement Your Bot
1. Open `student_template.py`
2. Find the `HangmanBot` class
3. Implement these methods:

```python
class HangmanBot:
    def __init__(self, training_words):
        # TODO: Train your model here
        # Load training_words.txt (176K words)
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
python student_template.py
```

Choose your preferred interface (Flask or Dash) and you'll get:
- Interactive Hangman game
- Real-time bot predictions
- Performance statistics
- Simulation results

### Step 4: Test Your Bot
```bash
python student_template.py
```

This will:
- Test your bot on sample words
- Launch web interface
- Show win rate and performance
- Provide interactive gameplay

### Step 5: Submit Your Project
1. Save your complete project (bot + web interface)
2. **Contact the instructor for API credentials** to submit your project
3. Once you receive the API endpoint, submit via:
   ```bash
   curl -X POST [API_ENDPOINT]/api/evaluate \
     -F "files=@my_project.py" \
     -F "student_id=your_name" \
     -F "model_name=my_bot"
   ```
4. Check your results:
   ```bash
   curl [API_ENDPOINT]/api/status/job_id
   ```

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

- `student_template.py` - Complete starter template with ML + web interface
- `training_words.txt` - Training dataset (176K words)
- `sample_words.txt` - Sample dataset for quick testing (1K words)
- `requirements.txt` - Python dependencies
- `README.md` - This file

## Important Notes

- **Training Data Only**: You can only use the provided training words
- **Hidden Evaluation**: Test words are never revealed to you
- **Fair Competition**: Consistent evaluation for all participants
- **Python Only**: No external languages or frameworks required

## API Endpoint

**IMPORTANT**: Contact the instructor to obtain the API endpoint for project submission.

**Note**: The API endpoint is not included in this repository for security reasons. Please reach out to the instructor for the submission URL and any required credentials.

## Security & Safety

This repository is designed to be safe and self-contained:
- No hardcoded credentials or API keys
- Protected by `.gitignore` to prevent sensitive file commits
- Contact instructor for API endpoints

## Getting Help

- Check the starter template for examples
- Test your bot locally before submitting
- Use the sample words for quick testing
- Submit early and often to see your progress
- Follow security best practices when working with the repository

Good luck with your Hangman ML Challenge!
