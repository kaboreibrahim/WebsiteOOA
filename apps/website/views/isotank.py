from django.shortcuts import render


def isotank(request):
    return render(request, 'pages/isotank.html')
