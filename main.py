from flask import Flask, render_template, request, jsonify
from flask_login import login_required, current_user
from models import db, User, Teachers, Subject, Groups, Speciality, CompactSchedule, Consultations
from auth import auth
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://petya_admin:admin@localhost/dbs24'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
app.register_blueprint(auth)

# Настройки доступа для разных ролей
ROLE_PERMISSIONS = {
    'admin': ['teachers', 'subject', 'groups', 'specialty', 'compact_shedule', 'consultations'],
    'teacher': ['teachers', 'subject', 'compact_shedule', 'consultations'],
    'student': ['compact_shedule', 'consultations']
}

# Подключение к БД для выполнения запросов
def get_db_session():
    engine = create_engine('postgresql://petya_admin:admin@localhost/dbs24')
    Session = sessionmaker(bind=engine)
    return Session()

@app.route('/')
@login_required
def dashboard():
    user_tables = ROLE_PERMISSIONS.get(current_user.role, [])
    return render_template('dashboard.html', tables=user_tables, username=current_user.username, role=current_user.role)

@app.route('/table/<table_name>')
@login_required
def view_table(table_name):
    if table_name not in ROLE_PERMISSIONS.get(current_user.role, []):
        return "Доступ запрещен", 403
    
    session = get_db_session()
    
    try:
        if table_name == 'teachers':
            data = session.query(Teachers).all()
        elif table_name == 'subject':
            data = session.query(Subject).all()
        elif table_name == 'groups':
            data = session.query(Groups).all()
        elif table_name == 'specialty':
            data = session.query(Speciality).all()
        elif table_name == 'compact_shedule':
            data = session.query(CompactSchedule).all()
        elif table_name == 'consultations':
            data = session.query(Consultations).all()
        else:
            return "Таблица не найдена", 404
        
        # Получение названий колонок
        if data:
            columns = [column.name for column in data[0].__table__.columns]
        else:
            columns = []
        
        session.close()
        return render_template('table_view.html', 
                             table_name=table_name, 
                             data=data, 
                             columns=columns,
                             username=current_user.username,
                             role=current_user.role)
    except Exception as e:
        session.close()
        return f"Ошибка: {str(e)}", 500

@app.route('/complex_query')
@login_required
def complex_query():
    session = get_db_session()
    
    try:
        # Сложный запрос с GROUP BY для разных ролей
        if current_user.role == 'admin':
            # Для администратора: количество предметов по типам
            query = session.query(
                Subject.subject_type,
                func.count(Subject.subject_id).label('count')
            ).group_by(Subject.subject_type).all()
            
            result = [{'subject_type': row[0], 'count': row[1]} for row in query]
            columns = ['subject_type', 'count']
            
        elif current_user.role == 'teacher':
            # Для преподавателя: количество консультаций по преподавателям
            query = session.query(
                Consultations.teacher_full_name,
                func.count(Consultations.id_consult).label('consultation_count')
            ).group_by(Consultations.teacher_full_name).all()
            
            result = [{'teacher_full_name': row[0], 'consultation_count': row[1]} for row in query]
            columns = ['teacher_full_name', 'consultation_count']
            
        elif current_user.role == 'student':
            # Для студента: расписание по зданиям
            query = session.query(
                CompactSchedule.building,
                func.count(CompactSchedule.id_schel).label('class_count')
            ).group_by(CompactSchedule.building).all()
            
            result = [{'building': row[0], 'class_count': row[1]} for row in query]
            columns = ['building', 'class_count']
        
        session.close()
        return render_template('table_view.html',
                             table_name="Результат сложного запроса",
                             data=result,
                             columns=columns,
                             username=current_user.username,
                             role=current_user.role,
                             is_complex_query=True)
    except Exception as e:
        session.close()
        return f"Ошибка выполнения запроса: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True)
