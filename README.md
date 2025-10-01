# SPA-Comment App

This project is a Single Page Application (SPA) for posting and replying to comments.

It features a Django REST Framework backend and a Vue.js frontend, all containerized with Docker. The application supports user authentication, nested comments, file uploads (with server-side image resizing), CAPTCHA verification, and real-time updates via WebSockets.

---

## Key Features

* **User Authentication**: Secure user registration and login system using JWT tokens.
* **Comment System**:
    * Users can create top-level comments and reply to any existing comment, creating nested (cascading) threads.
    * Top-level comments are paginated (25 per page) for easy navigation.
    * The comment list can be sorted by username, email, and creation date in both ascending and descending order.
* **Security**:
    * The comment form is protected by a CAPTCHA to prevent automated spam.
    * Measures are in place to protect against XSS attacks by sanitizing comment text from disallowed HTML tags.
* **File Uploads**:
    * Users can attach images (JPG, GIF, PNG) to comments. Images larger than 320x240 pixels are automatically resized server-side while maintaining aspect ratio.
    * Users can also attach text files (.txt) with a size limit of 100 KB.
* **Performance & UX**:
    * **Real-time Updates**: New comments appear for all connected users instantly without a page refresh, powered by WebSockets (Django Channels).
    * **Caching**: The main comment list is cached using Redis to ensure fast load times.
    * **Background Tasks**: Image resizing is handled asynchronously by a Celery worker, ensuring that user requests are not blocked by processing.

---

## Tech Stack

* **Backend**: Django, Django REST Framework
* **Frontend**: Vue.js, Vue Router
* **Database**: SQLite
* **Async Tasks & Caching**: Celery, Redis
* **Real-time**: Django Channels, WebSockets
* **Containerization**: Docker, Docker Compose
* **Authentication**: djoser, JWT

---

## Getting Started

To get a local copy up and running, follow these simple steps.

### Prerequisites

Make sure you have Docker and Docker Compose installed on your machine.

* Git

* Docker & Docker Compose

* Node.js (v18+ LTS recommended) and npm

### Installation

1.  **Clone the repository:**
    ```sh
    git clone https://github.com/Yepavlov/dzen_spa_app.git
    cd dzen_spa_app
    ```

2.  **Build and run the Docker containers:**
    This command will build the images and start all services (web server, Celery worker, Redis).
    ```sh
    docker-compose up --build web redis worker
    ```
    The backend API will be available at http://localhost:8000.

    In your second terminal, start the Vue.js development server:

    ```sh
    cd frontend
    npm install
    npm run dev
    ```
    The frontend will be available at http://localhost:5173

---

## Usage

Once the containers are up and running:

* The **Vue.js frontend** will be available at `http://localhost:5173`.
* The **Django REST API** will be available at `http://localhost:8000`.

You can now use the application:
1.  Navigate to `http://localhost:5173`.
2.  Register a new user and log in.
3.  Post new comments, reply to existing ones, and attach images or text files. New comments from other users will appear in real-time.