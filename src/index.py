from flask import Flask, jsonify, request
from flask_cors import CORS
from faunadb import query as q
from faunadb.client import FaunaClient
from dotenv import load_dotenv
from .services import get_address_by_cep, get_cep_by_address, post_local_faunadb, get_all_locais
from .utils import validate_cep

load_dotenv()

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return jsonify({'message': 'HELLO WORLD'})

@app.route('/cep/<cep>', methods=['GET'])
def consultar_cep(cep):
    if not cep:
        return jsonify({'error': 'CEP não fornecido'}), 400
    
    if not validate_cep(cep):
        return jsonify({'error': 'CEP inválido'}), 400
    
    address = get_address_by_cep(cep)
    if address:
        return jsonify(address), 200
    else:
        return jsonify({'error': 'CEP não encontrado'}), 404

@app.route('/endereco', methods=['POST'])
def consultar_cep_por_endereco():
    data = request.get_json()

    if not data:
        return jsonify({'error': 'Endereço não fornecido'}), 400

    address = get_cep_by_address(data)  
    if address:
        return jsonify(address), 200
    else:
        return jsonify({'error': 'Endereço não encontrado'}), 404
        
    
@app.route('/locais', methods=['POST'])
def save_local():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Dados não fornecidos'}), 400
    
    local = post_local_faunadb(data)
    if local:
        return jsonify(local), 201
    else:
        return jsonify({'error': 'Algo deu errado, tente novamente mais tarde'}), 500
    

@app.route('/locais', methods=['GET'])
def fetch_all_locais(): 
    locais = get_all_locais()  
    if locais:
        return jsonify(locais), 200
    else:
        return jsonify({'error': 'Ainda não temos locais salvos'}), 200

if __name__ == '__main__':
    app.run(port=5000, host='0.0.0.0', debug=True)
