
# Whitelisted User Authentication using Django 

## Overview

This is a brief overview of the idea behind our whitelisted user authentication system.

Users can submit account registration requests by providing their usernames, emails, and passwords. Once a request is submitted, the admin receives a notification via email and can choose to either approve or reject the user's request. Once the decision is made, the user will be notified via email accordingly.

---

## Installation & Setup

In case you would like to test the authentication backend locally, please follow these steps.

- create a virtual environment under /user-authentication directory
source venv/bin/activate

- install requirements.txt file
```bash
pip install -r requirements.txt
```


- create a .env file at the under /user-authentication/auth_project directory with the following environment variables.

```bash
EMAIL_SMTP_USER=adminemailaddress
EMAIL_SMTP_PASSWORD=adminemailpassword
DEFAULT_FROM_EMAIL=adminemailaddress
```

- run the project

```bash
python3 manage.py runserver 8001
```

The app will be accessible at: http://localhost:8001.
