from django.shortcuts import render

def home(request):
    context = {}
    return render(request, 'bulletin/templates/bulletin/home.html', context)
