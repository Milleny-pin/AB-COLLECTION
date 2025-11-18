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