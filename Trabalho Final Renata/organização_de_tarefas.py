import os

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

setores = ["Secretaria Administrativa", "Atendimento Geral", "Análise Operacional"]
tarefas = ["Organização Arquivos", "Atendimento ao Cliente", "Análise de Dados", "Suporte Técnico"]

matriz_tarefas = [["" for _ in range(len(tarefas))] for _ in range(len(setores))]
matriz_horarios = [["" for _ in range(len(tarefas))] for _ in range(len(setores))]

opcao = -1
while opcao != 0:
    limpar_tela()
    print("\n========== MENU PRINCIPAL ==========")
    print("1 - Cadastrar Dados")
    print("2 - Listar Dados")
    print("3 - Buscar Dados")
    print("4 - Atualizar Dados")
    print("5 - Relatório Filtrado")
    print("0 - Sair")
    print("====================================")

    try:
        opcao = int(input("Escolha uma opção: "))
    except ValueError:
        print("Opção inválida. Por favor, digite um número.")
        input("\nPressione Enter para continuar...")
        continue

    if opcao == 1:
        limpar_tela()
        print("--- CADASTRO DE TAREFAS ---\n")
        for i in range(len(setores)):
            print(f"Setor: {setores[i]}")
            for j in range(len(tarefas)):
                resposta = ""
                while resposta not in ["sim", "não"]:
                    resposta = input(f"  -> A tarefa '{tarefas[j]}' foi realizada? (sim/não): ").strip().lower()
                    if resposta not in ["sim", "não"]:
                        print("   ** Valor inválido! Por favor, digite 'sim' ou 'não'. **")
                
                matriz_tarefas[i][j] = resposta
                
                if resposta == "sim":
                    horario = input(f"     Horário da tarefa '{tarefas[j]}': ").strip()
                    matriz_horarios[i][j] = horario
                else:
                    matriz_horarios[i][j] = "N/A"
            print("-" * 30)
        input("\nDados cadastrados com sucesso! Pressione Enter para voltar ao menu...")

    elif opcao == 2:
        limpar_tela()
        print("--- VISUALIZAÇÃO DE DADOS ---\n")
        
        largura_setor = max(len(s) for s in setores)
        largura_coluna_tarefa = max(max(len(t) for t in tarefas), 10) + 4

        print("--- MATRIZ DE TAREFAS ---")
        print(f"{'Setor':<{largura_setor}} |", end="")
        for t in tarefas:
            print(f"{t:^{largura_coluna_tarefa}}", end="|")
        print("\n" + "-" * (largura_setor + 1) + ("-" * (largura_coluna_tarefa + 1)) * len(tarefas))
        
        for i in range(len(setores)):
            print(f"{setores[i]:<{largura_setor}} |", end="")
            for j in range(len(tarefas)):
                print(f"{matriz_tarefas[i][j]:^{largura_coluna_tarefa}}", end="|")
            print()

        print("\n--- MATRIZ DE HORÁRIOS ---")
        print(f"{'Setor':<{largura_setor}} |", end="")
        for t in tarefas:
            print(f"{t:^{largura_coluna_tarefa}}", end="|")
        print("\n" + "-" * (largura_setor + 1) + ("-" * (largura_coluna_tarefa + 1)) * len(tarefas))

        for i in range(len(setores)):
            print(f"{setores[i]:<{largura_setor}} |", end="")
            for j in range(len(tarefas)):
                print(f"{matriz_horarios[i][j]:^{largura_coluna_tarefa}}", end="|")
            print()

        input("\n\nPressione Enter para voltar ao menu...")

    elif opcao == 3:
        limpar_tela()
        print("--- BUSCAR DADOS ESPECÍFICOS ---\n")
        print("Setores disponíveis:", ", ".join(setores))
        setor_busca = input("Digite o nome do setor: ").strip()
        
        print("\nTarefas disponíveis:", ", ".join(tarefas))
        tarefa_busca = input("Digite o nome da tarefa: ").strip()

        if setor_busca in setores and tarefa_busca in tarefas:
            i = setores.index(setor_busca)
            j = tarefas.index(tarefa_busca)
            print("\n--- Resultado da Busca ---")
            print(f"Setor: {setores[i]}")
            print(f"Tarefa: {tarefas[j]}")
            print(f"Realizada: {matriz_tarefas[i][j]}")
            print(f"Horário: {matriz_horarios[i][j]}")
        else:
            print("\nSetor ou tarefa não encontrado.")
        input("\n\nPressione Enter para voltar ao menu...")

    elif opcao == 4:
        limpar_tela()
        print("--- ATUALIZAR DADOS ---\n")
        print("Setores:")
        for idx, setor in enumerate(setores):
            print(f"  {idx} - {setor}")
        try:
            i = int(input("Digite o NÚMERO da linha (setor) para atualizar: "))

            print("\nTarefas:")
            for idx, tarefa in enumerate(tarefas):
                print(f"  {idx} - {tarefa}")
            j = int(input("Digite o NÚMERO da coluna (tarefa) para atualizar: "))

            if 0 <= i < len(setores) and 0 <= j < len(tarefas):
                print(f"\nAtualizando dados para '{setores[i]}' -> '{tarefas[j]}'")
                print(f"Valor atual: {matriz_tarefas[i][j]}, Horário atual: {matriz_horarios[i][j]}")
                
                nova_tarefa = ""
                while nova_tarefa not in ["sim", "não"]:
                    nova_tarefa = input("Novo status (sim/não): ").strip().lower()
                    if nova_tarefa not in ["sim", "não"]:
                        print("   ** Valor inválido! Por favor, digite 'sim' ou 'não'. **")

                matriz_tarefas[i][j] = nova_tarefa
                
                if nova_tarefa == "sim":
                    novo_horario = input("Novo horário: ").strip()
                    matriz_horarios[i][j] = novo_horario
                else:
                    matriz_horarios[i][j] = "N/A"
                print("\nDados atualizados com sucesso!")
            else:
                print("\nÍndice fora do intervalo válido.")
        except ValueError:
            print("\nEntrada inválida. Por favor, digite um número de índice.")

        input("\n\nPressione Enter para voltar ao menu...")

    elif opcao == 5:
        limpar_tela()
        print("--- RELATÓRIO FILTRADO ---\n")
        filtro = ""
        while filtro not in ["sim", "não"]:
            filtro = input("Exibir tarefas com qual status? (sim/não): ").strip().lower()
            if filtro not in ["sim", "não"]:
                print("   ** Valor inválido! Por favor, digite 'sim' ou 'não'. **")

        print(f"\n--- Relatório de tarefas com status '{filtro}' ---")
        encontrou_registro = False
        for i in range(len(setores)):
            for j in range(len(tarefas)):
                if matriz_tarefas[i][j] == filtro:
                    print(f"- Setor: {setores[i]}, Tarefa: {tarefas[j]}, Horário: {matriz_horarios[i][j]}")
                    encontrou_registro = True
        
        if not encontrou_registro:
            print(f"Nenhuma tarefa encontrada com o status '{filtro}'.")

        input("\n\nPressione Enter para voltar ao menu...")

    elif opcao == 0:
        limpar_tela()
        print("Encerrando o programa... Até logo!")
        print("Programa feito por: Igor, Guilherme e Isaque.")
    
    else:
        if opcao != -1:
            print("Opção inválida. Tente novamente.")
            input("\nPressione Enter para continuar...")