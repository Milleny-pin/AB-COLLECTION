// Elementos DOM
const listaProdutos = document.getElementById("lista-produtos");
const listaSugestoes = document.getElementById("lista-sugestoes");
const messageContainer = document.getElementById("message-container");

// --- UTILS: Mensagens Customizadas (Substituindo alert()) ---
function showMessage(msg, type = 'success') {
    const color = type === 'success' ? 'bg-green-500' : 'bg-red-500';
    const icon = type === 'success' ? '✅' : '❌';
    
    const element = document.createElement('div');
    element.className = `${color} text-white px-4 py-3 rounded-lg shadow-xl mb-2 transition-all duration-300`;
    element.innerHTML = `${icon} ${msg}`;
    
    messageContainer.appendChild(element);
    
    setTimeout(() => {
        element.classList.add('opacity-0', 'translate-x-full');
        element.addEventListener('transitionend', () => element.remove());
    }, 3000);
}

// --- LÓGICA DE RENDERIZAÇÃO ---

function criarCardRender(dados, container) {
    
    const card = document.createElement("div");
    card.className = "card bg-white rounded-xl shadow-md p-4 flex flex-col items-center text-center";

    const img = document.createElement("img");
    img.src = dados.image_url || "https://placehold.co/400x533/cccccc/333333?text=Sem+Imagem"; 
    img.alt = dados.name;
    img.className = "w-full rounded-lg mb-3";

    const h2 = document.createElement("h2");
    h2.textContent = dados.name;
    h2.className = "text-lg font-semibold text-gray-800 truncate w-full";

    const h3 = document.createElement("h3");
    h3.textContent = "R$ " + Number(dados.price).toFixed(2);
    h3.className = "text-2xl font-bold text-red-600 my-2";

    const actionsDiv = document.createElement("div");
    actionsDiv.className = "flex justify-between space-x-2 w-full mt-4";

    const btn = document.createElement("button");
    btn.textContent = "⭐";
    btn.className = "favoritar-btn p-3 bg-yellow-500 text-white rounded-full shadow-lg hover:bg-yellow-600 transition duration-150";
    
    const botao = document.createElement("button");
    botao.textContent = "COMPRAR";
    botao.className = "comprar bg-indigo-500 text-white font-semibold py-2 px-4 rounded-full shadow-lg hover:bg-indigo-600 transition duration-150";

    // Evento do botão (assumindo user_id 1 para o exemplo)
    btn.onclick = () => favoritar(dados.id, 1);
    botao.onclick = () => showMessage(`Produto ${dados.name} adicionado ao carrinho!`, 'success');

    // Montagem
    actionsDiv.appendChild(btn);
    actionsDiv.appendChild(botao);

    card.appendChild(img);
    card.appendChild(h2);
    card.appendChild(h3);
    card.appendChild(actionsDiv);

    container.appendChild(card);
}


// --- FUNÇÕES DE BUSCA DA API ---

/**
 * Carrega a lista principal de produtos.
 */
async function carregarProdutosRender() {
    listaProdutos.innerHTML = '<p class="col-span-4 text-center text-indigo-500">Buscando produtos...</p>';
    try {
        const resposta = await fetch(`/historico_compras`);
        
        if (!resposta.ok) {
            throw new Error(`HTTP error! status: ${resposta.status}`);
        }
        
        const produtos = await resposta.json(); 

        listaProdutos.innerHTML = ''; 
        if (produtos && produtos.length > 0) {
            produtos.forEach(produto => criarCardRender(produto, listaProdutos));
        } else {
            listaProdutos.innerHTML = '<p class="col-span-4 text-center text-gray-600">Nenhum produto encontrado.</p>';
        }

    } catch (e) {
        console.error("Erro ao carregar produtos:", e);
        listaProdutos.innerHTML = '<p class="col-span-4 text-center text-red-600">Erro ao conectar com a API de produtos.</p>';
    }
}


async function carregarSugestoes() {
    listaSugestoes.innerHTML = '<p class="col-span-4 text-center text-indigo-500">Buscando sugestões...</p>';
    try {
     
        const resposta = await fetch(`${API_BASE_URL}/sugestoes`); 
        
        if (!resposta.ok) {
            throw new Error(`HTTP error! status: ${resposta.status}`);
        }
        
        const data = await resposta.json(); 

        listaSugestoes.innerHTML = ''; 
        
        if (data && data.products && data.products.length > 0) {
            // Renderiza no contêiner de sugestões
            data.products.forEach(produto => criarCardRender(produto, listaSugestoes)); 
        } else {
            listaSugestoes.innerHTML = '<p class="col-span-4 text-center text-gray-600">Nenhuma sugestão disponível.</p>';
        }

    } catch (e) {
        console.error("Erro ao carregar sugestões:", e);
        listaSugestoes.innerHTML = '<p class="col-span-4 text-center text-red-600">Erro ao conectar com a API de sugestões.</p>';
    }
}

// --- LÓGICA DE AÇÃO (Favoritar) ---

async function favoritar(produto_id, user_id) {
    try {
        const resposta = await fetch(`${API_BASE_URL}/favoritar`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ user_id, produto_id })
        });

        const data = await resposta.json();
        
        // Usa a notificação customizada
        if (resposta.ok) {
            showMessage(data.mensagem || "Produto favoritado com sucesso!", 'success');
        } else {
            showMessage(data.mensagem || "Erro ao favoritar o produto.", 'error');
        }
        
    } catch (e) {
        console.error("Erro ao favoritar:", e);
        showMessage("Falha na comunicação com o servidor.", 'error');
    }
}

// --- INICIALIZAÇÃO ---

function initializeApp() {
    // Estas duas linhas iniciam a busca pelas duas listas
    carregarProdutosRender();
    carregarSugestoes(); 
}

initializeApp();