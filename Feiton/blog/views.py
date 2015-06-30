from django.shortcuts import (
    render_to_response,
    get_object_or_404,
    Http404,
    redirect)
from django.template import RequestContext
from models import Article
from forms import ContactForm
from django.core.mail import send_mail

from Feiton.settings import ADMIN_EMAIL


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
    if request.method == 'POST':
        print request.POST
        letter = ContactForm(request.POST)
        if letter.is_valid():
            letter_cd = letter.cleaned_data
            send_mail(
                letter_cd['subject'],
                letter_cd['content'],
                letter_cd['email'],
                [ADMIN_EMAIL],
                # fail_silently=True
                )
            print "send done"
        return redirect("home_page")

    return render_to_response("contact_me.html",context_instance=RequestContext(request))


def about(request):
    raise Http404
