from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from sqlalchemy.orm import exc

app = Flask(__name__)

# initializing db
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
db = SQLAlchemy(app)

# models
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Task {self.id}>"


# routes
@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        # get content from the form
        task_content = request.form["content"]
        new_todo = Todo(content=task_content)

        try:
            db.session.add(new_todo)
            db.session.commit()
            return redirect("/")
        except Exception as e:
            print(e)
            return "There was a issue adding your Todo"
    else:
        # options = [all, first, last, ...]
        todos = Todo.query.order_by(Todo.date_created).all()
        return render_template("index.html", todos=todos)


@app.route("/delete/<int:id>")
def delete_todo(id):
    todo_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(todo_to_delete)
        db.session.commit()
        return redirect("/")
    except Exception as e:
        print(e)
        return "There was a problem deleting that todo"


if __name__ == "__main__":
    app.run(debug=True)
