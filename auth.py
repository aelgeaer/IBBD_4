from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from models import User

auth = Blueprint('auth', __name__)

USERS = {
    'admin': {'password': generate_password_hash('admin123'), 'role': 'admin'},
    'teacher': {'password': generate_password_hash('teacher123'), 'role': 'teacher'},
    'student': {'password': generate_password_hash('student123'), 'role': 'student'}
}

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username in USERS and check_password_hash(USERS[username]['password'], password):
            user = User(user_id=username, username=username, role=USERS[username]['role'])
            login_user(user)
            flash('Успешный вход в систему!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Неверное имя пользователя или пароль', 'error')
    
    return render_template('login.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли из системы', 'info')
    return redirect(url_for('auth.login'))
