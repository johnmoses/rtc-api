from django.shortcuts import render
from django.views.generic import TemplateView

class GeneralView(TemplateView):
    template_name = 'index.html'

def meeting(request, room_name, user_name):
    return render(request, 'meeting.html', {
        'room_name': room_name,
        'user_name': user_name,
    })
