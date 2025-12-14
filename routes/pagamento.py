import os
import json
from flask import Flask, jsonify, request
import mercadopago 


# Pgear Access Token no Painel de Desenvolvedores do Mercado Pago
MP_ACCESS_TOKEN = "APP_USR-..." 
mp = mercadopago.SDK(MP_ACCESS_TOKEN)


# --- ROTA 1: CRIAÇÃO DA PREFERÊNCIA DE PAGAMENTO MERCADO PAGO ---
@app.route("/create-mercadopago-preference", methods=["POST"])
def create_mercadopago_preference():
    data = request.json
    product_id = data.get("product_id")
    
    if not product_id or product_id not in MOCK_PRODUCTS:
        return jsonify({"error": "Produto não encontrado."}), 404
        
    product_info = MOCK_PRODUCTS[product_id]
    
    try:
        
        item = {
            "title": product_info['name'],
            "unit_price": product_info['price_cents'] / 100, 
            "quantity": 1,
            "currency_id": "BRL",
            "picture_url": product_info['image_url']
        }
        
        # Cria o payload da Preferência
        preference_data = {
            "items": [item],
            "metadata": {"product_id": product_id},
            # URL de notificação para o Webhook (DEVE ser uma URL pública)
            "notification_url": request.url_root + 'mercadopago-webhook', 
            "back_urls": {
                "success": request.url_root + 'success.html?mp_status=approved',
                "pending": request.url_root + 'pending.html?mp_status=pending',
                "failure": request.url_root + 'index.html?mp_status=failure',
            },
            "auto_return": "approved" 
        }

        preference_response = mp.preference().create(preference_data)
        preference = preference_response["response"]
        
        # Retorna a URL de redirecionamento (init_point)
        return jsonify({
            'success': True, 
            'preference_id': preference['id'],
            'checkout_url': preference['init_point'] # A URL de pagamento
        })
        
    except Exception as e:
        print(f"Erro ao criar preferência do Mercado Pago: {e}")
        return jsonify({'error': str(e)}), 400

# --- ROTA DE WEBHOOK DO MERCADO PAGO ---
@app.route('/mercadopago-webhook', methods=['POST'])
def mercadopago_webhook():
    # O Mercado Pago envia o ID do pagamento ou da ordem para esta rota
    
    data = request.json
    topic = data.get('topic')
    resource_id = data.get('id')

    if topic == 'payment' and resource_id:
        try:
            payment_info = mp.payment().get(resource_id)
            payment_status = payment_info['response']['status']
            
    
            if payment_status == 'approved':
                
                print("Pagamento APROVADO! Lógica de negócio executada.")
                pass 
                
        except Exception as e:
            print(f"Erro ao processar pagamento do Mercado Pago: {e}")
            return jsonify({'status': 'error'}), 500

    return jsonify({'status': 'success'}), 200