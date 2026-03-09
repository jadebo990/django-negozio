from django.shortcuts import render
from core.models import Cliente, Prodotto, Ordine, OrdineProdotto
from django.http import JsonResponse
import json

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

def getProdotti(request):
    prodotti = list(Prodotto.objects.values())
    return JsonResponse(prodotti, safe=False)




def detailOrdini(request, pk):
    if request.method == 'DELETE':
        return deleteOrdini(request, pk)
    elif request.method == 'PATCH':
        pass
    else:
        pass

def postOrdine(request):
    data = json.loads(request.body)
    data_ordine = data["ordine"]
    data_dettagli = data["dettagli"]

    cliente = Cliente.objects.get(pk=data_ordine["cliente"])
    
    # oppure sovrascrivo il metoodo create creando li dentro  i vari ordineprodotto??? #
    nuovo_ordine = Ordine.objects.create(cliente=cliente)
    for d in data_dettagli:
        prodotto = Prodotto.objects.get(pk=d["prodotto"])
        OrdineProdotto.objects.create(
            ordine=nuovo_ordine,
            prodotto=prodotto,
            quantita=d["quantita"],
            prezzo_unitario=prodotto.prezzo
        )
    
    return JsonResponse({"status" : "ok"})


def deleteOrdini(request, pk):
    ordine = Ordine.objects.get(pk=pk)
    ordine.delete()
    return JsonResponse({"status" : "ok"})