from django.shortcuts import render,get_object_or_404,Http404
from django.http import HttpResponse,HttpResponseRedirect
from django.views import View

from .models import ShortenerURL
from .forms import SubmitUrlForm
from analytics.models import ClickEvent
# Create your views here.

def home_view_fbv(request, *args, **kwargs):
    if request.method == "POST":
        print(request.POST)
    return render(request, "shortener/home.html", {})


class HomeView(View):

    def get(self, request, shortcode=None, *args, **kwargs):
        the_form = SubmitUrlForm()
        bg_image = 'https://upload.wikimedia.org/wikipedia/commons/0/05/20100726_Kalamitsi_Beach_Ionian_Sea_Lefkada_island_Greece.jpg'
        context = {
            "title": "dhalli.com",
            "form": the_form,
            "bg_image": bg_image
        }
        return render(request,"shortener/home.html",context)

    def post(self,request,*args,**kwargs):
        form = SubmitUrlForm(request.POST)
        # import pdb;pdb.set_trace()
        context = {
            "title": "dhalli.com ",
            "form": form,
        }
        template="shortener/home.html"
        if form.is_valid():
            new_url=form.cleaned_data.get("url")
            if "http" in new_url and not "www" in new_url:
                url=new_url.split("//")
                new_url=url[1]
            if not "www" in new_url:
                new_url = "www." + new_url
            if not "http" in new_url:
                new_url = "http://" + new_url
            if "https" in new_url:
                modified_url = new_url.replace('https', 'http')
                obj, created = ShortenerURL.objects.get_or_create(url=modified_url)
            else:
                obj,created=ShortenerURL.objects.get_or_create(url=new_url)
            context = {
                "object": obj,
                "created": created,
            }
            if created:
                template="shortener/success.html"
            else:
                template = "shortener/already-exists.html"
        return render(request,template,context)


class URLRedirectView(View):

    def get(self, request,shortcode=None,*args,**kwargs):
        qs = ShortenerURL.objects.filter(shortcode__iexact=shortcode)
        if qs.count() != 1 and not qs.exists():
            raise Http404
        obj = qs.first()
        print(ClickEvent.objects.create_event(obj))
        return  HttpResponseRedirect(obj.url)

