

document.addEventListener("DOMContentLoaded", async () => {
    console.log(1);
    await caricaClienti();
    console.log(2);

});

async function caricaClienti() {
    const response = await axios.get("/api/clienti/");
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