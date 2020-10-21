from flask import render_template
# from flask_login import login_required, current_user
# from flask_sqlalchemy import get_debug_queries
from . import main
# from .forms import EditProfileForm, EditProfileAdminForm, PostForm, CommentForm
from .. import db
from ..models import User, Course
# from ..decorators import admin_required, permission_required
from sqlalchemy.orm import scoped_session, sessionmaker, Query
from flask import current_app
import pandas as pd

@main.route('/')
def index():
    return render_template('main/index.html')

@main.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@main.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

# @main.route('/user/<username>')
# def user(username):
#     user = User.query.filter_by(username=username).first_or_404()
#     page = request.args.get('page', 1, type=int)
#     pagination = user.posts.order_by(Post.timestamp.desc()).paginate(
#         page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
#         error_out=False)
#     posts = pagination.items
#     return render_template('user.html', user=user, posts=posts,
#                            pagination=pagination)

