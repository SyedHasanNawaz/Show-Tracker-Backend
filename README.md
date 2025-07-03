# 📺 ShowTracker Backend

ShowTracker is a backend service designed to manage user authentication and TV show tracking. Built using **FastAPI** and **Python**, it features a modular structure with clear separation of routes, models, and database logic.

## 📁 Project Structure

```
ShowTracker Backend/
├── routes/
│   ├── episodes.py        # Episode-related routes
│   ├── shows.py           # Show catalog endpoints
│   ├── users.py           # User registration/login
│   ├── watched.py         # Track watched content
│   └── watchlist.py       # Manage user watchlists
├── auth.py                # Handles authentication (JWT)
├── database.py            # Database connection and session
├── main.py                # Entry point, initializes FastAPI app
├── models.py              # Database models and schemas
├── requirements.txt       # Python dependencies
├── Secret.env             # Environment variables (excluded from Git)
├── Procfile               # Deployment config (Heroku or similar)
└── .venv/                 # Virtual environment (excluded from Git)
```

## 🚀 Features

- 🔐 User authentication with JWT tokens
- 📺 CRUD APIs for shows and episodes
- ✅ Track watched episodes and user progress
- 📌 Manage watchlists per user
- 📁 Modular route-based architecture
- 📖 FastAPI interactive documentation at `/docs`

## 🛠️ Tech Stack

- **Language:** Python 3.x
- **Framework:** FastAPI
- **Database:** SQLite / PostgreSQL
- **ORM:** SQLAlchemy / Pydantic
- **Authentication:** JWT tokens via `auth.py`

## ⚙️ Setup Instructions

1. **Clone the Repository**

   ```sh
   git clone https://github.com/your-username/showtracker-backend.git
   cd showtracker-backend
   ```

2. **Set Up Virtual Environment**

   ```sh
   python -m venv .venv
   # For Linux/macOS
   source .venv/bin/activate
   # For Windows
   .venv\Scripts\activate
   ```

3. **Install Dependencies**

   ```sh
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**

   Create a file called `.env` or use your existing `Secret.env`:

   ```
   SECRET_KEY=your_secret_key
   DATABASE_URL=your_database_url
   ```

5. **Run the App**
   ```sh
   uvicorn main:app --reload
   ```

## 📂 API Overview

Explore and test the API using FastAPI's Swagger UI at:  
[http://localhost:8000/docs](http://localhost:8000/docs)

Main endpoints include:

- `POST /auth/login`
- `POST /auth/register`
- `GET /users/`
- `GET /shows/`
- `GET /episodes/`
- `GET /watchlist/`
- `POST /watched/`

## ✍️ Author

**Syed Hasan Nawaz**  
[GitHub Profile](https://github.com/SyedHasanNawaz)

## 📌 Notes

- Do **not** push `.env`, `.venv/`, or `.idea/` to GitHub
- Add all sensitive files to `.gitignore`
- This project is ready for deployment using a `Procfile` if needed (e.g., Heroku)
