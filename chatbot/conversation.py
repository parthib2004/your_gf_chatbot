import random
from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer

# Load the DialoGPT-medium model and tokenizer
model_name = "microsoft/DialoGPT-medium"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Define the text generation pipeline
chat_pipeline = pipeline("text-generation", model=model, tokenizer=tokenizer)

class Chatbot:
    def __init__(self):
        self.history = []
    
    def add_to_history(self, user_input, bot_response):
        self.history.append(f"User: {user_input}")
        self.history.append(f"Bot: {bot_response}")
        if len(self.history) > 10:  # Keep last 10 messages to avoid excessive history
            self.history = self.history[-10:]
    
    def generate_response(self, user_input):
        # Combine history into context
        context = " ".join(self.history) + f" User: {user_input}"
        
        input_ids = tokenizer.encode(context + tokenizer.eos_token, return_tensors="pt")
        response_ids = model.generate(
            input_ids,
            max_length=150,
            pad_token_id=tokenizer.eos_token_id,
            temperature=0.9,
            top_p=0.95,
            top_k=50
        )
        
        response = tokenizer.decode(response_ids[:, input_ids.shape[-1]:][0], skip_special_tokens=True)
        return response

# Initialize chatbot instance
chatbot = Chatbot()

def custom_response(user_input):
    flirt_phrases = ["horny", "naughty", "flirt", "sexy", "love","seduce","fuck","kiss","date","relationship","sex"]
    playful_responses = [
        "Aww, you’re so cheeky 😉.",
        "You’re being naughty! 😘",
        "Haha, you know how to tease! 😏",
        "Come on, behave yourself! 😜",
    ]
    
    # Check for keywords in user input
    if any(word in user_input.lower() for word in flirt_phrases):
        return random.choice(playful_responses)
    
    # If no keywords, generate a default response using the model
    input_ids = tokenizer.encode(user_input + tokenizer.eos_token, return_tensors="pt")
    response_ids = model.generate(input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id)
    response = tokenizer.decode(response_ids[:, input_ids.shape[-1]:][0], skip_special_tokens=True)
    return response
