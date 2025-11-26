# 📋 Sistema de Organização de Tarefas

> **Disciplina:** Laboratório de Programação I  
> **Tema:** Organização de Tarefas Institucionais

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)

## 📄 Descrição do Projeto

Este programa foi desenvolvido como **Trabalho Final** da disciplina. [cite_start]O objetivo principal é organizar e gerenciar o cumprimento de tarefas institucionais em diferentes setores de uma empresa/organização[cite: 1, 2].

[cite_start]O sistema utiliza conceitos fundamentais de lógica de programação, operando com **matrizes (3x4)** e **vetores unidimensionais fixos** para armazenar o status de realização ("sim"/"não") e os horários das tarefas[cite: 2, 3].

---

## 👥 Integrantes do Grupo

* **Guilherme Cetto**
* **Igor**
* **Isaque**

---

## 🏗️ Estruturas de Dados Utilizadas

[cite_start]O sistema mapeia a relação entre **Setores** (Linhas) e **Tarefas** (Colunas)[cite: 2]:

### 🏢 Vetor de Setores (Linhas)
1. Secretaria Administrativa
2. Atendimento Geral
3. Análise Operacional

### 📝 Vetor de Tarefas (Colunas)
1. Organização de Arquivos
2. Atendimento ao Cliente
3. Análise de Dados
4. Suporte Técnico

### 📊 Matrizes
* **Matriz de Realização (3x4):** Armazena se a tarefa foi feita (`sim` ou `não`).
* [cite_start]**Matriz de Horários (3x4):** Armazena os horários atribuídos para cada tarefa[cite: 3].

---

## ⚙️ Funcionalidades do Menu

[cite_start]O programa conta com um menu interativo com as seguintes opções[cite: 4]:

1.  **📥 Cadastrar dados:** Registra se a tarefa foi realizada e o horário programado.
2.  [cite_start]**📋 Listar dados:** Exibe as matrizes completas (Status e Horários) formatadas[cite: 5].
3.  [cite_start]**🔍 Buscar dados:** Consulta específica informando o nome do setor e da tarefa[cite: 6].
4.  [cite_start]**✏️ Atualizar dados:** Permite alterar manualmente uma célula específica via índices (linha/coluna)[cite: 7].
5.  [cite_start]**📑 Relatório com filtro:** Exibe apenas tarefas com status "sim" ou "não", conforme escolha do usuário[cite: 8].
0.  [cite_start]**❌ Sair:** Encerra a execução[cite: 9].

---

## 🚀 Como Executar

### Pré-requisitos
* Ter o **Python 3** instalado na máquina.

### Passo a Passo
1.  Baixe o arquivo do código fonte (`.py`).
2.  [cite_start]Abra o terminal ou sua IDE de preferência (VSCode, Thonny, IDLE, Pycharm)[cite: 10].
3.  Execute o arquivo.
4.  [cite_start]Siga as instruções do menu interativo no console[cite: 11].

> **Nota:** Ao inserir os dados, certifique-se de usar valores válidos (ex: responder apenas com "sim" ou "não" quando solicitado) para garantir o funcionamento correto do programa.

---

<div align="center">
  <sub>Trabalho Final - Laboratório de Programação I</sub>
</div>