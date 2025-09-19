from django.shortcuts import render,redirect
from .forms import ProfileForm
# from .models import Profile
# Create your views here.
def profile_view(request):
    profile = request.user.profile
    print(profile)
    return render(request, 'users/profile.html', {'profile': profile})

def profile_edit_view(request):
    forms = ProfileForm(instance=request.user.profile)
    
    if request.method == "POST":
        forms = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if forms.is_valid():
            forms.save()
            return redirect('profile')  # Redirect to profile page after saving
        
    return render(request, 'users/profile_edit.html',{'form': forms})