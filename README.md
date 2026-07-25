# AI Job Portal

A web-based Job Portal developed using **Python Flask** and **MySQL** that allows users to register, log in, browse jobs, post jobs, search for jobs, and apply for them.

---

## Features

- User Registration
- Secure Login & Logout
- Password Hashing
- Dashboard
- Post New Jobs
- View Available Jobs
- Search Jobs
- Apply for Jobs
- View My Applications
- Flash Messages
- MySQL Database Integration
- Responsive User Interface

---

## Technologies Used

- Python
- Flask
- MySQL
- HTML5
- CSS3
- Jinja2
- Werkzeug Security

---

## Project Structure

```
AI-Job-Portal/
│
├── app.py
├── config.py
├── database.py
├── requirements.txt
├── README.md
│
├── static/
│   ├── css/
│   │   └── style.css
│   └── images/
│
└── templates/
    ├── index.html
    ├── login.html
    ├── register.html
    ├── dashboard.html
    ├── jobs.html
    ├── post_job.html
    └── my_applications.html
```

---

## Database Tables

- users
- jobs
- applications

---

## Installation

1. Clone the repository

```bash
git clone https://github.com/your-username/AI-Job-Portal.git
```

2. Navigate to the project

```bash
cd AI-Job-Portal
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

4. Create a MySQL database

```sql
CREATE DATABASE job_portal;
```

5. Update your database credentials in `config.py`.

6. Run the application

```bash
python app.py
```

---

## Screenshots

Add screenshots of:

- Home Page
- Login Page
- Register Page
- Dashboard
- Available Jobs
- Post Job
- My Applications

---

## Future Improvements

- Resume Upload
- Email Notifications
- Admin Dashboard
- Company Profiles
- Job Categories
- Pagination
- User Profile Editing

---

## Author

**Satakshi Chauhan**

BCA Student | Python & Flask Developer

GitHub: https://github.com/your-username