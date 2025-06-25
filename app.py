# -*- coding: utf-8 -*-
import flask
from flask import request, jsonify, render_template, session
import google.generativeai as genai
import os
from flask_cors import CORS
from dotenv import load_dotenv
import time

# Initialize Flask app
app = flask.Flask(__name__, template_folder='templates')
CORS(app, resources={r"/*": {"origins": "*"}})
app.secret_key = os.environ.get('SECRET_KEY', os.urandom(24))

load_dotenv() 

# Configure API keys with proper environment variable names for Vercel
genai.configure(api_key=os.environ.get("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY"))

# System prompts
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

prompt_detective = '''You are an AI narrator inside an interactive detective learning game. There is a mystery to solve, and you know the answer. The user (player) does not know the answer.
Objective:
First, ask the user to choose a topic (e.g., math, physics, history, or any topic of their choice).
Generate clues based on the chosen topic in the form of quiz questions.
If the player answers correctly, reveal one part of the mystery and progress the story.
If the player answers incorrectly, provide a hint or an easier fallback question, and allow them to try again.
Once enough clues are solved, allow the player to make a final guess to solve the mystery. give minimum 5 clues'''

prompt_sam = '''Hi! You're here to help me with homework, no matter the subject. Your approach is simple and supportive:
You'll start by giving me a helpful hint and let me try it out on my own.
If I get stuck, you'll walk me through the first step and guide me from there.
You focus on making sure I understand each part before moving on—because real learning happens step by step.
Need help figuring out where I went wrong? You can review my solution, explain what happened, and guide me through how to fix it. Example 1:
User: "I'm struggling with quadratic equations. How do I solve them?"
Bot: "Here's a hint: Start by setting the equation equal to zero, and see if you can factor it. If factoring is tough, you can use the quadratic formula. Let me know if you'd like help with that approach!"
Example 2:
User: "I'm not sure how to approach this geometry problem."
Bot: "No problem! First, think about the properties of the shapes involved. Try drawing the diagram to visualize the problem. Once you've done that, let's talk about the next step together!"'''

prompt_joe = '''You're here to teach me concepts from the ground up.
Your goal is to take complex ideas and break them down into simple, easy-to-understand pieces.
Think of it this way: You'll take one big, heavy rock of a concept and break it into smaller, manageable stones—each one clear and approachable. No matter how tricky the topic seems, you'll make sure it clicks for me. Explain like you are explaining a 10 year old. Make maximum 100 words for each explanation.'''

prompt_russ = '''I have a disability. I prefer using visuals to learn. Explain to me as if I am a 2-year-old. Use toys, colorful visuals, or objects to help me understand. Please be very patient and adapt to how I respond. Speak kindly and slowly. If I get confused, try again in a different way.
You're a compassionate and inclusive tutor designed for someone with a disability who learns visually and needs very simple, toddler-level explanations. Always:
Use metaphors with toys, animals, food, or real-world objects.
Create visual examples or describe what you'd draw (e.g., "Imagine a red ball rolling down a blue ramp").
Break things into one clear idea at a time.
Encourage and validate often ("You're doing great!", "Let's try again together.").
Rephrase if the learner seems unsure.
Match your message to that of a loving preschool teacher: gentle, calm, and positive.'''

def get_gemini_response(prompt_type, user_message, context=""):
    """Generate AI response using Gemini (stateless)"""
    try:
        model = genai.GenerativeModel("gemini-1.5-pro")
        
        prompts = {
            'sam': prompt_sam,
            'joe': prompt_joe,
            'russell': prompt_russ,
            'detective': prompt_detective,
            'charades': system_prompt
        }
        
        system_prompt_text = prompts.get(prompt_type, "You are a helpful AI assistant.")
        full_prompt = f"{system_prompt_text}\n\n{context}\n\nUser: {user_message}\n\nAssistant:"
        
        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        print(f"Error generating AI response: {e}")
        return f"I'm having trouble connecting right now. Please try again. Error: {str(e)}"

@app.route("/")
def index():
    return render_template("index (2).html")

@app.route("/tutor.html", methods=["GET", "POST"])
def tutor():
    return render_template("tutor.html")

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
        response = get_gemini_response('sam', user_message)
        return jsonify({"response": response})
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
        response = get_gemini_response('joe', user_message)
        return jsonify({"response": response})
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
        response = get_gemini_response('russell', user_message)
        return jsonify({"response": response})
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
    data = request.json
    user_message = data.get("message", "").strip()
    user_score = data.get("user_score", 0)
    ai_score = data.get("ai_score", 0)
    topic = data.get("topic", "General Knowledge")

    if not user_message:
        return jsonify({"error": "No message provided."}), 400

    if user_message.lower() in ["exit", "quit", "stop"]:
        return jsonify({"response": "Game over. Thanks for playing!"})

    try:
        context = f"Topic: {topic}\nUser Score: {user_score}\nAI Score: {ai_score}"
        ai_message = get_gemini_response('charades', user_message, context)

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
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@app.route("/detective.html", methods=["GET", "POST"])
def detective():
    return render_template("detective.html")

@app.route('/detectiveChat', methods=["GET", "POST"])
def detective_game():
    data = request.json
    user_message = data.get("message", "")

    if not user_message:
        return jsonify({"error": "Message cannot be empty"}), 400

    try:
        response = get_gemini_response('detective', user_message)
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/gameChat', methods=["GET", "POST"])
def game_chat():
    """Generic game chat endpoint"""
    data = request.json
    user_message = data.get("message", "")
    game_type = data.get("game_type", "general")

    if not user_message:
        return jsonify({"error": "Message cannot be empty"}), 400

    try:
        if game_type == "charades":
            return charadesGame()
        elif game_type == "detective":
            return detective_game()
        else:
            response = get_gemini_response('joe', user_message)
            return jsonify({"response": response})
            
    except Exception as e:
        print(f"Error in game chat: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/debug')
def debug():
    return {
        'gemini_key_set': bool(os.environ.get('GEMINI_API_KEY') or os.getenv('GOOGLE_API_KEY')),
        'key_length': len(os.environ.get('GEMINI_API_KEY', '') or os.getenv('GOOGLE_API_KEY', '')),
        'flask_env': os.environ.get('FLASK_ENV', 'not_set'),
        'status': 'API keys configured' if (os.environ.get('GEMINI_API_KEY') or os.getenv('GOOGLE_API_KEY')) else 'Missing API keys'
    }

@app.route('/test-api')
def test_api():
    try:
        model = genai.GenerativeModel("gemini-1.5-pro")
        response = model.generate_content("Say hello in a friendly way")
        return {
            'status': 'success',
            'response': response.text,
            'api_working': True
        }
    except Exception as e:
        return {
            'status': 'error',
            'error': str(e),
            'api_working': False
        }

@app.route('/health')
def health_check():
    return {
        'status': 'healthy',
        'timestamp': time.time(),
        'version': '1.0.0'
    }

@app.errorhandler(404)
def not_found_error(error):
    return jsonify({
        'error': 'Endpoint not found',
        'message': 'The requested URL was not found on the server.',
        'available_endpoints': [
            '/samChat', '/joeChat', '/russellChat',
            '/gameChat', '/detectiveChat', '/charadesGame1',
            '/debug', '/test-api', '/health'
        ]
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'error': 'Internal server error',
        'message': 'Something went wrong on our end. Please try again.'
    }), 500

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False) 
