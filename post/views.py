from django.shortcuts import render

# Create your views here.
def home_view(request):
    # print(request)
    title = 'welcome to Zango'
    return render(request, 'post/home.html', {'title': title})