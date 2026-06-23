from django.shortcuts import render
from apps.website.models import Produit, Personne, Partenaire


def apropos(request):
    produits    = Produit.objects.filter(actif=True).order_by('ordre')
    dirigeants  = Personne.objects.filter(actif=True, role=Personne.Role.DIRIGEANT).order_by('ordre')

    departements = [
        {
            'slug':    Personne.Departement.ADMINISTRATIF,
            'label':   'Équipe Administrative',
            'sous':    'Comptabilité & Direction',
            'icone':   'account_balance',
            'membres': Personne.objects.filter(actif=True, role=Personne.Role.MEMBRE, departement=Personne.Departement.ADMINISTRATIF).order_by('ordre'),
        },
        {
            'slug':    Personne.Departement.OPERATIONNEL,
            'label':   'Équipe Opérationnelle',
            'sous':    'Logistique & gestion de stock',
            'icone':   'local_shipping',
            'membres': Personne.objects.filter(actif=True, role=Personne.Role.MEMBRE, departement=Personne.Departement.OPERATIONNEL).order_by('ordre'),
        },
         {
            'slug':    Personne.Departement.SOURCING,
            'label':   'Équipe Sourcing',
            'sous':    'Experts en approvisionnement',
            'icone':   'shopping_bag',
            'membres': Personne.objects.filter(actif=True, role=Personne.Role.MEMBRE, departement=Personne.Departement.SOURCING).order_by('ordre'),
        }, 
    ]

    partenaires = Partenaire.objects.filter(actif=True).order_by('ordre')

    context = {
        'produits':     produits,
        'dirigeants':   dirigeants,
        'departements': departements,
        'partenaires':  partenaires,
    }
    return render(request, 'pages/apropos.html', context)
