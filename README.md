# Whitelisted User Authentication using Django

## Overview

This project implements a whitelisted user authentication system using Django.

Users can submit account registration requests by providing their usernames, emails, and passwords. Once a request is submitted, the admin receives a notification via email and can choose to either approve or reject the user's request. After the decision is made, the user will be notified via email accordingly.

---

## Installation & Setup

Follow the steps below to run the authentication backend locally.

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd user-authentication
2. Create and activate a virtual environment
bash
Copy
Edit
python3 -m venv venv
source venv/bin/activate
3. Install project dependencies
bash
Copy
Edit
pip install -r requirements.txt
4. Create a .env file
Navigate to the user-authentication/auth_project/ directory and create a .env file with the following contents:

env
Copy
Edit
EMAIL_SMTP_USER=adminemailaddress
EMAIL_SMTP_PASSWORD=adminemailpassword
DEFAULT_FROM_EMAIL=adminemailaddress
Replace the placeholder values with your actual SMTP credentials.

5. Run the development server
From the user-authentication/auth_project/ directory, run:

bash
Copy
Edit
python3 manage.py runserver 8001
The app will be accessible at: http://localhost:8001


