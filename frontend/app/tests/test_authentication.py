import requests

BASE_URL = "http://localhost:8080"  # URL da sua aplicação Flask

def test_login_page():
    response = requests.get(f"{BASE_URL}/login")
    assert response.status_code == 200  # Verifica se a página de login está acessível

def test_register_page():
    response = requests.get(f"{BASE_URL}/register")
    assert response.status_code == 200  # Verifica se a página de registro está acessível