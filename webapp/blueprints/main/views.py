from flask import redirect,url_for,jsonify,request,flash,render_template
from flask_login import current_user, login_required
from . import main
from webapp.models import Projects,Tasks
from webapp.extensions import db
import ast


################################################################ HOME
@main.route('/')
@main.route('/index')
def index():
    if current_user.is_authenticated:
        proj = Projects.query.filter_by(user_id=current_user.id).all()
        task = Tasks.query.order_by(Tasks.task_position).all()
    else:
        return redirect(url_for('auth.login'))
    return render_template('index.html',title='Welcome',proj=proj,task=task)

@main.route('/account')
@login_required
def account():
    return render_template('account.html',title='ToDo')

################################################################# PROJECT

@main.route('/add_project',methods=['GET', 'POST'])
def add_project():	
    if request.method=='POST':
        if current_user.is_authenticated:
            proj = Projects(project_name=request.form['name'],user_id=current_user.id)
            db.session.add(proj)
            db.session.commit()
            flash('Project added - {}'.format(request.form['name']))
        else:
            return redirect(url_for('auth.login'))      	
    return redirect(url_for('main.index'))

@main.route('/delete_project',methods=['GET','POST'])
def delete_project():
    delete_id = request.form['id']
    taskToDelete = Tasks.query.filter_by(project_id=delete_id).delete()
    projToDelete = Projects.query.filter_by(id=delete_id).first()
    db.session.delete(projToDelete)
    db.session.commit()
    flash('Project deleted')
    return redirect(url_for('main.index'))

@main.route('/update_project',methods=['GET','POST'])
def update_project():
    update_id = request.form['id']
    project_name = request.form['project_name']
    print(project_name)
    projToUpdate = Projects.query.filter_by(id=update_id).first()
    projToUpdate.project_name = project_name
    db.session.add(projToUpdate)
    db.session.commit()
    flash('Project updated - {}'.format(project_name))
    return redirect(url_for('main.index'))

############################################################# TASKS

@main.route('/add_task/<id>',methods=['GET','POST'])
def add_task(id):
    if request.method=='POST':
        task = Tasks(task_name=request.form['task_name'],task_status=False,task_priority=request.form['task_priority'],date=request.form['task_date'],task_position=0,project_id=id)
        db.session.add(task)
        db.session.commit()
        flash('Task added - {}'.format(request.form['task_name']))
    return redirect(url_for('main.index'))

@main.route('/delete_task',methods=['GET','POST'])
def delete_task():
	delete_id = request.form['id']
	print(delete_id)
	taskToDelete = Tasks.query.get(delete_id)
	db.session.delete(taskToDelete)
	db.session.commit()
	flash('Task deleted')
	return redirect(url_for('main.index'))

@main.route('/update_task/<id>',methods=['GET','POST'])
def update_task(id):
    name = request.form['task_name']
    date = request.form['task_date']
    priority = request.form['task_priority']
    taskToUpdate = Tasks.query.filter_by(id=id).first()
    taskToUpdate.task_name = name
    taskToUpdate.date = date
    taskToUpdate.task_priority = priority

    db.session.add(taskToUpdate)
    db.session.commit()
    flash('Task updated - {}'.format(name))
    return redirect(url_for('main.index'))

################################################################### ADDITIONAL

@main.route('/task_done/<id>',methods=['GET','POST'])
def task_done(id):
    taskDone = Tasks.query.get(id)
    if taskDone.task_status:
        taskDone.task_status = False
        flash('Task start')
    else:
        taskDone.task_status = True
        flash('Task done')
    db.session.add(taskDone)
    db.session.commit()
    return redirect(url_for('main.index'))