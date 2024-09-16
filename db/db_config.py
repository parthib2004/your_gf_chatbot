from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['chatbot']
users = db['users']

def save_conversation(user_id, user_input, bot_response):
    users.update_one(
        {'_id': user_id},
        {'$push': {'conversations': {'input': user_input, 'response': bot_response}}},
        upsert=True
    )

