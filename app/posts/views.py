from . import post_bp


@post_bp.route('/', strict_slashes=False)
def all_posts():
    return "Posts blueprint works"