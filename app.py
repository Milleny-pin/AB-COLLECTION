import os
import uuid
import json
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from supabase import create_client, Client
from supabase.client import AuthApiError


load_dotenv()

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

supabase: Client = None
if not SUPABASE_URL or not SUPABASE_KEY:
    print("ERRO: As variáveis SUPABASE_URL e SUPABASE_KEY não foram encontradas no arquivo .env.")
    print("Verifique se o arquivo .env está na pasta e preenchido corretamente.")
else:
    try:
        # Cria a conexão com o cliente Supabase
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        print("Conexão com o Supabase estabelecida com sucesso!")
    except Exception as e:
        print(f"Erro ao conectar ao Supabase: {e}")
        supabase = None

#POST
@app.route("/items", methods=["POST "])
def add_product():
    data = request.json

    nome = data.get("nome")
    preco = data.get("preco")
    estoque = data.get("estoque")
    descricao = data.get("descricao")
    image_url = data.get("image_url")
    categoria = data.get("categoria")

    if not nome or preco is None or estoque or descricao is None or image_url or categoria is None: 
        return jsonify({"erro": "Dados incompletos. Requer: nome, preco, estoque"}), 400
    
    try:
        product_data = {
            "name": nome,
            "prime": preco, 
            "stock": estoque,
            "image_url": image_url,
            "category": categoria,
            "description": descricao
        }

       
        response = supabase.table("products").insert(product_data).select("id, description, name, price, stock, image_url, category").execute()

   
    except Exception as e: 
        print(f"Erro ao adicionar produto: {e}")
        return jsonify({"erro": f"Erro interno do servidor: {e}"}), 500

# DELETE
@app.route("/items/<string:product_id>", methods=["DELETE"])
def delete_product(product_id):
    """Deleta um produto (DELETE)."""
    try:
      
        response = supabase.table("products") \
                           .delete() \
                           .eq("id", product_id) \
                           .execute()
        
        
        if response.data:
       
            return "", 204 
        else:
            return jsonify({"erro": f"Produto com ID {product_id} não encontrado."}), 404

    except Exception as e:
        print(f"Erro ao deletar produto: {e}")
        return jsonify({"erro": f"Erro interno do servidor: {e}"}), 500

# PUT  
@app.route("/items/<string:product_id>", methods=["PUT"])
def add_product(product_id):
    data = request.json

    nome = data.get("nome")
    preco = data.get("preco")
    estoque = data.get("estoque")
    descricao = data.get("descricao")
    image_url = data.get("image_url")
    categoria = data.get("categoria")


    required = [nome, preco, estoque, descricao, image_url, categoria]
    if any(field is None for field in required):
        return jsonify({"erro": "Dados incompletos. Requer: nome, preco, estoque, descricao, image_url, categoria"}), 400

    try:
        product_data = {
            "name": nome,
            "price": preco,
            "stock": estoque,
            "image_url": image_url,
            "category": categoria,
            "description": descricao
        }

        response = (
            supabase.table("products")
            .update(product_data)
            .eq("id", product_id)
            .select("id, description, name, price, stock, image_url, category")
            .execute()
        )

        return jsonify(response.data), 200

    except Exception as e:
        print(f"Erro ao atualizar produto: {e}")
        return jsonify({"erro": "Erro interno do servidor"}), 500
    
# GET   
@app.route("/items/<string:product_id>", methods=["GET"])
def get_product_by_id(product_id):
    """Busca um único produto pelo seu ID (READ BY ID)."""
    try:
        # Usa .eq() para filtrar pelo ID e .single() para buscar 1 item
        response = supabase.table('products') \
                           .select("id, name, description, price, stock, image_url, category, is_available") \
                           .eq("id", product_id) \
                           .single() \
                           .execute()
        
        p = response.data 

      
        product_for_frontend = {
            "id": p["id"],
            "nome": p["name"],
            "descricao": p["description"],
            "preco": p["price"],
            "estoque": p["stock"],
            "image_url": p["image_url"],
            "categoria": p["category"],
            "disponivel": p["is_available"]
        }
        return jsonify(product_for_frontend), 200

    except Exception as e:
        print(f"Erro ao buscar produto por ID: {e}")
        return jsonify({"error": f"Produto com ID {product_id} não encontrado ou erro no servidor."}), 404
