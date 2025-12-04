from flask import Blueprint, jsonify
from database import supabase

produtos_bp = Blueprint("produtos", __name__, template_folder="templates")

# Listar produtos
@produtos_bp.route("/v1/listar_produtos", methods=["GET"])
def listar_produtos():
    response = (
        supabase.table("products")
        .select("name, description, price, image_url, category")
        .execute()
    )
    
    return jsonify(response.data), 200



