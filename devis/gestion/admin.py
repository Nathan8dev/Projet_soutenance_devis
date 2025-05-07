from django.contrib import admin
from gestion.models import Client, Devis, Entreprise, Particulier,LigneDevis

admin.site.register(Client)
admin.site.register(Devis)
admin.site.register(Entreprise)
admin.site.register(Particulier)
admin.site.register(LigneDevis)