import httpx
import pytest
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient

# Assumi che 'create_app' sia la funzione che configura e restituisce la tua applicazione FastAPI
# Se non hai una funzione del genere, dovrai configurare l'app manualmente qui
from yourapplication import create_app

# URL base per i test
BASE_URL = "http://testserver"

# Configura qui il nome del tuo database di test
TEST_DB_NAME = "test_db"

@pytest.fixture(scope="module")
def test_app():
    # Configura l'app per utilizzare il database di test
    app = create_app()
    app.state.db = AsyncIOMotorClient()[TEST_DB_NAME]

    # Crea un client per i test
    client = httpx.AsyncClient(app=app, base_url=BASE_URL)
    yield client
    # Pulisci eventuali dati di test dopo i test
    # Qui dovresti cancellare tutte le collezioni utilizzate nei test
    app.state.db.drop_database(TEST_DB_NAME)

# Qui sotto puoi creare i test per i vari endpoint
@pytest.mark.asyncio
async def test_create_user(test_app):
    # Assumi che "/users/" sia l'endpoint per creare un utente
    response = await test_app.post("/users/", json={"user_data": "test_data"})
    assert response.status_code == 200
    assert response.json() == {"message": "User created successfully"}

# Aggiungi altri test per i vari endpoint
