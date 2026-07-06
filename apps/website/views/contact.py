from django.shortcuts import redirect
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from apps.website.models.Contact import Contact


SUJETS_VALIDES = {'devis', 'logistique', 'sourcing', 'autre'}


def contact(request):
    if request.method != 'POST':
        return redirect('website:accueil')

    nom = request.POST.get('name', '').strip()
    email = request.POST.get('email', '').strip()
    sujet_key = request.POST.get('subject', 'autre')
    message = request.POST.get('message', '').strip()

    if not nom or not email or not message:
        messages.error(request, "Veuillez remplir tous les champs obligatoires.")
        return redirect('website:accueil')

    if sujet_key not in SUJETS_VALIDES:
        sujet_key = 'autre'

    contact_obj = Contact.objects.create(
        nom=nom,
        email=email,
        sujet=sujet_key,
        message=message,
    )

    sujet_label = contact_obj.get_sujet_display()
    ctx = {
        'nom': nom,
        'email': email,
        'sujet_label': sujet_label,
        'message': message,
    }

    try:
        # ── Notification interne ──────────────────────────────
        html_notif = render_to_string('emails/contact_notification.html', ctx)
        texte_notif = (
            f"Nouveau message de contact\n\n"
            f"Nom    : {nom}\nEmail  : {email}\nSujet  : {sujet_label}\n\n"
            f"Message :\n{message}"
        )
        notif = EmailMultiAlternatives(
            subject=f"[Contact OOA] {sujet_label} — {nom}",
            body=texte_notif,
            from_email=settings.EMAIL_HOST_USER,
            to=[settings.EMAIL_HOST_USER],
            cc=['serge.debetou@oils-of-africa.com'],
        )
        notif.attach_alternative(html_notif, "text/html")
        notif.send(fail_silently=False)

        # ── Confirmation à l'expéditeur ───────────────────────
        html_confirm = render_to_string('emails/contact_confirmation.html', ctx)
        texte_confirm = (
            f"Bonjour {nom},\n\n"
            "Nous avons bien reçu votre message et vous répondrons très vite.\n\n"
            "Cordialement,\nL'équipe Oils of Africa"
        )
        confirm = EmailMultiAlternatives(
            subject="Oils of Africa — Nous avons bien reçu votre message",
            body=texte_confirm,
            from_email=settings.EMAIL_HOST_USER,
            to=[email],
        )
        confirm.attach_alternative(html_confirm, "text/html")
        confirm.send(fail_silently=True)

    except Exception:
        pass  # L'enregistrement en base est garanti même si le mail échoue

    messages.success(request, "Votre message a bien été envoyé. Merci !")
    return redirect('website:accueil')
