from __future__ import annotations

import logging

from flask import Blueprint, jsonify, abort

from bp_posts.dao.comment import Comment
from bp_posts.dao.comment_dao import CommentDAO
from bp_posts.dao.post import Post
from bp_posts.dao.post_dao import PostDAO

from config import DATA_PATH_POSTS, DATA_PATH_COMMENTS

# Создаем блупринтишко
bp_api = Blueprint("bp_api", __name__)

# Создаем объекты под доступ к данным постов и челиков
post_dao = PostDAO(DATA_PATH_POSTS)
comments_dao = CommentDAO(DATA_PATH_COMMENTS)


@bp_api.route('/')
def api_posts_hello():
    return "Смотри документацию( удачи;) )"


api_logger = logging.getLogger("api_logger")


@bp_api.route('/posts/')
def api_posts_all():
    """ Эндпойнт(типа конечной точки) всех постов"""
    all_posts: list[Post] = post_dao.get_all()
    all_posts_as_dicts: list[dict] = ([post.as_dict() for post in all_posts])

    api_logger.debug("Запрошены все посты {pk}")

    return jsonify(all_posts_as_dicts), 200


@bp_api.route('/posts/<int:pk>/')
def api_posts_single(pk: int):
    """ Эндпойнт(конечная точка) для 1 поста"""
    post: Post | None = post_dao.get_by_pk(pk)

    if post is None:
        api_logger.debug(f"Обращение к посту которого нету {pk}")
        abort(404)

    api_logger.debug(f"Запрошен пост номер: {pk}")

    return jsonify(post.as_dict()), 200


@bp_api.errorhandler(404)
def api_error_404(error):
    api_logger.error(f"Ошибка{error}")
    return jsonify({"error": str(error)}), 404
