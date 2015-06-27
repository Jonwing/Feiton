from django.shortcuts import (render, render_to_response)
from models import Article


# Create your views here.
def index(request):
    # TODO: get the top-post and place it on home page
    latest_post = Article.objects.order_by("-publish_time").first()

    return render_to_response("index.html", {"latest_post": latest_post})
