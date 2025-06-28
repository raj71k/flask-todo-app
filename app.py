from flask import Flask, render_template, request, redirect, url_for, flash, get_flashed_messages
from models import db, Task
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'samarth71'  # required for flash()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Create DB on first run
with app.app_context():
    db.create_all()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        task_content = request.form.get("content")
        due_date_str = request.form.get("due_date")
        if not task_content:
            flash("⚠️ Task cannot be empty!", "warning")
            return redirect(url_for('index'))
        
        due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
        new_task = Task(content=task_content, due_date=due_date)
        db.session.add(new_task)
        db.session.commit()
        flash("✅ Task added successfully!", "success")
        return redirect(url_for("index"))

    tasks = Task.query.order_by(Task.due_date).all()
    return render_template("index.html", tasks=tasks)

@app.route("/delete/<int:id>")
def delete(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/edit/<int:id>", methods=['GET', 'POST'])
def edit(id):
    task = Task.query.get_or_404(id)
    if request.method == 'POST':
        task.content = request.form['content']
         # Convert the string to a Python date object
        date_str = request.form['due_date']
        task.due_date = datetime.strptime(date_str, '%Y-%m-%d').date()

        db.session.commit()
        return redirect(url_for('index'))

    return render_template('edit.html', task=task)

@app.route('/done/<int:id>')
def mark_done(id):
    task = Task.query.get_or_404(id)
    task.completed = True
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
