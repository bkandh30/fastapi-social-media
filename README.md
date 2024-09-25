# fastapi-social-media

This is a REST API for an Instagram type social media backend using FastAPI and SQLAlchemy.

## API Routes

### Auth

| METHOD | ROUTE                 | FUNCTIONALITY     |
| ------ | --------------------- | ----------------- |
| POST   | `/v1/auth/signup/`    | Register new user |
| POST   | `/v1/auth/login/`     | Login user        |
| GET    | `/v1/auth/profile`    | Current User      |
| PUT    | `/v1/auth/{username}` | Update User       |

### Posts

| METHOD | ROUTE                         | FUNCTIONALITY          |
| ------ | ----------------------------- | ---------------------- |
| POST   | `/v1/posts/`                  | Create Post            |
| DELETE | `/v1/posts/`                  | Delete Post            |
| GET    | `/v1/posts/user`              | Get Current User Posts |
| GET    | `/v1/posts/user/{username}`   | Get User Posts         |
| GET    | `/v1/posts/hashtag/{hashtag}` | Get Posts from Hashtag |
| GET    | `/v1/posts/feed`              | Get Random Posts       |
| POST   | `/v1/posts/like`              | Like Posts             |
| POST   | `/v1/posts/unlike`            | Unlike Post            |
| GET    | `/v1/posts/likes/{post_id}`   | Users Like Post        |
| GET    | `/v1/posts/{post_id}`         | Get Post               |

### Activity

| METHOD | ROUTE                          | FUNCTIONALITY            |
| ------ | ------------------------------ | ------------------------ |
| GET    | `/v1/activity/user/{username}` | Follow and Like Activity |

### Profile

| METHOD | ROUTE                             | FUNCTIONALITY |
| ------ | --------------------------------- | ------------- |
| POST   | `/v1/profile/user/{username}`     | Profile       |
| POST   | `/v1/profile/follow/{username}`   | Follow        |
| POST   | `/v1/profile/unfollow/{username}` | Unfollow      |
| GET    | `/v1/profile/followers`           | Get Followers |
| GET    | `/v1/profile/following`           | Get Following |
