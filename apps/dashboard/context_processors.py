def dashboard_globals(request):
    if request.user.is_authenticated and request.user.is_staff:
        from apps.website.models import Contact
        return {'sidebar_messages_non_lus': Contact.objects.filter(lu=False).count()}
    return {}
