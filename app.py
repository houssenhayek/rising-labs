from flask import Flask, render_template, request
import json
import os

app = Flask(__name__)

FILE = "users.json"

# create file if it doesn't exist
if not os.path.exists(FILE):
    with open(FILE, "w") as f:
        json.dump([], f)


# ---------------- HOME PAGE ----------------
@app.route("/")
def home():
    return render_template("index.html")


# ---------------- JOIN PAGE ----------------
@app.route("/join")
def join():
    return render_template("join.html")


# ---------------- FORM SUBMISSION ----------------
@app.route("/submit", methods=["POST"])
def submit():

    name = request.form.get("name")
    contact = request.form.get("contact")
    role = request.form.get("role")
    idea = request.form.get("idea")

    new_user = {
        "name": name,
        "contact": contact,
        "role": role,
        "idea": idea
    }

    with open(FILE, "r") as f:
        data = json.load(f)

    data.append(new_user)

    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)

    return "Thanks for joining Rising Labs 🚀"


# ---------------- ADMIN DASHBOARD ----------------
@app.route("/admin")
def admin():

    with open(FILE, "r") as f:
        data = json.load(f)

    html = """
    <html>
    <head>
        <title>Rising Labs Admin</title>
        <style>
            body {
                margin: 0;
                font-family: Arial;
                background: #0b0b0b;
                color: white;
            }

            .header {
                padding: 20px;
                text-align: center;
                color: #00ffcc;
                font-size: 24px;
                font-weight: bold;
            }

            .container {
                display: flex;
                flex-wrap: wrap;
                justify-content: center;
                padding: 20px;
                gap: 15px;
            }

            .card {
                background: #111;
                border: 1px solid #222;
                padding: 15px;
                width: 280px;
                border-radius: 10px;
                transition: 0.3s;
            }

            .card:hover {
                border-color: #00ffcc;
                transform: translateY(-5px);
            }

            .label {
                color: #00ffcc;
                font-size: 12px;
            }

            input {
                padding: 10px;
                width: 300px;
                margin: 20px auto;
                display: block;
                border-radius: 8px;
                border: none;
                background: #111;
                color: white;
                border: 1px solid #222;
            }
        </style>

        <script>
            function searchUsers() {
                let input = document.getElementById("search").value.toLowerCase();
                let cards = document.getElementsByClassName("card");

                for (let i = 0; i < cards.length; i++) {
                    let text = cards[i].innerText.toLowerCase();
                    if (text.includes(input)) {
                        cards[i].style.display = "block";
                    } else {
                        cards[i].style.display = "none";
                    }
                }
            }
        </script>
    </head>

    <body>

        <div class="header">Rising Labs Admin Dashboard</div>

        <input id="search" onkeyup="searchUsers()" placeholder="Search users...">

        <div class="container">
    """

    for user in data:
        html += f"""
        <div class="card">
            <p class="label">NAME</p>
            <p>{user['name']}</p>

            <p class="label">CONTACT</p>
            <p>{user['contact']}</p>

            <p class="label">ROLE</p>
            <p>{user['role']}</p>

            <p class="label">IDEA</p>
            <p>{user['idea']}</p>
        </div>
        """

    html += """
        </div>
    </body>
    </html>
    """

    return html

    


# ---------------- RUN SERVER ----------------
import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)