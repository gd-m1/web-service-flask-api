from flask import request, jsonify
from flask_restful import Resource, abort
from marshmallow import ValidationError
from flaskapi import api, db
from flaskapi.models import User, Post
from flaskapi.schemas import UserSchema, PostSchema, ArgsSchema

user_schema = UserSchema()
post_schema = PostSchema()
args_schema = ArgsSchema()


class ApiUsers(Resource):
    def get(self):
        """
        @api {get} /api/users Request User information
        @apiName GetUser
        @apiGroup User

        @apiParam {String} offset skips number of rows.
        @apiParam {String} limit allows to retrieve just a portion of rows.
        @apiParam {String} order_by constrains the result into a unique order (name, last_name, email).
        @apiParam {Number} id filters by id.
        @apiParam {String} email filters by email.
        @apiParam {String} name_substr filters by name substring.

        @apiSuccess {Objects[]} items array of data belonging to user (paginated).
        @apiSuccess {Objects[]} total_count array of data belonging to user (filtered)

        @apiSuccessExample Successful Response:
        HTTP/1.1 200 OK
        {
            "items": [
                {
                    "email": "johndoe@demo.com",
                    "id": 15,
                    "last_name": "Doe",
                    "name": "John",
                    "role": "author",
                    "state": "active"
                }
            ],
            "total_count": [
                {
                    "email": "johndoe@demo.com",
                    "id": 15,
                    "last_name": "Doe",
                    "name": "John",
                    "role": "author",
                    "state": "active"
                }
            ]
        }
        """
        # Validate parameters
        errors = args_schema.validate(request.args)
        if errors:
            abort(400, message=str(errors))

        total = User.query
        items = User.query

        if 'id' in request.args:
            id = request.args.get('id', type=int)
            result = total.filter_by(id=id).first()
            return jsonify(user_schema.dump(result))

        if 'order_by' in request.args:
            order_by = request.args.get('order_by')
            total = total.order_by(getattr(User, order_by))
            items = items.order_by(getattr(User, order_by))
        if 'email' in request.args:
            email = request.args.get('email')
            total = total.filter_by(email=email)
            items = items.filter_by(email=email)
        if 'name_substr' in request.args:
            name_substr = request.args.get('name_substr')
            total = total.filter((User.name.like(f'%{name_substr}%')))
            items = items.filter((User.name.like(f'%{name_substr}%')))

        if 'offset' in request.args:
            offset = request.args.get('offset')
            items = items.offset(offset)
        if 'limit' in request.args:
            limit = request.args.get('limit')
            items = items.limit(limit)

        return jsonify({'total_count': user_schema.dump(total, many=True),
                        'items': user_schema.dump(items, many=True)})

    def post(self):
        """
        @api {Post} /api/users Create a new User
        @apiName AddUser
        @apiGroup User

        @apiParam {String} name user name.
        @apiParam {String} last_name user last name.
        @apiParam {String} email user email.
        @apiParam {String} role (author or editor).
        @apiParam {String} state (active, inactive, deleted).

        @apiSuccess {String} message New user has been added.
        @apiSuccess {Objects[]} user array of new user data.

        @apiSuccessExample Successful Response:
        HTTP/1.1 200 OK
        {
            "message": "New user has been successfully added!",
            "user": {
                "email": "johndoe@demo.com",
                "id": 33,
                "last_name": "Doe",
                "name": "John",
                "role": "author",
                "state": "active"
            }
        }
        """
        # Validate incoming data
        try:
            new_user = user_schema.load(request.json)
        except ValidationError as e:
            return e.messages, 400

        # Check if email is already in database
        email = User.query.filter_by(email=new_user['email']).first()
        if email:
            abort(409, message='User with that email already exists!')

        add_user = User(name=new_user['name'],
                        last_name=new_user['last_name'],
                        email=new_user['email'],
                        role=new_user['role'],
                        state=new_user['state'])
        db.session.add(add_user)
        db.session.commit()

        return jsonify({'message': 'New user has been successfully added!',
                        'user': user_schema.dump(add_user)})


class ApiPosts(Resource):
    def get(self):
        """
        @api {get} /api/posts Request Post information
        @apiName GetPost
        @apiGroup Post

        @apiParam {String} offset skips number of rows.
        @apiParam {String} limit allows to retrieve just a portion of rows.
        @apiParam {String} order_by constrains the result into a unique order (name, last_name, email).
        @apiParam {Number} author filters by author.

        @apiSuccess {Objects[]} items array of data belonging to user (paginated).
        @apiSuccess {Objects[]} total_count array of data belonging to user (filtered)

        @apiSuccessExample Successful Response:
        HTTP/1.1 200 OK
        {
            "items": [
                {
                    "author": 9,
                    "description": "Finally got my first shot of Moderna",
                    "id": 10,
                    "title": "Moderna"
                }
            ],
            "total_count": [
                {
                    "author": 9,
                    "description": "Finally got my first shot of Moderna",
                    "id": 10,
                    "title": "Moderna"
                }
            ]
        }
        """
        # Validate parameters
        errors = args_schema.validate(request.args)
        if errors:
            abort(400, message=str(errors))

        # Get result from two models with join query
        total = db.session.query(User, Post).join(Post, User.id == Post.author)
        items = db.session.query(User, Post).join(Post, User.id == Post.author)

        if 'order_by' in request.args:
            order_by = request.args.get('order_by')
            total = total.order_by(getattr(User, order_by))
            items = items.order_by(getattr(User, order_by))
        if 'author' in request.args:
            author = request.args.get('author')
            total = total.filter_by(author=author)
            items = items.filter_by(author=author)

        if 'offset' in request.args:
            offset = request.args.get('offset')
            items = items.offset(offset)
        if 'limit' in request.args:
            limit = request.args.get('limit')
            items = items.limit(limit)

        # Separate all Post values from query in order to serialize it with schema
        total_post, items_post = [], []
        for _ in total.all():
            total_post.append(_.Post)
        for _ in items.all():
            items_post.append(_.Post)

        return jsonify({'total_count': post_schema.dump(total_post, many=True),
                        'items': post_schema.dump(items_post, many=True)})

    def post(self):
        """
        @api {Post} /api/posts Create a new Post
        @apiName AddPost
        @apiGroup Post

        @apiParam {String} title post title.
        @apiParam {String} description post.
        @apiParam {Number} author user id.

        @apiSuccess {String} message New post has been added.
        @apiSuccess {Objects[]} post array of new post data.

        @apiSuccessExample Successful Response:
        HTTP/1.1 200 OK
        {
            "message": "New post has been added",
            "post": {
                "author": 3,
                "description": "My first post",
                "id": 30,
                "title": "Test"
            }
        }
        """
        # Validate incoming data
        try:
            new_post = post_schema.load(request.json)
        except ValidationError as e:
            return e.messages, 400

        # Check if author is in database
        author = Post.query.filter_by(author=new_post['author']).first()
        if not author:
            abort(404, message='This user does not exist!')

        add_post = Post(title=new_post['title'],
                        description=new_post['description'],
                        author=new_post['author'])
        db.session.add(add_post)
        db.session.commit()

        return jsonify({'message': 'New post has been successfully added!',
                        'post': post_schema.dump(add_post)})


api.add_resource(ApiUsers, '/api/users')
api.add_resource(ApiPosts, '/api/posts')
