from flask import Blueprint, request, jsonify
from database import supabase

favoritar_bp = Blueprint("favoritar", __name__)

@favoritar_bp.route("/favoritar", methods=["POST"])
def favoritar():
    user_id = request.json.get("user_id")
    produto_id = request.json.get("produto_id")

    if not user_id or not produto_id:
        return jsonify({"erro": "user_id e produto_id são obrigatórios"}), 400

    # Verificar se já existe favorito
    response = supabase.table("favorites") \
        .select("id") \
        .eq("user_id", user_id) \
        .eq("produto_id", produto_id) \
        .execute()

    registros_encontrados = response.data

    if registros_encontrados:
        id_favorito = registros_encontrados[0]["id"]
        supabase.table("favorites").delete().eq("id", id_favorito).execute()
        return jsonify({"mensagem": "Favorito removido"})
    else:
        supabase.table("favorites").insert({
            "user_id": user_id,
            "produto_id": produto_id,
        }).execute()
        return jsonify({"mensagem": "Favorito adicionado"})
