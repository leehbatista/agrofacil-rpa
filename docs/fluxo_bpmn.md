
# Fluxo do Processo — AgroFácil RPA

## Representação do processo automatizado

```mermaid
flowchart TD
    A([Início]) --> B[Configurar logs]
    B --> C[Ler arquivo CSV de produtores]
    C --> D{Arquivo e cabeçalho válidos?}

    D -- Não --> E[Registrar erro]
    E --> F([Encerrar execução])

    D -- Sim --> G[Validar dados dos produtores]
    G --> H[Separar cadastros válidos e inválidos]
    H --> I[Registrar quantidade de cadastros]
    I --> J{Existem produtores válidos?}

    J -- Sim --> K[Selecionar próximo produtor]
    K --> L[Consultar API Open-Meteo]
    L --> M{Consulta realizada com sucesso?}

    M -- Não --> N[Registrar falha do produtor]
    N --> O{Existem outros produtores?}

    M -- Sim --> P[Analisar condições climáticas]
    P --> Q[Aplicar regras de negócio]
    Q --> R[Gerar alertas e recomendações]
    R --> S[Registrar processamento bem-sucedido]
    S --> O

    O -- Sim --> K
    O -- Não --> T[Organizar resultados]
    J -- Não --> T

    T --> U[Gerar arquivo JSON]
    U --> V{Arquivo salvo com sucesso?}
    V -- Não --> W[Registrar erro de gravação]
    W --> F
    V -- Sim --> X[Registrar finalização]
    X --> F
```

## Descrição do fluxo

O processo começa com a configuração dos logs e a leitura do cadastro de produtores.

Após a validação dos dados, o sistema separa os cadastros válidos dos inválidos e percorre os produtores válidos para consultar a previsão meteorológica.

Quando a consulta é bem-sucedida, as regras climáticas são aplicadas e os resultados são registrados. Quando ocorre uma falha, o erro é armazenado e o sistema continua com os próximos produtores.

Ao final, os resultados são organizados e exportados para um arquivo JSON.
