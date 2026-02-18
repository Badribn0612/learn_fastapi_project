## Simple Social (FastAPI + Streamlit)

A minimal social-style web app built with **FastAPI** for the backend and **Streamlit** for the frontend.  
Users can sign up, log in, upload images or videos (stored via ImageKit), see a feed of all posts, and delete their own posts.

## Features

- **User authentication**: Email/password auth, registration, password reset, and verification powered by `fastapi-users` with JWT.
- **Media upload**: Upload images and videos through the frontend; files are uploaded to ImageKit from the FastAPI backend.
- **Feed view**: Streamlit feed page showing all posts with uniform display and optional caption overlay on media.
- **Ownership & deletion**: Only the owner of a post can delete it; enforced in the backend with user-aware queries.
- **SQLite persistence**: Posts and users are stored in a local SQLite database via SQLAlchemy.

## Tech Stack

- **Backend**: FastAPI, SQLAlchemy (async), `fastapi-users`, aiosqlite
- **Frontend**: Streamlit
- **Auth**: JWT (via `fastapi-users`)
- **Storage / media**: ImageKit (via `imagekitio`)
- **Database**: SQLite (`test.db`)

## Project Structure

- `app/app.py` – FastAPI application, routes for upload, feed, and delete post; mounts auth/user routes from `fastapi-users`.
- `app/db.py` – Async SQLAlchemy engine, `User` and `Post` models, session and user DB helpers.
- `app/users.py` – `fastapi-users` configuration: `UserManager`, JWT strategy, auth backend, and dependency `current_active_user`.
- `app/schemas.py` – Pydantic schemas for posts and user models based on `fastapi-users` schemas.
- `app/images.py` – ImageKit client setup.
- `frontend.py` – Streamlit app: login/sign-up, upload page, and feed page consuming the FastAPI API.

## Prerequisites

- **Python** 3.10+ (recommended 3.11+)
- **pip** or another Python package manager
- An **ImageKit** account (for media storage)

## Installation

1. **Clone the repository**

   ```bash
   git clone <your-repo-url>
   cd learn_fastapi
   ```

2. **Create and activate a virtual environment** (recommended)

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**

   If you already have a `requirements.txt`, you can use:

   ```bash
   pip install -r requirements.txt
   ```

   Otherwise, install the key packages directly:

   ```bash
   pip install fastapi uvicorn[standard] sqlalchemy[asyncio] aiosqlite fastapi-users[sqlalchemy] \
       python-dotenv imagekitio streamlit requests httpx
   ```

## Environment Variables

Create a `.env` file in the project root (or wherever you run the app from) with at least:

- **`SECRET`** – Secret key used for JWT and token generation in `fastapi-users`.
- **`IMAGEKIT_PRIVATE_KEY`** – ImageKit private key used by the backend for uploads.

Example `.env`:

```bash
SECRET="change-this-secret-in-production"
IMAGEKIT_PRIVATE_KEY="your_imagekit_private_key"
```

You will also need to configure ImageKit so that uploaded URLs are valid from your frontend (public URL endpoint, etc.), using your ImageKit dashboard.

## Running the Backend (FastAPI)

From the project root, run:

```bash
uvicorn app.app:app --reload
```

The API will be available at `http://localhost:8000`.

Key endpoints:

- **`POST /auth/jwt/login`** – Login (username = email, password).
- **`POST /auth/register`** – Register new user.
- **`GET /users/me`** – Get current user profile.
- **`POST /upload`** – Authenticated media upload (used by the Streamlit app).
- **`GET /feed`** – Get list of posts for the feed.
- **`DELETE /posts/{post_id}`** – Delete a post you own.

The SQLite database file (`test.db`) will be created automatically on first run in the project directory.

## Running the Frontend (Streamlit)

With the backend running on `http://localhost:8000`, in another terminal (same virtual environment), run:

```bash
streamlit run frontend.py
```

This launches the Streamlit UI in your browser.

### Using the App

- **Sign up**: Enter an email and password, then click **Sign Up**.
- **Log in**: After registering, use **Login** to obtain a JWT and fetch your user info.
- **Upload**: Navigate to the upload page, choose an image/video and a caption, and submit.
- **Feed**: Browse all posts in the feed. If you own a post, you will see a delete button to remove it.

## Development Notes

- The app currently uses **SQLite** for local development via `sqlite+aiosqlite`; switching to a production database (e.g., PostgreSQL) will mainly involve updating `DATABASE_URL` and installing the appropriate driver.
- Authentication and user management are handled by `fastapi-users` using the `User` model defined in `app/db.py`.
- Media processing (including optional caption overlay for images/videos) is performed on the frontend by constructing ImageKit transformation URLs.
- For production, make sure you use strong secrets, HTTPS, and a more robust database and storage configuration.
