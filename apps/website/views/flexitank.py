from django.shortcuts import render


def flexitank(request):
    return render(request, 'pages/flexitank.html')
