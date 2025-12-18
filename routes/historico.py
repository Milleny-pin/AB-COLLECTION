from flask import Blueprint, render_template, request, jsonify
from database import supabase

historico_bp = Blueprint("historico", __name__, template_folder="templates")


def get_current_user_id():
    return session.get('user_id')


@historico_bp.route("/admin")
def exibir_historico():
    user_id = get_current_user_id()

    if not user_id:
        return jsonify({"erro": "Usuário não autenticado"}), 401
    
    try:
        response = (
            supabase.table("ordens")
            .select("*, ordens_itens!inner(produto_id, quantidade, preco_unitario, produtos(*))")
            .eq("user_id", user_id)
            .order("data_pedido", desc=True)
            .execute()
        )
        return jsonify(response.data), 200
    except Exception as e: 
        print(f"Erro ao buscar histórico de compras: {e}")
        return jsonify({"erro":"Falha ao buscar histórico de compras"}), 500