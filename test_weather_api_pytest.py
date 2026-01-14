import requests
import pytest

# --- Fixture: Preparação dos Dados ---

@pytest.fixture(scope="module")
def api_response():
    """
    Fixture do Pytest para chamar a API uma única vez e fornecer a resposta
    para todas as funções de teste no módulo.
    """
    # 1. Definição do endpoint (URL fixa para consistência do teste)
    url = "https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&current_weather=true"
    
    # 2. Chamada da API
    response = requests.get(url, timeout=10 )
    
    # Retorna o objeto de resposta completo para os testes
    return response

# --- Testes: Funções de Verificação ---

def test_api_request_succeeds(api_response):
    """
    Valida se a requisição à API teve sucesso (Status Code 200).
    """
    assert api_response.status_code == 200, f"Erro na requisição. Status: {api_response.status_code}"

def test_temperature_unit_is_celsius(api_response):
    """
    Valida se a unidade de temperatura na resposta é Celsius ('°C').
    """
    data = api_response.json()
    unit = data.get("current_weather_units", {}).get("temperature")
    assert unit == "°C", f"Unidade de temperatura esperada: °C, mas obtida: {unit}"

def test_temperature_value_is_valid_number(api_response):
    """
    Valida se o valor da temperatura é um número (int ou float).
    """
    data = api_response.json()
    temp = data.get("current_weather", {}).get("temperature")
    assert temp is not None, "Chave 'temperature' não encontrada na resposta."
    assert isinstance(temp, (int, float)), f"A temperatura não é um número válido. Tipo obtido: {type(temp)}"

def test_timezone_is_gmt(api_response):
    """
    Valida se o fuso horário ('timezone') na resposta é 'GMT'.
    """
    data = api_response.json()
    timezone = data.get("timezone")
    assert timezone == "GMT", f"Fuso horário esperado: GMT, mas obtido: {timezone}"

def test_response_contains_current_weather_key(api_response):
    """
    Valida se a chave 'current_weather' está presente na resposta JSON.
    """
    data = api_response.json()
    assert "current_weather" in data, "A chave 'current_weather' é obrigatória na resposta."

# --- Como Executar ---
# 1. Instale o pytest e o requests:
#    pip install pytest requests
#
# 2. Salve este código como 'test_weather_api_pytest.py'.
#
# 3. No terminal, na mesma pasta do arquivo, execute o comando:
#    pytest -v
