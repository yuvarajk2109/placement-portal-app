import bcrypt
import random
from datetime import datetime, date, timedelta
from extensions import db
from models import User, Student, Company, Department, Branch, Skill, PlacementDrive, Interview, Application, Placement
from models.student import student_skill
from models.placement_drive import drive_branch, drive_skill

# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────

def _hash(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def _already_seeded(label: str) -> bool:
    """Simple check: if students already exist we skip the big seed."""
    if label == 'students':
        return Student.query.first() is not None
    if label == 'companies':
        return Company.query.first() is not None
    if label == 'drives':
        return PlacementDrive.query.first() is not None
    if label == 'applications':
        return Application.query.first() is not None
    return False

# ─────────────────────────────────────────────────────────────────────────────
# Tamil Nadu Names
# ─────────────────────────────────────────────────────────────────────────────

FIRST_NAMES_MALE = [
    "Aadhav", "Aakash", "Aravind", "Arun", "Ashwin", "Balaji", "Bharath", "Chandru",
    "Dhanush", "Dinesh", "Ezhil", "Ganesh", "Gokul", "Hari", "Harish", "Inban",
    "Jagadeesh", "Karthik", "Karthikeyan", "Kavin", "Kishore", "Kumar", "Logesh",
    "Madhan", "Manikandan", "Mohan", "Mukesh", "Murali", "Nandha", "Naveen",
    "Oviya", "Prabhu", "Pradeep", "Prakash", "Pranav", "Rajesh", "Rajan",
    "Ramesh", "Ravi", "Sanjay", "Saravanan", "Senthil", "Shankar", "Siva",
    "Suresh", "Surya", "Tamil", "Tharun", "Udhay", "Varun",
    "Velu", "Venkat", "Vignesh", "Vijay", "Vikram", "Vinoth", "Vishnu",
    "Yuvan", "Yuvaraj", "Lokesh", "Bala", "Deepak", "Gautam", "Iniyan",
    "Jegan", "Kathir", "Mani", "Navin", "Pandi", "Ranjith"
]

FIRST_NAMES_FEMALE = [
    "Aishwarya", "Anitha", "Bharathi", "Brindha", "Chitra", "Deepa", "Divya",
    "Gayathri", "Hema", "Indhu", "Janani", "Kalpana", "Kavitha", "Lakshmi",
    "Lavanya", "Madhumitha", "Meena", "Nandhini", "Nithya", "Pavithra",
    "Priya", "Ramya", "Sangeetha", "Saranya", "Selvi", "Shalini", "Shanthi",
    "Sneha", "Soundarya", "Sowmya", "Suganya", "Swathi", "Tamilarasi",
    "Thenmozhi", "Uma", "Vaani", "Vanitha", "Vasuki", "Vidya", "Yamini"
]

LAST_NAMES = [
    "Annamalai", "Arumugam", "Balasubramanian", "Chandrasekaran", "Chelladurai",
    "Durai", "Eswaran", "Ganapathy", "Govindasamy", "Iyer",
    "Jayaraman", "Kalyanasundaram", "Kannan", "Krishnamurthy", "Kumaran",
    "Lakshman", "Muthusamy", "Nagarajan", "Natarajan", "Palaniappan",
    "Pandian", "Raghunathan", "Rajendran", "Ramasamy", "Ranganathan",
    "Saravanan", "Selvaraj", "Shanmugam", "Subramanian", "Sundaram",
    "Thangavel", "Thirunavukkarasu", "Vaithyanathan", "Velmurugan", "Venkataraman",
    "Venkatesan", "Ayyappan", "Bharathiraja", "Dhanapal", "Elango",
    "Gurusamy", "Hariharan", "Ilango", "Jeyaraj", "Kathiresan",
    "Mahalingam", "Periyasamy", "Rajagopal", "Srinivasan", "Thirumalai"
]

# ─────────────────────────────────────────────────────────────────────────────
# 1. Admin
# ─────────────────────────────────────────────────────────────────────────────

def seed_admin():
    admin = User.query.filter_by(role='admin').first()
    admin_email = 'admin@placement.edu'
    if not admin:
        admin = User(
            email = admin_email,
            password = _hash('admin123'),
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

# ─────────────────────────────────────────────────────────────────────────────
# 2. Departments & Branches
# ─────────────────────────────────────────────────────────────────────────────

def seed_departments_and_branches():
    departments = [
        {
            'id': 101,
            'name': 'Information Technology',
            'branches': ['Artificial Intelligence and Data Science', 'Information Technology']
        },
        {
            'id': 102,
            'name': 'Computer Technology',
            'branches': ['Computer Science']
        },
        {
            'id': 103,
            'name': 'Electronics Engineering',
            'branches': ['Electronics and Communication', 'Electrical Engineering']
        },
        {
            'id': 104,
            'name': 'Instrumentation Engineering',
            'branches': ['Instrumentation Engineering']
        },
        {
            'id': 105,
            'name': 'Mechanical Engineering',
            'branches': ['Mechanical Engineering', 'Production Technology']
        },
        {
            'id': 106,
            'name': 'Rubber and Plastics Technology',
            'branches': ['Rubber and Plastics Technology'],
        },
        {
            'id': 107,
            'name': 'Applied Sciences and Humanities',
            'branches': ['Ethics and Society', 'Chemical Engineering'],
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

# ─────────────────────────────────────────────────────────────────────────────
# 3. Skills
# ─────────────────────────────────────────────────────────────────────────────

def seed_skills():
    skills = [
        "Python", "Java", "C++", "Spring", "Spring Boot", "JavaScript", "Angular", "React", "Vue.js", "Node.js",
        "SQL", "MongoDB", "Machine Learning", "Data Analysis", "Cloud Computing", "Data Science", "Data Engineering",
        "AWS", "Docker", "Kubernetes", "DevOps", "Agile Methodologies", "Azure", "GCP",
        "Communication", "Problem Solving", "Teamwork", "Arduino", "Deep Learning", "Generative AI"
    ]
    for skill_name in skills:
        existing = Skill.query.filter_by(skill_name=skill_name).first()
        if not existing:
            db.session.add(Skill(skill_name=skill_name))
    db.session.commit()
    print('[SEED]\tSkills seeded successfully.')

# ─────────────────────────────────────────────────────────────────────────────
# 4. Students (600 total: 550 active + 50 passed out)
# ─────────────────────────────────────────────────────────────────────────────

def seed_students():
    if _already_seeded('students'):
        print('[SEED]\tStudents already seeded. Skipping.')
        return

    random.seed(42)  # reproducible
    branches = Branch.query.all()
    all_skills = Skill.query.all()
    all_first_names = FIRST_NAMES_MALE + FIRST_NAMES_FEMALE
    password_hash = _hash('user123')

    # Build a mapping: branch -> dept_id
    branch_dept_map = {b.branch_id: b.dept_id for b in branches}

    student_count = 0
    blacklist_indices = set(random.sample(range(550), 15))  # 15 blacklisted among active students

    # Track next serial per (year, dept_id) to avoid collisions between branches in same dept
    # e.g. dept 101 has AI&DS and IT — first branch gets 001-050, second gets 051-100
    active_serial_counter = {}   # key: (join_year, dept_id) -> next serial
    passedout_serial_counter = {}  # key: dept_id -> next serial

    # ── Active students: 2023 (year 4) and 2024 (year 3), 50 per branch ──
    for branch in branches:
        dept_id = branch_dept_map[branch.branch_id]
        for i in range(50):
            # First 25: year 2023 (4th year), next 25: year 2024 (3rd year)
            if i < 25:
                join_year = 2023
                year_of_study = 4
            else:
                join_year = 2024
                year_of_study = 3

            key = (join_year, dept_id)
            serial = active_serial_counter.get(key, 1)
            active_serial_counter[key] = serial + 1

            register_no = f"{join_year}{dept_id:03d}{serial:03d}"
            email = f"{register_no}@university.edu"

            fname = random.choice(all_first_names)
            lname = random.choice(LAST_NAMES)
            dob = date(
                random.randint(2002, 2005),
                random.randint(1, 12),
                random.randint(1, 28)
            )
            phone = f"{random.choice(['9', '8', '7', '6'])}{random.randint(100000000, 999999999)}"
            cgpa = round(random.uniform(6.0, 9.8), 1)

            is_blacklisted = student_count in blacklist_indices

            user = User(
                email = email,
                password = password_hash,
                role = 'student',
                is_active = True,
                is_blacklisted = is_blacklisted,
                is_verified = True
            )
            db.session.add(user)
            db.session.flush()

            student = Student(
                register_no = register_no,
                user_id = user.user_id,
                fname = fname,
                lname = lname,
                dob = dob,
                phone = phone,
                cgpa = cgpa,
                year_of_study = year_of_study,
                branch_id = branch.branch_id
            )
            db.session.add(student)
            db.session.flush()

            # Assign 3-6 random skills
            num_skills = random.randint(3, 6)
            chosen_skills = random.sample(all_skills, min(num_skills, len(all_skills)))
            for skill in chosen_skills:
                db.session.execute(student_skill.insert().values(
                    register_no=register_no,
                    skill_id=skill.skill_id
                ))

            student_count += 1

    # ── Passed-out students: 2022 (is_active=False), ~5 per branch ──
    # We need ~50 total across 11 branches, so ~4-5 each
    passed_out_per_branch = []
    remaining = 50
    for idx, branch in enumerate(branches):
        count = min(5, remaining) if idx < 10 else remaining
        passed_out_per_branch.append(count)
        remaining -= count

    for branch_idx, branch in enumerate(branches):
        dept_id = branch_dept_map[branch.branch_id]
        count = passed_out_per_branch[branch_idx]
        for i in range(count):
            serial = passedout_serial_counter.get(dept_id, 1)
            passedout_serial_counter[dept_id] = serial + 1

            register_no = f"2022{dept_id:03d}{serial:03d}"
            email = f"{register_no}@university.edu"

            fname = random.choice(all_first_names)
            lname = random.choice(LAST_NAMES)
            dob = date(
                random.randint(2000, 2003),
                random.randint(1, 12),
                random.randint(1, 28)
            )
            phone = f"{random.choice(['9', '8', '7', '6'])}{random.randint(100000000, 999999999)}"
            cgpa = round(random.uniform(6.0, 9.5), 1)

            user = User(
                email = email,
                password = password_hash,
                role = 'student',
                is_active = False,
                is_blacklisted = False,
                is_verified = True
            )
            db.session.add(user)
            db.session.flush()

            student = Student(
                register_no = register_no,
                user_id = user.user_id,
                fname = fname,
                lname = lname,
                dob = dob,
                phone = phone,
                cgpa = cgpa,
                year_of_study = 5,  # graduated / passed out
                branch_id = branch.branch_id
            )
            db.session.add(student)
            db.session.flush()

            # Assign 3-5 random skills
            num_skills = random.randint(3, 5)
            chosen_skills = random.sample(all_skills, min(num_skills, len(all_skills)))
            for skill in chosen_skills:
                db.session.execute(student_skill.insert().values(
                    register_no=register_no,
                    skill_id=skill.skill_id
                ))

    db.session.commit()
    print(f'[SEED]\t{student_count} active students + 50 passed-out students seeded.')

# ─────────────────────────────────────────────────────────────────────────────
# 5. Companies (15 total)
# ─────────────────────────────────────────────────────────────────────────────

COMPANIES_DATA = [
    {
        'name': 'Amazon', 'industry': 'E-commerce & Cloud Computing',
        'website': 'https://www.amazon.com', 'location': 'Hyderabad, India',
        'description': 'Amazon is a multinational technology company focusing on e-commerce, cloud computing, and artificial intelligence.',
        'hr_name': 'Priya Sharma', 'hr_phone': '9876543201',
        'status': 'Approved',
    },
    {
        'name': 'Google', 'industry': 'Technology',
        'website': 'https://www.google.com', 'location': 'Bangalore, India',
        'description': 'Google is a global technology leader specializing in internet services, software, and hardware.',
        'hr_name': 'Rahul Menon', 'hr_phone': '9876543202',
        'status': 'Approved',
    },
    {
        'name': 'Apple', 'industry': 'Consumer Electronics & Software',
        'website': 'https://www.apple.com', 'location': 'Chennai, India',
        'description': 'Apple designs and manufactures consumer electronics, software, and online services.',
        'hr_name': 'Lakshmi Iyer', 'hr_phone': '9876543203',
        'status': 'Approved',
    },
    {
        'name': 'Wells Fargo', 'industry': 'Banking & Financial Services',
        'website': 'https://www.wellsfargo.com', 'location': 'Hyderabad, India',
        'description': 'Wells Fargo is a leading diversified financial services company with operations globally.',
        'hr_name': 'Anil Kumar', 'hr_phone': '9876543204',
        'status': 'Approved',
    },
    {
        'name': 'Fidelity Investments', 'industry': 'Financial Services',
        'website': 'https://www.fidelity.com', 'location': 'Chennai, India',
        'description': 'Fidelity Investments is an American multinational financial services corporation.',
        'hr_name': 'Meena Rajan', 'hr_phone': '9876543205',
        'status': 'Approved',
    },
    {
        'name': 'DE Shaw', 'industry': 'Financial Services & Technology',
        'website': 'https://www.deshaw.com', 'location': 'Hyderabad, India',
        'description': 'DE Shaw is a global investment and technology firm known for quantitative trading.',
        'hr_name': 'Karthik Nair', 'hr_phone': '9876543206',
        'status': 'Approved',
    },
    {
        'name': 'Microsoft', 'industry': 'Technology',
        'website': 'https://www.microsoft.com', 'location': 'Bangalore, India',
        'description': 'Microsoft is a technology corporation producing software, hardware, and cloud services.',
        'hr_name': 'Divya Subramanian', 'hr_phone': '9876543207',
        'status': 'Approved',
    },
    {
        'name': 'Infosys', 'industry': 'IT Consulting & Services',
        'website': 'https://www.infosys.com', 'location': 'Mysuru, India',
        'description': 'Infosys is a global leader in consulting, technology services, and digital transformation.',
        'hr_name': 'Venkat Raman', 'hr_phone': '9876543208',
        'status': 'Approved',
    },
    {
        'name': 'TCS', 'industry': 'IT Services & Consulting',
        'website': 'https://www.tcs.com', 'location': 'Mumbai, India',
        'description': 'Tata Consultancy Services is an Indian multinational IT services and consulting company.',
        'hr_name': 'Suresh Pillai', 'hr_phone': '9876543209',
        'status': 'Approved',
    },
    {
        'name': 'Oracle', 'industry': 'Enterprise Software',
        'website': 'https://www.oracle.com', 'location': 'Bangalore, India',
        'description': 'Oracle Corporation provides cloud infrastructure, database software, and enterprise solutions.',
        'hr_name': 'Ashwin Babu', 'hr_phone': '9876543210',
        'status': 'Approved',  # Approved company status, but user will be blacklisted
        'blacklisted': True,
    },
    {
        'name': 'Wipro', 'industry': 'IT Services',
        'website': 'https://www.wipro.com', 'location': 'Bangalore, India',
        'description': 'Wipro Limited is a leading Indian IT services company with a global presence.',
        'hr_name': 'Ramya Krishnan', 'hr_phone': '9876543211',
        'status': 'Pending',
    },
    {
        'name': 'Accenture', 'industry': 'Consulting & IT Services',
        'website': 'https://www.accenture.com', 'location': 'Chennai, India',
        'description': 'Accenture is a global professional services company offering strategy, consulting, and technology services.',
        'hr_name': 'Deepa Venkatesh', 'hr_phone': '9876543212',
        'status': 'Pending',
    },
    {
        'name': 'Capgemini', 'industry': 'IT Consulting',
        'website': 'https://www.capgemini.com', 'location': 'Mumbai, India',
        'description': 'Capgemini is a global leader in consulting, technology services, and digital transformation.',
        'hr_name': 'Ganesh Moorthy', 'hr_phone': '9876543213',
        'status': 'Pending',
    },
    {
        'name': 'Cognizant', 'industry': 'IT Services',
        'website': 'https://www.cognizant.com', 'location': 'Chennai, India',
        'description': 'Cognizant is an American multinational providing IT services, consulting, and business process outsourcing.',
        'hr_name': 'Nithya Sundaram', 'hr_phone': '9876543214',
        'status': 'Pending',
    },
    {
        'name': 'HCL Technologies', 'industry': 'Technology & IT Services',
        'website': 'https://www.hcltech.com', 'location': 'Noida, India',
        'description': 'HCL Technologies is a multinational IT services and consulting company.',
        'hr_name': 'Bala Murugan', 'hr_phone': '9876543215',
        'status': 'Pending',
    },
]

def seed_companies():
    if _already_seeded('companies'):
        print('[SEED]\tCompanies already seeded. Skipping.')
        return

    password_hash = _hash('com123')

    for idx, comp in enumerate(COMPANIES_DATA, start=1):
        login_email = f"company{idx:02d}@email.com"
        company_name_lower = comp['name'].lower().replace(' ', '')
        hr_email = f"{company_name_lower}@placement.com"

        is_blacklisted = comp.get('blacklisted', False)

        user = User(
            email = login_email,
            password = password_hash,
            role = 'company',
            is_active = not is_blacklisted,
            is_blacklisted = is_blacklisted,
            is_verified = True
        )
        db.session.add(user)
        db.session.flush()

        company = Company(
            user_id = user.user_id,
            company_name = comp['name'],
            industry = comp['industry'],
            website = comp['website'],
            location = comp['location'],
            description = comp['description'],
            hr_name = comp['hr_name'],
            hr_email = hr_email,
            hr_phone = comp['hr_phone'],
            status = comp['status']
        )
        db.session.add(company)

    db.session.commit()
    print('[SEED]\t15 companies seeded successfully.')

# ─────────────────────────────────────────────────────────────────────────────
# 6. Drives (~25 drives from 9 approved companies)
# ─────────────────────────────────────────────────────────────────────────────

# Drive data: (company_index (1-based), job_title, drive_type, cgpa_req, salary_min, salary_max, location, is_completed)
DRIVES_DATA = [
    # ── 5 COMPLETED drives ──
    (1, 'Software Development Intern',         '2M Internship',       6.5, 15000, 25000, 'Hyderabad',  True),
    (2, 'Cloud Engineering Intern',            '5M Internship',       7.0, 40000, 60000, 'Bangalore',  True),
    (3, 'iOS Developer',                       'Direct Placement',    7.5, 800000, 1200000, 'Chennai', True),
    (4, 'Data Analyst Intern',                 '6M Internship',       6.5, 30000, 45000, 'Hyderabad',  True),
    (5, 'QA Automation Intern',                '2M Internship',       6.0, 12000, 20000, 'Chennai',    True),

    # ── ONGOING / APPROVED drives ──
    # Amazon (company 1)
    (1, 'Backend Developer Intern',            '6M Internship',       7.0, 35000, 55000, 'Hyderabad',  False),
    (1, 'SDE - Full Time',                     'Direct Placement',    7.5, 1000000, 1800000, 'Hyderabad', False),

    # Google (company 2)
    (2, 'ML Research Intern',                  '2M Internship',       7.5, 20000, 40000, 'Bangalore',  False),
    (2, 'Software Engineer',                   'Direct Placement',    8.0, 1500000, 2500000, 'Bangalore', False),

    # Apple (company 3)
    (3, 'Hardware Test Intern',                '2M Internship',       6.5, 18000, 30000, 'Chennai',    False),
    (3, 'Embedded Systems Intern',             '5M Internship',       7.0, 40000, 65000, 'Chennai',    False),

    # Wells Fargo (company 4)
    (4, 'Risk Analytics Intern',               '2M Internship',       6.5, 15000, 25000, 'Hyderabad',  False),
    (4, 'Software Developer',                  '6M Internship + Performance-based Placement', 7.0, 500000, 900000, 'Hyderabad', False),

    # Fidelity (company 5)
    (5, 'Full Stack Developer Intern',         '5M Internship',       7.0, 35000, 50000, 'Chennai',    False),
    (5, 'Platform Engineer',                   'Direct Placement',    7.5, 900000, 1400000, 'Chennai',  False),

    # DE Shaw (company 6)
    (6, 'Quantitative Analyst Intern',         '2M Internship',       8.0, 25000, 50000, 'Hyderabad',  False),
    (6, 'Systems Developer',                   '6M Internship + Placement', 7.5, 600000, 1100000, 'Hyderabad', False),

    # Microsoft (company 7)
    (7, 'Azure Cloud Intern',                  '2M Internship',       7.0, 20000, 35000, 'Bangalore',  False),
    (7, 'Software Engineer Intern',            '5M Internship + Placement', 7.0, 500000, 800000, 'Bangalore', False),
    (7, 'Product Engineer',                    'Direct Placement',    7.5, 1200000, 2000000, 'Bangalore', False),

    # Infosys (company 8)
    (8, 'Systems Engineer Trainee',            '2M Internship',       6.0, 10000, 18000, 'Mysuru',     False),
    (8, 'Technology Analyst Intern',           '6M Internship',       6.5, 25000, 38000, 'Pune',       False),

    # TCS (company 9)
    (9, 'Digital Trainee',                     '2M Internship',       6.0, 10000, 15000, 'Mumbai',     False),
    (9, 'Assistant Systems Engineer',          '5M Internship + Performance-based Placement', 6.5, 350000, 700000, 'Chennai', False),
]

# Job descriptions for each drive
JOB_DESCRIPTIONS = [
    "Work on building and maintaining scalable software systems. Collaborate with cross-functional teams to deliver high-quality products.",
    "Design and implement cloud-based infrastructure solutions. Work with cutting-edge technologies in a collaborative environment.",
    "Develop native iOS applications for Apple's ecosystem. Work closely with design and engineering teams to build world-class products.",
    "Analyze large datasets to extract meaningful insights. Build dashboards and predictive models using modern analytics tools.",
    "Design and execute automated test suites for software products. Ensure product quality through comprehensive testing strategies.",
    "Build robust backend services using modern frameworks. Work on microservices architecture and API development.",
    "Design and develop full-stack applications. Lead projects from ideation to deployment in an agile environment.",
    "Conduct research in machine learning and AI. Develop novel algorithms and models for real-world applications.",
    "Build scalable software systems for Google's products. Work with world-class engineers on challenging problems.",
    "Test and validate hardware components. Collaborate with engineering teams on product quality assurance.",
    "Design embedded systems for Apple's hardware products. Work with sensors, microcontrollers, and real-time systems.",
    "Develop risk assessment models and analytics pipelines. Work with financial data to identify patterns and mitigate risks.",
    "Build enterprise software solutions for banking and financial services. Work on high-performance, secure applications.",
    "Develop full-stack web applications using modern frameworks. Contribute to microservices and cloud-native architectures.",
    "Build and maintain platform infrastructure. Work on CI/CD pipelines, monitoring, and deployment automation.",
    "Develop quantitative trading models and algorithms. Apply mathematical and statistical methods to financial markets.",
    "Build distributed systems for financial technology platforms. Work on low-latency, high-throughput applications.",
    "Develop cloud solutions on the Azure platform. Work with containerization, serverless computing, and DevOps.",
    "Build software products for Microsoft's enterprise solutions. Work on full-stack development with modern technologies.",
    "Design and develop products for Microsoft's cloud platform. Lead feature development in an agile team.",
    "Join as a Systems Engineer Trainee and undergo comprehensive training. Work on client projects across various technologies.",
    "Analyze and develop technology solutions for global clients. Work on enterprise applications and digital transformation.",
    "Join TCS's digital practice. Work on emerging technologies including cloud, AI, and blockchain.",
    "Build and maintain enterprise applications. Work with clients to deliver technology solutions at scale.",
]

def seed_drives():
    if _already_seeded('drives'):
        print('[SEED]\tDrives already seeded. Skipping.')
        return

    random.seed(42)
    companies = Company.query.order_by(Company.company_id).all()
    branches = Branch.query.all()
    all_skills = Skill.query.all()

    now = datetime.now()

    for idx, drive_data in enumerate(DRIVES_DATA):
        comp_idx, job_title, drive_type, cgpa_req, sal_min, sal_max, location, is_completed = drive_data

        company = companies[comp_idx - 1]  # 1-indexed to 0-indexed

        if is_completed:
            # Past deadline: 1-3 months ago
            days_ago = random.randint(30, 90)
            deadline = now - timedelta(days=days_ago)
            created = deadline - timedelta(days=random.randint(15, 30))
            status = 'Closed'
        else:
            # Future deadline: 1-3 months from now
            days_ahead = random.randint(30, 90)
            deadline = now + timedelta(days=days_ahead)
            created = now - timedelta(days=random.randint(5, 20))
            status = 'Approved'

        desc = JOB_DESCRIPTIONS[idx] if idx < len(JOB_DESCRIPTIONS) else f"Exciting opportunity at {company.company_name} for {job_title}."

        drive = PlacementDrive(
            company_id = company.company_id,
            job_title = job_title,
            job_desc = desc,
            drive_type = drive_type,
            cgpa_requirement = cgpa_req,
            salary_min = sal_min,
            salary_max = sal_max,
            location = location,
            application_deadline = deadline,
            status = status,
            created_at = created,
            updated_at = created
        )
        db.session.add(drive)
        db.session.flush()

        # Assign eligible branches (2-5 random branches, or all for large companies)
        if drive_type == '2M Internship':
            # Open to more branches
            num_branches = random.randint(4, min(8, len(branches)))
        else:
            num_branches = random.randint(2, min(5, len(branches)))

        eligible = random.sample(branches, num_branches)
        for branch in eligible:
            db.session.execute(drive_branch.insert().values(
                drive_id=drive.drive_id,
                branch_id=branch.branch_id
            ))

        # Assign required skills (2-4 random skills)
        num_skills = random.randint(2, 4)
        chosen_skills = random.sample(all_skills, num_skills)
        for skill in chosen_skills:
            db.session.execute(drive_skill.insert().values(
                drive_id=drive.drive_id,
                skill_id=skill.skill_id
            ))

    db.session.commit()
    print(f'[SEED]\t{len(DRIVES_DATA)} drives seeded successfully.')

# ─────────────────────────────────────────────────────────────────────────────
# 7. Interviews (for completed drives)
# ─────────────────────────────────────────────────────────────────────────────

INTERVIEW_TEMPLATES = [
    [
        ('Online Assessment', 'Online'),
        ('Technical Interview', 'On-Campus'),
        ('HR Interview', 'On-Campus'),
    ],
    [
        ('Aptitude Test', 'Online'),
        ('Technical Interview', 'On-Campus'),
    ],
    [
        ('Coding Challenge', 'Online'),
        ('Technical Interview Round 1', 'On-Campus'),
        ('Technical Interview Round 2', 'On-Campus'),
    ],
    [
        ('Online Assessment', 'Online'),
        ('Group Discussion', 'On-Campus'),
        ('HR Interview', 'On-Campus'),
    ],
    [
        ('Aptitude Test', 'Online'),
        ('Technical Interview', 'On-Campus'),
        ('Managerial Interview', 'Virtual'),
    ],
]

def seed_interviews():
    """Create interview rounds for the 5 completed drives."""
    completed_drives = PlacementDrive.query.filter_by(status='Closed').all()

    if not completed_drives:
        print('[SEED]\tNo completed drives found for interviews. Skipping.')
        return

    if Interview.query.first():
        print('[SEED]\tInterviews already seeded. Skipping.')
        return

    for idx, drive in enumerate(completed_drives):
        template = INTERVIEW_TEMPLATES[idx % len(INTERVIEW_TEMPLATES)]
        base_date = drive.application_deadline + timedelta(days=5)

        for round_num, (title, location) in enumerate(template, start=1):
            interview_date = base_date + timedelta(days=(round_num - 1) * 7)
            interview = Interview(
                drive_id = drive.drive_id,
                round_number = round_num,
                round_title = title,
                interview_date = interview_date,
                location = location
            )
            db.session.add(interview)

    db.session.commit()
    print(f'[SEED]\tInterviews seeded for {len(completed_drives)} completed drives.')

# ─────────────────────────────────────────────────────────────────────────────
# 8. Applications & Placements
# ─────────────────────────────────────────────────────────────────────────────

def seed_applications_and_placements():
    if _already_seeded('applications'):
        print('[SEED]\tApplications already seeded. Skipping.')
        return

    random.seed(42)

    all_drives = PlacementDrive.query.all()
    completed_drives = [d for d in all_drives if d.status == 'Closed']
    active_drives = [d for d in all_drives if d.status == 'Approved']

    # Get all active, non-blacklisted students
    active_students = (
        Student.query
        .join(User)
        .filter(User.is_active == True, User.is_blacklisted == False)
        .all()
    )

    # Track placed students (register_nos) so they can't apply to more drives
    placed_students = set()
    # Track (register_no, drive_id) to prevent duplicate applications
    applied_pairs = set()

    def get_eligible_students(drive):
        """Get students eligible for a drive based on constraints."""
        eligible_branch_ids = {b.branch_id for b in drive.eligible_branches}
        eligible = []
        for student in active_students:
            if student.register_no in placed_students:
                continue
            if student.branch_id not in eligible_branch_ids:
                continue
            if student.cgpa < drive.cgpa_requirement:
                continue
            # Year constraint
            if student.year_of_study == 3 and drive.drive_type != '2M Internship':
                continue
            if student.year_of_study == 4 and drive.drive_type == '2M Internship':
                continue
            # Skip passed-out students (year_of_study == 5)
            if student.year_of_study not in (3, 4):
                continue
            if (student.register_no, drive.drive_id) in applied_pairs:
                continue
            eligible.append(student)
        return eligible

    # ── Applications for COMPLETED drives ──
    for drive in completed_drives:
        eligible = get_eligible_students(drive)
        if not eligible:
            continue

        # 30-60 applications per completed drive (or all eligible if fewer)
        num_applicants = min(random.randint(30, 60), len(eligible))
        applicants = random.sample(eligible, num_applicants)

        # Get interview rounds for this drive
        interviews = Interview.query.filter_by(drive_id=drive.drive_id).order_by(Interview.round_number).all()
        final_round = interviews[-1] if interviews else None

        # Decide how many get each status
        num_selected = random.randint(5, 10)
        num_rejected = random.randint(5, 10)
        num_shortlisted = random.randint(3, 5)

        for i, student in enumerate(applicants):
            applied_date = drive.created_at + timedelta(days=random.randint(1, 14))
            applied_pairs.add((student.register_no, drive.drive_id))

            if i < num_selected:
                status = 'Selected'
                current_round_id = final_round.interview_id if final_round else None
                feedback = 'Excellent performance across all rounds. Offer extended.'
            elif i < num_selected + num_rejected:
                status = 'Rejected'
                round_idx = random.randint(0, len(interviews) - 1) if interviews else None
                current_round_id = interviews[round_idx].interview_id if round_idx is not None else None
                feedback = random.choice([
                    'Did not meet the technical requirements for this role.',
                    'Performance below expectations in the interview round.',
                    'Better suited for a different role. Encouraged to reapply.',
                    'Good fundamentals but needs more practical experience.',
                ])
            elif i < num_selected + num_rejected + num_shortlisted:
                status = 'Shortlisted'
                current_round_id = None
                feedback = None
            else:
                # Remaining are Applied or Withdrawn
                if random.random() < 0.15:
                    status = 'Withdrawn'
                    feedback = 'Student withdrew from the process.'
                else:
                    status = 'Applied'
                    feedback = None
                current_round_id = None

            application = Application(
                register_no = student.register_no,
                drive_id = drive.drive_id,
                applied_date = applied_date,
                application_status = status,
                current_round_id = current_round_id,
                feedback = feedback
            )
            db.session.add(application)
            db.session.flush()

            # Create placement for Selected students
            if status == 'Selected':
                placement = Placement(
                    application_id = application.application_id,
                    position = drive.job_title,
                    drive_type = drive.drive_type,
                    salary = drive.salary_max,
                    joining_date = date(2026, random.randint(7, 9), random.randint(1, 28))
                )
                db.session.add(placement)
                placed_students.add(student.register_no)

    db.session.flush()

    # ── Applications for ACTIVE/APPROVED drives ──
    for drive in active_drives:
        eligible = get_eligible_students(drive)
        if not eligible:
            continue

        # 10-30 applications per active drive
        num_applicants = min(random.randint(10, 30), len(eligible))
        applicants = random.sample(eligible, num_applicants)

        for i, student in enumerate(applicants):
            applied_date = drive.created_at + timedelta(days=random.randint(1, 10))
            applied_pairs.add((student.register_no, drive.drive_id))

            # Mostly Applied, some Shortlisted
            if random.random() < 0.2:
                status = 'Shortlisted'
            else:
                status = 'Applied'

            application = Application(
                register_no = student.register_no,
                drive_id = drive.drive_id,
                applied_date = applied_date,
                application_status = status,
                feedback = None
            )
            db.session.add(application)

    db.session.commit()
    total_apps = Application.query.count()
    total_placements = Placement.query.count()
    print(f'[SEED]\t{total_apps} applications and {total_placements} placements seeded.')

# ─────────────────────────────────────────────────────────────────────────────
# Run All Seeds
# ─────────────────────────────────────────────────────────────────────────────

def run_seed():
    seed_admin()
    seed_departments_and_branches()
    seed_skills()
    seed_students()
    seed_companies()
    seed_drives()
    seed_interviews()
    seed_applications_and_placements()