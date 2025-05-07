from django.db import models
from django.contrib.auth.models import User

class Client(models.Model):

    id_user = models.ForeignKey(User, on_delete=models.CASCADE)
    nom = models.CharField(max_length=250)
    lieu = models.CharField(max_length=250)
    email = models.CharField(max_length=250)
    contact1 = models.IntegerField()
    contact2 = models.IntegerField()
    infos_supp = models.CharField(max_length=250)
    TYPE_CLIENT=[
        ('particulier', 'Particulier'),
        ('entreprise', 'Entreprise'),
    ]
    type = models.CharField(max_length=50, choices=TYPE_CLIENT)
    def __str__(self):
        return self.nom
class Entreprise(Client):
    date_creation = models.DateField()
    immatriculation = models.CharField(max_length=250)

class Particulier(Client):
    prenom = models.CharField(max_length=250)





class Devis(models.Model):

    STATUTS_CHOICES = [
        ('valide', 'Devis validé'),
        ('refuse', 'Devis refusé'),
        ('en_cours', 'Devis en cours'),
    ]

    id_client = models.ForeignKey(Client, on_delete=models.CASCADE)
    numero = models.IntegerField(primary_key=True, unique=True)
    date_creation = models.DateField(auto_now_add=True)
    objet_devis = models.CharField(max_length=255)
    statut = models.CharField(max_length=20, choices=STATUTS_CHOICES, default='en_cours')
    total_ht = models.DecimalField(max_digits=10, decimal_places=2)
    total_ttc = models.DecimalField(max_digits=10, decimal_places=2)
    def __str__(self):
        return self.objet_devis


class LigneDevis(models.Model):
    devis = models.ForeignKey(Devis, on_delete=models.CASCADE)
    designation = models.CharField(max_length=255)
    quantite = models.IntegerField()
    prix_unitaire = models.DecimalField(max_digits=200, decimal_places=2)
    prix_ht = models.DecimalField(max_digits=200, decimal_places=2)
    total_ht = models.DecimalField(max_digits=200, decimal_places=2)
    tva = models.DecimalField(max_digits=200, decimal_places=2)
    total_ttc = models.DecimalField(max_digits=200, decimal_places=2)
    def __str__(self):
        return self.designation


