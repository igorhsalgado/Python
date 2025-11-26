import discord
from discord.ext import commands
from datetime import datetime

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

db_moradores = []
db_funcionarios = []
db_acessos = []
db_agendamentos = []
db_veiculos = []

config_espacos = {
    "churrasqueira": {"capacidade": 20, "taxa": 50.00},
    "salao": {"capacidade": 100, "taxa": 200.00}
}

# --- EVENTOS DO BOT ---

@bot.event
async def on_ready():
    print(f'✅ Sistema de Condomínio iniciado como {bot.user}')
    print('------ Bancos de Dados Carregados ------')
    await bot.change_presence(activity=discord.Game(name="!ajuda para comandos"))

# --- COMANDOS DO SISTEMA ---

@bot.command(name="ajuda")
async def ajuda(ctx):
    """Exibe o menu de ajuda com interface visual atualizada."""
    embed = discord.Embed(
        title="🏢 Painel de Controle - Condomínio v1.6",
        description="Sistema Integrado de Gestão, Segurança e Tráfego.",
        color=discord.Color.dark_blue()
    )

    embed.add_field(
        name="👥 Gestão de Pessoas",
        value="`!cadastrar_morador <nome> <cpf> <unidade> <bloco>`\n`!listar_moradores`\n`!registrar_ponto <nome> <setor>`",
        inline=False
    )

    embed.add_field(
        name="🚗 Controle Veicular",
        value="`!cadastrar_veiculo <placa> <cpf_dono> <modelo>`\n`!ler_placa <placa>`\n`!listar_veiculos`",
        inline=False
    )

    embed.add_field(
        name="🛡️ Portaria e Segurança",
        value="`!entrada <visitante> <cpf> <destino>`\n`!alerta <motivo>`",
        inline=False
    )

    embed.add_field(
        name="📅 Outros",
        value="`!agendar <espaco> <data> <cpf>`\n`!relatorio`",
        inline=False
    )

    embed.set_footer(text="Sistema operando em tempo real.")
    await ctx.send(embed=embed)

# 1. Cadastro de Morador (Baseado em Pessoa/Morador)
@bot.command()
async def cadastrar_morador(ctx, nome: str, cpf: str, unidade: str, bloco: str):
    # Verifica se já existe
    for m in db_moradores:
        if m['cpf'] == cpf:
            await ctx.send("❌ Erro: CPF já cadastrado.")
            return

    novo_morador = {
        "nome": nome,
        "cpf": cpf,
        "unidade": unidade,
        "bloco": bloco,
        "tipo": "Proprietario"
    }
    db_moradores.append(novo_morador)

    # Interface Visual de Sucesso
    embed = discord.Embed(title="✅ Morador Cadastrado", color=discord.Color.green())
    embed.add_field(name="Nome", value=nome, inline=True)
    embed.add_field(name="Unidade", value=f"{unidade}-{bloco}", inline=True)
    embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/2558/2558054.png")

    await ctx.send(embed=embed)


# Listar todos os Moradores
@bot.command()
async def listar_moradores(ctx):
    # Verifica se a lista está vazia
    if not db_moradores:
        embed = discord.Embed(title="👥 Lista de Moradores", description="Nenhum morador cadastrado ainda.",
                              color=discord.Color.light_grey())
        await ctx.send(embed=embed)
        return

    # Monta o texto com a lista
    lista_texto = ""
    for m in db_moradores:
        lista_texto += f"• **{m['nome']}** - Apto {m['unidade']} (Bl {m['bloco']})\n"

    # Cria o visual (Embed)
    embed = discord.Embed(title="👥 Moradores do Condomínio", description=lista_texto, color=discord.Color.blue())
    embed.set_footer(text=f"Total: {len(db_moradores)} moradores")

    await ctx.send(embed=embed)


# Registro de Ponto (Baseado em Funcionario)
@bot.command()
async def registrar_ponto(ctx, nome: str, setor: str):
    hora_atual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    # Adiciona ao log geral
    registro = {
        "visitante": f"[FUNC] {nome}",
        "cpf_visitante": "N/A",
        "autorizado_por": f"Setor {setor}",
        "data": hora_atual,
        "tipo": "Ponto Eletrônico"
    }
    db_acessos.append(registro)

    embed = discord.Embed(title="⏰ Ponto Registrado", color=discord.Color.gold())
    embed.description = f"Funcionário **{nome}** ({setor}) registrou ponto."
    embed.set_footer(text=f"Horário: {hora_atual}")

    await ctx.send(embed=embed)


#  Controle de Acesso Inteligente (Unidade OU Espaço Comum)
@bot.command()
async def entrada(ctx, nome_visitante: str, cpf_visitante: str, destino: str):
    # Converte para minúsculo para aceitar "Churrasqueira", "CHURRASQUEIRA", etc.
    destino_tratado = destino.lower()

    morador_responsavel = None

    if destino_tratado in config_espacos:
        # Pega a data de HOJE para ver se tem festa rolando
        data_hoje = datetime.now().strftime("%d/%m/%Y")

        # Procura nos agendamentos: O espaço é esse? A data é hoje?
        reserva_encontrada = next(
            (a for a in db_agendamentos if a['espaco'] == destino_tratado and a['data'] == data_hoje), None)

        if reserva_encontrada:
            # Achamos a reserva! O "dono" da festa é o responsável
            nome_anfitriao = reserva_encontrada['morador']
            # Busca os dados completos desse morador
            morador_responsavel = next((m for m in db_moradores if m['nome'] == nome_anfitriao), None)
        else:
            await ctx.send(
                f"❌ Ninguém reservou o(a) **{destino}** para hoje ({data_hoje}). A entrada não pode ser liberada.")
            return

    # --- LÓGICA 2: O destino é uma Unidade (Apartamento)? ---
    else:
        # Busca morador pelo número da unidade (ex: "101", "200")
        morador_responsavel = next((m for m in db_moradores if m['unidade'] == destino), None)

    # --- VERIFICAÇÃO FINAL ---
    if not morador_responsavel:
        embed = discord.Embed(title="⛔ Acesso Negado",
                              description=f"Destino **{destino}** não encontrado (não é unidade, nem espaço com reserva hoje).",
                              color=discord.Color.red())
        await ctx.send(embed=embed)
        return

    # Registrar o Acesso no Banco de Dados
    hora_atual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    novo_acesso = {
        "visitante": nome_visitante,
        "cpf_visitante": cpf_visitante,
        "autorizado_por": morador_responsavel['nome'],  # Aqui vai o nome de quem reservou ou do dono do apê
        "data": hora_atual,
        "tipo": "Entrada Visitante"
    }
    db_acessos.append(novo_acesso)

    # Resposta Visual Bonita
    embed = discord.Embed(title="🚪 Entrada Liberada", color=discord.Color.green())
    embed.add_field(name="Visitante", value=nome_visitante, inline=True)
    embed.add_field(name="Destino", value=destino.capitalize(), inline=True)
    embed.add_field(name="Autorizado por", value=morador_responsavel['nome'], inline=False)
    embed.set_footer(text=f"Registro: {hora_atual}")

    await ctx.send(embed=embed)


# Agendamento de Espaço Comum (Com bloqueio de datas passadas)
@bot.command()
async def agendar(ctx, espaco: str, data_str: str, cpf_morador: str):
    espaco = espaco.lower()

    # 1. Verificar se o espaço existe
    if espaco not in config_espacos:
        await ctx.send(f"❌ Espaço inválido. Disponíveis: {', '.join(config_espacos.keys())}")
        return

    # 2. Verificar se o morador existe
    morador = next((m for m in db_moradores if m['cpf'] == cpf_morador), None)
    if not morador:
        await ctx.send("❌ CPF não encontrado no sistema.")
        return

    # --- NOVO: Conversão e Verificação de Data ---
    try:
        data_reserva = datetime.strptime(data_str, "%d/%m/%Y")

        # Pega a data de hoje (sem as horas, só dia/mês/ano)
        hoje = datetime.now()

        if data_reserva.date() < hoje.date():
            await ctx.send(f"⚠️ Não é possível agendar para o passado ({data_str}).")
            return

    except ValueError:
        await ctx.send("❌ Formato de data inválido. Use DD/MM/AAAA (Ex: 25/12/2025)")
        return

    # 3. Verificar disponibilidade (Se já tem alguém nesse dia)
    for agenda in db_agendamentos:
        if agenda['espaco'] == espaco and agenda['data'] == data_str:
            await ctx.send(f"⚠️ O espaço **{espaco}** já está reservado para o dia {data_str}.")
            return

    # 4. Confirmar Reserva
    novo_agendamento = {
        "espaco": espaco,
        "morador": morador['nome'],
        "data": data_str,
        "status": "Confirmado",
        "taxa": config_espacos[espaco]['taxa']
    }
    db_agendamentos.append(novo_agendamento)

    embed = discord.Embed(title="🗓️ Reserva Confirmada", color=discord.Color.purple())
    embed.add_field(name="Espaço", value=espaco.capitalize(), inline=True)
    embed.add_field(name="Data", value=data_str, inline=True)
    embed.add_field(name="Morador", value=morador['nome'], inline=False)
    embed.add_field(name="Taxa", value=f"R$ {config_espacos[espaco]['taxa']}", inline=False)

    await ctx.send(embed=embed)


# Relatório Geral (Visualização dos Logs)
@bot.command()
async def relatorio(ctx):
    embed = discord.Embed(title="📊 Relatório do Condomínio", color=discord.Color.dark_grey())

    # Listar últimos 5 acessos
    acessos_str = ""
    if not db_acessos:
        acessos_str = "Nenhum registro recente."
    else:
        for a in db_acessos[-5:]:  # Pega os últimos 5
            acessos_str += f"• {a['data']} - **{a['visitante']}** (Aut: {a['autorizado_por']})\n"

    embed.add_field(name="📜 Últimos Acessos/Pontos", value=acessos_str, inline=False)

    # Listar Agendamentos
    agendas_str = ""
    if not db_agendamentos:
        agendas_str = "Nenhuma reserva futura."
    else:
        for ag in db_agendamentos:
            agendas_str += f"• {ag['data']} - **{ag['espaco'].capitalize()}** ({ag['morador']})\n"

    embed.add_field(name="📅 Próximas Reservas", value=agendas_str, inline=False)

    await ctx.send(embed=embed)


# 7. Cadastro de Veículos (Atualizado para aceitar nomes compostos)
@bot.command()
async def cadastrar_veiculo(ctx, placa: str, cpf_dono: str, *, modelo: str):
    """
    Cadastra um veículo.
    Uso: !cadastrar_veiculo <PLACA> <CPF> <MODELO DO CARRO>
    Ex: !cadastrar_veiculo ABC-1234 123.456.789-00 Fiat Uno Mille
    """
    # 1. Limpeza da placa
    placa_limpa = placa.upper().replace("-", "")

    # 2. Verificar se o morador existe
    dono = next((m for m in db_moradores if m['cpf'] == cpf_dono), None)
    if not dono:
        await ctx.send("❌ CPF do proprietário não encontrado. Verifique se digitou o CPF antes do modelo.")
        return

    # 3. Verificar se a placa já existe
    if any(v['placa'] == placa_limpa for v in db_veiculos):
        await ctx.send("❌ Esta placa já está cadastrada.")
        return

    # 4. Salvar
    novo_veiculo = {
        "placa": placa_limpa,
        "modelo": modelo.title(),
        "dono": dono['nome'],
        "unidade": dono['unidade'],
        "status": "Fora"
    }
    db_veiculos.append(novo_veiculo)

    embed = discord.Embed(title="🚗 Veículo Cadastrado", color=discord.Color.blue())
    embed.add_field(name="Placa", value=placa_limpa, inline=True)
    embed.add_field(name="Proprietário", value=dono['nome'], inline=True)
    embed.add_field(name="Modelo", value=modelo.title(), inline=False)
    embed.set_footer(text="Status inicial: Fora do Condomínio")

    await ctx.send(embed=embed)

# Verificação do estado do veículo (se está ou não no condomínio)
@bot.command()
async def ler_placa(ctx, placa: str):
    """Simula a câmera entrada/saída."""
    placa_limpa = placa.upper().replace("-", "")
    veiculo = next((v for v in db_veiculos if v['placa'] == placa_limpa), None)
    hora_atual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    if veiculo:
        # Verifica o status atual (Se não tiver status, assume que está 'Fora')
        status_atual = veiculo.get("status", "Fora")

        if status_atual == "Fora":
            # --- LÓGICA DE ENTRADA ---
            veiculo['status'] = "Dentro"  # Atualiza status
            tipo_acao = "Entrada Veicular"
            cor_embed = discord.Color.green()
            msg_titulo = "🟢 Entrada Registrada"
            msg_desc = "Bem-vindo de volta!"
        else:
            # --- LÓGICA DE SAÍDA ---
            veiculo['status'] = "Fora"  # Atualiza status
            tipo_acao = "Saída Veicular"
            cor_embed = discord.Color.orange()
            msg_titulo = "🟠 Saída Registrada"
            msg_desc = "Até logo!"

        # Registrar Log
        db_acessos.append({
            "visitante": f"Veículo: {veiculo['modelo']}",
            "cpf_visitante": veiculo['placa'],
            "autorizado_por": "Sistema LPR (Automático)",
            "data": hora_atual,
            "tipo": tipo_acao
        })

        # Visual
        embed = discord.Embed(title=msg_titulo, description=msg_desc, color=cor_embed)
        embed.add_field(name="Veículo", value=f"{veiculo['modelo']} ({veiculo['placa']})", inline=True)
        embed.add_field(name="Morador", value=f"{veiculo['dono']} - Apto {veiculo['unidade']}", inline=False)
        embed.add_field(name="Novo Status", value=f"Agora está: **{veiculo['status'].upper()}**", inline=False)
        embed.set_footer(text=f"Ação: {tipo_acao}")
        await ctx.send(embed=embed)

    else:
        # Acesso Negado (Não muda)
        embed = discord.Embed(title="🔴 Bloqueio de Segurança", color=discord.Color.red())
        embed.description = f"A placa **{placa_limpa}** não consta no sistema."
        await ctx.send(embed=embed)

# Listar todos os Veículos e Status
@bot.command()
async def listar_veiculos(ctx):
    # Verifica se a lista está vazia
    if not db_veiculos:
        embed = discord.Embed(title="🚗 Frota do Condomínio", description="Nenhum veículo cadastrado ainda.",
                              color=discord.Color.light_grey())
        await ctx.send(embed=embed)
        return

    # Monta o texto com a lista
    lista_texto = ""
    for v in db_veiculos:
        # Define o emoji baseado no status
        status_atual = v.get('status', 'Fora')
        emoji_status = "🟢" if status_atual == "Dentro" else "🔴"

        lista_texto += f"{emoji_status} **{v['placa']}** | {v['modelo']}\n"
        lista_texto += f"   └── Dono: {v['dono']} (Apto {v['unidade']})\n\n"

    # Cria o visual (Embed)
    embed = discord.Embed(title="🚗 Controle de Frota", description=lista_texto, color=discord.Color.blue())
    embed.set_footer(text="🟢 = No Condomínio | 🔴 = Na Rua")

    await ctx.send(embed=embed)


# 6. Alerta de Segurança (Tempo Real)
@bot.command()
async def alerta(ctx, *, motivo: str):
    """
    Envia um alerta crítico para o canal.
    Uso: !alerta Fogo no bloco B
    """
    hora_atual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    # 1. Notificação Sonora/Visual (Simulada pelo @here)
    # O @here notifica todos que estão online no momento
    await ctx.send("@here 🚨 **ATENÇÃO: OCORRÊNCIA DE SEGURANÇA REGISTRADA** 🚨")

    # 2. Registro no Banco de Dados (Para auditoria futura)
    novo_log = {
        "visitante": "ALERTA DE SEGURANÇA",
        "cpf_visitante": "N/A",
        "autorizado_por": f"Reportado por: {ctx.author.name}",
        "data": hora_atual,
        "tipo": f"ALERTA: {motivo.upper()}"
    }
    db_acessos.append(novo_log)

    # 3. Interface Visual de Emergência (Vermelho Sangue)
    embed = discord.Embed(
        title="📢 ALERTA EM TEMPO REAL",
        description=f"**Ocorrência:** {motivo.upper()}",
        color=discord.Color.from_rgb(255, 0, 0)  # Vermelho puro
    )
    embed.add_field(name="Reportado por", value=ctx.author.mention, inline=True)
    embed.add_field(name="Horário", value=hora_atual, inline=True)
    embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/564/564619.png")  # Ícone de sirene
    embed.set_footer(text="Equipe de segurança acionada automaticamente.")

    await ctx.send(embed=embed)


# --- EXECUÇÃO ---
# Substitua pelo seu TOKEN
bot.run('SEU_TOKEN_AQUI')