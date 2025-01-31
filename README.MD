# Password Manager

A simple password manager application built with Python and aiohttp. This application allows users to register, log in, generate, retrieve, and delete passwords.

## Features

- User registration and login
- Password hashing and verification
- JWT-based authentication
- Generate secure passwords
- Retrieve and delete stored passwords

## Endpoints

- `POST /register` - Register a new user
- `POST /login` - Log in an existing user
- `POST /password/generate` - Generate a new password. It accepts optional 'length' and 'label' parameters
- `GET /passwords` - Retrieve all stored passwords
- `DELETE /password/{password_id}` - Delete a specific password

## Setup

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Set up environment variables in a `.env` file
4. Run the application: `python app/main.py`

## Dependencies

- Python
- aiohttp
- bcrypt
- jwt
- python-dotenv

## Future Features

- One-time link Password Sharing
- Password search
- Expiry Notifications with Celery