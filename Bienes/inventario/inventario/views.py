from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView


@login_required
def index(request):
    return render (request, 'index.html')

def lockout(request, credentials, *args, **kwargs):
    messages.add_message(request=request, level=messages.ERROR,message='Usuario Bloqueado') 
    return render(request,'registration/login.html')

class Error404(TemplateView):
    template_name='error/404.html'
    
class Error505(TemplateView):
    template_name='error/505.html'
    
    @classmethod
    def as_error_view(cls):
        v=cls.as_view()
        def view(request):
            r=v(request)
            r.render()
            return r
        return view