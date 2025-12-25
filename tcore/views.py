from typing import Any
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import ListView, TemplateView, DetailView
from tcore.models import Slider, About, Input, Page, Setting, Analysis
from django.contrib import messages
from taggit.models import Tag
from django.db.models import Count
from .models import Scenario
from .forms import ScenarioForm

class IndexView(ListView):
    template_name= "index.html"
    model = Slider

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Sliders'] = Slider.objects.all()
        context['Abouts'] = About.objects.first()
        context['Inputs'] = Input.objects.all()

        return context
    
class BaseView(object):
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['PBlogs']=Input.objects.order_by('-views')[:5]
        context['most_common_tags'] = Tag.objects.annotate(num_times=Count('taggit_taggeditem_items')).order_by('-num_times')[:5]

        return context
        
    
class AboutView(ListView):
    template_name= "about.html"
    context_object_name="Abouts"
    queryset=About.objects.first()
   

class TagDetailView(ListView):
    template_name = 'tag-details.html'
    context_object_name = 'Inputs'

    def get_queryset(self):
        tag_name = self.kwargs.get('tag_name')
        return Input.objects.filter(tags__name__in=[tag_name])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag_name'] = self.kwargs.get('tag_name')
        return context

class AnalysisView(ListView):
    template_name= "analysis.html"
    context_object_name= 'Analysiss'
    queryset=Analysis.objects.last()

class BlogView(BaseView, ListView):
    template_name= "blog.html"
    context_object_name = "Inputs"
    queryset = Input.objects.all()
    paginate_by = 4

class BlogDetailView(BaseView, DetailView):
    model = Input
    template_name = "blog-details.html"
    context_object_name = "input"
    slug_url_kwarg = "slug"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        obj.views+=1
        obj.save()
        return obj
    
class BlogSearchView(BaseView, ListView):
    model = Input
    template_name = 'blog-search.html'
    context_object_name = "Inputs"

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Input.objects.filter(title__icontains=query)
        return Input.objects.none()

class ContactView(TemplateView):
    template_name= "input.html"
    def post(self, request, *args, **kwargs):
        full_name = request.POST.get('fullName')
        job = request.POST.get('job')
        email = request.POST.get('email')
        title = request.POST.get('title')
        message = request.POST.get('message')
        tags = request.POST.get('tags')

        try:
            input_instance = Input.objects.create(
                full_name=full_name,
                job=job,
                email=email,
                title=title,
                message=message

            )

            if tags:
                tag_list = [tag.strip() for tag in tags.split(',')]
                input_instance.tags.add(*tag_list)

            messages.success(request,'İletiniz başarıyla gönderildi.')

        except Exception as e:
            messages.error(request, f'Mesaj gönderimi başarısız oldu: {e}')

        return HttpResponseRedirect(reverse('input'))
    
class PageDetailView(BaseView, DetailView):
    model = Page
    template_name='page-detail.html'
    context_object_name="page"
    slug_url_kwarg="slug"

def scenario_page(request):
    if request.method == 'POST':
        form = ScenarioForm(request.POST, request.FILES)
        if form.is_valid():
            scenario = form.save(commit=False)
            scenario.uploaded_by = request.user
            scenario.save()
            return redirect('scenario_page')
    else:
        form = ScenarioForm()

    scenarios = Scenario.objects.all()
    return render(request, 'scenario_page.html', {'form': form, 'scenarios': scenarios})


