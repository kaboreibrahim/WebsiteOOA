from django.shortcuts import render


def apropos(request):
    context = {}
    return render(request, 'pages/apropos.html', context)
