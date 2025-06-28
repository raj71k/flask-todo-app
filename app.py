from flask import Flask, render_template, request, redirect, url_for
from models import db, Task
from datetime import datetime

app = Flask(__name__)
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
        if task_content and due_date_str:
            due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
            new_task = Task(content=task_content, due_date=due_date)
            db.session.add(new_task)
            db.session.commit()
        return redirect(url_for("index"))

    tasks = Task.query.order_by(Task.due_date).all()
    return render_template("index.html", tasks=tasks)

@app.route("/delete/<int:id>")
def delete(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
