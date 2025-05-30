# FastAPI Social Media API Backend

---

This project provides a robust and scalable **RESTful API backend for a social media application**, reminiscent of platforms like Instagram. Built with **FastAPI** for high performance and **SQLAlchemy** for efficient database interactions, this API handles core social media functionalities, including user authentication, post management, likes, follows, and activity tracking.

---

## Features

* **User Authentication & Authorization**: Secure user registration, login, and profile management.
* **Dynamic Post Management**: Create, retrieve, and delete posts.
* **Content Discovery**: Fetch posts by user or hashtag, and discover new content via a randomized feed.
* **Interaction Features**: Implement liking/unliking posts and tracking user interactions.
* **Follow System**: Users can follow and unfollow others, and retrieve lists of followers and following.
* **Activity Tracking**: Monitor follow and like activities for users.
* **FastAPI Performance**: Leverages FastAPI's asynchronous capabilities for high concurrency and speed.
* **SQLAlchemy ORM**: Utilizes SQLAlchemy for seamless and robust database operations.

---

## Technologies Used

* **Python 3.x**
* **FastAPI**: Modern, fast (high-performance) web framework for building APIs with Python 3.7+ based on standard Python type hints.
* **SQLAlchemy**: The Python SQL toolkit and Object Relational Mapper that gives developers the full power of SQL.
* **Uvicorn**: An ASGI server for FastAPI.
* **Other dependencies**: To get the complete list of python modules, view the requirements.txt file.

---

### Installation

1.  **Clone the repository:**

    ```bash
    git clone [https://github.com/yourusername/fastapi-social-media.git](https://github.com/yourusername/fastapi-social-media.git)
    cd fastapi-social-media
    ```

2.  **Create a virtual environment**:

    ```bash
    source venv/bin/activate
    ```

3.  **Install the required dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

---

## API Routes

The API is structured with clear, versioned endpoints for different functionalities. All routes are prefixed with `/v1/`.

### Authentication

Handles user registration, login, and profile management.

| METHOD | ROUTE | FUNCTIONALITY | Authentication Required |
| :----- | :------------------ | :-------------------- | :---------------------- |
| `POST` | `/v1/auth/signup/` | Register a new user | No |
| `POST` | `/v1/auth/login/` | Authenticate and log in a user | No |
| `GET` | `/v1/auth/profile` | Retrieve the current authenticated user's profile | Yes |
| `PUT` | `/v1/auth/{username}` | Update the profile of a specific user | Yes (User must own profile) |

### Posts

Manages creation, retrieval, and interaction with social media posts.

| METHOD | ROUTE | FUNCTIONALITY | Authentication Required |
| :----- | :-------------------------------- | :--------------------------- | :---------------------- |
| `POST` | `/v1/posts/` | Create a new post | Yes |
| `DELETE` | `/v1/posts/{post_id}` | Delete a specific post | Yes (User must own post) |
| `GET` | `/v1/posts/user` | Get all posts by the current authenticated user | Yes |
| `GET` | `/v1/posts/user/{username}` | Get all posts by a specified user | No |
| `GET` | `/v1/posts/hashtag/{hashtag}` | Get all posts containing a specific hashtag | No |
| `GET` | `/v1/posts/feed` | Retrieve a feed of random posts | No (or Optional) |
| `POST` | `/v1/posts/like/{post_id}` | Like a specific post | Yes |
| `POST` | `/v1/posts/unlike/{post_id}` | Unlike a specific post | Yes |
| `GET` | `/v1/posts/likes/{post_id}` | Get users who liked a specific post | No |
| `GET` | `/v1/posts/{post_id}` | Retrieve details of a single post | No |

### Activity

Provides insights into user interactions like follows and likes.

| METHOD | ROUTE | FUNCTIONALITY | Authentication Required |
| :----- | :----------------------------- | :------------------------------ | :---------------------- |
| `GET` | `/v1/activity/user/{username}` | Retrieve follow and like activity for a user | No |

### Profile

Manages user profiles and the follow/unfollow system.

| METHOD | ROUTE | FUNCTIONALITY | Authentication Required |
| :----- | :---------------------------------- | :------------------ | :---------------------- |
| `GET` | `/v1/profile/user/{username}` | Retrieve a user's profile information | No |
| `POST` | `/v1/profile/follow/{username}` | Follow a specified user | Yes |
| `POST` | `/v1/profile/unfollow/{username}` | Unfollow a specified user | Yes |
| `GET` | `/v1/profile/followers` | Get users who follow the current user | Yes |
| `GET` | `/v1/profile/following` | Get users the current user is following | Yes |

---

## Running the Application

To start the FastAPI application using Uvicorn:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

- `main:app`: Assumes your FastAPI application instance (app) is in a file named main.py. Adjust if your file or app variable is named differently.

- `--reload`: Enables hot-reloading so the server restarts automatically on code changes.

- `--host 0.0.0.0`: Makes the server accessible from outside your local machine (useful for Docker or network testing).

- `--port 8000`: Specifies the port to run the server on.

Once running, you can access the interactive API documentation (Swagger UI) at `http://localhost:8000/docs`.

---
