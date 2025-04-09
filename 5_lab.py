from flask import Flask, jsonify, request
from typing import List, Dict

class Comment:
    def __init__(self, id: int, user_id: int, content: str):
        self.id = id
        self.user_id = user_id
        self.content = content

    def to_dict(self):
        return {"id": self.id, "user_id": self.user_id, "content": self.content}

class Post:
    def __init__(self, id: int, user_id: int, title: str, content: str):
        self.id = id
        self.user_id = user_id
        self.title = title
        self.content = content
        self.comments: List[Comment] = []

    def add_comment(self, comment: Comment):
        self.comments.append(comment)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "title": self.title,
            "content": self.content,
            "comments": [comment.to_dict() for comment in self.comments]
        }

class User:
    def __init__(self, id: int, username: str):
        self.id = id
        self.username = username
        self.posts: List[Post] = []

    def add_post(self, post: Post):
        self.posts.append(post)

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "posts": [post.to_dict() for post in self.posts]
        }

class InMemoryAPI:
    def __init__(self):
        self.users: Dict[int, User] = {}
        self.posts: Dict[int, Post] = {}
        self.comments: Dict[int, Comment] = {}

    def create_user(self, id: int, username: str):
        if id in self.users:
            return {"error": "User already exists"}
        user = User(id, username)
        self.users[id] = user
        return user.to_dict()

    def get_user(self, id: int):
        user = self.users.get(id)
        if not user:
            return {"error": "User not found"}
        return user.to_dict()

    def update_user(self, id: int, username: str):
        user = self.users.get(id)
        if not user:
            return {"error": "User not found"}
        user.username = username
        return user.to_dict()

    def delete_user(self, id: int):
        if id not in self.users:
            return {"error": "User not found"}
        del self.users[id]
        return {"message": "User deleted"}

    def create_post(self, id: int, user_id: int, title: str, content: str):
        if id in self.posts:
            return {"error": "Post already exists"}
        user = self.users.get(user_id)
        if not user:
            return {"error": "User not found"}
        post = Post(id, user_id, title, content)
        user.add_post(post)
        self.posts[id] = post
        return post.to_dict()

    def get_post(self, id: int):
        post = self.posts.get(id)
        if not post:
            return {"error": "Post not found"}
        return post.to_dict()

    def update_post(self, id: int, title: str, content: str):
        post = self.posts.get(id)
        if not post:
            return {"error": "Post not found"}
        post.title = title
        post.content = content
        return post.to_dict()

    def delete_post(self, id: int):
        if id not in self.posts:
            return {"error": "Post not found"}
        post = self.posts.pop(id)
        user = self.users.get(post.user_id)
        if user:
            user.posts.remove(post)
        return {"message": "Post deleted"}

    def create_comment(self, id: int, user_id: int, post_id: int, content: str):
        if id in self.comments:
            return {"error": "Comment already exists"}
        post = self.posts.get(post_id)
        if not post:
            return {"error": "Post not found"}
        comment = Comment(id, user_id, content)
        post.add_comment(comment)
        self.comments[id] = comment
        return comment.to_dict()

    def get_comment(self, id: int):
        comment = self.comments.get(id)
        if not comment:
            return {"error": "Comment not found"}
        return comment.to_dict()

    def update_comment(self, id: int, content: str):
        comment = self.comments.get(id)
        if not comment:
            return {"error": "Comment not found"}
        comment.content = content
        return comment.to_dict()

    def delete_comment(self, id: int):
        if id not in self.comments:
            return {"error": "Comment not found"}
        comment = self.comments.pop(id)
        for post in self.posts.values():
            if comment in post.comments:
                post.comments.remove(comment)
        return {"message": "Comment deleted"}

api = InMemoryAPI()

app = Flask(__name__)

@app.route("/users", methods=["POST"])
def create_user():
    data = request.json
    return jsonify(api.create_user(data["id"], data["username"]))

@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    return jsonify(api.get_user(user_id))

@app.route("/posts", methods=["POST"])
def create_post():
    data = request.json
    return jsonify(api.create_post(data["id"], data["user_id"], data["title"], data["content"]))

@app.route("/posts/<int:post_id>", methods=["GET"])
def get_post(post_id):
    return jsonify(api.get_post(post_id))

@app.route("/comments", methods=["POST"])
def create_comment():
    data = request.json
    return jsonify(api.create_comment(data["id"], data["user_id"], data["post_id"], data["content"]))

@app.route("/comments/<int:comment_id>", methods=["GET"])
def get_comment(comment_id):
    return jsonify(api.get_comment(comment_id))

if __name__ == "__main__":
    app.run(debug=True)
