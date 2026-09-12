import joblib

model = joblib.load("model/chatbot_model.pkl")

responses = {
    "exam": "The exam schedule will be announced on the college website.",
    "courses": "Our college offers courses like CSE, ECE, Mechanical, and Civil Engineering.",
    "timing": "College timing is from 9:00 AM to 4:00 PM.",
    "library": "The library is open from 9:00 AM to 5:00 PM.",
    "hostel": "Hostel facilities are available for students.",
    "fees": "For fee details, please contact the accounts department.",
    "attendance": "Minimum 75% attendance is required.",
    "placement": "Our college provides good placement opportunities."
}

while True:
    question = input("You: ")

    if question.lower() == "exit":
        print("Chatbot: Goodbye!")
        break

    intent = model.predict([question])[0]

    print("Chatbot:", responses[intent])