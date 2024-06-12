

# Fluxo Prefect da API Rick and Morty

  

## Visão Geral

Este projeto define um fluxo Prefect para buscar, processar e salvar dados da [API Rick and Morty](https://rickandmortyapi.com/documentation/#rest)
Ele utiliza tasks para realizar operações específicas, como buscar dados, processá-los, gerar nomes de arquivo e salvar os dados processados. 
O fluxo aceita a maioria dos endpoints  REST da API para recuperar um ou varios dados de cada recurso:


	- "https://rickandmortyapi.com/api/character",
	- "https://rickandmortyapi.com/api/character/2"
	- "https://rickandmortyapi.com/api/location",
	- "https://rickandmortyapi.com/api/location/3,21"
	- "https://rickandmortyapi.com/api/episode"


## Conceitos Principais Prefect

-  **Tasks**: Representam operações específicas a serem realizadas, como buscar dados de uma API ou processar dados JSON.

-  **Flows**: Uma coleção de tasks organizadas para definir a lógica e orquestração de um processo complexo.

> Ao definir tasks no Prefect, é comum configurá-las com parâmetros que afetam seu comportamento durante a execução. Aqui estão os parâmetros utilizados nas tasks deste fluxo Prefect e sua finalidade:

- `retries`: Este parâmetro determina o número de vezes que a tarefa será reexecutada em caso de falha. Se a execução de uma tarefa falhar, o Prefect tentará executá-la novamente de acordo com o número especificado de retries.

- `retry_delay_seconds`: Este parâmetro define o intervalo de tempo, em segundos, entre as tentativas de reexecução da tarefa em caso de falha. Após uma falha, o Prefect aguardará esse período antes de tentar executar a tarefa novamente.

- `cache_expiration`: Este parâmetro define o tempo de expiração do cache da tarefa. Após esse período, o resultado da tarefa será considerado obsoleto e a tarefa será executada novamente para obter um novo resultado.

> No projeto há variaveis de ambiente setadas para configurar os valores de retries e retry_delay_seconds


  

## Configuração do Ambiente

1. Clone este repositório.

2. Crie um arquivo `.env` com as variáveis de ambiente necessárias:

	> Dica: Use o comando se estiver no linux
		`cv .env_sample .env`

3. Crie um ambiente virtual python de acordo com seu SO
	> Saiba mais sobre na [documentação](https://docs.python.org/3/library/venv.html)

4. Instale as dependências necessárias usando o poetry:
	`poetry install`
	>Saiba mais na [documentação](https://pypi.org/project/poetry/)

  

## Uso

Para executar o fluxo Prefect, execute o script com a URL da API desejada como parâmetro usando o seguinte comando:

	`python api_flow.py -url "https://rickandmortyapi.com/api/character/2"`
	`python api_flow.py

  
  > Se nenhum parametro for fornecido será usada a url default configurada na variavel de ambiente API_URL

## Tecnologias

 - [Python: 3.12.*](https://docs.python.org/3/)
 - [Prefect: 2.19.4](https://docs.prefect.io/latest/tutorial/)
 - [Poetry](https://python-poetry.org/docs/)
 - [Black: 24.4.2](https://pypi.org/project/black/)
