# 🏢 Sistema de Gestão de Condomínio via Discord Bot

> **Status do Projeto:** 🚀 Em desenvolvimento (MVP Funcional)

Este projeto consiste em um **Bot para Discord** desenvolvido em **Python**, focado na gestão simplificada de um condomínio. A arquitetura do sistema foi baseada fielmente em um **Diagrama de Classes UML** (se encontra no final do arquivo), traduzindo conceitos de Orientação a Objetos para uma aplicação prática e interativa.

O objetivo é permitir que porteiros e administradores realizem cadastros, controlem acessos e gerenciem reservas de áreas comuns diretamente pela interface de chat do Discord.

## 🛠 Tecnologias Utilizadas

* **Linguagem:** Python 3.x
* **Biblioteca Principal:** `discord.py` (Interação com a API do Discord)
* **Paradigma:** Programação Assíncrona (`asyncio`) e Estruturas de Dados em Memória.

## 📂 Estrutura e Explicação do Código

O código foi construído em um **arquivo único** (`main.py`) para facilitar a implementação e testes rápidos, seguindo uma lógica funcional que espelha as classes do diagrama UML original. Abaixo, o detalhamento de cada seção do código:

### 1. Importações e Configuração
```python
import discord
from discord.ext import commands
from datetime import datetime
```
- `discord / commands`: Núcleo da aplicação. Permite a conexão com o Gateway do Discord, leitura de eventos e criação de comandos personalizados.

- `datetime`: Essencial para registrar logs de acesso e validar datas de reservas, conforme solicitado no UML (`data_hora: datetime`).

- **Intents**: Configuração de permissões (`message_content`, `members`) para que o bot possa ler as mensagens dos usuários.

### 2. Persistência de Dados (Simulação de Banco)

Para este MVP, utilizamos listas de dicionários para armazenar os dados em tempo de execução, substituindo as tabelas de um banco de dados relacional:

- `db_moradores`: Armazena nome, CPF, unidade e bloco.

- `db_acessos`: Log histórico de entradas e saídas (Visitantes e Funcionários).

- `db_agendamentos`: Controle de reservas de espaços comuns.

- `config_espacos`: Dicionário de configuração contendo capacidade e taxas dos espaços (Churrasqueira, Salão).

### 3. Funcionalidades e Comandos

O bot opera através de comandos com o prefixo !. Cada comando implementa uma regra de negócio do diagrama UML:

👥 Cadastro de Moradores (`!cadastrar_morador`)

- Lógica: Recebe os dados do morador e valida se o CPF já existe na lista `db_moradores` antes de inserir.

- Retorno: Feedback visual (Embed verde) confirmando o cadastro.

🚧 Controle de Acesso (`!entrada` e `!registrar_ponto`)

- Visitantes (`!entrada`): Implementa a associação do UML entre Visitante e Morador. O sistema verifica se a "unidade destino" possui um morador responsável para autorizar a entrada.

- Funcionários (`!registrar_ponto`): Registra o horário e o setor do funcionário, gerando um log de auditoria.

📅 Reservas e Agendamentos (`!agendar`)

- Regra de Negócio: Verifica a disponibilidade do espaço (método `verificar_disponibilidade`). O sistema impede que duas pessoas reservem o mesmo espaço na mesma data.

- Cálculo: Retorna automaticamente o valor da taxa baseado na configuração do espaço.

📊 Relatórios (`!relatorio`)

- Gera um painel visual listando os últimos acessos registrados na portaria e as próximas reservas confirmadas, permitindo uma visão geral rápida para a administração.

## 🚀 Como Executar o Projeto

Pré-requisitos

- Python 3.8 ou superior instalado.

- Conta no Discord Developer Portal (para obter o Token).

### Passo a Passo

1. Clone o repositório:

    ```bash 
    git clone [https://github.com/SEU-USUARIO/NOME-DO-REPO.git](https://github.com/SEU-USUARIO/NOME-DO-REPO.git)
    cd NOME-DO-REPO

2. Instale as dependências:

   ```bash
   pip install discord.py
   ```
3. Configuração do Token:

- Abra o arquivo `main.py`.

- Insira seu Token do Discord na última linha: `bot.run('SEU_TOKEN_AQUI')`.

4. Execute o bot:

    ```bash
    python main.py
    ```

## 📸 Exemplo de Uso

Comando: `!entrada "Ana Silva" "123.456.789-00" "101"`

Resposta do Bot:

🚪 Entrada Liberada

- Visitante: Ana Silva

- Destino: Apto 101

- Autorizado por: Carlos (Proprietário)

- Registro: 26/11/2025 14:30:00

## 🔮 Melhorias Futuras

[ ] Implementação de banco de dados SQLite/PostgreSQL para persistência real dos dados.

[ ] Criação de cargos automáticos no Discord para Moradores verificados.

[ ] Sistema de notificação via DM para o morador quando um visitante chegar.

## UML
<img width="3335" height="1364" alt="Image" src="https://github.com/user-attachments/assets/db0acfce-daac-4fcb-88f1-f80ce74e70a0" />

## 👨‍💻 Autor
Igor Hermann Salgado



