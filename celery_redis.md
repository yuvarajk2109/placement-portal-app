# Celery & Redis Integration Guide — Placement Portal Backend

This document is a **complete, sequential, step-by-step guide** for adding Celery (background tasks) and Redis (message broker + caching) to the existing Placement Portal Flask backend. Every piece of code here is **final, production-ready code** — not patterns or pseudocode.

> [!IMPORTANT]
> **Platform note**: Celery does **not** run natively on Windows. You must run the Celery worker + Celery Beat + Redis server inside **WSL (Ubuntu)**. The Flask dev server can still run on Windows, but the Redis URL must point to WSL's Redis instance (usually `redis://localhost:6379`).

---

## Table of Contents

1. [Prerequisites — Install Redis in WSL](#step-1--install-redis-in-wsl)
2. [Update `config.py` — Add Redis & Celery Config](#step-2--update-configpy)
3. [Update `extensions.py` — Add Redis Client](#step-3--update-extensionspy)
4. [Create `utils/cache_utils.py` — Redis Caching Utilities](#step-4--create-utilscache_utilspy)
5. [Create `backend/jobs/` Directory — Celery App & Tasks](#step-5--create-the-backendjobs-directory)
   - 5a. `jobs/__init__.py`
   - 5b. `jobs/celery_app.py` — Celery instance
   - 5c. `jobs/daily_reminder.py` — Scheduled daily email reminders
   - 5d. `jobs/monthly_report.py` — Scheduled monthly admin report
   - 5e. `jobs/export_csv.py` — User-triggered CSV export
6. [Create `backend/templates/monthly_report.html` — Email Template](#step-6--create-the-email-template)
7. [Update `app.py` — Wire Celery Into Flask](#step-7--update-apppy)
8. [Add CSV Export Endpoint to Student Routes](#step-8--add-csv-export-endpoint)
9. [Add `@cache_response` Decorators to GET Routes](#step-9--add-cache-decorators-to-routes)
10. [Add `invalidate_cache()` Calls to Service Methods](#step-10--add-cache-invalidation-to-services)
11. [How to Run Everything](#step-11--how-to-run-everything)
12. [How to Test / Verify](#step-12--how-to-test--verify)
13. [Concepts Explained](#concepts-explained)

---

## Step 1 — Install Redis in WSL

**What**: Redis is an in-memory key-value store. We use it for two things:
1. **Celery message broker** — Celery uses Redis to queue task messages (like "send daily reminders now").
2. **API response caching** — We store frequently-requested API responses in Redis so repeated calls are instant.

**Why WSL**: Redis is a Linux-native tool. On Windows, the recommended approach is to run Redis inside WSL Ubuntu.

### 1.1 Install Redis

Open your WSL Ubuntu terminal and run:

```bash
sudo apt update
sudo apt install redis-server -y
```

### 1.2 Start Redis

```bash
# Start the Redis server
sudo service redis-server start

# Verify it's running
redis-cli ping
# Should print: PONG
```

> [!TIP]
> Redis runs on `localhost:6379` by default. Since WSL shares the network with Windows, your Flask app on Windows can connect to `redis://localhost:6379` and it will reach the WSL Redis instance.

### 1.3 (Optional) Make Redis start automatically

```bash
sudo systemctl enable redis-server
```

Or, if systemd isn't available in your WSL, just run `sudo service redis-server start` each time you open WSL.

---

## Step 2 — Update `config.py`

**What**: Add three new configuration values for Redis and Celery URLs.

**Why**: 
- `CELERY_BROKER_URL` — tells Celery where to find Redis to send/receive task messages. We use database `0` in Redis.
- `CELERY_RESULT_BACKEND` — tells Celery where to store task results (success/failure info). Same Redis, database `0`.
- `REDIS_URL` — the Redis connection used for API response caching. We use database `1` to keep cache data separate from Celery data.

**File**: [config.py](/backend/config.py)

**Add these 4 lines at the end of the `Config` class** (after `APPLICATION_ACTIONS`):

```python
    # ========================
    # Redis & Celery (Milestone 7 & 8)
    # ========================
    CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0')
    CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')
    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/1')
```

**Explanation of Redis database numbers**:
- Redis has 16 databases (0–15) by default. They're like namespaces.
- Database `0` → Celery broker + result backend (task messages).
- Database `1` → API response cache.
- This prevents Celery's internal keys from colliding with our cache keys.

### Full `config.py` after edit:

```python
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'yuvaraj_k')
    ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    UPLOAD_FOLDER = os.path.join(ROOT_DIR, 'uploads')

    DATABASE_PATH = os.path.abspath(os.path.join(ROOT_DIR, "db", "placement_portal.db"))
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{DATABASE_PATH}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'yuvaraj_k_jwt_secret_key')
    JWT_ACCESS_TOKEN_EXPIRES = 3600
    JWT_REFRESH_TOKEN_EXPIRES = 86400

    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv('MAIL_USERNAME', 'Starspinix')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD', 'pbqd dxrv olub rqcr')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER', 'starspinix@gmail.com')

    RESUME_FOLDER = os.path.join(UPLOAD_FOLDER, 'resumes')
    ALLOWED_RESUME_EXTENSIONS = {'pdf', 'doc', 'docx'}
    MAX_RESUME_SIZE = 5 * 1024 * 1024

    VALID_DRIVE_TYPES = [
        '2M Internship',
        '5M Internship',
        '6M Internship',
        '5M Internship + Placement',
        '6M Internship + Placement',
        '5M Internship + Performance-based Placement',
        '6M Internship + Performance-based Placement',
        'Direct Placement'
    ]

    STUDENT_APPLICATION_STATUSES = [
        'Applied',
        'Shortlisted',
        'Selected for Next Round',
        'Selected',
        'Rejected',
        'Withdrawn',
        'Not Applied'
    ]

    APPLICATION_ACTIONS = [
        'Shortlisted', 
        'Selected for Next Round', 
        'Selected', 
        'Rejected'
    ]

    # ========================
    # Redis & Celery (Milestone 7 & 8)
    # ========================
    CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0')
    CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')
    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/1')
```

---

## Step 3 — Update `extensions.py`

**What**: Add a Redis client instance alongside the existing Flask extensions.

**Why**: We need a global `redis_client` object that `cache_utils.py` can import and use. We use `redis.from_url()` to create the client from the `REDIS_URL` config. If Redis isn't running, we set `redis_client = None` so the app still works — caching is gracefully disabled.

**File**: [extensions.py](/backend/extensions.py)

### Full replacement `extensions.py`:

```python
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from flask_cors import CORS
import redis
import os

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
mail = Mail()
cors = CORS()

# Redis client for API response caching (Milestone 8).
# Uses REDIS_URL from config/env. If Redis is not running,
# redis_client is set to None and caching is silently disabled.
try:
    redis_client = redis.from_url(
        os.getenv('REDIS_URL', 'redis://localhost:6379/1')
    )
    redis_client.ping()  # Test the connection immediately
except Exception:
    redis_client = None
```

**What each line does**:
- `import redis` — the `redis` package is already in `requirements.txt` (version 6.4.0).
- `redis.from_url(...)` — creates a Redis client from a URL like `redis://localhost:6379/1`.
- `.ping()` — sends a `PING` command to Redis. If it responds `PONG`, the connection is alive.
- The `try/except` ensures that if Redis isn't running, `redis_client` is `None` and the app doesn't crash. Every function in `cache_utils.py` checks for `None` before using it.

---

## Step 4 — Create `utils/cache_utils.py`

**What**: A utility module with two functions:
1. `cache_response(ttl, key_prefix)` — a **decorator** for GET API routes that caches their JSON responses in Redis.
2. `invalidate_cache(pattern)` — a function that deletes cached keys when data changes.

**Why**: Without caching, every API call hits the SQLite database. For high-traffic read endpoints (dashboard stats, drive lists, student lists), we can store the response in Redis for a few minutes. When data changes (a drive is approved, a student applies), we call `invalidate_cache()` to clear stale data.

**File**: `backend/utils/cache_utils.py` (NEW FILE)

```python
import json
from functools import wraps
from flask import request
from extensions import redis_client
import logging

logger = logging.getLogger(__name__)

DEFAULT_TTL = 300  # 5 minutes (in seconds)


def cache_response(ttl=DEFAULT_TTL, key_prefix=None):
    """
    Decorator to cache JSON API responses in Redis.

    How it works:
    1. When a GET request comes in, we build a cache key from the
       key_prefix + the full URL path + query string.
    2. We check Redis for that key. If found → return the cached JSON
       immediately (cache HIT). No database query happens.
    3. If not found (cache MISS) → call the actual route function,
       store the response in Redis with an expiry time (TTL), then
       return it.

    Args:
        ttl (int): Time-to-live in seconds. After this, Redis auto-deletes
                   the key. Default is 300 (5 minutes).
        key_prefix (str): A label like 'admin_dashboard' or 'student_drives'.
                          Used to group related cache keys so we can
                          invalidate them together.
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            # If Redis is not available, skip caching entirely
            if redis_client is None:
                return fn(*args, **kwargs)

            # Build a unique cache key:
            #   cache:admin_dashboard:/api/admin/dashboard?
            # request.full_path includes query params, so
            # /api/student/drives?page=1 and ?page=2 are different keys.
            prefix = key_prefix or fn.__name__
            cache_key = f"cache:{prefix}:{request.full_path}"

            # --- Try to read from cache ---
            try:
                cached = redis_client.get(cache_key)
                if cached:
                    logger.debug(f"Cache HIT: {cache_key}")
                    return json.loads(cached), 200
            except Exception as e:
                logger.warning(f"Redis read error: {e}")

            # --- Cache MISS — call the actual route function ---
            result = fn(*args, **kwargs)

            # Only cache successful (200) responses.
            # Route functions return (dict, status_code) tuples.
            if isinstance(result, tuple):
                response_data, status_code = result
                if status_code == 200:
                    try:
                        redis_client.setex(
                            cache_key,     # key name
                            ttl,           # expiry in seconds
                            json.dumps(response_data)  # JSON string
                        )
                        logger.debug(f"Cache SET: {cache_key} (TTL={ttl}s)")
                    except Exception as e:
                        logger.warning(f"Redis write error: {e}")
                return response_data, status_code

            return result
        return wrapper
    return decorator


def invalidate_cache(pattern):
    """
    Delete all Redis cache keys matching a pattern.

    When data changes (e.g., a drive is approved), we need to remove
    stale cached responses. This function finds all keys like
    `cache:admin_drives:*` and deletes them.

    Args:
        pattern (str): The key_prefix to match.
                       e.g. 'admin_drives' will delete all keys matching
                       'cache:admin_drives:*'
    """
    if redis_client is None:
        return
    try:
        keys = redis_client.keys(f"cache:{pattern}:*")
        if keys:
            redis_client.delete(*keys)
            logger.info(f"Cache invalidated: {len(keys)} keys matching '{pattern}'")
    except Exception as e:
        logger.warning(f"Redis invalidation error: {e}")
```

**How `setex` works**: `redis_client.setex(key, ttl, value)` sets a key with an automatic expiry. After `ttl` seconds, Redis deletes it automatically. This means even if we forget to invalidate, stale data only lasts a few minutes.

**How `keys` + `delete` works**: `redis_client.keys("cache:admin_drives:*")` returns all keys starting with that prefix. Then `redis_client.delete(*keys)` deletes them all at once.

---

## Step 5 — Create the `backend/jobs/` Directory

**What**: A new `jobs/` package containing the Celery app factory and three background task modules.

**Why Celery**: Some operations are too slow or should be scheduled:
- **Daily reminders** — every morning at 8 AM, email students about upcoming drive deadlines.
- **Monthly reports** — on the 1st of each month, email the admin a summary of last month's activity.
- **CSV export** — when a student clicks "Export", generate a CSV file and email it. This can take time, so we do it in the background and notify when done.

Celery runs as a **separate process** alongside Flask. Flask sends task requests to Redis ("please run `send_daily_reminders`"), and the Celery worker process picks them up and executes them.

### 5a. Create `backend/jobs/__init__.py` (empty file)

```python
# This file makes 'jobs' a Python package.
# It can remain empty.
```

### 5b. Create `backend/jobs/celery_app.py`

**What**: The factory function that creates a Celery instance tied to your Flask app.

**Why**: Celery needs access to Flask's app context (to use SQLAlchemy, Flask-Mail, etc.). The `ContextTask` class ensures every Celery task runs inside Flask's context.

```python
from celery import Celery
from celery.schedules import crontab


def make_celery(app):
    """
    Create a Celery instance tied to the Flask app context.

    How it works:
    1. We create a Celery instance, pointing it at Redis as the broker
       (where task messages are queued) and backend (where results are stored).
    2. We define a beat_schedule — these are cron-like scheduled tasks that
       Celery Beat will trigger automatically.
    3. We create a custom ContextTask that wraps every task execution
       inside Flask's app_context(). This is critical because our tasks
       use SQLAlchemy (db.session) and Flask-Mail (mail.send), which
       require Flask's context to work.

    Args:
        app: The Flask application instance.

    Returns:
        celery: A configured Celery instance.
    """
    celery = Celery(
        app.import_name,
        broker=app.config['CELERY_BROKER_URL'],
        backend=app.config['CELERY_RESULT_BACKEND'],
    )
    celery.conf.update(app.config)

    # ----- Scheduled tasks (run by Celery Beat) -----
    celery.conf.beat_schedule = {
        'daily-reminder': {
            'task': 'jobs.daily_reminder.send_daily_reminders',
            'schedule': crontab(hour=8, minute=0),
            # Runs every day at 8:00 AM.
            # crontab(hour=8, minute=0) means:
            #   minute=0  → at the 0th minute
            #   hour=8    → at the 8th hour
            #   day/month/dow = * (every day)
        },
        'monthly-report': {
            'task': 'jobs.monthly_report.generate_monthly_report',
            'schedule': crontab(day_of_month=1, hour=6, minute=0),
            # Runs on the 1st of every month at 6:00 AM.
        },
    }

    class ContextTask(celery.Task):
        """
        A custom Task class that pushes Flask's app context
        before running any task. Without this, db.session and
        mail.send() would fail with 'working outside application context'.
        """
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery
```

**Key concepts**:
- `broker` — the Redis URL where Celery sends task messages. Think of it as a to-do list in Redis.
- `backend` — where Celery stores task results (success/failure status). Also Redis.
- `beat_schedule` — a dict of tasks that Celery Beat triggers on a schedule. Without Beat, only user-triggered tasks work.
- `crontab(hour=8, minute=0)` — runs at 08:00 every day, like a Linux cron job `0 8 * * *`.
- `ContextTask` — ensures Flask's database connection, mail client, etc. are available inside tasks.

### 5c. Create `backend/jobs/daily_reminder.py`

**What**: A scheduled task that runs every morning. It finds approved placement drives with deadlines in the next 3 days, checks which eligible students haven't applied yet, and emails them a reminder.

**Why**: Students might forget about deadlines. Automatic reminders increase application rates.

```python
from datetime import date, timedelta
from flask_mail import Message
from extensions import db, mail
from models.application import Application
from models.placement_drive import PlacementDrive
from models.student import Student
from models.user import User
import logging

logger = logging.getLogger(__name__)


def send_daily_reminders(self):
    """
    Scheduled task: runs daily at 8 AM (configured in celery_app.py).

    Logic:
    1. Find all approved drives whose application_deadline is between
       today and 3 days from now (inclusive).
    2. For each active, verified student:
       a. Check year-based eligibility (Year 3 → only '2M Internship',
          Year 4 → everything except '2M Internship').
       b. Check if they've already applied.
       c. Check if their CGPA meets the requirement.
    3. If there are eligible drives the student hasn't applied to,
       send them an email listing those drives.

    The `self` parameter is required because Celery binds the function
    as a method on its Task class (via celery.task()).
    """
    upcoming_date = date.today() + timedelta(days=3)

    # Find drives with deadlines in the next 3 days
    drives = PlacementDrive.query.filter(
        PlacementDrive.status == 'Approved',
        PlacementDrive.application_deadline <= upcoming_date,
        PlacementDrive.application_deadline >= date.today(),
    ).all()

    if not drives:
        logger.info("[REMINDER] No upcoming deadlines found.")
        return "No reminders sent."

    # Find all active, verified students
    students = Student.query.join(User).filter(
        User.is_active == True,
        User.is_blacklisted == False,
        User.is_verified == True,
    ).all()

    count = 0
    for student in students:
        user = User.query.get(student.user_id)
        eligible_drives = []

        for drive in drives:
            # Year-based eligibility check
            if student.year_of_study == 3 and drive.drive_type != '2M Internship':
                continue
            if student.year_of_study == 4 and drive.drive_type == '2M Internship':
                continue

            # Check if already applied
            already_applied = Application.query.filter_by(
                register_no=student.register_no,
                drive_id=drive.drive_id,
            ).first()

            # Only include if not applied AND CGPA meets requirement
            if not already_applied and student.cgpa >= drive.cgpa_requirement:
                eligible_drives.append(drive)

        if eligible_drives:
            drive_list = "\n".join(
                f"  - {d.job_title} (Deadline: {d.application_deadline.strftime('%Y-%m-%d %H:%M')})"
                for d in eligible_drives
            )
            try:
                msg = Message(
                    subject="Placement Portal - Upcoming Deadline Reminder",
                    recipients=[user.email],
                    body=(
                        f"Hi {student.fname},\n\n"
                        f"The following placement drives have upcoming deadlines:\n"
                        f"{drive_list}\n\n"
                        f"Don't miss out - apply now!\n\n"
                        f"Regards,\nPlacement Portal Team"
                    ),
                )
                mail.send(msg)
                count += 1
            except Exception as e:
                logger.error(f"Failed to send reminder to {user.email}: {e}")

    logger.info(f"[REMINDER] Sent reminders to {count} students.")
    return f"Sent {count} reminders."
```

> [!NOTE]
> **Codebase-specific adaptations made** (vs the implementation plan):
> - `student.first_name` → `student.fname` (actual model field name)
> - `drive.deadline` → `drive.application_deadline` (actual model field name)
> - Drive type values use spaces: `'2M Internship'` not `'2m_internship'`
> - Status comparison uses `'Approved'` (capitalized, matching actual DB values)

### 5d. Create `backend/jobs/monthly_report.py`

**What**: A scheduled task that runs on the 1st of every month. It generates a summary of last month's placement activity (drives, applications, selections, placements) as an HTML email and sends it to the admin.

**Why**: The admin gets a periodic overview without needing to check the dashboard manually.

```python
from datetime import date, timedelta
from flask import render_template
from flask_mail import Message
from extensions import db, mail
from models.placement_drive import PlacementDrive
from models.application import Application
from models.placement import Placement
from models.user import User
import logging

logger = logging.getLogger(__name__)


def generate_monthly_report(self):
    """
    Scheduled task: runs on the 1st of every month at 6 AM.

    Logic:
    1. Calculate last month's date range.
    2. Count: drives created, applications received, students selected,
       confirmed placements — all within that date range.
    3. Render an HTML template with these stats.
    4. Email the report to the admin user.

    The `self` parameter is required by Celery's task binding.
    """
    today = date.today()
    first_of_this_month = today.replace(day=1)
    last_month_end = first_of_this_month - timedelta(days=1)
    last_month_start = last_month_end.replace(day=1)

    # Count stats for last month
    drives_count = PlacementDrive.query.filter(
        PlacementDrive.created_at >= last_month_start,
        PlacementDrive.created_at <= last_month_end,
    ).count()

    applications_count = Application.query.filter(
        Application.applied_date >= last_month_start,
        Application.applied_date <= last_month_end,
    ).count()

    selected_count = Application.query.filter(
        Application.application_status == 'Selected',
        Application.updated_at >= last_month_start,
        Application.updated_at <= last_month_end,
    ).count()

    placements_count = Placement.query.filter(
        Placement.created_at >= last_month_start,
        Placement.created_at <= last_month_end,
    ).count()

    report_data = {
        'month': last_month_start.strftime('%B %Y'),       # e.g. "June 2026"
        'drives_count': drives_count,
        'applications_count': applications_count,
        'selected_count': selected_count,
        'placements_count': placements_count,
        'generated_on': today.isoformat(),
    }

    # Render the HTML email template
    html_content = render_template('monthly_report.html', **report_data)

    # Find the admin user and send the report
    admin = User.query.filter_by(role='admin').first()
    if admin:
        try:
            msg = Message(
                subject=f"Placement Portal - Monthly Report ({report_data['month']})",
                recipients=[admin.email],
                html=html_content,
            )
            mail.send(msg)
            logger.info(f"[REPORT] Monthly report sent to {admin.email}")
        except Exception as e:
            logger.error(f"Failed to send monthly report: {e}")

    return report_data
```

### 5e. Create `backend/jobs/export_csv.py`

**What**: A user-triggered async task. When a student clicks "Export Applications", this task:
1. Queries all their applications from the database.
2. Writes them to a CSV file.
3. Emails the CSV as an attachment to the student.

**Why**: Generating a CSV with many applications and sending an email can take several seconds. By offloading it to Celery, the API responds instantly ("Export started!") while the heavy work happens in the background.

```python
import csv
import os
from datetime import datetime
from extensions import db, mail
from flask_mail import Message
from models.application import Application
from models.placement_drive import PlacementDrive
from models.company import Company
from models.student import Student
from models.user import User
import logging

logger = logging.getLogger(__name__)

# Directory where exported CSV files are saved
EXPORT_DIR = os.path.join(os.path.dirname(__file__), '..', 'uploads', 'exports')


def export_applications_csv(self, user_id):
    """
    User-triggered async task.

    Called when a student hits POST /api/student/export/applications.
    The route sends the task to Celery (via .delay(user_id)), and the
    student gets an immediate response. This function runs in the
    Celery worker process.

    Logic:
    1. Find the student by user_id.
    2. Query all their applications, ordered by date (newest first).
    3. Write to CSV with columns: Register No, Company Name, Drive Title,
       Drive Type, Application Status, Applied Date, Updated At.
    4. Email the CSV file to the student as an attachment.

    Args:
        self: Celery task instance (injected by Celery's task binding).
        user_id (int): The user_id of the student requesting the export.
    """
    # Ensure the export directory exists
    os.makedirs(EXPORT_DIR, exist_ok=True)

    student = Student.query.filter_by(user_id=user_id).first()
    if not student:
        logger.error(f"Student not found for user_id={user_id}")
        return "Student not found"

    user = User.query.get(user_id)
    applications = Application.query.filter_by(
        register_no=student.register_no
    ).order_by(Application.applied_date.desc()).all()

    # Generate CSV file
    timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
    filename = f"applications_{student.register_no}_{timestamp}.csv"
    filepath = os.path.join(EXPORT_DIR, filename)

    with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        # Header row
        writer.writerow([
            'Register No', 'Company Name',
            'Drive Title', 'Drive Type', 'Application Status',
            'Applied Date', 'Updated At'
        ])
        # Data rows
        for app in applications:
            drive = PlacementDrive.query.get(app.drive_id)
            company = Company.query.get(drive.company_id) if drive else None
            writer.writerow([
                student.register_no,
                company.company_name if company else 'N/A',
                drive.job_title if drive else 'N/A',
                drive.drive_type if drive else 'N/A',
                app.application_status,
                app.applied_date.isoformat() if app.applied_date else '',
                app.updated_at.isoformat() if app.updated_at else '',
            ])

    # Send the CSV as an email attachment
    try:
        msg = Message(
            subject="Placement Portal - Your Application Export is Ready",
            recipients=[user.email],
            body=(
                f"Hi {student.fname},\n\n"
                f"Your application history export is attached.\n\n"
                f"Regards,\nPlacement Portal Team"
            ),
        )
        with open(filepath, 'rb') as f:
            msg.attach(filename, 'text/csv', f.read())
        mail.send(msg)
        logger.info(f"[EXPORT] CSV sent to {user.email}")
    except Exception as e:
        logger.error(f"Failed to send CSV export: {e}")

    return {"file": filename, "status": "completed"}
```

---

## Step 6 — Create the Email Template

**What**: An HTML template for the monthly report email. Flask's `render_template()` renders this with the report data.

**Why**: HTML emails look much better than plain text. The template uses inline styles because most email clients don't support external CSS.

**File**: `backend/templates/monthly_report.html` (NEW FILE — create the `templates/` directory)

```html
<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        h1 { color: #2c3e50; }
        table { border-collapse: collapse; width: 60%; margin: 20px 0; }
        th, td { border: 1px solid #bdc3c7; padding: 10px 15px; text-align: left; }
        th { background-color: #2c3e50; color: white; }
        tr:nth-child(even) { background-color: #ecf0f1; }
        .footer { margin-top: 30px; font-size: 12px; color: #7f8c8d; }
    </style>
</head>
<body>
    <h1>Placement Portal - Monthly Activity Report</h1>
    <p><strong>Month:</strong> {{ month }}</p>
    <p><strong>Generated On:</strong> {{ generated_on }}</p>

    <table>
        <tr><th>Metric</th><th>Count</th></tr>
        <tr><td>Placement Drives Conducted</td><td>{{ drives_count }}</td></tr>
        <tr><td>Total Applications Received</td><td>{{ applications_count }}</td></tr>
        <tr><td>Students Selected</td><td>{{ selected_count }}</td></tr>
        <tr><td>Confirmed Placements</td><td>{{ placements_count }}</td></tr>
    </table>

    <div class="footer">
        <p>This is an automated report generated by the Placement Portal system.</p>
    </div>
</body>
</html>
```

**Template variables** (passed from `generate_monthly_report()`):
- `{{ month }}` — e.g. "June 2026"
- `{{ generated_on }}` — e.g. "2026-07-01"
- `{{ drives_count }}`, `{{ applications_count }}`, `{{ selected_count }}`, `{{ placements_count }}` — integer counts

---

## Step 7 — Update `app.py`

**What**: Wire the Celery instance into the Flask app so that:
1. The Celery worker can be started with `celery -A app.celery ...`
2. The three task functions are registered with Celery.
3. The `celery` object is accessible at module level (needed by the Celery CLI).

**Why**: Celery needs to discover tasks and bind them to the Flask app context. The `celery` variable must be at module level so the `celery -A app.celery worker` command can find it.

**File**: [app.py](/backend/app.py)

### Full replacement `app.py`:

```python
import logging
from flask import Flask
from config import Config
from extensions import db, migrate, jwt, mail, cors
from routes import register_blueprints
from utils.error_handlers import register_error_handlers
from seed import run_seed

def create_app(config_class = Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    logging.basicConfig(
        level = logging.INFO,
        format = '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
    )
    app.logger.setLevel(logging.INFO)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    mail.init_app(app)
    cors.init_app(app)

    register_blueprints(app)
    register_error_handlers(app)

    with app.app_context():
        db.create_all()
        print("[APP]\tAll DB Tables Created.")
        run_seed()
        print("[SEED]\tDB Seeding Complete.")

    return app

# =============================================
# Celery Integration (Milestone 7)
# =============================================
# The `celery` variable MUST be at module level so the Celery CLI
# can find it: `celery -A app.celery worker --loglevel=info`
#
# How this works:
# 1. We create the Flask app.
# 2. We create a Celery instance tied to that app (via make_celery).
# 3. We register our three task functions with Celery, giving each
#    a unique name that matches what's in celery_app.py's beat_schedule.

from jobs.celery_app import make_celery

app = create_app()
celery = make_celery(app)

# Register Celery tasks
# Each task function is wrapped with celery.task() which:
#   - Makes it callable via .delay() or .apply_async()
#   - Ensures it runs inside Flask's app context (via ContextTask)
#   - Registers it by the `name` so Celery Beat can find it
from jobs.daily_reminder import send_daily_reminders
from jobs.monthly_report import generate_monthly_report
from jobs.export_csv import export_applications_csv

celery.task(name='jobs.daily_reminder.send_daily_reminders')(send_daily_reminders)
celery.task(name='jobs.monthly_report.generate_monthly_report')(generate_monthly_report)
celery.task(name='jobs.export_csv.export_applications_csv')(export_applications_csv)

if __name__ == '__main__':
    app.run(debug = True, port = 8443)
```

**What changed from the original**:
- Moved `app = create_app()` **outside** `if __name__ == '__main__'` and to module level. This is necessary because the Celery CLI (`celery -A app.celery worker`) imports `app.py` as a module — it doesn't run `if __name__ == '__main__'`.
- Added Celery imports and task registration.
- The `celery` variable is now accessible as `app.celery` from the CLI.

> [!WARNING]
> Because `app = create_app()` now runs at module level, it will execute on import (including when the Celery worker starts). This means `db.create_all()` and `run_seed()` also run. This is fine — they're idempotent (safe to run multiple times).

---

## Step 8 — Add CSV Export Endpoint

**What**: A new `POST /api/student/export/applications` endpoint in `student_routes.py`. When called, it sends the CSV export task to Celery and responds immediately.

**Why**: The student triggers the export from the frontend. The API doesn't block — it returns instantly with "Export started". The actual CSV generation happens in the Celery worker, and the student receives the CSV via email.

**File**: [student_routes.py](/backend/routes/student_routes.py)

**Add this at the end of the file** (after the `get_placement` route):

```python
# ===============================
# EXPORT
# ===============================

@student_bp.route('/export/applications', methods = ['POST'])
@role_required('student')
def export_applications(current_user_id):
    """
    Trigger an async CSV export of the student's application history.
    The CSV will be emailed to the student's registered email address.
    """
    from jobs.export_csv import export_applications_csv
    # .delay() sends the task to Celery's Redis queue.
    # The Celery worker picks it up and runs export_applications_csv().
    # This line returns IMMEDIATELY — it does NOT wait for the task to finish.
    export_applications_csv.delay(current_user_id)
    return jsonify({
        "message": "Export started. You will receive the CSV via email shortly."
    }), 202  # 202 Accepted = request accepted, processing not complete
```

**How `.delay()` works**:
- `export_applications_csv.delay(current_user_id)` serializes the function name and arguments into a message, pushes it to the Redis queue, and returns an `AsyncResult` object.
- The Celery worker process (running separately) picks up the message and calls `export_applications_csv(self, user_id)`.
- HTTP status `202 Accepted` tells the client "I've accepted your request but processing isn't done yet."

---

## Step 9 — Add Cache Decorators to Routes

**What**: Add `@cache_response()` decorators to the **GET** endpoints that benefit most from caching. These are the list/dashboard endpoints that are read frequently but change infrequently.

**Why**: Without caching, every page load of the admin dashboard or student drives list queries the database. With caching, repeated requests within the TTL window are served from Redis in microseconds.

**The decorator goes AFTER `@role_required` so the auth check happens first** (we don't want to serve cached data to unauthorized users — but since the cache key includes the full URL path, and the auth check happens before the cache check, this is fine).

### 9.1 — `admin_routes.py`

**File**: [admin_routes.py](/backend/routes/admin_routes.py)

**Add import at the top** (after the existing imports on line 3):

```python
from utils.cache_utils import cache_response
```

**Then add `@cache_response(...)` to these 4 GET routes:**

```python
@admin_bp.route('/dashboard', methods = ['GET'])
@role_required('admin')
@cache_response(ttl=120, key_prefix='admin_dashboard')    # ← ADD THIS
def dashboard():
    result, status = AdminService.get_dashboard()
    return jsonify(result), status
```

```python
@admin_bp.route('/companies', methods = ['GET'])
@role_required('admin')
@cache_response(ttl=180, key_prefix='admin_companies')    # ← ADD THIS
def list_companies():
    # ... (existing code unchanged)
```

```python
@admin_bp.route('/drives', methods = ['GET'])
@role_required('admin')
@cache_response(ttl=180, key_prefix='admin_drives')       # ← ADD THIS
def list_drives():
    # ... (existing code unchanged)
```

```python
@admin_bp.route('/students', methods = ['GET'])
@role_required('admin')
@cache_response(ttl=180, key_prefix='admin_students')     # ← ADD THIS
def list_students():
    # ... (existing code unchanged)
```

**TTL choices**:
- Dashboard: 120s (2 min) — stats change moderately often.
- Companies/Drives/Students lists: 180s (3 min) — change less often.

### Full `admin_routes.py` after all edits:

```python
from flask import Blueprint, request, jsonify
from utils.decorators import role_required
from services.admin_service import AdminService
from utils.cache_utils import cache_response

admin_bp = Blueprint('admin', __name__, url_prefix = '/api/admin')

@admin_bp.route('/dashboard', methods = ['GET'])
@role_required('admin')
@cache_response(ttl=120, key_prefix='admin_dashboard')
def dashboard():
    result, status = AdminService.get_dashboard()
    return jsonify(result), status

# ==================
# COMPANY MANAGEMENT

# 1. List All Companies
# 2. Approve a Company
# 3. Reject a Company
# 4. Remove a Company
# 5. Blacklist a Company
# 6. Unblacklist a Company
# ==================

@admin_bp.route('/companies', methods = ['GET'])
@role_required('admin')
@cache_response(ttl=180, key_prefix='admin_companies')
def list_companies():
    status_filter = request.args.get('status')
    search = request.args.get('search')
    page = request.args.get('page', 1, type = int)
    per_page = request.args.get('per_page', 20, type = int)
    result, status = AdminService.list_companies(status_filter, search, page, per_page)
    return jsonify(result), status

@admin_bp.route('/companies/<int:company_id>/approve', methods = ['PUT'])
@role_required('admin')
def approve_company(company_id):
    result, status = AdminService.update_company_status(company_id, 'Approved')
    return jsonify(result), status

@admin_bp.route('/companies/<int:company_id>/reject', methods = ['PUT'])
@role_required('admin')
def reject_company(company_id):
    result, status = AdminService.update_company_status(company_id, 'Rejected')
    return jsonify(result), status

@admin_bp.route('/companies/<int:company_id>', methods = ['DELETE'])
@role_required('admin')
def remove_company(company_id):
    result, status = AdminService.remove_company(company_id)
    return jsonify(result), status

@admin_bp.route('/companies/<int:company_id>/blacklist', methods = ['PUT'])
@role_required('admin')
def blacklist_company(company_id):
    result, status = AdminService.toggle_blacklist_company(company_id, blacklist = True)
    return jsonify(result), status

@admin_bp.route('/companies/<int:company_id>/unblacklist', methods = ['PUT'])
@role_required('admin')
def unblacklist_company(company_id):
    result, status = AdminService.toggle_blacklist_company(company_id, blacklist = False)
    return jsonify(result), status

# =================
# DRIVE MANAGEMENT

# 1. List All Drives
# 2. Approve a Drive
# 3. Reject a Drive
# =================

@admin_bp.route('/drives', methods = ['GET'])
@role_required('admin')
@cache_response(ttl=180, key_prefix='admin_drives')
def list_drives():
    status_filter = request.args.get('status')
    page = request.args.get('page', 1, type = int)
    per_page = request.args.get('per_page', 20, type = int)
    result, status = AdminService.list_drives(status_filter, page, per_page)
    return jsonify(result), status

@admin_bp.route('/drives/<int:drive_id>/approve', methods = ['PUT'])
@role_required('admin')
def approve_drive(drive_id):
    result, status = AdminService.update_drive_status(drive_id, 'Approved')
    return jsonify(result), status

@admin_bp.route('/drives/<int:drive_id>/reject', methods = ['PUT'])
@role_required('admin')
def reject_drive(drive_id):
    result, status = AdminService.update_drive_status(drive_id, 'Rejected')
    return jsonify(result), status

# ==================
# STUDENT MANAGEMENT

# 1. List all Students
# 2. Blacklist Student
# 3. Unblacklist Student
# 4. Deactivate Student Account
# 5. Reactivate Student Account
# ==================

@admin_bp.route('/students', methods = ['GET'])
@role_required('admin')
@cache_response(ttl=180, key_prefix='admin_students')
def list_students():
    search = request.args.get('search')
    status_filter = request.args.get('status')
    page = request.args.get('page', 1, type = int)
    per_page = request.args.get('per_page', 20, type = int)
    result, status = AdminService.list_students(status_filter, search, page, per_page)
    return jsonify(result), status

@admin_bp.route('/students/<string:register_no>/blacklist', methods = ['PUT'])
@role_required('admin')
def blacklist_student(register_no):
    result, status = AdminService.toggle_blacklist_student(register_no, blacklist = True)
    return jsonify(result), status

@admin_bp.route('/students/<string:register_no>/unblacklist', methods = ['PUT'])
@role_required('admin')
def unblacklist_student(register_no):
    result, status = AdminService.toggle_blacklist_student(register_no, blacklist = False)
    return jsonify(result), status

@admin_bp.route('/students/<string:register_no>/deactivate', methods = ['PUT'])
@role_required('admin')
def deactivate_student(register_no):
    result, status = AdminService.toggle_active_student(register_no, active = False)
    return jsonify(result), status

@admin_bp.route('/students/<string:register_no>/activate', methods = ['PUT'])
@role_required('admin')
def activate_student(register_no):
    result, status = AdminService.toggle_active_student(register_no, active = True)
    return jsonify(result), status

# ==================
# APPLICATIONS MANAGEMENT

# 1. List All Applications
# ==================

@admin_bp.route('/applications', methods = ['GET'])
@role_required('admin')
def list_all_applications():
    page = request.args.get('page', 1, type = int)
    per_page = request.args.get('per_page', 20, type = int)
    result, status = AdminService.list_all_applications(page, per_page)
    return jsonify(result), status

# ==================
# PLACEMENT MANAGEMENT

# 1. List All Placements
# 2. View Specific Placement Details
# ==================

@admin_bp.route('/placements', methods = ['GET'])
@role_required('admin')
def list_all_placements():
    page = request.args.get('page', 1, type = int)
    per_page = request.args.get('per_page', 20, type = int)
    result, status = AdminService.list_all_placements(page, per_page)
    return jsonify(result), status

@admin_bp.route('/placements/<int:placement_id>', methods = ['GET'])
@role_required('admin')
def get_placement_record(placement_id):
    result, status = AdminService.get_placement_record(placement_id)
    return jsonify(result), status
```

### 9.2 — `company_routes.py`

**File**: [company_routes.py](/backend/routes/company_routes.py)

**Add import** at the top:

```python
from utils.cache_utils import cache_response
```

**Add decorator to the dashboard route:**

```python
@company_bp.route('/dashboard', methods = ['GET'])
@role_required('company')
@cache_response(ttl=120, key_prefix='company_dashboard')    # ← ADD THIS
def dashboard(current_user_id):
    result, status = CompanyService.get_dashboard(current_user_id)
    return jsonify(result), status
```

### 9.3 — `student_routes.py`

**File**: [student_routes.py](/backend/routes/student_routes.py)

**Add import** at the top:

```python
from utils.cache_utils import cache_response
```

**Add decorator to the drives list route:**

```python
@student_bp.route('/drives', methods = ['GET'])
@role_required('student')
@cache_response(ttl=300, key_prefix='student_drives')       # ← ADD THIS
def list_eligible_drives(current_user_id):
    # ... (existing code unchanged)
```

TTL of 300s (5 min) because the drives list doesn't change very often.

### 9.4 — `shared_routes.py`

**File**: [shared_routes.py](/backend/routes/shared_routes.py)

**Add import** at the top:

```python
from utils.cache_utils import cache_response
```

**Add decorator to the skills route:**

```python
@shared_bp.route('/skills', methods = ['GET'])
@cache_response(ttl=600, key_prefix='shared_skills')        # ← ADD THIS
def list_skills():
    result, status = SharedService.list_skills()
    return jsonify(result), status
```

TTL of 600s (10 min) because skills are rarely added/removed.

---

## Step 10 — Add Cache Invalidation to Services

**What**: After every mutation (create, update, delete) in the service layer, call `invalidate_cache()` to clear stale cached responses.

**Why**: If the admin approves a drive, the cached `student_drives` list is now stale (it still shows the drive as pending). We need to delete those cache keys so the next request fetches fresh data from the DB.

**Rule of thumb**: After `db.session.commit()`, invalidate all cache prefixes whose data could have been affected.

### 10.1 — `admin_service.py`

**File**: [admin_service.py](/backend/services/admin_service.py)

**Add import at the top** (after `import logging`):

```python
from utils.cache_utils import invalidate_cache
```

**Then add `invalidate_cache()` calls in these methods, just BEFORE each `return` statement (after the `db.session.commit()`):**

| Method | Add these lines before `return` |
|--------|-------------------------------|
| `update_company_status()` | `invalidate_cache('admin_companies')` and `invalidate_cache('admin_dashboard')` |
| `remove_company()` | `invalidate_cache('admin_companies')` and `invalidate_cache('admin_dashboard')` |
| `toggle_blacklist_company()` | `invalidate_cache('admin_companies')` and `invalidate_cache('admin_dashboard')` |
| `update_drive_status()` | `invalidate_cache('admin_drives')`, `invalidate_cache('admin_dashboard')`, and `invalidate_cache('student_drives')` |
| `toggle_blacklist_student()` | `invalidate_cache('admin_students')` and `invalidate_cache('admin_dashboard')` |
| `toggle_active_student()` | `invalidate_cache('admin_students')` and `invalidate_cache('admin_dashboard')` |
| `create_skill()` | `invalidate_cache('shared_skills')` |
| `delete_skill()` | `invalidate_cache('shared_skills')` |

**Example — `update_company_status()` before and after:**

```diff
     @staticmethod
     def update_company_status(company_id, new_status):
         company = Company.query.get(company_id)
         if not company:
             return {"error": "Company not found"}, 404
 
         company.status = new_status
         db.session.commit()
 
+        invalidate_cache('admin_companies')
+        invalidate_cache('admin_dashboard')
+
         logger.info(f"Status of Company '{company.company_name}' updated to {new_status}.")
         return {"message": f"Company {new_status} successfully."}, 200
```

**Example — `update_drive_status()` before and after:**

```diff
     @staticmethod
     def update_drive_status(drive_id, new_status):
         drive = PlacementDrive.query.get(drive_id)
         if not drive:
             return {"error": "Drive not found"}, 404
 
         drive.status = new_status
         db.session.commit()
 
+        invalidate_cache('admin_drives')
+        invalidate_cache('admin_dashboard')
+        invalidate_cache('student_drives')
+
         logger.info(f"Status of Drive '{drive.job_title}' (id = {drive_id}) updated to {new_status}")
         return {"message": f"Drive {new_status} successfully"}, 200
```

**Example — `create_skill()` before and after:**

```diff
     @staticmethod
     def create_skill(data):
         name = data['skill_name'].strip()
         if Skill.query.filter(Skill.skill_name.ilike(name)).first():
             return {"error": "Skill already exists"}, 409
 
         skill = Skill(skill_name = name)
         db.session.add(skill)
         db.session.commit()
 
+        invalidate_cache('shared_skills')
+
         logger.info(f"Skill created: {name} (id = {skill.skill_id})")
         return {
             "message": "Skill created successfully",
             "skill_id": skill.skill_id,
             "skill_name": skill.skill_name
         }, 201
```

Apply the same pattern to all the methods listed in the table above. The `import` goes once at the top; each method gets its specific `invalidate_cache()` calls.

### 10.2 — `drive_service.py`

**File**: [drive_service.py](/backend/services/drive_service.py)

**Add import at the top:**

```python
from utils.cache_utils import invalidate_cache
```

**Add invalidation calls in these methods:**

| Method | Add these lines before `return` |
|--------|-------------------------------|
| `create_drive()` | `invalidate_cache('admin_drives')`, `invalidate_cache('admin_dashboard')`, `invalidate_cache('company_dashboard')` |
| `update_drive()` | `invalidate_cache('admin_drives')`, `invalidate_cache('student_drives')` |
| `close_drive()` | `invalidate_cache('admin_drives')`, `invalidate_cache('student_drives')`, `invalidate_cache('admin_dashboard')`, `invalidate_cache('company_dashboard')` |

### 10.3 — `application_service.py`

**File**: [application_service.py](/backend/services/application_service.py)

**Add import at the top:**

```python
from utils.cache_utils import invalidate_cache
```

**Add invalidation calls in these methods:**

| Method | Add these lines before `return` |
|--------|-------------------------------|
| `update_application_status()` | `invalidate_cache('admin_dashboard')`, `invalidate_cache('company_dashboard')` |
| `apply_for_drive()` | `invalidate_cache('admin_dashboard')`, `invalidate_cache('company_dashboard')` |

---

## Step 11 — How to Run Everything

You need **4 terminal sessions** running simultaneously. Redis and Celery must run in WSL; Flask can run on Windows or WSL.

### Terminal 1 — Start Redis (WSL)

```bash
# In WSL Ubuntu
sudo service redis-server start
redis-cli ping  # Should print PONG
```

### Terminal 2 — Start Celery Worker (WSL)

```bash
# Navigate to the backend directory (adjust path for your WSL mount)
cd /mnt/e/Studies/BSD_DSA/Diploma/MAD\ 2/placement-portal-app/backend

# Activate your virtualenv if you have one
source venv/bin/activate  # or: . venv/bin/activate

# Start the Celery worker
celery -A app.celery worker --loglevel=info --pool=solo
```

**What this does**:
- `-A app.celery` — tells Celery to look for the `celery` variable in `app.py`.
- `worker` — starts a worker process that listens for tasks on Redis.
- `--loglevel=info` — shows info-level logs (task received, completed, failed).
- `--pool=solo` — uses a single-threaded execution pool. This is important because SQLite doesn't handle concurrent writes well.

### Terminal 3 — Start Celery Beat (WSL)

```bash
# Same directory, same virtualenv
cd /mnt/e/Studies/BSD_DSA/Diploma/MAD\ 2/placement-portal-app/backend
source venv/bin/activate

celery -A app.celery beat --loglevel=info
```

**What this does**:
- `beat` — starts the scheduler that triggers periodic tasks (daily reminder at 8 AM, monthly report on the 1st).
- Without Beat, only user-triggered tasks (like CSV export) work. Scheduled tasks need Beat.

### Terminal 4 — Start Flask (Windows or WSL)

```bash
# On Windows (your normal terminal)
cd e:\Studies\BSD_DSA\Diploma\MAD 2\placement-portal-app\backend
python app.py

# OR in WSL:
cd /mnt/e/Studies/BSD_DSA/Diploma/MAD\ 2/placement-portal-app/backend
python app.py
```

### Process Diagram

```
┌─────────────────┐    task message     ┌──────────────────┐
│   Flask App      │ ─────────────────→ │   Redis Server    │
│   (port 8443)    │    (via .delay())  │  (port 6379)      │
│                  │                    │  DB 0: tasks      │
│                  │ ←─── cache read ── │  DB 1: cache      │
│                  │ ───→ cache write → │                    │
└─────────────────┘                    └──────────────────┘
                                              │
                                              │ picks up tasks
                                              ▼
                                       ┌──────────────────┐
                                       │  Celery Worker    │
                                       │  (runs tasks)     │
                                       │                    │
                                       │  Celery Beat       │
                                       │  (triggers         │
                                       │   scheduled tasks) │
                                       └──────────────────┘
```

---

## Step 12 — How to Test / Verify

### 12.1 Test Redis Caching

1. Start Redis + Flask.
2. Log in as admin, hit `GET /api/admin/dashboard` via Postman or the frontend.
3. Check Redis for cached keys:
   ```bash
   redis-cli -n 1 KEYS "cache:*"
   ```
   You should see something like `cache:admin_dashboard:/api/admin/dashboard?`.
4. Hit the same endpoint again — check Flask logs. You should **not** see a database query log, and the response should be faster.
5. Now approve a company (PUT request). Check Redis again — the `admin_dashboard` and `admin_companies` cache keys should be gone.

### 12.2 Test CSV Export (Celery Task)

1. Start Redis + Celery Worker + Flask.
2. Log in as a student.
3. `POST /api/student/export/applications` — should immediately return:
   ```json
   {
     "message": "Export started. You will receive the CSV via email shortly."
   }
   ```
4. Check the Celery worker terminal — you should see the task being received and completed.
5. Check the student's email — they should receive the CSV attachment.
6. Check `backend/uploads/exports/` — the CSV file should exist there.

### 12.3 Test Scheduled Tasks (Daily Reminder)

For testing, you can temporarily change the schedule in `celery_app.py`:

```python
# Change this:
'schedule': crontab(hour=8, minute=0),
# To this (runs every 1 minute):
'schedule': crontab(),  # or: 60.0 (every 60 seconds)
```

Then start Celery Beat and watch the worker terminal for the task firing.

> [!CAUTION]
> Remember to change the schedule back to the real values before deploying!

### 12.4 Test Redis Connection Failure (Graceful Degradation)

1. Stop Redis: `sudo service redis-server stop`
2. Restart Flask.
3. Hit any cached endpoint — it should still work (slower, hitting the DB directly).
4. Check Flask logs for `Redis read error` warnings.

---

## Concepts Explained

### What is Celery?

Celery is a **distributed task queue**. It lets you run Python functions **asynchronously** (in the background, in a separate process). 

**Without Celery**: When a student requests a CSV export, the Flask route would generate the CSV, send the email, and only THEN return a response. If this takes 10 seconds, the student waits 10 seconds.

**With Celery**: The Flask route says "hey Celery, please run this function" (via `.delay()`), and immediately returns a response. The Celery worker (a separate process) picks up the task and does the heavy work. The student sees an instant response.

### What is Redis?

Redis is an **in-memory key-value store** — think of it as a giant dictionary that lives in RAM. It's extremely fast (sub-millisecond reads).

We use it for two purposes:
1. **Message broker for Celery** — Celery puts task messages in Redis, and workers read from Redis. Redis acts as the "mailbox" between Flask and the Celery worker.
2. **API response cache** — We store JSON responses keyed by their URL. When the same URL is requested again within the TTL, we return the cached response instead of querying the database.

### What is Celery Beat?

Celery Beat is a **scheduler**. It's like a cron daemon for Celery. It reads the `beat_schedule` config and, at the right time, sends a task message to Redis. The Celery worker then picks it up and executes it.

Without Beat, only **user-triggered** tasks work (like CSV export via `.delay()`). With Beat, **scheduled** tasks work too (daily reminders, monthly reports).

### What is `--pool=solo`?

Celery workers can use different execution pools:
- `prefork` (default on Linux) — multiple child processes for parallel execution.
- `solo` — single-threaded, one task at a time.

We use `solo` because:
1. SQLite doesn't handle concurrent writes (it locks the entire database file).
2. For a diploma project, parallel execution isn't necessary.
3. It's simpler to debug.

### Why separate Redis databases?

Redis has 16 databases (numbered 0–15). We use:
- DB 0 for Celery (broker + results)
- DB 1 for API caching

This prevents Celery's internal keys (like `celery-task-meta-*`) from mixing with our cache keys (`cache:admin_dashboard:*`). It also means we can flush one without affecting the other: `redis-cli -n 1 FLUSHDB` clears the cache without affecting Celery's queued tasks.

---

## Summary of All File Changes

| File | Action | What |
|------|--------|------|
| [config.py](/backend/config.py) | **MODIFY** | Add 3 config vars: `CELERY_BROKER_URL`, `CELERY_RESULT_BACKEND`, `REDIS_URL` |
| [extensions.py](/backend/extensions.py) | **MODIFY** | Add `import redis`, `redis_client` with connection test |
| `backend/utils/cache_utils.py` | **NEW** | `cache_response()` decorator + `invalidate_cache()` function |
| `backend/jobs/__init__.py` | **NEW** | Empty package init |
| `backend/jobs/celery_app.py` | **NEW** | `make_celery()` factory with beat schedule |
| `backend/jobs/daily_reminder.py` | **NEW** | Scheduled: daily deadline reminder emails |
| `backend/jobs/monthly_report.py` | **NEW** | Scheduled: monthly placement activity report |
| `backend/jobs/export_csv.py` | **NEW** | User-triggered: CSV export + email attachment |
| `backend/templates/monthly_report.html` | **NEW** | HTML email template for monthly report |
| [app.py](/backend/app.py) | **MODIFY** | Add Celery integration, move `app = create_app()` to module level, register tasks |
| [student_routes.py](/backend/routes/student_routes.py) | **MODIFY** | Add `POST /export/applications` endpoint |
| [admin_routes.py](/backend/routes/admin_routes.py) | **MODIFY** | Add `@cache_response` to 4 GET routes |
| [company_routes.py](/backend/routes/company_routes.py) | **MODIFY** | Add `@cache_response` to dashboard route |
| [shared_routes.py](/backend/routes/shared_routes.py) | **MODIFY** | Add `@cache_response` to skills route |
| [admin_service.py](/backend/services/admin_service.py) | **MODIFY** | Add `invalidate_cache()` calls to 8 methods |
| [drive_service.py](/backend/services/drive_service.py) | **MODIFY** | Add `invalidate_cache()` calls to 3 methods |
| [application_service.py](/backend/services/application_service.py) | **MODIFY** | Add `invalidate_cache()` calls to 2 methods |