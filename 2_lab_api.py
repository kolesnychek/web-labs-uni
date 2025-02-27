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
        post = self.posts.get(comment.user_id)
        if post:
            post.comments.remove(comment)
        return {"message": "Comment deleted"}

api = InMemoryAPI()
api.create_user(1, "JohnDoe")
api.create_user(2, "JaneSmith")
api.create_post(1, 1, "My First Post", "This is a post content")
api.create_comment(1, 2, 1, "Nice post!")
api.create_comment(2, 1, 1, "Thank you!")
print(api.get_post(1))
api.update_post(1, "Updated Post Title", "Updated content")
print(api.get_post(1))
api.delete_comment(1)
print(api.get_post(1))
api.delete_post(1)
api.delete_user(1)