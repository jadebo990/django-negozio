from django.shortcuts import render
from core.models import Cliente, Prodotto, Ordine
from django.http import JsonResponse

def home(request):
    return render(request, "home.html")


def prodotti(request):
    prodotti = Prodotto.objects.all()

    context = {
        "prodotti" : prodotti
    }

    return render(request, "prodotti.html", context)


def ordini(request):
    ordini = Ordine.objects.all()

    context = {
        "ordini" : ordini
    }

    return render(request, "ordini.html", context)
    
def getClienti(request):
    ##### opzione 1
    # clienti = Cliente.objects.all()
    # return JsonResponse(clienti)
    #####
    # Non funziona perchè objects.all() restituisce un QuerySet (oggetto speciale Django che rappresenta una query sql non ancora eseguita - lazy evaluation)
    # nello specifico, un QuerySet di oggetti Cliente, che json non sa come rappresentare
    # uso perciò objects.values() per ottenere un QuerySet di dict (comunque non leggibile da json) 
    # clienti = Cliente.objects.values()
    # essendo però ancora un QuerySet, lo converto in una lista python con list()
    clienti = list(Cliente.objects.values())

    # ora ho quindi una lista py leggibile da json
    # Di default JsonResponse accetta solo dict e clienti è una lista di dict
    # per risolvere specifico safe
    return JsonResponse(clienti, safe=False)