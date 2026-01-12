from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

def init_db():
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS tasks 
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, content TEXT)''')
    conn.commit()
    conn.close()

# 1. Define the GET route (READ)
@app.route('/tasks', methods=['GET'])
def get_tasks():
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks")
    rows = cursor.fetchall()
    conn.close()
    tasks = [{"id": row[0], "content": row[1]} for row in rows]
    return jsonify(tasks)

# 2. Define the POST route (CREATE)
@app.route('/tasks', methods=['POST'])
def add_task():
    data = request.json
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (content) VALUES (?)", (data['content'],))
    conn.commit()
    conn.close()
    return jsonify({"message": "Task added!"}), 201

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    # SQL query to delete based on the ID passed in the URL
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Task deleted successfully!"})

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    # This SQL command finds the task by ID and adds "(Completed)" to the text
    cursor.execute("UPDATE tasks SET content = content || ' (Completed)' WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Task marked as completed!"})

@app.route('/')
def home():
    return render_template('index.html')


# 3. START the server last
if __name__ == '__main__':
    init_db()
    # This must be the very last thing in the file
    app.run(debug=True)
