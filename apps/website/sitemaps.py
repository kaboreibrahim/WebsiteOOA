from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class StaticViewSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.8

    def items(self):
        return [
            'website:accueil',
            'website:apropos',
            'website:sourcing',
            'website:flexitank',
            'website:isotank',
            'website:produit_list',
        ]

    def location(self, item):
        return reverse(item)
