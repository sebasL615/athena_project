import re
import nltk
from nltk.chat.util import Chat, reflections
from datetime import datetime, timedelta
import random
import requests

# Updated Vocabulary words and definitions
vocabulary = {
    "cogitate": "to think deeply",
    "effervescent": "bubbling, lively",
    "halcyon": "calm, peaceful",
    "labyrinthine": "complicated, maze-like",
    "serendipity": "finding something good without looking for it",
    "ephemeral": "lasting for a very short time",
    "luminescent": "emitting light not caused by heat",
    "perspicacious": "having a ready insight into and understanding of things",
    "quintessential": "representing the most perfect or typical example of a quality or class",
    "verdant": "green with grass or other rich vegetation"
}

# Motivational quotes
quotes = [
    "The only limit to our realization of tomorrow is our doubts of today. - Franklin D. Roosevelt",
    "The future belongs to those who believe in the beauty of their dreams. - Eleanor Roosevelt",
    "Do not wait to strike till the iron is hot; but make it hot by striking. - William Butler Yeats",
    "The best time to plant a tree was 20 years ago. The second best time is now. - Chinese Proverb",
    "Your time is limited, so don't waste it living someone else's life. - Steve Jobs",
    "The harder you work for something, the greater you’ll feel when you achieve it.",
    "Dream big and dare to fail. - Norman Vaughan",
    "Don't watch the clock; do what it does. Keep going. - Sam Levenson",
    "Keep your face always toward the sunshine—and shadows will fall behind you. - Walt Whitman",
    "Act as if what you do makes a difference. It does. - William James"
]

# Workout progress tracking
workout_log = []

def log_workout(workout):
    workout_log.append(workout)
    print(f"Workout logged: {workout}")

def get_workout_log():
    return workout_log

# Goal tracking
goals = []

def set_goal(goal):
    goals.append(goal)
    print(f"Goal set: {goal}")

def get_goals():
    return goals

# Search function using DuckDuckGo API
def search_web(query):
    response = requests.get(f"https://api.duckduckgo.com/?q={query}&format=json")
    if response.status_code == 200:
        data = response.json()
        return data.get('Abstract', 'No abstract found')
    else:
        return "Failed to retrieve results"

# Pairs with keywords and freeform text handling
pairs = [
    [
        r"my name is (.*)",
        ["Hello %1, how are you today?",]
    ],
    [
        r"hi|hey|hello",
        ["Hello!", "Hey there!", "Hi! How can I assist you today?"]
    ],
    [
        r"good morning",
        ["Good morning! Did you sleep well?"]
    ],
    [
        r"good afternoon",
        ["Good afternoon! How's your day going?"]
    ],
    [
        r"good evening",
        ["Good evening! Relaxing or working late?"]
    ],
    [
        r"howdy|what's up",
        ["Howdy! How can I help you today?", "Hey! What's up?", "What can I do for you?"]
    ],
    [
        r"(.*) your name?",
        ["I am Athena, created by Sebastian.",]
    ],
    [
        r"(.*) how are you?",
        ["I'm doing good, how about you?",]
    ],
    [
        r"tell me about (.*)",
        ["AI, or Artificial Intelligence, is the simulation of human intelligence in machines. What aspect of AI interests you?",]
    ],
    [
        r"what's the capital of (.*)",
        ["The capital of France is Paris.",]
    ],
    [
        r"how do I (.*)",
        ["To make a cup of coffee: Grind coffee beans, boil water, pour over grounds in a filter, and let it brew. Enjoy!",]
    ],
    [
        r"i completed (.*) workout",
        ["Great job on completing %1 workout!", lambda groups: log_workout(groups[0])]
    ],
    [
        r"show my workout log",
        ["Here are your workouts: " + ', '.join(get_workout_log()),]
    ],
    [
        r"quiz me on a word",
        [random.choice(list(vocabulary.keys())),]
    ],
    [
        r"what is the definition of (.*)",
        ["%1 means " + vocabulary.get("%1", "I don't know that word."),]
    ],
    [
        r"use (.*) in a sentence",
        ["Sure! 'She found herself in a %1 situation, where everything seemed overly complex.'",]
    ],
    [
        r"set a goal to (.*)",
        ["Goal set: %1", lambda groups: set_goal(groups[0])]
    ],
    [
        r"show my goals",
        ["Here are your goals: " + ', '.join(get_goals()),]
    ],
    [
        r"give me a quote",
        [random.choice(quotes),]
    ],
    [
        r"search (.*)",
        [lambda groups: "Here's what I found: " + search_web(groups[0])]
    ],
    [
        r"date",
        ["The current date is %1.",]
    ],
    [
        r"time",
        ["The current time is %1.",]
    ],
    [
        r"sorry (.*)",
        ["No worries", "It's okay",]
    ],
    [
        r"bye|goodbye|quit",
        ["Bye!", "Goodbye! It was nice talking to you"]
    ],
]

def correct_grammar(text):
    corrections = {
        r'\byour\b': 'you\'re',
        r'\byou\'re\b': 'your',
        r'\btheir\b': 'they\'re',
        r'\bthey\'re\b': 'their',
        r'\bthere\b': 'their',
        r'\bthen\b': 'than',
        r'\bthan\b': 'then'
    }
    for pattern, replacement in corrections.items():
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    return text

def get_current_date():
    return datetime.now().strftime("%Y-%m-%d")

def get_current_time():
    return datetime.now().strftime("%I:%M %p")

def chat():
    current_date = get_current_date()
    current_time = get_current_time()
    motivational_quote = random.choice(quotes)
    greeting = f"Hi! I am Athena. Today is {current_date} and the current time is {current_time}. Here’s a quote to get you started: '{motivational_quote}'. Type 'bye', 'goodbye', or 'quit' to exit"
    print(greeting)
    
    chatbot = Chat(pairs, reflections)
    while True:
        try:
            user_input = input(">")
            if user_input.lower() in ["bye", "goodbye", "quit"]:
                bye_message = "Bye!"
                print(bye_message)
                break
            corrected_input = correct_grammar(user_input)

            if "date" in corrected_input.lower():
                date_response = f"The current date is {get_current_date()}"
                print(date_response)
                continue
            elif "time" in corrected_input.lower():
                time_response = f"The current time is {get_current_time()}"
                print(time_response)
                continue

            response = chatbot.respond(corrected_input)
            print(response)

        except Exception as e:
            print(f"An error occurred: {e}")
            break

if __name__ == "__main__":
    chat()
