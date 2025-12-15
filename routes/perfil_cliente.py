from flask import Blueprint, jsonify, request, session 
from database import supabase 
from datetime import datetime 

perfil_bp = Blueprint("perfil", __name__)

def get_current_user_data():
    user_id = session.get('user_id')
    user_email = session.get('user_email')

    if user_id and user_email:
        return {
            "id": user_id,
            "email": user_email
        }
    return {"id": None, "email": None}


@perfil_bp.route("/exibir_perfil", methods=["GET"])
def area_perfil():
    user_data = get_current_user_data()
    user_id = user_data.get("id")
    user_email = user_data.get("email")
    
    if not user_id:
        return jsonify({"erro": "Usuário não autenticado."}), 401

    try:
        response = (
            supabase.table("profiles")
            .select("*, telefones(*), enderecos(*)")
            .eq("user_id", user_id)
            .single()
            .execute()
        )
        
        profile_data = response.data
        
        if profile_data:
            profile_data["email"] = user_email
        
        return jsonify(profile_data), 200
        
    except Exception as e:
        print(f"Erro ao buscar perfil: {e}")
        return jsonify({"erro": "Falha ao carregar dados do perfil."}), 500

@perfil_bp.route("/editar_perfil", methods=["POST", "PUT"])
def atualizar_perfil():
    user_data = get_current_user_data()
    user_id = user_data.get("id")
    data = request.json
    
    if not user_id:
        return jsonify({"erro": "Usuário não autenticado."}), 401

    profile_updates = {
        "nome_completo": data.get("full_name"),
        "data_nascimento": data.get("nascimento"),
        "image_url": data.get("image_url"),
        "updated_at": datetime.now().isoformat()
    }
    
    profile_updates = {k: v for k, v in profile_updates.items() if v is not None}

    try:
        supabase.table("profiles") \
            .update(profile_updates) \
            .eq("user_id", user_id) \
            .execute()
            
    except Exception as e:
        print(f"Erro ao atualizar PROFILE: {e}")
        return jsonify({"erro": "Erro ao atualizar dados principais do perfil."}), 500
        
    
    telefones_list = data.get("telefones", [])
    for telefone in telefones_list:
        tel_id = telefone.get("id")
        tel_number = telefone.get("numero")
        
        if tel_number:
            payload_telefone = {
                "numero": tel_number,
                "user_id": user_id,
            }
            
            try:
                if tel_id:
                    supabase.table("telefones") \
                        .update(payload_telefone) \
                        .eq("id", tel_id) \
                        .execute()
                else:
                    supabase.table("telefones") \
                        .insert(payload_telefone) \
                        .execute()
            except Exception as e:
                print(f"Erro ao processar telefone {tel_number}: {e}")


    enderecos_list = data.get("enderecos", [])
    for endereco in enderecos_list:
        end_id = endereco.get("id")
        end_rua = endereco.get("rua")
        
        if end_rua:
            payload_endereco = {
                "user_id": user_id,
                "rua": end_rua,
            }

            try:
                if end_id:
                    supabase.table("enderecos") \
                        .update(payload_endereco) \
                        .eq("id", end_id) \
                        .execute()
                else:
                    supabase.table("enderecos") \
                        .insert(payload_endereco) \
                        .execute()
            except Exception as e:
                print(f"Erro ao processar endereço {end_rua}: {e}")

    return jsonify({"mensagem": "Perfil e informações relacionadas atualizados com sucesso!"}), 200