from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import ChatMessageCreateForm

# Create your views here.
@login_required
def chat_view(request):
    chat_group = get_object_or_404(ChatGroup, group_name="Public-chat")
    chat_messages = chat_group.chat_messages.all()[:30]
    
    # save to db
    # if request.method == 'POST':
    # htmx request ma change gareko to get the message from backend as partials
      # HTMX request - return only the new message partial
    # HTMX request - return only the new message partial
    # if request.htmx:
    if request.method == 'POST' and (request.htmx or request.headers.get('HX-Request')):
        form = ChatMessageCreateForm(request.POST)
        print("POST data:", request.POST)  
        if form.is_valid():
            message = form.save(commit=False)
            message.author = request.user
            message.group = chat_group
            message.save()
            context = {'message': message, 'user': request.user}
            return render(request, 'chat/partials/chat_message_p.html', context)
        
        else:
            #  print("❌ Form invalid:", form.errors)
            print("❌ Form invalid:", form.errors)  # <- debugging line
             
    # Regular full page
    form = ChatMessageCreateForm()
    context = {
        'chat_messages': chat_messages,
        'form': form,
        'chat_group': chat_group,
    }
    return render(request, 'chat/chat.html', context)
