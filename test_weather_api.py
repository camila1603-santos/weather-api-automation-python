import requests

def test_weather_api_data():
    url = "https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&current_weather=true"
    response = requests.get(url)
    data = response.json()

    # --- VALIDAÇÕES DE QA ---
    
    # Valida se a requisição teve sucesso (Status Code 200)
    assert response.status_code == 200, f"Erro: Status {response.status_code}"

    # Valida se a unidade de temperatura é Celsius
    unit = data["current_weather_units"]["temperature"]
    assert unit == "°C", f"Esperado °C, mas veio {unit}"

    # Valida se a temperatura é um número (int ou float)
    temp = data["current_weather"]["temperature"]
    assert isinstance(temp, (int, float)), "A temperatura não é um número válido"

    # Valida se o fuso horário é GMT
    assert data["timezone"] == "GMT"

    print(f"\nTeste concluído com sucesso!")
    print(f"Temperatura atual: {temp}{unit}")

# Executa a função
if __name__ == "__main__":
    test_weather_api_data()