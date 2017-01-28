from flask import jsonify, render_template, g

from models import User
from schemas import UserSchema

# TODO put these into a class instead of a function. blueprints should help.
def create_views(app):
    user_schema = UserSchema()
    users_schema = UserSchema(many=True)

    @app.route('/')
    def hello():
        return render_template('hello.html')

    @app.route('/<name>')
    def hello_name(name):
        user = User(name=name)
        g.session.add(user)
        g.session.commit()
        return user_detail(user.id)

    @app.route('/users/')
    def users():
        all_users = g.session.query(User).all()
        result = users_schema.dump(all_users)
        return jsonify(result.data)

    @app.route('/users/<id>')
    def user_detail(id):
        user = g.session.query(User).get(id)
        return jsonify(user_schema.dump(user).data)
