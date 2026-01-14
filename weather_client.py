import requests
from typing import Any, Dict, Optional
# import requests: traz a biblioteca "requests", que serve pra fazer requisições HTTP (tipo abrir uma URL)
# from typing ...: só serve pra ajudar a "documentar" tipos (não muda como o programa roda)


class WeatherAPIClient:
    # class = uma "fábrica" de objetos. Aqui vamos criar um cliente para falar com a API.

    BASE_URL = "https://api.open-meteo.com/v1/forecast"
    # BASE_URL = uma constante (um texto fixo) com o endereço principal da API

    def __init__(self, latitude: float, longitude: float, session: Optional[requests.Session] = None):
        # __init__ é o "construtor": ele roda quando você cria um objeto dessa classe.
        # latitude e longitude são números (float) que indicam o local.
        # session é opcional: se você não passar, ele cria uma Session por conta própria.

        self.latitude = latitude
        # self.latitude guarda a latitude dentro do objeto (self = "este objeto")

        self.longitude = longitude
        # self.longitude guarda a longitude dentro do objeto

        self.session = session or requests.Session()
        # "session or requests.Session()" significa:
        # - se você passou uma session, usa ela
        # - senão, cria uma nova requests.Session()
        # Session ajuda a reaproveitar conexão e deixar chamadas HTTP mais eficientes

    def get_weather_data(self) -> Dict[str, Any]:
        # define um método (função dentro da classe)
        # ele vai buscar os dados da API e retornar um dicionário (Dict) com qualquer coisa dentro (Any)

        params = {
            "latitude": self.latitude,
            "longitude": self.longitude,
            "current_weather": "true",
        }
        # params é um dicionário com parâmetros da URL
        # em vez de escrever a URL inteira com "?" e "&", você passa params e o requests monta pra você

        resp = self.session.get(self.BASE_URL, params=params, timeout=10)
        # faz um GET na API:
        # - self.BASE_URL é o endereço
        # - params vira a parte "?latitude=...&longitude=...&current_weather=true"
        # - timeout=10 significa: se demorar mais de 10s, dá erro (pra não travar)

        resp.raise_for_status()
        # se o status não for 200 (ex.: 404, 500), isso levanta um erro automaticamente

        return resp.json()
        # pega o corpo da resposta (que vem em JSON) e converte para dicionário Python


class WeatherAPIValidator:
    # essa classe existe só para VALIDAR os dados que vieram da API

    def __init__(self, data: Dict[str, Any]):
        # quando você cria o validador, você passa o JSON (como dicionário) pra ele

        self.data = data
        # guarda os dados dentro do objeto

    def validate_temperature_unit(self) -> None:
        # esse método valida a unidade e a temperatura
        # -> None significa que ele não retorna nada
        # se algo estiver errado, ele "estoura" um erro usando assert

        unit = self.data.get("current_weather_units", {}).get("temperature")
        # self.data.get("current_weather_units", {}) tenta pegar a chave "current_weather_units"
        # se não existir, ele devolve {} (dicionário vazio)
        # depois .get("temperature") tenta pegar "temperature" dentro disso
        #
        # isso evita KeyError (erro de chave não encontrada) e deixa mais seguro

        assert unit == "°C", f"Unidade esperada: °C, obtida: {unit}"
        # assert é uma verificação:
        # - se unit for "°C", ok, continua
        # - se for diferente, o programa dá erro com essa mensagem

        temperature = self.data["current_weather"]["temperature"]
        # aqui a gente pega direto com ["..."] porque esperamos que exista
        # self.data["current_weather"] pega o bloco current_weather
        # ["temperature"] pega o número da temperatura

        assert -100 < temperature < 60, f"Temperatura fora do range esperado: {temperature}°C"
        # garante que a temperatura faz sentido (sanity check)
        # -100 e 60 é só um intervalo bem amplo pra evitar valores absurdos


def main():
    # main() é uma função que organiza o "fluxo principal" do programa

    client = WeatherAPIClient(latitude=52.52, longitude=13.41)
    # cria um objeto do tipo WeatherAPIClient com latitude e longitude
    # isso "instancia" a classe (cria um cliente real)

    data = client.get_weather_data()
    # chama o método que faz a requisição e retorna o JSON (como dicionário)
    # data agora é o JSON inteiro da API

    print("=== Dados do Clima ===\n")
    # print() escreve no terminal

    print(f"Temperatura atual: {data['current_weather']['temperature']}°C")
    # f"..." é uma f-string: permite colocar variáveis dentro do texto
    # aqui pega a temperatura dentro do JSON

    print(f"Velocidade do vento: {data['current_weather']['windspeed']} km/h")
    # pega a velocidade do vento dentro do JSON

    print(f"Horário: {data['current_weather']['time']}")
    # pega o horário da medição dentro do JSON

    print("\n=== Validações ===\n")
    # imprime um título antes das validações

    validator = WeatherAPIValidator(data)
    # cria um validador passando os dados que vieram da API

    validator.validate_temperature_unit()
    # roda a validação da unidade e do range de temperatura
    # se algo estiver errado, aqui vai "estourar" um erro

    print("✓ Unidade de temperatura OK (°C)")
    # se chegou aqui, passou na validação da unidade

    print("✓ Temperatura em range OK")
    # se chegou aqui, passou na validação do range também


if __name__ == "__main__":
    # esse if é um padrão do Python:
    # ele garante que o main() só rode quando você executar este arquivo diretamente
    # (e não quando você importar este arquivo em outro)

    main()
    # chama a função principal

