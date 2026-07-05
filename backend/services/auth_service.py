import bcrypt
import random
import string
from datetime import datetime, timedelta
from flask_jwt_extended import create_access_token, create_refresh_token
from flask_mail import Message
from extensions import db, mail
from models.user import User
from models.student import Student
from models.skill import Skill
from models.branch import Branch
from models.company import Company
import logging

logger = logging.getLogger(__name__)

class AuthService:

    @staticmethod
    def register_student(data):
        year = data.get('year_of_study')
        if year not in (3, 4):
            return {
                "error": "Only 3rd and 4th year students are allowed to register."
            }, 400
        
        email = data['email']
        
        if User.query.filter_by(email=email).first():
            return {
                "error": "Email already registered."
            }, 409
        
        if Student.query.filter_by(register_no=data['register_no']).first():
            return {
                "error": "Register number already exists."
            }, 409
        
        
        password_hash = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        otp = ''.join(random.choices(string.digits, k = 6))

        user = User(
            email = email,
            password = password_hash,
            role = 'student',
            is_verified = False,
            otp_code = otp,
            otp_expires_at = datetime.now() + timedelta(minutes = 10)
        )
        db.session.add(user)
        db.session.flush()

        student = Student(
            user_id = user.user_id,
            register_no = data['register_no'],
            fname = data['fname'],
            lname = data['lname'],
            dob = data['dob'],
            phone = data.get('phone'),
            cgpa = data['cgpa'],
            year_of_study = year,
            branch_id = data['branch_id']
        )
        db.session.add(student)

        skill_ids = data.get('skill_ids', [])
        if skill_ids:
            skills = Skill.query.filter(Skill.skill_id.in_(skill_ids)).all()
            student.skills.extend(skills)

        db.session.commit()

        try:
            message = Message(
                subject = 'Placement Portal - Email Verification',
                recipients = [email],
                body = f'''
                    Your OTP for email verification is {otp}\n
                    The OTP expires in exactly 10 minutes.
                '''
            )
            mail.send(message)
        except Exception as e:
            logger.warning("Could NOT send OTP email:", exc_info=True)
            logger.info(f"[DEV] OTP for {email}: {otp}")

        return {
            "message": "Registration successful. Please verify your email with OTP.",
            "user_id": user.user_id
        }, 201
    
    @staticmethod
    def verify_otp(data):
        user = User.query.filter_by(email = data['email']).first()
        if not user:
            return {
                "error": "User not found"
            }, 400
        if user.is_verified:
            return {
                "error": "User already verified."
            }, 400
        if user.otp_code != data['otp']:
            return {
                "error": "Invalid OTP"
            }, 401
        if user.otp_expires_at < datetime.now():
            return {
                "error": "OTP has expired"
            }, 401
        
        user.is_verified = True
        user.otp_code = None
        user.otp_expires_at = None
        db.session.commit()

        return {
            "message": "Email verified successfully"
        }, 200
    
    @staticmethod
    def register_company(data):
        email = data['email']
        
        if User.query.filter_by(email=email).first():
            return {
                "error": "Email already registered."
            }, 409
        
        password_hash = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        user = User(
            email = email,
            password = password_hash,
            role = 'company',
            is_verified = True
        )
        db.session.add(user)
        db.session.flush()

        company = Company(
            user_id =user.user_id,
            company_name = data['company_name'],
            industry = data.get('industry'),
            website = data.get('website'),
            location = data.get('location'),
            description = data.get('description'),
            hr_name = data.get('hr_name'),
            hr_email = data['hr_email'],
            hr_phone = data.get('hr_phone'),
            status = 'Pending'
        )
        db.session.add(company)
        db.session.commit()

        return {
            "message": "Company registered. Awaiting admin approval.",
            "company_id": company.company_id
        }, 201
    
    @staticmethod
    def login(data):
        user = User.query.filter_by(email = data['email']).first()
        if not user:
            return {
                "error": "Invalid email"
            }, 401
        
        if not bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):
            return {
                "error": "Invalid password"
            }, 401
        
        if not user.is_active:
            return {
                "error": "Account is deactivated"
            }, 403
        
        if user.is_blacklisted:
            return {
                "error": "Account is blacklisted"
            }, 403
        
        if not user.is_verified:
            return {
                "error": "Email not verified. Please verifiy OTP first."
            }, 403
        
        if user.role == 'company':
            company = Company.query.filter_by(user_id = user.user_id).first()
            if company and company.status != 'approved':
                return {
                    "error": f"Company registration is {company.status}. Please wait for admin approval."
                }, 403
            
        access_token = create_access_token(identity = user.user_id)
        refresh_token = create_refresh_token(identity = user.user_id)

        return {
            "message": "Login successful",
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": {
                "user_id": user.user_id,
                "email": user.email,
                "role": user.role
            }
        }, 200
    
    @staticmethod
    def get_current_user(user_id):
        user = User.query.get(user_id)
        if not user:
            return {
                "error": "User not found"
            }, 404
        
        result = {
            "user_id": user.user_id,
            "email": user.email,
            "role": user.role,
            "is_active": user.is_active
        }

        if user.role == 'student' and user.student:
            student = user.student
            branch_name = student.branch.branch_name
            result["profile"] = {
                "register_no": student.register_no,
                "name": f"{student.fname} {student.lname}",
                "cgpa": student.cgpa,
                "branch": branch_name,
                "year_of_study": student.year_of_study
            }
        elif user.role == 'company' and user.company:
            company = user.company
            result["profile"] = {
                "company_id": company.company_id,
                "company_name": company.company_name,
                "status": company.status,
                "industry": company.industry,
            }
        return result, 200