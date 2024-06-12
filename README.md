#docs
Cada operação importante será uma tarefa.
Organizar as tarefas em um fluxo.
Adicionar lógica de retry e timeout


diferença entre flow e task no prefect


task = representa uma função que executa uma operação específica,como fazer uma solicitação HTTP, processar dados ou executar uma consulta em um banco de dados. São projetadas para serem reutilizáveis em diferentes fluxos.Cada tarefa é executada de forma independente

Flow = é uma coleção organizada de tasks que define a lógica de orquestração de um processo mais complexo. Ele representa o pipeline ou o fluxo de trabalho completo. incluindo a definição da ordem das tarefas, o tratamento de dependências, a coordenação de retentativas e o gerenciamento de falhas.