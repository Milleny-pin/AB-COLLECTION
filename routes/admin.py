from flask import Blueprint, render_template, request, jsonify
from database import supabase

admin_bp = Blueprint("admin", __name__, template_folder="templates")

# ------------------ PÁGINA DO PAINEL ADMIN ------------------
@admin_bp.route("/admin")
def admin_home():
    return render_template("admin.html")   # um template separado só do admin


# ------------------ CADASTRAR PRODUTO (POST) ------------------
@admin_bp.route("/admin/cadastrar_produto", methods=["POST"])
def admin_cadastrar_produto():
    nome = request.form.get("nome")
    preco = request.form.get("preco")
    estoque = request.form.get("estoque")
    descricao = request.form.get("descricao")
    categoria = request.form.get("categoria")
    imagem_file = request.files.get("image_url")

    # validação
    if not all([nome, preco, estoque, descricao, categoria, imagem_file]):
        return jsonify({"erro": "Todos os campos são obrigatórios."}), 400

    # Upload da imagem
    try:
        filename = f"{nome.replace(' ', '_')}.jpg"
        supabase.storage.from_("products").upload(filename, imagem_file)
        public_url = supabase.storage.from_("products").get_public_url(filename)
    except Exception as e:
        return jsonify({"erro": f"Erro ao enviar imagem: {e}"}), 500

    # Inserir no banco
    try:
        product_data = {
            "name": nome,
            "price": float(preco),
            "stock": int(estoque),
            "description": descricao,
            "category": categoria,
            "image_url": public_url
        }

        supabase.table("products").insert(product_data).execute()

        return jsonify({
            "mensagem": "Produto cadastrado com sucesso!",
            "produto": product_data
        }), 201
    
    except Exception as e:
        return jsonify({"erro": f"Erro ao inserir: {e}"}), 500
