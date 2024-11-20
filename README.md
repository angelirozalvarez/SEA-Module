# Originally for Software Engineering & Agile
Level 5 Software Engineering &amp; Agile (QAC020N227S)

# Repurposed for Software Engineering & DevOps
Level 6 Software Engineering & DevOps (QAC020X328)

    By Angeli Roz Bautista Alvarez

App Name

    Trade Management System (TM System)

Description

    The Trade Management System (TM System) is a trade management platform that enables a user to sign up as admin or regular user. The app features three main pages: the ‘Trades’, ‘Traders, and ‘Banks’ page, wherein the admin and the regular user can perform functionalities including creating, retrieving, and updating records from the trades, traders and banks tables. However, only the admin users can perform the delete functionality. The users would be able to track the status of a trade and assign traders and banks to a specific trade.

Database

    SQLite3 was initially used in the localhost environment, afterwhich a database migration took place using PostgreSQL. The Trades table is the main entity featured in TM System with a one-to-many relationship with both the Traders and the Banks tables. The Entity Relationship Diagram (ERD) is demonstrated in the main assignment document referenced in Task 1.
    

Demo

    The live app can be accessed using this link: 
    https://tmsystem-4aab3b77316c.herokuapp.com/

Installation

    To run this project, there are certain dependencies to be installed. Homebrew is used to install things. Here are the specific requirements and versions of dependencies used which are also found in requirements.txt:
    asgiref==3.7.2
    boto3==1.34.56
    botocore==1.34.57
    crispy-tailwind==1.0.3
    dj-database-url==2.1.0
    Django==5.0.2
    django-crispy-forms==2.1
    django-filter==23.5
    django-storages==1.14.2
    gunicorn==21.2.0
    jmespath==1.0.1
    packaging==23.2
    pillow==10.2.0
    psycopg2==2.9.9
    psycopg2-binary==2.9.9
    pytest==8.0.2
    pytest-cov==4.1.0
    pytest-django==4.8.0
    python-dateutil==2.9.0.post0
    pytz==2024.1
    s3transfer==0.10.0
    six==1.16.0
    sqlparse==0.4.4
    typing_extensions==4.10.0
    urllib3==2.0.7
    whitenoise==6.6.0



    Please run the following:
    pip install virtualenv
    virtualenv venv
    venv\Scripts\activate
    pip install Django
    pip install -r requirements.txt
    pip install psycopg2
    python manage.py runserver

    You may need to comment out the following on your local in settings.py in the TMSystem directory:
    
    import dj_database_url
    db_from_env = dj_database_url.config(conn_max_age=600)
    DATABASES['default'].update(db_from_env)

    Hope it works.

Deployment
    
    The app is deployed via Heroku.
