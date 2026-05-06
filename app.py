from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///wedding.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db=SQLAlchemy(app)

#DATABASE MODEL ONE TABLE IN YOUR DATABASE
class Task(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(200),nullable=False)
    assigned_to=db.Column(db.String(100),nullable=False)
    status=db.Column(db.String(20),default='Pending')


def __repr__(self):
    return f'<Task {self.title}>'


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/tasks')
def tasks():
    all_tasks=Task.query.all()
    return render_template('tasks.html', tasks=all_tasks)

if __name__ == '__main__':
    app.run(debug=True)