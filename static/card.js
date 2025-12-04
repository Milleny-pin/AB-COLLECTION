// =========================
// 1) CARREGAR PRODUTOS
// =========================
async function carregarProdutos() {
    try {
        const resposta = await fetch("http://localhost:5000/produtos"); // sua rota GET
        const produtos = await resposta.json();

        produtos.forEach(produto => criarCard(produto)); // ← cria o HTML automático
    } catch (e) {
        console.error("Erro ao carregar produtos", e);
    }
}


// =========================
// 2) CRIAR CARD NO APPEND CHILD
// =========================
function criarCard(dados) {

    const container = document.getElementById("lista-produtos");

    const card = document.createElement("div");
    card.className = "card";

    const img = document.createElement("img");
    img.src = dados.image_url; // ← pega do banco
    img.alt = dados.name;

    const h2 = document.createElement("h2");
    h2.textContent = dados.name;

    const h3 = document.createElement("h3");
    h3.textContent = "R$ " + Number(dados.price).toFixed(2);

    const btn = document.createElement("button");
    btn.textContent = "⭐";
    btn.className = "favoritar-btn";

    // Evento do botão
    btn.onclick = () => favoritar(dados.id, 1); // << produto_id , user_id fixo de exemplo


    // Montagem (equivalente ao appendChild)
    card.appendChild(img);
    card.appendChild(h2);
    card.appendChild(h3);
    card.appendChild(btn);

    container.appendChild(card);
}


// =========================
// 3) FUNÇÃO PARA FAVORITAR
// =========================
async function favoritar(produto_id, user_id) {
    try {
        const resposta = await fetch("http://localhost:5000/favoritar", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ user_id, produto_id })
        });

        const data = await resposta.json();
        alert(data.mensagem);
        
    } catch (e) {
        console.error("Erro ao favoritar:", e);
    }
}


// =========================
// INICIAR AUTOMATICAMENTE
// =========================
carregarProdutos();
