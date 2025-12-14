async function comprarProdutoMercadoPago(product_id) {
    loadingOverlay.classList.remove('hidden'); 
    
    try {
        // 1. Chama o backend para criar a Preferência de Pagamento
        const response = await fetch(`${API_BASE_URL}/create-mercadopago-preference`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ product_id: product_id })
        });

        const data = await response.json();

        if (!response.ok || data.error) {
            throw new Error(data.error || 'Falha ao criar preferência de pagamento MP.');
        }
        
        // 2. Redireciona o usuário para a página de pagamento do Mercado Pago
        window.location.href = data.checkout_url;
        
    } catch (e) {
        loadingOverlay.classList.add('hidden'); 
        console.error("Erro no checkout Mercado Pago:", e);
        showMessage(`Erro no pagamento Mercado Pago: ${e.message}`, 'error');
    }
}