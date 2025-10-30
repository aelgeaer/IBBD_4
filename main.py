from flask import Flask, render_template, request, jsonify
from flask_login import LoginManager, login_required, current_user
from models import db, User, Teachers, Subject, Groups, Speciality, CompactSchedule, Consultations
from auth import auth
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here-change-this-in-production'
# Update with your actual password - try 'postgres' first
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://musliqul:postgres@server2_data:5432/dbs24'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

app.register_blueprint(auth)

@login_manager.user_loader
def load_user(user_id):
    # Create user with proper parameters
    if user_id == 'admin':
        return User(user_id=user_id, username=user_id, role='admin')
    elif user_id == 'teacher':
        return User(user_id=user_id, username=user_id, role='teacher')
    elif user_id == 'student':
        return User(user_id=user_id, username=user_id, role='student')
    return None

ROLE_PERMISSIONS = {
    'admin': ['teachers', 'subject', 'groups', 'specialty', 'compact_shedule', 'consultations'],
    'teacher': ['teachers', 'subject', 'compact_shedule', 'consultations'],
    'student': ['compact_shedule', 'consultations']
}

def get_db_session():
    # Update with your actual password - try 'postgres' first
    engine = create_engine('postgresql://postgres:musliqul@server2_data:5432/dbs24')
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
        if current_user.role == 'admin':
            query = session.query(
                Subject.subject_type,
                func.count(Subject.subject_id).label('count')
            ).group_by(Subject.subject_type).all()
            
            result = [{'subject_type': row[0], 'count': row[1]} for row in query]
            columns = ['subject_type', 'count']
            
        elif current_user.role == 'teacher':
            query = session.query(
                Consultations.teacher_full_name,
                func.count(Consultations.id_consult).label('consultation_count')
            ).group_by(Consultations.teacher_full_name).all()
            
            result = [{'teacher_full_name': row[0], 'consultation_count': row[1]} for row in query]
            columns = ['teacher_full_name', 'consultation_count']
            
        elif current_user.role == 'student':
            query = session.query(
                CompactSchedule.building,
                func.count(CompactSchedule.id_schel).label('class_count')
            ).group_by(CompactSchedule.building).all()
            
            result = [{'building': row[0], 'class_count': row[1]} for row in query]
            columns = ['building', 'class_count']
        else:
            result = []
            columns = []
        
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
    app.run(debug=True, host='0.0.0.0', port=5000)
