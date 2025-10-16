from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import ChatGroup, GroupMessage
from .forms import ChatMessageCreateForm

@login_required
def chat_view(request):
    chat_group = get_object_or_404(ChatGroup, group_name="Public-chat")
    chat_messages = chat_group.chat_messages.all()[:30]

    # HTMX POST: save new message
    if request.method == 'POST' and request.htmx:
        form = ChatMessageCreateForm(request.POST)
        # print("POST data:", request.POST)  
        if form.is_valid():
            message = form.save(commit=False)
            message.author = request.user
            message.group = chat_group
            message.save()
            print("✅ Message saved:", message.body)
            context = {'message': message, 'user': request.user}
            return render(request, 'chat/partials/chat_message_p.html', context)
        else:
            print("❌ Form invalid:", form.errors)

    # Regular GET
    form = ChatMessageCreateForm()
    context = {
        'chat_messages': chat_messages,
        'form': form,
        'chat_group': chat_group,
        'user': request.user,
    }
    return render(request, 'chat/chat.html', context)
