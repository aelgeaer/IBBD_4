from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.orm import declarative_base

db = SQLAlchemy()
Base = declarative_base()

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(50), nullable=False)

class Teachers(Base):
    __tablename__ = 'teachers'
    teacher_id = Column(Integer(), primary_key=True)
    teacher_full_name = Column(Text)
    department = Column(Text)
    email = Column(Text)
    phone = Column(Text)
    consultation_time = Column(Text)
    working_bulding = Column(Text)

class Subject(Base):
    __tablename__ = 'subject'
    subject_id = Column(Integer, primary_key=True)
    subject_name = Column(Text)
    subject_type = Column(Text)
    teacher_id = Column(Integer, ForeignKey('teachers.teacher_id'))
    group_id = Column(Integer, ForeignKey('groups.group_id'))

class Groups(Base):
    __tablename__ = 'groups'
    group_id = Column(Integer, primary_key=True)
    course_number = Column(Integer)
    admin_full_name = Column(Text)
    admin_contacts = Column(Text)
    specialty_code = Column(Integer, ForeignKey('specialty.specialty_code'))

class Speciality(Base):
    __tablename__ = "specialty"
    specialty_code = Column(Integer, primary_key=True)
    specialty_name = Column(Text)
    department = Column(Text)

class CompactSchedule(Base):
    __tablename__ = 'compact_shedule'
    id_schel = Column(Integer, primary_key=True)
    subject_name = Column(Text)
    classes_start_time = Column(Text)
    classes_end_time = Column(Text)
    building = Column(Text)
    teacher_full_name = Column(Text)

class Consultations(Base):
    __tablename__ = 'consultations'
    id_consult = Column(Integer, primary_key=True)
    subject_name = Column(Text)
    teacher_full_name = Column(Text)
    department = Column(Text)
    email = Column(Text)
    phone = Column(Text)
    consultation_time = Column(Text)
    working_bulding = Column(Text)
