# PDD — Process Design Document
## Projeto AgroFácil RPA

### 1. Identificação do processo

**Nome:** Automação de análise climática para pequenos produtores rurais.

**Projeto:** AgroFácil RPA.

**Disciplina:** Global Solution 2026.2 — CitizenTech.

**Objetivo:** Automatizar a consulta e análise de informações meteorológicas para auxiliar pequenos produtores no acompanhamento das condições climáticas de suas plantações.

### 2. Descrição do problema

Pequenos produtores rurais precisam acompanhar constantemente as condições climáticas para tomar decisões relacionadas ao cuidado de suas plantações.

A consulta manual de previsões meteorológicas e a identificação de possíveis riscos podem demandar tempo e dificultar o acompanhamento das informações.

O AgroFácil busca reduzir esse trabalho por meio da automação da consulta, análise e organização dos dados climáticos.

### 3. Objetivo da automação

O processo automatizado tem como objetivo:

- Ler os dados cadastrados dos produtores.
- Validar as informações recebidas.
- Consultar previsões meteorológicas por meio da API Open-Meteo.
- Identificar possíveis riscos climáticos.
- Gerar alertas e recomendações.
- Armazenar os resultados em arquivo JSON.
- Registrar as etapas da execução em logs.

### 4. Entradas do processo

| Entrada | Descrição |
|---|---|
| Arquivo CSV | Cadastro dos produtores rurais |
| ID | Identificador do produtor |
| Nome | Nome do produtor |
| Cultura | Tipo de plantação |
| Latitude | Coordenada geográfica |
| Longitude | Coordenada geográfica |
| API Open-Meteo | Fonte das informações meteorológicas |

### 5. Etapas do processo

1. Iniciar a execução do AgroFácil.
2. Configurar o sistema de logs.
3. Ler o arquivo CSV com os dados dos produtores.
4. Validar os campos obrigatórios, coordenadas e possíveis duplicidades.
5. Separar os cadastros válidos dos inválidos.
6. Percorrer a lista de produtores válidos.
7. Consultar a previsão meteorológica de cada produtor.
8. Analisar as condições climáticas conforme as regras de negócio.
9. Gerar alertas e recomendações.
10. Registrar o resultado de cada processamento.
11. Exportar os resultados em arquivo JSON.
12. Finalizar a execução.

### 6. Regras de negócio

O sistema utiliza as seguintes condições ilustrativas:

- **Geada:** temperatura mínima prevista menor ou igual a 2 °C.
- **Chuva forte:** precipitação diária maior ou igual a 20 mm.
- **Possível seca:** precipitação acumulada inferior a 5 mm e temperatura máxima igual ou superior a 30 °C.
- **Baixa previsão de chuva:** precipitação acumulada inferior a 5 mm.

Quando nenhuma condição de risco é identificada, o sistema informa que não foram encontrados riscos conforme as regras implementadas.

As regras são demonstrativas e precisam de validação agronômica antes de serem utilizadas em decisões reais de produção.

### 7. Decisões e condições

Durante o processamento, o sistema verifica:

- Se o arquivo CSV existe e possui cabeçalho válido.
- Se os dados de cada produtor são válidos.
- Se existem IDs duplicados.
- Se a consulta meteorológica foi realizada com sucesso.
- Se a previsão retornada contém os dados necessários.
- Se alguma regra climática foi atendida.

Os produtores com cadastros inválidos são separados, enquanto falhas individuais de consulta são registradas sem interromper o processamento dos demais produtores.

### 8. Tratamento de exceções

| Situação | Tratamento |
|---|---|
| Arquivo CSV inexistente | Registrar erro e interromper a execução |
| Cadastro inválido | Separar o registro e continuar |
| ID duplicado | Descartar o registro duplicado |
| Coordenadas inválidas | Descartar o cadastro |
| Timeout da API | Registrar a falha do produtor |
| Erro de conexão | Registrar a falha do produtor |
| Falha ao salvar JSON | Registrar o erro |

### 9. Saídas do processo

O sistema gera:

- **Arquivo JSON:** contém data da execução, totais processados, cadastros inválidos, falhas, dados climáticos, alertas e recomendações.
- **Arquivo de log:** registra horários, etapas, sucessos e falhas da execução.

### 10. Tecnologias utilizadas

- Python: desenvolvimento da automação.
- Requests: comunicação com a API meteorológica.
- Open-Meteo: fornecimento de dados climáticos.
- CSV: entrada dos cadastros.
- JSON: armazenamento dos resultados.
- Logging: registro e auditoria da execução.
- Unittest: testes automatizados.

### 11. Testes

O projeto possui 13 testes automatizados, distribuídos entre:

- Testes das regras de negócio.
- Testes de validação dos cadastros.
- Testes de consulta à API e tratamento de falhas.

Na última execução, os 13 testes foram aprovados.

### 12. Considerações finais

O AgroFácil RPA automatiza etapas de consulta e análise climática, contribuindo para organizar informações que podem auxiliar pequenos produtores rurais.

A solução foi desenvolvida como protótipo acadêmico, utilizando dados fictícios e regras demonstrativas, com possibilidade de evolução e integração com outras funcionalidades do MVP.