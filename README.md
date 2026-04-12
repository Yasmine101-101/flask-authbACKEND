# flask-authbACKEND
# Notes App Backend

## Description

A secure REST API backend for a notes app. Built with Flask and SQLAlchemy, it lets users sign up, log in, and manage their own personal notes. Each user can only see and edit their own notes.

## Installation

1. Clone the repo:
```bash
git https://github.com/Yasmine101-101/flask-authbACKEND.git
cd notes-app
```

2. Install dependencies:
```bash
pipenv install
pipenv shell
```

3. Go into the server folder:
```bash
cd server
```

4. Set up the database:
```bash
flask db init
flask db migrate -m "initial migration"
flask db upgrade head
```

5. Seed the database:
```bash
python seed.py
```

## How to Run

```bash
python app.py
```

App runs on `http://127.0.0.1:5555`

## API Endpoints

### Auth

| Method | Endpoint | What it does |
|--------|----------|-------------|
| POST | /signup | create a new user |
| POST | /login | log in a user |
| DELETE | /logout | log out a user |
| GET | /check_session | check if user is logged in |

### Notes

| Method | Endpoint | What it does |
|--------|----------|-------------|
| GET | /notes | get all notes for logged in user (paginated) |
| POST | /notes | create a new note |
| PATCH | /notes/\<id\> | update a note |
| DELETE | /notes/\<id\> | delete a note |

## Example Request Bodies

### Signup / Login
```json
{
    "username": "yasmin",
    "password": "password123"
}
```

### Create a Note
```json
{
    "title": "My first note",
    "content": "This is the content of my note"
}
```

### Pagination
```
GET /notes?page=1&per_page=10
```