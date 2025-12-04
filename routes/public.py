from flask import Blueprint, render_template, request, jsonify,  redirect, url_for, session
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager 
import os
from datetime import timedelta
from database import supabase

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'usuario.login_cliente'
usuario_bp = Blueprint("usuario", __name__, template_folder="templates")

# ------------------ ROTA INICIAL ------------------
@usuario_bp.route('/home')
def usuario_home():
    
    if 'user_email' not in session:
        return redirect(url_for('usuario.login_cliente'))
        
    return render_template('home.html', user_email=session['user_email'])

# ------------------ CADASTRAR CLIENTE ------------------

@usuario_bp.route('/register', methods=["POST"])
def register():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email e senha são obrigatórios."}), 400

    try:
      
        response = supabase.auth.sign_up(
            {
                "email": email,
                "password": password,
            }
        )
        
        if response.user and response.user.id:
            return jsonify({"message": "Usuário criado com sucesso!"}), 201
        else:
            return jsonify({"message": "Usuário criado. Verifique seu e-mail para confirmar o cadastro."}), 202

    except Exception as e:
        error_message = str(e)
        if "User already registered" in error_message:
            return jsonify({"error": "Este e-mail já está cadastrado."}), 409
        else:
            print(f"Erro detalhado do Supabase: {error_message}")
            return jsonify({"error": "Erro ao tentar cadastrar usuário."}), 500
        
# ------------------ LOGIN CLIENTE ------------------
@usuario_bp.route('/login', methods=['GET', 'POST'])
def login_cliente():
    # Se o usuário já estiver logado, redireciona para a home
    if 'user_email' in session:
        return redirect(url_for('usuario.usuario_home'))
    
     # Se for um GET, apenas renderiza o formulário, passando a mensagem (se houver)
    if request.method == 'GET':
        message = request.args.get('message')
        return render_template('login.html', message=message)
    
    # Se for um POST ( formulário de login)
    if request.method =='POST':
        email = request.form.get("email")
        password = request.form.get("password")

        
        if not email or not password:
            return render_template('login.html', error="Email e senha são obrigatórios.")
        
        try:
          
            # CHAMAR O LOGIN DO SUPABASE
            response = supabase.auth.sign_in_with_password(
                {
                    "email": email,
                    "password": password,
                }
            )
            
            if response.session and response.user:
             session['user_id'] = response.user.id
             session['user_email'] = response.user.email
             session['access_token'] = response.session.access_token

             return redirect(url_for('usuario.usuario_home'))
            
            else:
              
                 return render_template('login.html', error="Credenciais inválidas ou e-mail não confirmado.")

        except Exception as e:
          
            print(f"Erro ao tentar logar: {e}")
            return render_template('login.html', error="Login falhou. Verifique seu e-mail e senha.")
        
# ------------------ LOGOUT ------------------
@usuario_bp.route('/logout', methods=['POST'])
def logout():
    session.pop('access-token', None)
    session.pop('user_id', None)
    session.pop('user_email', None)

    return redirect (url_for('usuario.login_cliente'))


        


    

