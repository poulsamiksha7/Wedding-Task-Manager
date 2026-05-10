from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///wedding.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'weddingapp2026'

db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    assigned_to = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), default='Pending')

    def __repr__(self):               # ← INSIDE the class. Indented.
        return f'<Task {self.title}>'


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/tasks')
def tasks():
    all_tasks = Task.query.all()      # ← fetch from DB
    return render_template('tasks.html', tasks=all_tasks)


@app.route('/add', methods=['GET', 'POST'])
def add_task():
    if request.method == 'POST':
        title = request.form.get('title')
        assigned_to = request.form.get('assigned_to')
        status = request.form.get('status')

        new_task = Task(title=title, assigned_to=assigned_to, status=status)
        db.session.add(new_task)
        db.session.commit()

        return redirect(url_for('tasks'))

    return render_template('add_task.html')

@app.route('/edit/<int:task_id>', methods=['GET','POST'])
def edit_task(task_id):
    task=Task.query.get_or_404(task_id)

    if request.method=='POST':
        task.title=request.form.get('title')
        task.assigned_to=request.form.get('assigned_to')
        task.status=request.form.get('status')
        db.session.add(task)
        db.session.commit()
        return redirect(url_for('tasks'))
    
    return render_template('edit_task.html',task=task)

@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    task=Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('tasks'))


if __name__ == '__main__':
    app.run(debug=True)