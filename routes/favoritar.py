from flask import Blueprint, render_template, request, jsonify, Flask
from database import supabase

app = Flask(__name__)

@app.route("/")
def favoritar():
 response = supabase.table('favorites').select('id')\
    .eq('user_id', user_id)\
    .eq('produto_id', produto_id)\
    .execute()

registros_encontrados = response.data

if registros_encontrados:
 supabase.table('favorites').delete()\
 .eq('id', id_favoritos)\
 .execute()

else:
 supabase.tavle('favorites').insert({
  "user_id": user_id,
  "produto_id": produto_id, 
 }).execute()
 

if __name__ == "__main__":
 app.run(debug=True)
