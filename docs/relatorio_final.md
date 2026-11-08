# RELATÓRIO FINAL — AGROFÁCIL RPA

**Global Solution 2026.2 — CitizenTech**  
**Instituição:** FIAP

**Integrantes:**
Leticia Fontana Baptista – rm550289
Julia Palomari – rm551910
Vinicius Sobreira Borges - rm97767
Julia Ortiz – rm550204

## 1. Apresentação do projeto

O AgroFácil é uma solução tecnológica desenvolvida para auxiliar pequenos produtores rurais no acompanhamento das condições climáticas.

O projeto utiliza automação em Python para consultar previsões meteorológicas, analisar dados e gerar alertas e recomendações que podem apoiar o cuidado com as plantações.

## 2. Problema identificado

Pequenos produtores precisam acompanhar as condições climáticas para tomar decisões relacionadas à irrigação e à proteção de suas plantações.

A consulta manual de informações meteorológicas pode demandar tempo e dificultar a identificação de situações que merecem atenção.

O AgroFácil busca contribuir para esse cenário por meio da automação da coleta e análise de dados climáticos.

## 3. Objetivo e benefícios

O objetivo é automatizar o processo de consulta e análise meteorológica para organizar informações relevantes aos produtores.

Entre os benefícios esperados estão:
- Redução de tarefas manuais de consulta.
- Organização das informações climáticas.
- Identificação automatizada de possíveis riscos.
- Geração de alertas e recomendações.
- Registro das execuções para acompanhamento.

## 4. Funcionamento da solução

O sistema recebe um arquivo CSV com os dados dos produtores, valida os cadastros e utiliza suas coordenadas geográficas para consultar a API Open-Meteo.

As informações recebidas são analisadas por regras de negócio implementadas em Python. Ao final, os resultados são armazenados em um arquivo JSON e as etapas da execução são registradas em logs.

## 5. Processo automatizado

O fluxo contempla:

1. Configuração dos logs.
2. Leitura do cadastro de produtores.
3. Validação dos dados.
4. Separação dos registros válidos e inválidos.
5. Consulta meteorológica para cada produtor válido.
6. Aplicação das regras de negócio.
7. Geração de alertas e recomendações.
8. Registro de sucessos e falhas.
9. Exportação dos resultados em JSON.

O detalhamento do processo está documentado no PDD e no arquivo de fluxo do projeto.

## 6. Tecnologias utilizadas

| Tecnologia | Aplicação |
|---|---|
| Python | Desenvolvimento da automação |
| Requests | Requisições à API |
| Open-Meteo | Fonte de dados meteorológicos |
| CSV | Entrada dos dados |
| JSON | Saída dos resultados |
| Logging | Registro de execução |
| Unittest | Testes automatizados |

## 7. Regras de negócio

O protótipo utiliza as seguintes regras ilustrativas:

- Risco de geada: temperatura mínima menor ou igual a 2 °C.
- Chuva forte: precipitação diária maior ou igual a 20 mm.
- Possível seca: precipitação acumulada inferior a 5 mm e temperatura máxima igual ou superior a 30 °C.
- Baixa previsão de chuva: precipitação acumulada inferior a 5 mm.

As regras precisam ser validadas por especialistas e ajustadas conforme a cultura agrícola, o solo e as condições locais antes de qualquer aplicação real.

## 8. Tratamento de exceções e resiliência

O sistema possui mecanismos para lidar com situações inesperadas:

- Arquivo CSV inexistente.
- Cabeçalho inválido.
- Cadastros incompletos.
- Coordenadas inválidas.
- IDs duplicados.
- Timeout na consulta meteorológica.
- Falhas de conexão com a API.
- Erros na gravação dos resultados.

Falhas individuais de consulta são registradas sem impedir o processamento dos demais produtores.

## 9. Logs e auditoria

O sistema utiliza a biblioteca Logging do Python para registrar informações como:

- Início e finalização da execução.
- Quantidade de produtores válidos e inválidos.
- Processamentos realizados com sucesso.
- Falhas durante as consultas.
- Geração do arquivo de saída.

Os registros são armazenados em `logs/agrofacil.log`.

## 10. Integração com o MVP

A solução utiliza a API Open-Meteo para obter informações meteorológicas a partir das coordenadas geográficas dos produtores.

Os resultados são exportados em JSON, permitindo que outras aplicações possam consumir e utilizar as informações posteriormente.

## 11. Testes realizados

Foram implementados 13 testes automatizados utilizando Unittest.

Os testes contemplam:
- Regras de decisão climática.
- Identificação de geada, seca e chuva forte.
- Situações sem riscos identificados.
- Previsão climática vazia.
- Validação de produtores.
- Identificação de IDs duplicados.
- Coordenadas inválidas.
- Arquivo inexistente.
- Consulta meteorológica bem-sucedida.
- Timeout e falha de conexão.

**Resultado registrado na última execução: 13 testes aprovados.**

## 12. Segurança e LGPD

O protótipo utiliza dados fictícios de produtores para fins acadêmicos.

A solução não necessita de informações pessoais sensíveis para realizar a análise climática. Os dados utilizados são limitados às informações necessárias para identificar os registros e consultar a localização geográfica.

Em uma implantação real, seria necessário definir controles de acesso, proteção dos dados e políticas de retenção adequadas.


## 13. Considerações finais

O AgroFácil demonstra como a automação pode contribuir para organizar informações meteorológicas e apoiar pequenos produtores rurais.

O desenvolvimento integra consulta a uma API externa, processamento de dados, regras de decisão, tratamento de exceções, geração de arquivos estruturados e testes automatizados.

Como protótipo acadêmico, a solução apresenta uma base que pode ser ampliada futuramente com novas funcionalidades e integração com outras aplicações.