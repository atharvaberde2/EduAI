# -*- coding: utf-8 -*-
"""
Created on Thu Mar 27 14:59:55 2025


@author: athar
"""

import flask
from flask import request, jsonify, render_template, session
import google.generativeai as genai
import os
from flask_cors import CORS
import openai
from dotenv import load_dotenv
# Initialize Flask app
app = flask.Flask(__name__, template_folder='templates')
CORS(app, resources={r"/*": {"origins": "*"}})
app.secret_key = os.urandom(24)
genai.configure(api_key=”")
load_dotenv() 
#genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

openai.api_key = os.getenv("OPENAI_API_KEY")
game_data = {}


model = genai.GenerativeModel("gemini-1.5-pro")
system_prompt = (
    "You are playing charades with the user. Follow these rules:\n"
    "- Ask the user to pick a topic first.\n"
    "- Once they pick a topic, secretly choose a word related to it.\n"
    "- Give the user a hint, but do NOT reveal the word.\n"
    "- The user gets 3 attempts to guess. If they fail, reveal the word.\n"
    "- If they guess correctly, they get 1 point.\n"
    "- Then, it's the AI's turn. The user will pick a word and give hints.\n"
    "- The AI gets 3 tries to guess.\n"
    "- First to reach 5 points wins.\n"
    "- Keep track of hints and scores.\n"
    "Once the topic is chosen, keep it consistent throughout the game for all rounds.\n"
    "When user gets the word correct, say 'You are correct! and add 1 point to the user score.\n"
    "When AI gets the word correct, say 'Great I got it' and add 1 point to the AI score.\n"
    "Do NOT ask the user to pick the topic again once it's selected.\n"
)

prompt_detective = (''' You are an AI narrator inside an interactive detective learning game. There is a mystery to solve, and you know the answer. The user (player) does not know the answer.
Objective:
First, ask the user to choose a topic (e.g., math, physics, history, or any topic of their choice).
Generate clues based on the chosen topic in the form of quiz questions.
If the player answers correctly, reveal one part of the mystery and progress the story.
If the player answers incorrectly, provide a hint or an easier fallback question, and allow them to try again.
Once enough clues are solved, allow the player to make a final guess to solve the mystery. give minimum 5 clues

''')

messages = [{"role": "system", "content": system_prompt}]
prompt_sam = ''' Hi! You’re here to help me with homework, no matter the subject. Your approach is simple and supportive:
You’ll start by giving me a helpful hint and let me try it out on my own.
If I get stuck, you’ll walk me through the first step and guide me from there.
You focus on making sure I understand each part before moving on—because real learning happens step by step.
Need help figuring out where I went wrong? You can review my solution, explain what happened, and guide me through how to fix it. Example 1:
User: "I'm struggling with quadratic equations. How do I solve them?"
Bot: "Here's a hint: Start by setting the equation equal to zero, and see if you can factor it. If factoring is tough, you can use the quadratic formula. Let me know if you'd like help with that approach!"
Example 2:
User: "I'm not sure how to approach this geometry problem."
Bot: "No problem! First, think about the properties of the shapes involved. Try drawing the diagram to visualize the problem. Once you've done that, let's talk about the next step together!" '''

prompt_joe = '''You're here to teach me concepts from the ground up.
Your goal is to take complex ideas and break them down into simple, easy-to-understand pieces.
Think of it this way: You'll take one big, heavy rock of a concept and break it into smaller, manageable stones—each one clear and approachable. No matter how tricky the topic seems, you'll make sure it clicks for me. Explain like you are explaing a 10 year old. Make maximum 100 words for each explanation. ---
'''

prompt_russ = ''' I have a disability. I prefer using visuals to learn. Explain to me as if I am a 2-year-old. Use toys, colorful visuals, or objects to help me understand. Please be very patient and adapt to how I respond. Speak kindly and slowly. If I get confused, try again in a different way.
You're a compassionate and inclusive tutor designed for someone with a disability who learns visually and needs very simple, toddler-level explanations. Always:
Use metaphors with toys, animals, food, or real-world objects.
Create visual examples or describe what you’d draw (e.g., “Imagine a red ball rolling down a blue ramp”).
Break things into one clear idea at a time.
Encourage and validate often ("You’re doing great!", “Let’s try again together.”).
Rephrase if the learner seems unsure.
Match your message to that of a loving preschool teacher: gentle, calm, and positive.'''

chat_sam = model.start_chat(history=[
    {"role": "user", "parts": [prompt_sam]}
])

chat_joe = model.start_chat(history = [{"role": "user", "parts": [prompt_joe]}])
chat_russell = model.start_chat(history = [{"role": "user", "parts": [prompt_russ]}])
chat_detective = model.start_chat(history=[{"role": "user", "parts": [prompt_detective]}])
user_score = 0
ai_score = 0
game_state = {
    "user_score": 0,
    "ai_score": 0,
    "current_word": None,
    "user_selected_word": None,
    "turn": "AI",  # AI starts first
}
game_topic = None


def get_ai_response(prompt):
    """Helper function to call OpenAI's GPT-4 for responses."""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "You are playing a text-based charades game."},
                  {"role": "user", "content": prompt}]
    )
    return response["choices"][0]["message"]["content"].strip()


@app.route("/")
def index():
    return render_template("index (2).html")


@app.route("/tutor.html", methods=["GET", "POST"])
def tutor():
    return render_template("tutor.html")  # Ensure tutor.html exists in templates/

@app.route("/sam.html", methods=["GET", "POST"])
def sam():
    return render_template("sam.html") 

@app.route("/sam-chat.html", methods=["GET", "POST"])
def sam_chat():
    return render_template("sam-chat.html")

@app.route("/samChat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message", "")

    if not user_message:
        return jsonify({"error": "Message cannot be empty"}), 400

    try:
        #response = model.generate_content(prompt_sam + "\n" + user_message)
        response = chat_sam.send_message(user_message)
        return jsonify({"response": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/joe.html", methods=["GET", "POST"])
def joe():
    return render_template("joe.html") 

@app.route("/joe-chat.html", methods=["GET", "POST"])
def joe_chat():
    return render_template("joe-chat.html") 

@app.route("/joeChat", methods=["POST", "GET"])
def joechat():
    data = request.json
    user_message = data.get("message", "")

    if not user_message:
        return jsonify({"error": "Message cannot be empty"}), 400

    try:
        response = chat_joe.send_message(user_message)
        return jsonify({"response": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/russell.html", methods=["GET", "POST"])
def russell():
    return render_template("russell.html")

@app.route("/russell-chat.html", methods=["GET", "POST"])
def russell_chat():
    return render_template("russell-chat.html")

@app.route("/russellChat", methods=["POST", "GET"])
def russell_chat_handler():
    data = request.json
    user_message = data.get("message", "")

    if not user_message:
        return jsonify({"error": "Message cannot be empty"}), 400

    try:
        response = chat_russell.send_message(user_message)
        return jsonify({"response": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/game-page.html", methods=["GET", "POST"])
def game():
    return render_template("game-page (4).html")


@app.route("/charades.html", methods=["GET", "POST"])
def charades():
    return render_template("charades.html")

@app.route("/charadesGame1", methods=["POST", "GET"])
def charadesGame():
    global user_score, ai_score, messages


    data = request.json
    user_message = data.get("message", "").strip()


    if not user_message:
        return jsonify({"error": "No message provided."}), 400


    if user_message.lower() in ["exit", "quit", "stop"]:
        return jsonify({"response": "Game over. Thanks for playing!"})


    # Add user's message
    messages.append({"role": "user", "content": user_message})


    try:
        # Get AI response
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",
            messages=messages,
            temperature=0.7
        )


        ai_message = response["choices"][0]["message"]["content"]
        messages.append({"role": "assistant", "content": ai_message})


        # Update scores based on AI response content
        if "you are correct" in ai_message.lower():
            user_score += 1
        if "great, i got it" in ai_message.lower():
            ai_score += 1


        if user_score >= 5:
            ai_message += "\n\n🎉 Congratulations! You win the game!"
            user_score = 0
            ai_score = 0
        elif ai_score >= 5:
            ai_message += "\n\n🤖 AI wins the game! Better luck next time."
            user_score = 0
            ai_score = 0


        return jsonify({
            "response": ai_message,
            "user_score": user_score,
            "ai_score": ai_score
        })


    except Exception as e:
        import traceback
        traceback.print_exc()  # Logs the full error to terminal
        return jsonify({"error": str(e)}), 500

def get_ai_response(prompt):
    """Helper function to call OpenAI's GPT-4 for responses."""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "You are playing a text-based charades game."},
                  {"role": "user", "content": prompt}]
    )
    return response["choices"][0]["message"]["content"].strip()



    
@app.route("/detective.html", methods = ["GET", "POST"])
def detective():
    return render_template("detective.html")

@app.route('/detectiveChat', methods = ["GET", "POST"])
def detective_game():
    data = request.json
    user_message = data.get("message", "")

    if not user_message:
        return jsonify({"error": "Message cannot be empty"}), 400

    try:
        response = chat_detective.send_message(user_message)
        return jsonify({"response": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500



if __name__ == "__main__":
    app.run(debug = True, port = 5000, host='0.0.0.0')
