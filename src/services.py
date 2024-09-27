import requests
from .lib import client
from faunadb import query as q
from faunadb.errors import FaunaError

BASE_URL_VIACEP = "https://viacep.com.br/ws/"

def get_address_by_cep(cep):
    url = f"{BASE_URL_VIACEP}{cep}/json/"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

def get_cep_by_address(endereco):
    api_url = f"{BASE_URL_VIACEP}{endereco['UF']}/{endereco['cidade']}/{endereco['logradouro']}/json/"
    
    try:
        response = requests.get(api_url)
        response.raise_for_status()  

        data = response.json()
        
        if isinstance(data, list) and data:
            return data  
        else:
            return None
        
    except requests.exceptions.RequestException as e:
        print(f'Erro ao consultar o endereço: {e}')
        return None
    
def post_local_faunadb(local):
    try:
        result = client.query(
            q.create(
                q.collection("Locais"),
                {"data": local}
            )
        )
        return result['data'] 
    except FaunaError as e:
        print(f'Erro ao consultar o endereço: {e}')
        return None
    
def get_all_locais():
    try:
        result = client.query(
            q.paginate(
                q.documents(q.collection("Locais")),
                size=100 
            )
        )

        locais_data = []
        for ref in result['data']:
            local = client.query(q.get(ref))
            locais_data.append({
                'id': ref.id(),  
                **local['data']         
            })

        return locais_data

    except FaunaError as e:
        print(f'Erro ao consultar o FaunaDB: {e}')
        return []
    except Exception as e:
        print(f'Erro desconhecido: {e}')
        return []
