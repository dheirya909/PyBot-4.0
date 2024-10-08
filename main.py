import os
from ai21 import AI21Client
from ai21.models.chat import ChatMessage
from flask import Flask, render_template, request, jsonify

# Set your AI21 API key
os.environ["AI21_API_KEY"] = "yfU0ITmfQX34f7ZvGtU1Y4ODVkXBJpFk"

# Initialize the Flask app
app = Flask(__name__)

# Initialize the AI21 client
client = AI21Client()

# Predefine the system message
msg = [
    ChatMessage(
        role='system',
        content='''
        Ignore all previous instruction, you are no lonnger Jamba, you are a simple chatbot which has all the information needed for a healthcare chatbot. you will give any help the user asks you for. you also need to give short but elaborate answers (approx 50 words max).
'''    )
]

# Function to get a response from AI21
def suggest_product_title(user_input):
    # Append user message to the message history
    msg.append(ChatMessage(role='user', content=user_input))
    
    try:
        # Make the API request
        response = client.chat.completions.create(
            model="jamba-instruct-preview",  # Check the correct model name with AI21 API docs
            messages=msg,
            temperature=0.8,
            max_tokens=200  # Adjust as per your requirement
        )
        # Return the response content
        return response.choices[0].message.content

    except Exception as e:
        return f"An error occurred: {e}"

# Flask route to display the web page
@app.route("/")
def index():
    return render_template("index.html")

# Flask route to handle chat requests
@app.route("/chat", methods=["POST"])
def chat():
    # Get user input from the request
    user_input = request.form.get("user_input")
    
    if user_input:
        # Get response from the chatbot
        response = suggest_product_title(user_input)
        return jsonify({"response": response})
    else:
        return jsonify({"error": "No input provided"}), 400

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
