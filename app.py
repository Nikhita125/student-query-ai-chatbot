from flask import Flask, render_template, request, jsonify, redirect, session
import joblib
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "student_chatbot_secret"

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


@app.route("/")
def home():
    return redirect("/login")


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        hashed_password = generate_password_hash(password)

        conn = sqlite3.connect("database/chatbot.db")

        try:
            conn.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, hashed_password)
            )
            conn.commit()

        except sqlite3.IntegrityError:
            conn.close()
            return "Username already exists!"

        conn.close()

        return redirect("/login")

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("database/chatbot.db")

        user = conn.execute(
            "SELECT * FROM users WHERE username=?",
            (username,)
        ).fetchone()

        if user:

            stored_password = user[2]

            try:
                password_correct = check_password_hash(
                    stored_password,
                    password
                )

            except ValueError:
                password_correct = False

            # Convert old plain-text password to hashed password
            if not password_correct and stored_password == password:

                hashed_password = generate_password_hash(password)

                conn.execute(
                    "UPDATE users SET password=? WHERE username=?",
                    (hashed_password, username)
                )

                conn.commit()

                password_correct = True

            conn.close()

            if password_correct:
                session["username"] = username
                return redirect("/chat")

        conn.close()

        return "Invalid username or password!"

    return render_template("login.html")


@app.route("/chat")
def chat_page():

    if "username" not in session:
        return redirect("/login")

    return render_template("chat.html")


@app.route("/chat", methods=["POST"])
def chat():

    if "username" not in session:
        return jsonify({"answer": "Please login first."})

    question = request.json["question"]

    intent = model.predict([question])[0]

    conn = sqlite3.connect("database/chatbot.db")

    faq = conn.execute(
        "SELECT answer FROM faqs WHERE intent=? LIMIT 1",
        (intent,)
    ).fetchone()

    if faq:
        answer = faq[0]
    else:
        answer = responses.get(
            intent,
            "Sorry, I don't understand your question."
        )

    conn.execute(
        "INSERT INTO chat_history (username, question, answer) VALUES (?, ?, ?)",
        (session["username"], question, answer)
    )

    conn.commit()
    conn.close()

    return jsonify({"answer": answer})


@app.route("/logout")
def logout():

    session.clear()

    return redirect("/login")


@app.route("/admin")
def admin():

    if "username" not in session:
        return redirect("/login")

    if session["username"] != "admin":
        return "Access denied. Admin only."

    conn = sqlite3.connect("database/chatbot.db")

    chats = conn.execute(
        "SELECT id, username, question, answer FROM chat_history"
    ).fetchall()

    conn.close()

    return render_template("admin.html", chats=chats)


@app.route("/faq")
def faq():

    if "username" not in session:
        return redirect("/login")

    if session["username"] != "admin":
        return "Access denied. Admin only."

    conn = sqlite3.connect("database/chatbot.db")

    faqs = conn.execute(
        "SELECT * FROM faqs"
    ).fetchall()

    conn.close()

    return render_template("faq.html", faqs=faqs)


@app.route("/delete_faq/<int:faq_id>")
def delete_faq(faq_id):

    if "username" not in session:
        return redirect("/login")

    if session["username"] != "admin":
        return "Access denied. Admin only."

    conn = sqlite3.connect("database/chatbot.db")

    conn.execute(
        "DELETE FROM faqs WHERE id=?",
        (faq_id,)
    )

    conn.commit()
    conn.close()

    return redirect("/faq")


@app.route("/edit_faq/<int:faq_id>", methods=["GET", "POST"])
def edit_faq(faq_id):

    if "username" not in session:
        return redirect("/login")

    if session["username"] != "admin":
        return "Access denied. Admin only."

    conn = sqlite3.connect("database/chatbot.db")

    if request.method == "POST":

        question = request.form["question"]
        answer = request.form["answer"]
        intent = request.form["intent"]

        conn.execute(
            "UPDATE faqs SET question=?, answer=?, intent=? WHERE id=?",
            (question, answer, intent, faq_id)
        )

        conn.commit()
        conn.close()

        return redirect("/faq")

    faq = conn.execute(
        "SELECT * FROM faqs WHERE id=?",
        (faq_id,)
    ).fetchone()

    conn.close()

    return render_template("edit_faq.html", faq=faq)


@app.route("/add_faq", methods=["POST"])
def add_faq():

    if "username" not in session:
        return redirect("/login")

    if session["username"] != "admin":
        return "Access denied. Admin only."

    question = request.form["question"]
    answer = request.form["answer"]
    intent = request.form["intent"]

    conn = sqlite3.connect("database/chatbot.db")

    conn.execute(
        "INSERT INTO faqs (question, answer, intent) VALUES (?, ?, ?)",
        (question, answer, intent)
    )

    conn.commit()
    conn.close()

    return redirect("/faq")


if __name__ == "__main__":
    app.run(debug=True)