

document.addEventListener("DOMContentLoaded", async () => {

    const token = document.querySelector('[name=csrfmiddlewaretoken]').value;
    axios.defaults.headers.common['X-CSRFToken'] = token;
    
    await caricaClienti();
    await caricaProdotti();

    
    

});

let dettagliProdotti = [];
document.getElementById("btnAggiungiProdotto").addEventListener("click", () => {

    const prodotto = document.getElementById('selectProdotto');
    const quantita = document.getElementById('quantitaProdotto').value;

    const prodottoId = prodotto.value;
    const prodottoSelezionato = prodotto.options[prodotto.selectedIndex].text;

    const prodottoString = prodottoSelezionato.split(" - €");
    const prodottoNome = prodottoString[0];
    const prodottoPrezzo = prodottoString[1];


    if(!prodottoId) {
        alert('Errore! non hai selezionato nessun prodotto.');
        return;
    }
    if(!quantita) {
        alert('Errore! la quantità non può essere minore di 1.')
        return;
    }

    // controllo se il prodotto selezionato è già stato inserito
    //...

    const dettaglio = {
        prodotto : parseInt(prodottoId),
        quantita : parseInt(quantita),
        prezzo_unitario : prodottoPrezzo
    }

    dettagliProdotti.push(dettaglio);
    

    const table = document.getElementById('tableDettagli');
    const tr = document.createElement('tr');
    tr.innerHTML = `
        <td>${prodottoNome}</td>
        <td>${quantita}</td>
        <td>${prodottoPrezzo}</td>
        <td>
            <button class="btn btn-danger btnDeleteProdotto">X</button>
        </td>
    `;   
    
    tr.querySelector('.btnDeleteProdotto').addEventListener("click", () => {
        tr.remove();
        // prendo l'indice del tr appena aggiunto
        const index = dettagliProdotti.indexOf(dettaglio)
        // e lo passo a splice così da rimuoverlo (va all'indice index ed elimina 1 elemento)
        dettagliProdotti.splice(index, 1);
        aggiornaDettagliProdotti();
    })

    table.append(tr); 

    aggiornaDettagliProdotti();

});

async function caricaClienti() {
    const response = await axios.get('/api/clienti/');
    const clienti = response.data;

    const select = document.getElementById('selectCliente');
    select.innerHTML = '';
    
    clienti.forEach(c => {
        const option = document.createElement('option');
        option.value = c.id;
        option.textContent = c.email;
        select.append(option);
    });
}

async function caricaProdotti() {
    const response = await axios.get('/api/prodotti/');
    const prodotti = response.data;

    const select = document.getElementById('selectProdotto');
    select.innerHTML = '';

    prodotti.forEach(p => {
        const option = document.createElement('option');
        option.value = p.id;
        option.textContent = `${p.nome} - €${p.prezzo}`;
        select.append(option);
    })
}

document.getElementById("formOrdine").addEventListener("submit", (e) => {
    e.preventDefault();

    if(dettagliProdotti.length == 0) {
        alert("Errore! aggiungi almeno un prodotto")
        return;
    }

    const cliente = document.getElementById('selectCliente').value;

    const ordine = {
        cliente : cliente,
    };
    
    axios.post('/api/ordini/', {
        ordine,
        dettagli : dettagliProdotti
    })
        .then(response => {
            alert("Ordine creato correttamente!")
            window.location.reload();
        })
        .catch(error => {
            alert("Errore durante la creazione dell'ordine")
            console.log(error)
        })
});


document.querySelectorAll('.btnDeleteOrdine').forEach(btn => {
    btn.addEventListener("click", () => {
        if(!confirm("Confermi l'eliminazione?")) {
            alert("Processo annullato");
            return;
        }

        const id_ordine = btn.dataset.idOrdine;
        axios.delete(`/api/ordini/${id_ordine}/`)
            .then(response => {
                alert("Eliminazione riuscita");
                window.location.reload();
            })
            .catch(error => {
                console.log(error)
            })
        

    })
})

document.getElementById("btnAnnulla").addEventListener("click", () => {
    resetForm();
    dettagliProdotti = []
    aggiornaDettagliProdotti()
})

function resetForm() {
    const form = document.getElementById('formOrdine');
    form.reset()
}

function aggiornaDettagliProdotti() {
    const divDettagli = document.getElementById('divDettagli');
    if(dettagliProdotti.length == 0) {
        const table = document.getElementById('tableDettagli');
        table.innerHTML = '';
        divDettagli.classList.add('d-none');
    }else{
        divDettagli.classList.remove('d-none');
    }
}

