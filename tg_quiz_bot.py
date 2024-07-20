import telebot
from telebot.types import PollAnswer
import time
import random
from collections import defaultdict
import threading
import json

# Bot initialization with the provided token
bot = telebot.TeleBot('BOT API')

# List of authorized user IDs (replace these with actual user IDs)
AUTHORIZED_USERS = [user id]

# The specific chat ID where quizzes will be sent
QUIZ_CHAT_ID = chat id

# Quiz questions
quiz_questions = [
    {
        "question": "Put question here",
        "answer": "No/Yes", ## Choose whether Yes or No answer only
        "hint": "Hint" ## This will display if answered wrong.
    },
]
# Function to add 'options' key to questions
def add_options_to_questions():
    for question in quiz_questions:
        if 'options' not in question:
            question['options'] = ["Yes", "No"]

# Add options to all questions
add_options_to_questions()

# Global variables for quiz session
quiz_session_active = False
user_scores = defaultdict(int)
quiz_count = 0
poll_answers = {}
session_questions = []

def validate_questions():
    """
    Validates the format of all questions and prints any issues found.
    """
    for i, question in enumerate(quiz_questions):
        if not isinstance(question, dict):
            print(f"Error: Question {i} is not a dictionary.")
            continue
        for key in ['question', 'options', 'answer', 'hint']:
            if key not in question:
                print(f"Error: Question {i} is missing the '{key}' key.")
        if 'options' in question and not isinstance(question['options'], list):
            print(f"Error: 'options' for question {i} is not a list.")
        if 'options' in question and 'answer' in question and question['answer'] not in question['options']:
            print(f"Error: The answer for question {i} is not in the options list.")

def select_quiz_questions():
    """
    Selects 5 unique random questions for the quiz session.
    """
    global session_questions
    session_questions = random.sample(quiz_questions, min(5, len(quiz_questions)))

def send_quiz():
    """
    Sends a single quiz question to the designated chat.
    Uses the pre-selected questions for the session.
    """
    global quiz_count
    if quiz_count < len(session_questions):
        question = session_questions[quiz_count]
        try:
            options = question['options']
            correct_option_id = options.index(question['answer'])
            
            sent_poll = bot.send_poll(
                chat_id=QUIZ_CHAT_ID,
                question=question['question'],
                options=options,
                type='quiz',
                correct_option_id=correct_option_id,
                is_anonymous=False,
                explanation=question['hint']
            )
            
            quiz_count += 1
            
            # Store the correct answer
            poll_answers[sent_poll.poll.id] = correct_option_id
        except KeyError as e:
            print(f"Error: Missing key in question {quiz_count}: {e}")
            print(f"Problematic question: {json.dumps(question, indent=2)}")
        except ValueError as e:
            print(f"Error: Incorrect value in question {quiz_count}: {e}")
            print(f"Problematic question: {json.dumps(question, indent=2)}")

@bot.poll_answer_handler()
def handle_poll_answer(poll_answer: PollAnswer):
    """
    Handles user responses to polls.
    If the answer is correct, increments the user's score.
    """
    if quiz_session_active and poll_answer.poll_id in poll_answers:
        correct_option_id = poll_answers[poll_answer.poll_id]
        if poll_answer.option_ids[0] == correct_option_id:
            user_scores[poll_answer.user.id] += 1

def start_quiz_session():
    """
    Starts a new quiz session.
    Selects 5 unique questions, then sends them over 10 minutes.
    """
    global quiz_session_active, user_scores, quiz_count, poll_answers
    quiz_session_active = True
    user_scores.clear()
    quiz_count = 0
    poll_answers.clear()
    
    select_quiz_questions()  # Select questions for this session
    
    bot.send_message(QUIZ_CHAT_ID, "SOFA.org Quiz session starting! 5 quizzes will be sent over the next 10 minutes.")
    
    # Schedule 5 quizzes, one every 2 minutes
    for i in range(5):
        threading.Timer(i * 2 * 60, send_quiz).start()
    
    # Schedule the end of the session after 10 minutes
    threading.Timer(10 * 60, end_quiz_session).start()

def end_quiz_session():
    """
    Ends the current quiz session.
    Calculates and sends the final scores to the chat.
    """
    global quiz_session_active
    quiz_session_active = False
    
    # Prepare and send the score summary
    summary = "SOFA.org Quiz session ended! Here are the scores:\n\n"
    for user_id, score in user_scores.items():
        user = bot.get_chat_member(QUIZ_CHAT_ID, user_id).user
        summary += f"{user.first_name}: {score} correct answers\n"
    
    bot.send_message(QUIZ_CHAT_ID, summary)

def is_authorized(user_id):
    """
    Checks if the user is authorized to use the bot.
    """
    return user_id in AUTHORIZED_USERS

@bot.message_handler(commands=['start'])
def start(message):
    """
    Handles the /start command.
    Sends a welcome message explaining how to use the bot, but only to authorized users.
    """
    if is_authorized(message.from_user.id):
        bot.reply_to(message, "Welcome to the SOFA.org Quiz Bot! Use /startquiz to start a 10-minute quiz session with 5 quizzes about SOFA.org.")
    else:
        bot.reply_to(message, "Sorry, you are not authorized to use this bot.")

@bot.message_handler(commands=['startquiz'])
def start_quiz(message):
    """
    Handles the /startquiz command.
    Starts a new quiz session if one is not already active, but only for authorized users.
    """
    global quiz_session_active
    if is_authorized(message.from_user.id):
        if not quiz_session_active:
            start_quiz_session()
        else:
            bot.reply_to(message, "A quiz session is already active. Please wait for it to finish.")
    else:
        bot.reply_to(message, "Sorry, you are not authorized to start a quiz session.")

# Validate questions before starting the bot
print("Validating questions...")
validate_questions()

# Start the bot
print("Starting bot...")
bot.infinity_polling(timeout=10, long_polling_timeout = 5)