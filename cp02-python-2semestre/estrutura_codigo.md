# Estrutura do Código: Sistema de Estoque (Vendas e Relatórios)

Este documento explica a estrutura lógica e as decisões arquiteturais tomadas para implementar os requisitos de **Vendas**, **Relatórios** e as **Interfaces** (CLI e GUI), preservando estritamente as classes originais do arquivo `stock_class.py`.

## 1. Princípio de Extensão (Herança)

Uma das regras principais do enunciado era utilizar o código de `stock_class.py` como base sem alterar seu código original. Para adicionar o **Histórico de Movimentações** (entradas, saídas e atualizações) de forma automática ao manipular o estoque, utilizamos o conceito de **Herança Orientada a Objetos**.

- **Classe `EstoqueAvancado` (em `vendas.py`)**: 
  - Herda diretamente da classe `Estoque` (importada de `stock_class.py`).
  - Sobrescreve os métodos principais de modificação: `cadastrar_produto`, `adicionar_estoque`, `remover_estoque` e `atualizar_estoque`.
  - Dentro de cada método sobrescrito, chamamos o método original através da função `super()`. Isso garante que todo o comportamento original (validações, lógicas de erro, impressões no console) seja preservado intacto.
  - Imediatamente após a chamada de `super()`, a nossa nova classe verifica se a operação teve sucesso (checando as quantidades no dicionário) e registra um evento no `historico_movimentacoes` contendo data, hora, tipo da operação e quantidade.

## 2. Lógica de Vendas

Para isolar o fluxo de vendas do controle básico de estoque, criamos uma nova classe baseada no princípio de responsabilidade única.

- **Classe `GerenciadorVendas` (em `vendas.py`)**:
  - Recebe uma instância de `EstoqueAvancado` no seu construtor (Injeção de Dependência).
  - **`registrar_venda`**: Recebe o código do produto, a quantidade desejada e um percentual de desconto opcional. A classe valida se há estoque suficiente e invoca o método `remover_estoque` do objeto `EstoqueAvancado` — o que significa que a baixa do estoque e o registro do histórico ocorrem num único fluxo. Em seguida, processa as deduções de desconto e calcula o valor final a pagar.
  - **`emitir_recibo`**: Formata e exibe uma "nota fiscal" simplificada exibindo os dados do produto, quantidades, descontos e o valor bruto a pagar. O sistema registra todas essas vendas numa lista `vendas_realizadas`.

## 3. Lógica de Relatórios

- **Classe `Relatorios` (em `vendas.py`)**:
  - Centraliza a formatação e visualização dos dados agregados.
  - **`relatorio_vendas`**: Itera pela lista de `vendas_realizadas` da classe `GerenciadorVendas` e imprime os detalhes de forma estruturada, além de somar e apresentar o total financeiro arrecadado por todas as vendas.
  - **`relatorio_estoque`**: Repassa o comando diretamente ao método `exibir_estoque()` da classe base `Estoque`, reaproveitando o código original.
  - **`historico_movimentacoes`**: Itera de forma limpa pelo log salvo na classe `EstoqueAvancado`, demonstrando a rastreabilidade (adições e remoções de cada produto).

## 4. Interfaces do Usuário

Foram desenvolvidas duas abordagens de interação para englobar os requisitos exigidos.

### 4.1 Interface em Linha de Comando (CLI)
- Encontra-se no arquivo **`cli.py`**.
- Utiliza apenas as funções nativas e primitivas do Python (`print`, `input` e uma estrutura `while True`).
- Totalmente agnóstica a bibliotecas externas, permitindo que a aplicação seja executada até nos ambientes mais restritos. Protege a aplicação capturando possíveis erros do usuário (`try/except ValueError`) caso letras sejam inseridas no lugar de números em códigos ou quantidades.

### 4.2 Interface Gráfica de Usuário (GUI)
- Encontra-se no arquivo **`gui.py`**.
- Utiliza a biblioteca moderna **`customtkinter`**.
- Adotamos uma arquitetura de visualização baseada em abas (*Tabs*):
  - **Cadastrar Produto:** Formulário com múltiplos campos.
  - **Estoque:** Seção para adicionar ou remover estoque.
  - **Vendas:** Inclusão do campo de desconto e exibição simultânea do recibo formatado na tela em uma grande caixa de texto.
  - **Relatórios:** Uma interface limpa com três botões distintos que jogam as saídas textuais num quadro-branco central.
- **Tratamento Dinâmico de Console:** Uma vez que as classes do sistema (originais e as que criamos) emitem muito texto diretamente no terminal via `print()`, implementamos na GUI um redirecionamento silencioso através de `io.StringIO` junto ao `sys.stdout`. Isso nos permite "capturar" esses prints e injetá-los perfeitamente nos elementos gráficos de texto (`CTkTextbox`), sem a necessidade de reescrever as funções para que retornem *strings*.
