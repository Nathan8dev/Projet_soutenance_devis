#importation de tout les paquets dont on a besoin
from django.shortcuts import render, redirect, get_object_or_404
from django.core.validators import validate_email
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import Client, Devis, Particulier,Entreprise,LigneDevis
import json
from django.http import HttpResponseRedirect

import io
import os
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
from html2docx import html2docx
from django.template.loader import get_template



#-------------------------------user-----------------------------------------------------------------------
def accueil_site(request):
    return render(request,'gestion/accueil.html')


def Inscription(request):
    error = False
    message = ""
    if request.method == 'POST':
        nom = request.POST.get('nom')
        email = request.POST.get('email')
        password = request.POST.get('password')
        repassword = request.POST.get('repassword')
        try:
            validate_email(email)
        except:
            error = True
            message = "Entrez un email valid!"
        if error == False:
            if password != repassword:
                error = True
                message = "Les deux mots de passes ne correspondent pas!"
        user = User.objects.filter(Q(email=email) | Q(username=nom)).first()
        if user:
            error = True
            message = f"Un utilisateur avec email {email} ou le nom d'utilisateur {nom} existe dejà!"
        if error == False:
            user = User.objects.create_user(
                username=nom,
                email=email,
                password=password,
            )
            user.save()


            print(f'================{nom},{email},{password} =================')

            return redirect('connexion')

    return render(request, 'gestion/inscription.html',{'error':error,'message':message})

def Connexion(request):
    message = ''
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user=User.objects.filter(email=email).first()
        if user:
            auth_user = authenticate(username=user.username, password=password)
            if auth_user:
                login(request, auth_user)
                print(f'{auth_user.email},  {auth_user.password}')
                return redirect('accueil')
            else:
                message = f'le mot de pass entré est incorrect!'
                print('========== mot de passe incorrect! =========')
        else:
            message = f'cet utilisateur n\'existe pas'
            print('utilisateur n\'existe pas')
    return render(request, 'gestion/connexion.html',{'message': message})


@login_required(login_url='connexion')
def Accueil(request):
    return render(request,'gestion/index.html')


def log_out(request):
    logout(request)
    return redirect('connexion')


#-------------------------------------------clients------------------------------------------------
@login_required(login_url='connexion')
def Ajouter_Client(request):

    error = False
    message = ""
    if request.method == 'POST':
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        lieu = request.POST.get('lieu')
        email = request.POST.get('email')
        contact1 = request.POST.get('contact1')
        infos_supp = request.POST.get('infos_supp')
        try:
            validate_email(email)
        except:
            error = True
            message = "Entrez un email valid!"
        client = Particulier.objects.filter(Q(email=email) | Q(nom=nom)).first()
        if client:
            error = True
            message = f"Un cient avec email {email} ou le nom d'utilisateur {nom} existe dejà!"
        if error == False:
            client = Particulier.objects.create(
                id_user=request.user,
                nom=nom,
                prenom=prenom,
                email=email,
                lieu=lieu,
                contact1=contact1,
                infos_supp=infos_supp,
                type='particulier',
            )
            client.save()
            print(f'================{nom},{prenom},{lieu} =================')
            return redirect('accueil')
    return render(request,'gestion/enregistrer_client.html',{'message': message, 'error': error})


@login_required(login_url='connexion')
def Ajouter_entreprise(request):
    error = False
    message = ""
    if request.method == 'POST':
        nom_entreprise = request.POST.get('nom')
        date_creation = request.POST.get('date_creation')
        immatriculation = request.POST.get('immatriculation')
        lieu = request.POST.get('lieu')
        email = request.POST.get('email')
        contact1 = request.POST.get('contact1')
        infos_supp = request.POST.get('infos_supp')
        try:
            validate_email(email)
        except:
            error = True
            message = "Entrez un email valid!"
        client = Entreprise.objects.filter(Q(email=email) | Q(nom=nom_entreprise)).first()
        if client:
            error = True
            message = f"Un cient avec email {email} ou le nom d'utilisateur {nom_entreprise} existe dejà!"
        if error == False:

            client = Entreprise.objects.create(
                id_user=request.user,
                nom=nom_entreprise,
                date_creation=date_creation,
                immatriculation=immatriculation,
                lieu=lieu,
                email=email,
                contact1=contact1,
                infos_supp=infos_supp,
                type='entreprise',
            )
            client.save()
            print(f'================{nom_entreprise},{lieu} =================')
            return redirect('accueil')
    return render(request, 'gestion/enregistrer_entreprise.html', {'message': message, 'error': error})


@login_required(login_url='connexion')
def Liste_client(request):
    particuliers = Particulier.objects.filter(id_user=request.user)
    entreprises = Entreprise.objects.filter(id_user=request.user)

    return render(request, 'gestion/liste_client.html',{'particuliers':particuliers, 'entreprises': entreprises})


@login_required(login_url='connexion')
def Detail_client(request, id):
    clients = Client.objects.get(id=id)
    if clients.type == 'particulier':
        particulier = Particulier.objects.get(id=id)
        return render(request, 'gestion/detail_client.html', {'client': clients, 'particulier': particulier})
    if clients.type == 'entreprise':
        entreprise = Entreprise.objects.get(id=id)
        return render(request,'gestion/detail_client.html',{'client': clients, 'entreprise': entreprise})
    
    
@login_required(login_url='connexion')
def detail_client(request, id):
    clients = Client.objects.get(id=id)
    if clients.type == 'particulier':
        particulier = Particulier.objects.get(id=id)
        return render(request, 'gestion/modifier_client.html', {'client': clients, 'particulier': particulier})
    if clients.type == 'entreprise':
        entreprise = Entreprise.objects.get(id=id)
        return render(request, 'gestion/modifier_client.html', {'client': clients, 'entreprise': entreprise})


@login_required(login_url='connexion')
def Modifier_client(request, id):
    client = get_object_or_404(Client, id=id)
    if request.method == 'POST':
        if client.type == 'particulier':
            client.nom = request.POST.get('nom')
            client.prenom = request.POST.get('prenom')
            client.lieu = request.POST.get('lieu')
            client.email = request.POST.get('email')
            client.contact1 = request.POST.get('contact1')
            client.infos_supp = request.POST.get('infos_supp')
            client.type = 'particulier'

            client.save()
            return redirect('liste_client')
        if client.type == 'entreprise':
            client.nom = request.POST.get('nom')
            client.lieu = request.POST.get('lieu')
            client.email = request.POST.get('email')
            client.contact1 = request.POST.get('contact1')
            client.infos_supp = request.POST.get('infos_supp')
            client.type = 'entreprise'
            client.immatriculation = request.POST.get('immatriculation')
            client.date_creation = request.POST.get('date_creation')

            client.save()
            return redirect('liste_client')

    return render(request, 'gestion/modifier_client.html')


@login_required(login_url='connexion')
def Delete_client(request, id):
    client = get_object_or_404(Client, id=id)
    client.delete()
    return redirect('liste_client')



#----------------------------------------------devis------------------------------------------------------------------
@login_required(login_url='connexion')
def Afficher_devis(request):
    clients = Client.objects.filter(id_user=request.user)
    return render(request, 'gestion/enregistrer_devis.html',{'clients': clients})


@login_required(login_url='connexion')
def Creer_devis(request):
    produits = request.COOKIES.get('produit')
    totalht = 0
    totalttc = 0

    if request.method == 'POST':

        produit = json.loads(produits)
        print(produit)

        for i in produit:
            prixttc = i['prixTTC']
            totalttc += float(prixttc)
        print(totalttc)

        for i in produit:
            prixHT = i['prixHT']
            totalht += float(prixHT)
        print(totalht)

        object_devis = request.POST.get('objet_devis')
        client = request.POST.get('client')
        id_client = Client.objects.get(id=client)
        Devis.objects.create(
            id_client = id_client,
            objet_devis = object_devis,
            total_ht = totalht,
            total_ttc = totalttc,
        )
        devis = Devis.objects.last()
        if devis:
            for i in produit:
                LigneDevis.objects.create(
                    devis = devis,
                    designation = i['designation'],
                    quantite = i['quantite'],
                    prix_unitaire = i['prix'],
                    prix_ht = i['prixHT'],
                    tva = i['tva'],
                    total_ht = totalht,
                    total_ttc = (int(i['quantite']) * float(i['prixHT']))*float(i['tva'])/100,
                )

            return redirect('creerdevis')

    return render(request, 'gestion/creer_devis.html')


def DevisFinal(request):
    dernier_devis = Devis.objects.latest('numero')

    lignes_devis = LigneDevis.objects.filter(devis=dernier_devis)

    nom_client = dernier_devis.id_client
    numero = dernier_devis.numero
    date_devis = dernier_devis.date_creation
    objet = dernier_devis.objet_devis
    total_ttc = dernier_devis.total_ttc
    total_ht = dernier_devis.total_ht
    total_TVA = 0
    for ligne in lignes_devis:
        TVA = ligne.tva
        total_TVA+=TVA

    response = render(request, 'gestion/creerdevis.html',
                      {'client': nom_client,
                       'numero': numero,
                       'date_devis': date_devis,
                       'objet': objet,
                       'lignes_devis': lignes_devis,
                       'total_ttc': total_ttc,
                       'total_ht': total_ht,
                       'total_TVA': total_TVA,
                       }
                      )
    response.delete_cookie('produit')
    return response


def Search_devis(request):
    recherche = request.GET.get('recherche')
    if recherche:
        clients = Client.objects.filter(nom__icontains=recherche)
        return render(request, 'gestion/chercher_devis.html', {'clients': clients})


def Generer_pdf(request):
    dernier_devis = Devis.objects.latest('numero')

    lignes_devis = LigneDevis.objects.filter(devis=dernier_devis)

    nom_client = dernier_devis.id_client
    numero = dernier_devis.numero
    date_devis = dernier_devis.date_creation
    objet = dernier_devis.objet_devis
    total_ttc = dernier_devis.total_ttc
    total_ht = dernier_devis.total_ht
    total_TVA = 0
    for ligne in lignes_devis:
        TVA = ligne.tva
        total_TVA += TVA
    context = {
        'client': nom_client,
        'numero': numero,
        'date_devis': date_devis,
        'objet': objet,
        'lignes_devis': lignes_devis,
        'total_ttc': total_ttc,
        'total_ht': total_ht,
        'total_TVA': total_TVA,
    }
    html_string = render_to_string('gestion/pdfdevis.html', context)
    html = HTML(string=html_string)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="devis.pdf"'
    html.write_pdf(response)
    return response


def Generer_word(request):
    template = get_template('gestion/pdfdevis.html')
    dernier_devis = Devis.objects.latest('numero')

    lignes_devis = LigneDevis.objects.filter(devis=dernier_devis)

    nom_client = dernier_devis.id_client
    numero = dernier_devis.numero
    date_devis = dernier_devis.date_creation
    objet = dernier_devis.objet_devis
    total_ttc = dernier_devis.total_ttc
    total_ht = dernier_devis.total_ht
    total_TVA = 0
    for ligne in lignes_devis:
        TVA = ligne.tva
        total_TVA += TVA
    context = {
        'client': nom_client,
        'numero': numero,
        'date_devis': date_devis,
        'objet': objet,
        'lignes_devis': lignes_devis,
        'total_ttc': total_ttc,
        'total_ht': total_ht,
        'total_TVA': total_TVA,
    }
    html_content = template.render(context)

    document = html2docx(html_content, title=f"Devis {numero}")
    document.save('devis.docx')

    with open('devis.docx', 'rb') as f:
        response = HttpResponse(f.read(), content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        response['Content-Disposition'] = f'attachment; filename="devis_{numero}.docx"'
        return response


@login_required(login_url='connexion')
def Liste_devis(request):
    deviss = Devis.objects.filter(id_user=request.user)
    return render(request, 'gestion/liste_devis.html', {'deviss': deviss})


@login_required(login_url='connexion')
def Detail_devis(request,numero):
    deviss = Devis.objects.get(numero=numero)
    return render(request, 'gestion/detail_devis.html', {'deviss': deviss})


@login_required(login_url='connexion')
def Supprimer_devis(request, numero):
    devis = get_object_or_404(Devis, numero=numero)
    devis.delete()
    return redirect('liste_devis')