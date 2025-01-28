from flask import Flask, render_template, request, jsonify
from datetime import datetime

app = Flask(__name__)

# Фейковая база данных для хранения пользователей
users = []

# Главная страница с использованием HTML-шаблона
@app.route("/")
def home():
    return """
    <html>
        <head>
            <title>Flask App</title>
        </head>
        <body>
            <h1>Welcome to Flask App!</h1>
            <p>Choose an endpoint:</p>
            <ul>
                <li><a href="/users">List of Users</a></li>
                <li><a href="/time">Current Time</a></li>
                <li><a href="/add-user">Add a User</a></li>
                <li><a href="/math">Math API</a></li>
            </ul>
        </body>
    </html>
    """

# Маршрут для отображения текущего времени
@app.route("/time")
def current_time():
    now = datetime.now()
    return jsonify({"current_time": now.strftime("%Y-%m-%d %H:%M:%S")})

# Маршрут для отображения списка пользователей
@app.route("/users")
def list_users():
    if not users:
        return jsonify({"message": "No users found"})
    return jsonify({"users": users})

# Маршрут для добавления нового пользователя через форму
@app.route("/add-user", methods=["GET", "POST"])
def add_user():
    if request.method == "POST":
        name = request.form.get("name")
        age = request.form.get("age")
        if not name or not age:
            return jsonify({"error": "Name and age are required"}), 400
        users.append({"name": name, "age": int(age)})
        return jsonify({"message": "User added successfully", "user": {"name": name, "age": int(age)}})

    return """
    <html>
        <head>
            <title>Add User</title>
        </head>
        <body>
            <h1>Add a New User</h1>
            <form method="POST" action="/add-user">
                <label for="name">Name:</label><br>
                <input type="text" id="name" name="name"><br>
                <label for="age">Age:</label><br>
                <input type="number" id="age" name="age"><br><br>
                <input type="submit" value="Submit">
            </form>
        </body>
    </html>
    """

# API для выполнения математических операций
@app.route("/math", methods=["GET", "POST"])
def math_operations():
    if request.method == "POST":
        data = request.json
        operation = data.get("operation")
        num1 = data.get("num1")
        num2 = data.get("num2")

        if not operation or num1 is None or num2 is None:
            return jsonify({"error": "Operation, num1, and num2 are required"}), 400

        if operation == "add":
            result = num1 + num2
        elif operation == "subtract":
            result = num1 - num2
        elif operation == "multiply":
            result = num1 * num2
        elif operation == "divide":
            if num2 == 0:
                return jsonify({"error": "Cannot divide by zero"}), 400
            result = num1 / num2
        else:
            return jsonify({"error": "Invalid operation"}), 400

        return jsonify({"result": result})

    return """
    <html>
        <head>
            <title>Math API</title>
        </head>
        <body>
            <h1>Math API</h1>
            <p>Use POST requests to perform operations.</p>
            <p>Example payload:</p>
            <pre>
{
    "operation": "add",
    "num1": 5,
    "num2": 3
}
            </pre>
        </body>
    </html>
    """

# Запуск сервера
if __name__ == "__main__":
    app.run(debug=True)
