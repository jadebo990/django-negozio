from django.db import models

class Cliente(models.Model):
    nome = models.CharField(max_length=50)
    email = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.email}"

class Prodotto(models.Model):
    class Categoria(models.TextChoices):
        SPORT = "SPO"
        TECH = "TEC"
        MODA = "MOD"

    nome = models.CharField(max_length=50)
    categoria = models.CharField(
        max_length = 3,
        choices = Categoria.choices
    )
    prezzo = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.nome}"

class Ordine(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    prodotti = models.ManyToManyField(Prodotto, through='OrdineProdotto')
    totale = models.DecimalField(
        max_digits = 10, 
        decimal_places = 2,
        default = 0
    )

    def calcola_totale(self):
        totale = 0
        for d in self.dettagli.all():
            totale += d.prezzo_unitario * d.quantita
        self.totale = totale

    def __str__(self):
        return f"{self.cliente.email}"
    
class OrdineProdotto(models.Model):
    # Relazione da OrdineProdotto verso Ordine
    # Django crea anche quella inversa (da Ordine verso OrdineProdotto), seguendo la regola 'nomeClasseMinuscolo_set',
    # a meno che non si specifici related_name
    ordine = models.ForeignKey(Ordine, on_delete=models.CASCADE, related_name='dettagli')

    prodotto = models.ForeignKey(Prodotto, on_delete=models.CASCADE)
    quantita = models.PositiveIntegerField()
    prezzo_unitario = models.DecimalField(max_digits=5, decimal_places=2)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.ordine.calcola_totale()
        self.ordine.save()

    def __str__(self):
        return f"{self.ordine} {self.prodotto}"


