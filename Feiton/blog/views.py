from django.shortcuts import (
    render_to_response,
    get_object_or_404,
    Http404)
from models import Article


# Create your views here.
def index(request):
    # TODO: get the top-post and place it on home page
    specified_post = Article.objects.order_by("-publish_time").first()

    return render_to_response("index.html", {"article": specified_post})


def articles_list(request):
    articles = Article.objects.order_by("-publish_time").all()
    return render_to_response("articles.html", {"articles": articles})


def article_detail(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    return render_to_response("article_detail.html", {"article": article})


def contact_me(request):
    raise Http404


def about(request):
    raise Http404
