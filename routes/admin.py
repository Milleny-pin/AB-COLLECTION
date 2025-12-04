from flask import Blueprint, render_template, request, jsonify
from database import supabase

admin_bp = Blueprint("admin", __name__, template_folder="templates")

# ------------------ PÁGINA DO PAINEL ADMIN ------------------
@admin_bp.route("/admin")
def admin_home():
    return render_template("admin.html")


# ------------------ CADASTRAR PRODUTO E VARIANTE (POST) ------------------
@admin_bp.route("/admin/cadastrar_produto", methods=["POST"])
def admin_cadastrar_produto():
    # ------------------ DADOS DO PRODUTO ------------------
    nome = request.form.get("nome")
    preco = request.form.get("preco")
    estoque_produto = request.form.get("estoque_produto_form") 
    descricao = request.form.get("descricao")
    categoria = request.form.get("categoria")
    imagem_file = request.files.get("image_url") 

    # ------------------ DADOS DA VARIANTE INICIAL ------------------
    cor = request.form.get("cor")
    estoque = request.form.get("estoque") 
    sku = request.form.get("sku")
    tamanho = request.form.get("tamanho") 

    # ------------------ VALIDAÇÃO ------------------
    if not all([nome, preco, descricao, categoria, imagem_file, cor, estoque, sku, tamanho]):
        return jsonify({"erro": "Todos os campos (Produto e Variante Inicial) são obrigatórios."}), 400

    product_id = None
    public_url = None

    # ------------------ UPLOAD DA IMAGEM ------------------
    try:
        filename = f"{nome.replace(' ', '_')}_{sku}.jpg"
        supabase.storage.from_("products").upload(filename, imagem_file.read(), file_options={"content-type": imagem_file.content_type})
        public_url = supabase.storage.from_("products").get_public_url(filename)
    except Exception as e:
        return jsonify({"erro": f"Erro ao enviar imagem: {e}"}), 500

    # ------------------ INSERIR PRODUTO E RECUPERAR ID ------------------
    try:
        product_data = {
            "name": nome,
            "price": float(preco), 
            "stock": int(estoque_produto) if estoque_produto else 0, 
            "description": descricao,
            "category": categoria,
            "image_url": public_url,
        }

        result = supabase.table("products").insert(product_data).execute()
        
        inserted_data = result.data[1] 
        if inserted_data and len(inserted_data) > 0:
            product_id = inserted_data[0].get("id") 
        else:
            raise Exception("Não foi possível obter o ID do produto inserido.")
            
    except Exception as e:
        return jsonify({"erro": f"Erro ao inserir Produto no banco: {e}"}), 500

    
    # ------------------ INSERIR VARIANTE COM CHAVE ESTRANGEIRA ------------------
    try:
        variant_data = {
            "product_id": product_id, 
            "color": cor,
            "sku": sku,
            "stock_level": int(estoque), 
            "tamanho": tamanho 
        }

        supabase.table("product_variante").insert(variant_data).execute()

        return jsonify({
            "mensagem": "Produto e Variante Inicial cadastrados com sucesso!",
            "produto_id": product_id,
            "sku": sku
        }), 201
    
    except Exception as e:
        return jsonify({"erro": f"Erro ao inserir Variante: {e}"}), 500