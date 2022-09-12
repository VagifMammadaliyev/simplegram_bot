import random
import requests
from decouple import config


NUMBER_OF_USERS = config("NUMBER_OF_USERS", cast=int, default=0)
MAX_POSTS_PER_USER = config("MAX_POSTS_PER_USER", cast=int, default=0)
MAX_LIKES_PER_USER = config("MAX_LIKES_PER_USER", cast=int, default=0)
BASE_API_URL = config("BASE_API_URL")


def create_user(user_index):
    user_object = {
        "first_name": f"First #{user_index}",
        "last_name": f"Last #{user_index}",
        "email": f"user{user_index}@example.com",
        "password": f"123password-{user_index}=#",
    }
    requests.post(
        f"{BASE_API_URL}/auth/register",
        json=user_object,
    )
    return user_object


def login_user(user_object):
    response = requests.post(
        f"{BASE_API_URL}/auth/login",
        json={
            "email": user_object["email"],
            "password": user_object["password"],
        },
    )
    return response.json()["access_token"]


def create_post(user_object):
    response = requests.post(
        f"{BASE_API_URL}/posts",
        json={
            "title": "Hello World",
            "content": "This is my first post",
        },
        headers={
            "Authorization": f"Bearer {user_object['access_token']}",
        },
    )
    return response.json()["_id"]


def like_post(user_object, post_id):
    requests.post(
        f"{BASE_API_URL}/posts/{post_id}/like",
        headers={
            "Authorization": f"Bearer {user_object['access_token']}",
        },
    )


def main():
    users = []
    posts = []

    for i in range(NUMBER_OF_USERS):
        user = create_user(i)
        users.append(user)

    for user in users:
        access_token = login_user(user)
        user["access_token"] = access_token

        for i in range(random.randint(0, MAX_POSTS_PER_USER)):
            post_id = create_post(user)
            posts.append(post_id)

    for user in users:
        for i in range(random.randint(0, MAX_LIKES_PER_USER)):
            like_post(user, random.choice(posts))


if __name__ == "__main__":
    main()
