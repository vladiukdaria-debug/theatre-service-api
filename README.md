# Theatre Service API

Theatre Service API is a Django REST Framework project for managing theatre performances and online ticket reservations.

## Features

- Manage actors and genres
- Manage plays
- Manage theatre halls
- Manage performances
- User authentication
- Create ticket reservations
- Select rows and seats
- Prevent double booking of the same seat
- Validate seats according to theatre hall size
- Users can view only their own reservations

## Technologies

- Python
- Django
- Django REST Framework
- SQLite
- Token Authentication

## Database Structure

The project contains the following models:

- Actor
- Genre
- Play
- TheatreHall
- Performance
- Reservation
- Ticket
- User (Django built-in user model)

## Installation

Clone the repository:

```bash
git clone https://github.com/vladiukdaria-debug/theatre-service-api.git
cd theatre-service-api
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

On macOS/Linux:

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Apply migrations:

```bash
python manage.py migrate
```

Create a superuser:

```bash
python manage.py createsuperuser
```

Run the server:

```bash
python manage.py runserver
```

## API Endpoints

| Endpoint | Description |
|---|---|
| `/api/theatre/actors/` | Actors |
| `/api/theatre/genres/` | Genres |
| `/api/theatre/plays/` | Plays |
| `/api/theatre/theatre-halls/` | Theatre halls |
| `/api/theatre/performances/` | Performances |
| `/api/theatre/reservations/` | User reservations |
| `/api/user/token/` | Get authentication token |

## Authentication

Get a token:

```http
POST /api/user/token/
```

Example request:

```json
{
  "username": "your_username",
  "password": "your_password"
}
```

Use the returned token in authenticated requests:

```text
Authorization: Token your_token
```

## Reservation Example

Create a reservation:

```http
POST /api/theatre/reservations/
```

```json
{
  "tickets": [
    {
      "row": 3,
      "seat": 5,
      "performance": 1
    },
    {
      "row": 3,
      "seat": 6,
      "performance": 1
    }
  ]
}
```

## Tests

Run tests with:

```bash
python manage.py test
```

## Author

Daria Vladiuk
