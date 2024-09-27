import os
from faunadb import query as q
from faunadb.client import FaunaClient
from dotenv import load_dotenv

load_dotenv()

fauna_secret = os.getenv('FAUNA_SECRET_KEY')

if fauna_secret is None:
    raise ValueError("A chave secreta do FaunaDB não foi encontrada. Verifique o arquivo .env.")

client = FaunaClient(secret=fauna_secret)