from flask import Flask, render_template, redirect, url_for, request,flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash,check_password_hash
from flask import jsonify
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///wedding.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'weddingapp2026'

db = SQLAlchemy(app)

login_manager=LoginManager(app)
login_manager.login_view='login'
login_manager.login_message_category='warning'

# models
class User(UserMixin,db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(100),unique=True,nullable=False)
    email=db.Column(db.String(150),unique=True,nullable=False)
    password=db.Column(db.String(200),nullable=False)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    assigned_to = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), default='Pending')

    def __repr__(self):              
        return f'<Task {self.title}>'
    
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# auth routes
@app.route('/register',methods=['GET','POST'])
def register():
    if request.method=='POST':
        username=request.form.get('username').strip()
        email=request.form.get('email').strip()
        password=request.form.get('password')

        if not username or not email or not password:
            flash('All fields are required!','danger')
            return redirect(url_for('register'))
        
        hashed_pw=generate_password_hash(password)
        new_user=User(username=username,email=email,password=hashed_pw)
        db.session.add(new_user)
        db.session.commit()
        flash('Account created! Please login','success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login',methods=['GET','POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')

        if not email or not password:
            flash('All fields are required!', 'danger')
            return redirect(url_for('login'))

        user = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password, password):
            flash('Invalid email or password!', 'danger')
            return redirect(url_for('login'))

        login_user(user)
        flash(f'Welcome back, {user.username}!', 'success')
        return redirect(url_for('tasks'))

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully!','info')
    return redirect(url_for('login'))


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/tasks')
@login_required
def tasks():
    all_tasks = Task.query.all()     
    return render_template('tasks.html', tasks=all_tasks)


@app.route('/add', methods=['GET', 'POST'])
@login_required
def add_task():
    if request.method == 'POST':
        title = request.form.get('title').strip()
        assigned_to = request.form.get('assigned_to').strip()
        status = request.form.get('status')

        if not title or not assigned_to:
            flash('All fields are required!', 'danger')
            return redirect(url_for('add_task'))
        
        if len(title)<3:
            flash('Task title must be at least 3 characters!','warning')
            return redirect(url_for('add_task'))

        new_task = Task(title=title, assigned_to=assigned_to, status=status)
        db.session.add(new_task)
        db.session.commit()

        return redirect(url_for('tasks'))

    return render_template('add_task.html')

@app.route('/edit/<int:task_id>', methods=['GET','POST'])
@login_required
def edit_task(task_id):
    task=Task.query.get_or_404(task_id)

    if request.method=='POST':
        title=request.form.get('title').strip()
        assigned_to=request.form.get('assigned_to').strip()
        status=request.form.get('status')

        if not title or not assigned_to:
            flash('All fields are required!','danger')
            return redirect(url_for('edit_task',task_id=task_id))
        
        task.title=title
        task.assigned_to=assigned_to
        task.status=status

        db.session.add(task)
        db.session.commit()
        flash('Task updated successfully!','success')
        return redirect(url_for('tasks'))
    
    return render_template('edit_task.html',task=task)

@app.route('/delete/<int:task_id>')
@login_required
def delete_task(task_id):
    task=Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    flash('Task updated successfully!','success ')
    return redirect(url_for('tasks'))

@app.route('/api/tasks',methods=['GET'])
def api_get_tasks():
    tasks=Task.query.all()
    task_list=[]
    for task in tasks:
        task_list.append({

            'id':task.id,
            'title':task.title,
            'assigned_to':task.assigned_to,
            'status':task.status
        })
    return jsonify({'tasks':task_list,'total':len(task_list)})

@app.route('/api/tasks/<int:task_id>',methods=['GET'])
def api_get_task(task_id):
    task=Task.query.get_or_404(task_id)
    return jsonify({
        'id':task.id,
        'title':task.title,
        'assigned_to': task.assigned_to,
        'status':task.status
    })

@app.route('/api/tasks',methods=['POST'])
def api_create_task():
    data=request.get_json()

    if not data:
        return jsonify({'error':'No data provided'}),400
    
    title=data.get('title','').strip()
    assigned_to=data.get('assigned_to','').strip()
    status=data.get('status','Pending')

    if not title or not assigned_to:
        return jsonify({'error':'title and assigned_to are required'}),400
    
    new_task=Task(title=title,assigned_to=assigned_to,status=status)
    db.session.add(new_task)
    db.session.commit()

    return jsonify({
        'message':'Task created successfully',
        'task':{
            'id':new_task.id,
            'title':new_task.title,
            'assigned_to':new_task.assigned_to,
            'status':new_task.status
        }
    }),201

@app.route('/api/tasks/<int:task_id>',methods=['PUT'])
def api_update_task(task_id):
    task=Task.query.get_or_404(task_id)
    data=request.get_json()

    if not data:
        return jsonify({'error':'No data provided'}),400
    
    task.title=data.get('title',task.title).strip()
    task.assigned_to=data.get('assigned_to',task.assigned_to).strip()
    task.status=data.get('status',task.status)

    db.session.commit()

    return jsonify({
        'message':'Task updated successfully',
        'task':{
            'id':task_id,
            'assigned_to':task.assigned_to,
            'status':task.status
        }
    })

@app.route('/api/tasks/<int:task_id>',methods=['DELETE'])
def api_delete_task(task_id):
    task=Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({'message':f'Task {task_id} deleted successfully'})



if __name__ == '__main__':
    app.run(debug=True)