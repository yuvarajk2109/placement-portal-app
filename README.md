# Placement Portal Application
Institutes require efficient systems to manage campus recruitment activities involving companies and students. Currently, many institutes rely on spreadsheets, emails, or manual coordination, which makes it difficult to manage company approvals, placement drives, student registrations, and application tracking. This Placement Portal Application (PPA), a fully web-based and responsive application, allows the Admin/Institute, Companies, and Students to interact with the system based on their roles.

## Frameworks
- Flask for API
- VueJS for UI
- SQLite for database
- Redis for caching
- Redis and Celery for batch jobs

## Setup

### 1. Setting up the Backend

Run the following commands from your root directory, which contains the folder 'backend':
```
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 2. DB Initialisation and Migrations

DB Initialisation HAS to be done as a one-time setup to enable migrations. In the backend folder itself, run this command: 

```
flask db init 
```

After any changes to DB Schema via the Models, there's no need to delete the DB data - just migrate with:

```
flask db migrate
flask db upgrade
```

### 3. Frontend Setup

Simply to install node_modules. Again, from the root directory, which contains the 'frontend' folder, execute these commands:

```
cd frontend
npm install
```

### 4. Redis

In WSL Ubuntu, run the following commands to install Redis. Upon entering `sudo apt update`, you will be asked for your password.

```
sudo apt update
sudo apt install redis-server -y
```

### 5. Ubuntu Backend Setup

Ubuntu will not be able to take the virtual environment from windows. We need to setup the virtual environment separately on ubuntu as well!

Navigate to your project backend directory. Essentially, it is `/mnt/{{ full_windows_directory_path }}` 

```
cd "/mnt/e/Studies/BSD_DSA/Diploma/MAD 2/placement-portal-app/backend"
```

Install the python3-venv package if you don't have it. Upon entering `sudo apt update`, you will be asked for your password.

```
sudo apt update
sudo apt install python3-venv python3-pip -y
```

Now, create a new WSL-specific venv, activate it and install all required packages:

```
python3 -m venv venv-wsl
source venv-wsl/bin/activate
pip install -r requirements.txt
```

## Running the Application

### Terminal 1 - Windows - Frontend

```
cd frontend
npm run dev
```

### Terminal 2 - Windows - Backend

```
cd backend
flask run
```

### Terminal 3 - Ubuntu - Redis

```
sudo service redis-server start
redis-cli ping
```

### Terminal 4 - Ubuntu - Celery Worker

```
cd "/mnt/e/Studies/BSD_DSA/Diploma/MAD 2/placement-portal-app/backend"
source venv-wsl/bin/activate
celery -A app.celery worker --loglevel=info --pool=solo
```

### Terminal 5 - Ubuntu - Celery Beat

```
cd "/mnt/e/Studies/BSD_DSA/Diploma/MAD 2/placement-portal-app/backend"
source venv-wsl/bin/activate
celery -A app.celery beat --loglevel=info
```

Beat ensures that scheduled tasks also work.

### MailHog

Run the MailHog application, and open it on `http://127.0.0.1:8025/` OR `localhost:8025`. This enables testing email sending without actually sending any real emails!

## Miscellaneous

### To check Redis for cached keys:

```
redis-cli -n 1 KEYS "cache:*"
```

### To stop Redis server:

```
sudo service redis-server stop
```