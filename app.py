import os
import mysql.connector
from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = "my_secrets"

# ---------------- DATABASE ----------------

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",      # Change this if your MySQL password is different
    database="chatbot"
)

cursor = db.cursor()

print("Database Connected Successfully!")

cursor.execute("SELECT * FROM users")
print(cursor.fetchall())

# ---------------- OPENAI ----------------
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# ---------------- LOGIN ----------------

@app.route("/", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        if username == "admin" and password == "1234":
            session["user"] = username
            return redirect(url_for("index"))

        return "Invalid Username or Password"

    return render_template("login.html")

# ---------------- CHATBOT ----------------

@app.route("/chatbot")
def index():

    if "user" not in session:
        return redirect(url_for("login"))

    return render_template("index.html")

# ---------------- CHAT API ----------------

@app.route("/chat", methods=["POST"])
def chat():

    if "user" not in session:
        return jsonify({"reply": "Please login first."})

    user_message = request.json.get("message")

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "user", "content": user_message}
            ]
        )

        return jsonify({
            "reply": response.choices[0].message.content
        })

    except Exception as e:
        return jsonify({
            "reply": str(e)
        })

# ---------------- PAGES ----------------

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/features")
def features():
    return render_template("features.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/users")
def users():

    if "user" not in session:
        return redirect(url_for("login"))

    cursor.execute("SELECT * FROM users")
    all_users = cursor.fetchall()

    return render_template("users.html", users=all_users)


@app.route("/user/<int:id>")
def user_details(id):

    if "user" not in session:
        return redirect(url_for("login"))

    cursor.execute("SELECT * FROM users WHERE id=%s", (id,))
    user = cursor.fetchone()

    return render_template("user_details.html", user=user)

@app.route("/api/user/<int:id>")
def get_user(id):

    cursor.execute("SELECT * FROM users WHERE id=%s", (id,))
    # cursor.execute(f"SELECT * FROM users WHERE id={id}")
    user = cursor.fetchone()

    if user is None:
        return jsonify({"error": "User not found"}), 404

    return jsonify({
        "id": user[0], 
        "name": user[1],
        "email": user[2],
        "contact": user[3],
        "city": user[4]
    })
# ---------------- EDIT USER ----------------

@app.route("/edit_user/<int:id>")
def edit_user(id):

    if "user" not in session:
        return redirect(url_for("login"))

    cursor.execute("SELECT * FROM users WHERE id=%s", (id,))
    user = cursor.fetchone()

    return render_template("edit_user.html", user=user)


# ---------------- UPDATE USER ----------------

@app.route("/update_user/<int:id>", methods=["POST"])
def update_user(id):

    if "user" not in session:
        return redirect(url_for("login"))

    name = request.form["name"]
    email = request.form["email"]
    contact = request.form["contact"]
    city = request.form["city"]

    cursor.execute("""
        UPDATE users
        SET
            name=%s,
            email=%s,
            contact=%s,
            city=%s
        WHERE id=%s
    """, (name, email, contact, city, id))

    db.commit()

    return redirect("/users")


# ---------------- DELETE USER ----------------

@app.route("/delete_user/<int:id>")
def delete_user(id):

    if "user" not in session:
        return redirect(url_for("login"))

    cursor.execute("DELETE FROM users WHERE id=%s", (id,))
    db.commit()

    return redirect("/users")

# ---------------- CREATE USER ----------------

@app.route("/create-user")



@app.route("/create-user", methods=["GET", "POST"])
def create_user():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        contact = request.form["contact"]
        city = request.form["city"]

        cursor.execute(
            "INSERT INTO users(name,email,contact,city) VALUES(%s,%s,%s,%s)",
            (name, email, contact, city)
        )

        db.commit()

        return redirect("/users")

    return render_template("create_user.html")
@app.route("/google-chatbot")
def google_chatbot():

    if "user" not in session:
        return redirect(url_for("login"))

    return render_template("google_chatbot.html")



@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))


# ---------------- RUN ----------------

if __name__ == "__main__":
    app.run(debug=True)
