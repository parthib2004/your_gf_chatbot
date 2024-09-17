from flask import Flask, request, render_template, jsonify
from chatbot.conversation import custom_response

app = Flask(__name__)

# Example user_id (can be dynamic based on user login in future)
user_id = 'user'  # example user

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        # Get the JSON data from the request
        data = request.get_json()
        user_input = data.get('message', '')

        if not user_input:
            return jsonify({'response': 'No input provided'}), 400
        
        # Generate chatbot response
        response = custom_response(user_input)
        
        # Return the chatbot response as JSON
        return jsonify({'response': response})

    except Exception as e:
        return jsonify({'response': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
