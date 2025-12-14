from flask import Blueprint, jsonify

from database import supabase 

renderizar_bp = Blueprint("renderizar", __name__)

SQL_RELATED_PRODUCTS_QUERY = """
(
    SELECT id, name, price, category, image_url, sales_count, created_at
    FROM products
    WHERE stock > 0
    ORDER BY sales_count DESC
    LIMIT 2
)
UNION 
(
    SELECT id, name, price, category, image_url, sales_count, created_at
    FROM products
    WHERE stock > 0
    ORDER BY created_at DESC
    LIMIT 10
)
ORDER BY sales_count DESC, created_at DESC
LIMIT 10;
"""

@renderizar_bp.route("/sugestoes", methods=["GET"])
def get_sugestoes():
    try:

        mock_data = [
            {"id": "p1", "name": "Top Vendas 1", "price": 100.0, "category": "A"},
            {"id": "p2", "name": "Top Vendas 2", "price": 90.0, "category": "B"},
            {"id": "p3", "name": "Recente 1", "price": 80.0, "category": "C"},
        ]
        
        return jsonify({
            "success": True, 
            "products": mock_data 
        }), 200

    except Exception as e:
        print(f"Erro ao buscar sugestões: {e}")
        return jsonify({"success": False, "message": "Erro interno do servidor."}), 500