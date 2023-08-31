from flask import (
    Blueprint,render_template,request,url_for,redirect,flash, session, g
)
from werkzeug.security import generate_password_hash, check_password_hash

from .models import User
from todor import db

bp = Blueprint('auth', __name__ , url_prefix='/auth')

@bp.route('/register', methods = ('GET','POST'))

def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User(username, generate_password_hash(password))

        error = None
    
        #Consulta a base de datos
        user_name = User.query.filter_by(username = username).first() #Frist primer resultado q encuentr
        if user_name == None:
            db.session.add(user) # agrega a base de datos
            db.session.commit() # refresca 
            return redirect (url_for('auth.login')) # redirecciona
        else:
            error = f'El usuario {username} ya esta registado' #error xD
            flash(error)


    return render_template('auth/register.html')

@bp.route('/login', methods = ('GET','POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        error = None

        #validar datos
        user = User.query.filter_by(username = username).first()
        if user == None:
            error = "Nombre de usuario incorrecto"
        elif not check_password_hash(user.password, password):
            error = "Contraseña Incorrecta"

        #Iniciar session
        if error is None:
            session.clear() # limpiamos session
            session['user_id'] = user.id #Iniciando session en la clave
            return redirect(url_for('todo.index'))

        flash(error)


    return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id') #obetenemos id de inciio y lo guardamos es decir lo recuperamos

    if user_id is None: # nadie a iniciado session
        g.user = None # tiene un valor nulo si existe un id 
    else:
        g.user = User.query.get_or_404(user_id) # Si existe va a retornar un usario y sino va a devolver un error


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

import functools #requiere iniciar sesion

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view

