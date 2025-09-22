from django.shortcuts import render,redirect
from .forms import ProfileForm
from django.shortcuts import get_object_or_404
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.http import Http404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# from .models import Profile
# Create your views here.
def profile_view(request, username=None):
    if username:
        profile = get_object_or_404(User, username=username).profile
    else:
        try:
            profile = request.user.profile
        except:
            raise Http404

    # print(profile)
    return render(request, 'users/profile.html', {'profile': profile})

@login_required
def profile_edit_view(request):
    forms = ProfileForm(instance=request.user.profile)
    
    if request.method == "POST":
        forms = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if forms.is_valid():
            forms.save()
            return redirect('profile')  # Redirect to profile page after saving
        
    return render(request, 'users/profile_edit.html',{'form': forms})

@login_required
def profile_delete_view(request):
    user = request.user
    if request.method == "POST":
        logout(request)
        user.delete()
        # return redirect('profile')\
        messages.success(request, "Account deleted!")
        return redirect('home')
    
    return render(request, 'users/profile_delete.html')