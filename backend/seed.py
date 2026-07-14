import bcrypt
from extensions import db
from models import User, Department, Branch, Skill

def seed_admin():
    admin = User.query.filter_by(role='admin').first()
    admin_email = 'starspinix@gmail.com'
    if not admin:
        password_hash = bcrypt.hashpw('admin123'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        admin = User(
            email = admin_email,
            password = password_hash,
            role = 'admin',
            is_active = True,
            is_blacklisted = False,
            is_verified = True
        )
        db.session.add(admin)
        db.session.commit()
        print('[SEED]\tAdmin user created:', admin_email)
    else:
        print('[SEED]\tAdmin user already exists:', admin_email)

def seed_departments_and_branches():
    departments = [
        {
            'id': 101,
            'name': 'Computer Science',
            'branches': ['Artificial Intelligence and Data Science', 'Information Technology']
        },
        {
            'id': 102,
            'name': 'Electronics',
            'branches': ['Communication', 'VLSI', 'Embedded Systems']
        },
        {
            'id': 103,
            'name': 'Mechanical',
            'branches': ['Automobile', 'Robotics', 'Thermal Engineering']
        }
    ]
    for dept_data in departments:
        dept = Department.query.filter_by(dept_name=dept_data['name']).first()
        if not dept:
            dept = Department(dept_id = dept_data['id'], dept_name = dept_data['name'])
            db.session.add(dept)
            db.session.flush()
        for branch in dept_data['branches']:
            existing_branch = Branch.query.filter_by(branch_name=branch, dept_id=dept.dept_id).first()
            if not existing_branch:
                new_branch = Branch(branch_name=branch, dept_id=dept.dept_id)
                db.session.add(new_branch)
    db.session.commit()
    print('[SEED]\tDepartments and branches seeded successfully.')

def seed_skills():
    skills = [
        "Python", "Java", "C++", "JavaScript", "React", "Vue.js", "Node.js", 
        "SQL", "MongoDB", "Machine Learning", "Data Analysis", "Cloud Computing", 
        "AWS", "Docker", "Kubernetes", "DevOps", "Agile Methodologies", 
        "Communication", "Problem Solving", "Teamwork"
    ]
    for skill_name in skills:
        existing = Skill.query.filter_by(skill_name=skill_name).first()
        if not existing:
            db.session.add(Skill(skill_name=skill_name))
    db.session.commit()
    print('[SEED]\tSkills seeded successfully.')

def run_seed():
    seed_admin()
    seed_departments_and_branches()
    seed_skills()