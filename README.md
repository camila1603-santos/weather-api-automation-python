# Projeto de Demonstração: Cliente e Teste de API de Clima

Este repositório contém três scripts Python que interagem com a API de clima gratuita [Open-Meteo](https://open-meteo.com/ ). O objetivo é demonstrar a evolução desde um simples cliente de API até um conjunto de testes automatizados profissionais com `pytest`.

## Os Scripts: Uma Jornada em 3 Passos

Os scripts representam uma progressão natural no desenvolvimento de software:

1.  **`weather_client.py`**: Um cliente de API robusto, projetado para ser integrado em uma aplicação. **(O Aplicativo)**
2.  **`test_weather_api.py`**: Um script de teste simples e funcional para validar a API. **(O Teste Inicial)**
3.  **`test_weather_api_pytest.py`**: Uma suíte de testes profissional usando o framework `pytest`. **(O Teste Avançado)**

---

### 1. `weather_client.py` - O Aplicativo

Este script funciona como um pequeno aplicativo que busca e exibe os dados de clima para uma localização específica (neste caso, Berlim). Seu foco é **usar** a API para obter e apresentar uma informação útil.

**Principais Características:**

*   **Orientado a Objetos**: O código é dividido em classes (`WeatherAPIClient` e `WeatherAPIValidator`), cada uma com uma responsabilidade clara.
*   **Flexibilidade**: O cliente é inicializado com latitude e longitude, tornando-o facilmente adaptável para buscar o clima de qualquer lugar do mundo.
*   **Boas Práticas**: Utiliza sessões (`requests.Session`) para otimizar conexões e `raise_for_status()` para um tratamento de erros mais seguro.

**Como Executar:**
```bash
python weather_client.py
```

**Saída Esperada:**
```
=== Dados do Clima ===

Temperatura atual: 12.5°C
Velocidade do vento: 10.2 km/h
Horário: 2026-01-14T13:00

=== Validações ===

✓ Unidade de temperatura OK (°C)
✓ Temperatura em range OK
```

---

### 2. `test_weather_api.py` - O Teste Inicial

Este script é um teste de ponta a ponta (end-to-end) que verifica se a API está funcionando conforme o esperado. Seu foco é **validar** o serviço externo de forma direta e funcional.

**Principais Características:**

*   **Foco em Validação**: O objetivo é testar a API, não consumir os dados para um usuário.
*   **Especificidade**: Utiliza uma URL fixa para garantir que o teste seja consistente e repetível.
*   **Verificações Rigorosas (`assert`)**: Usa múltiplas declarações `assert` para validar o status da requisição, o contrato dos dados (unidades, fuso horário) e o tipo dos dados.
*   **Falha Rápida**: Se qualquer `assert` falhar, o script para imediatamente e aponta o erro.

**Como Executar:**
```bash
python test_weather_api.py
```

**Saída Esperada (se tudo estiver correto):**
```
Teste concluído com sucesso!
Temperatura atual: 12.5°C
```

---

### 3. `test_weather_api_pytest.py` - O Teste Avançado com `pytest`

Este script eleva o nível do teste automatizado utilizando o framework `pytest`, o padrão de fato para testes em Python. Ele realiza as mesmas validações, mas de uma forma mais estruturada, eficiente e escalável.

**Principais Vantagens do `pytest`:**

*   **Fixtures para Preparação**: Usa uma `fixture` (`@pytest.fixture`) para fazer a chamada à API **uma única vez**, compartilhando a mesma resposta com todos os testes. Isso torna a suíte de testes muito mais rápida.
*   **Testes Atômicos**: Cada validação é separada em sua própria função de teste (`test_...`). Se uma validação falhar, as outras ainda são executadas, fornecendo um relatório completo do estado da API.
*   **Relatórios Claros**: A saída do `pytest` informa exatamente qual teste passou e qual falhou, facilitando a identificação de problemas.
*   **Descoberta Automática**: O `pytest` encontra e executa todos os testes no projeto automaticamente, sem a necessidade de chamá-los manualmente.

**Como Executar:**

1.  Instale as dependências:
    ```bash
    pip install pytest requests
    ```
2.  Execute o `pytest` no seu terminal (o `-v` é para um relatório mais detalhado):
    ```bash
    pytest -v
    ```

**Saída Esperada:**
```
============================= test session starts ==============================
...
collected 5 items

test_weather_api_pytest.py::test_api_request_succeeds PASSED          [ 20%]
test_weather_api_pytest.py::test_temperature_unit_is_celsius PASSED   [ 40%]
test_weather_api_pytest.py::test_temperature_value_is_valid_number PASSED [ 60%]
test_weather_api_pytest.py::test_timezone_is_gmt PASSED               [ 80%]
test_weather_api_pytest.py::test_response_contains_current_weather_key PASSED [100%]

============================== 5 passed in ...s ===============================
```

---

## Tabela Comparativa: Cliente vs. Testes

| Característica | `weather_client.py` (O Aplicativo) | `test_weather_api.py` (O Teste Inicial) | `test_weather_api_pytest.py` (O Teste Avançado) |
| :--------------- | :----------------------------------- | :------------------------------------ | :------------------------------------------------ |
| **Objetivo** | Usar a API para uma aplicação. | Validar o comportamento da API. | Validar a API de forma robusta e escalável. |
| **Design** | Flexível e reutilizável (Classes). | Específico e direto (Função única). | Modular e eficiente (Fixtures e Testes Atômicos). |
| **Eficiência** | Uma chamada por execução. | Uma chamada por execução. | **Uma chamada para múltiplos testes.** |
| **Feedback** | Informação útil para o usuário. | Sucesso ou falha única. | Relatório detalhado de cada validação. |
| **Analogia** | Um **carro** que usa o motor. | Um **mecânico** que liga o motor uma vez. | Uma **bancada de testes** que mede vários parâmetros do motor de uma só vez. |

## Conclusão

Este repositório demonstra a importância de não apenas consumir uma API, mas também de garantir sua confiabilidade através de testes automatizados. Começando com um teste simples e evoluindo para um framework profissional como o `pytest`, podemos construir sistemas mais resilientes e fáceis de manter.


