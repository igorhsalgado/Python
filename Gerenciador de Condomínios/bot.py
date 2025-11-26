import discord
from discord.ext import commands
from datetime import datetime

# --- CONFIGURAÇÃO INICIAL ---
# Intents são permissões necessárias para o bot ler mensagens e membros
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

# Armazena dicionários: {'nome': str, 'cpf': str, 'unidade': str, 'bloco': str, 'tipo': str}
db_moradores = []

# Armazena dicionários: {'nome': str, 'cargo': str, 'setor': str}
db_funcionarios = []

# Armazena dicionários: {'visitante': str, 'cpf_visitante': str, 'autorizado_por': str, 'data': str, 'tipo': str}
db_acessos = []

# Armazena dicionários: {'espaco': str, 'morador': str, 'data': str, 'status': str}
db_agendamentos = []

# Configuração fixa dos espaços (UML: EspacoComum)
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
    """Exibe o menu de ajuda com interface visual."""
    embed = discord.Embed(
        title="🏢 Painel de Controle - Condomínio",
        description="Sistema de gestão baseado em comandos. Utilize os prefixos abaixo:",
        color=discord.Color.blue()
    )

    embed.add_field(name="👥 Moradores", value="`!cadastrar_morador <nome> <cpf> <unidade> <bloco>`", inline=False)
    embed.add_field(name="👮 Funcionários", value="`!registrar_ponto <nome_funcionario> <setor>`", inline=False)
    embed.add_field(name="🚧 Portaria/Visitantes", value="`!entrada <visitante> <cpf> <unidade_destino>`", inline=False)
    embed.add_field(name="📅 Reservas", value="`!agendar <espaco> <data dd/mm/aaaa> <cpf_morador>`", inline=False)
    embed.add_field(name="📊 Relatórios", value="`!relatorio` (Ver logs de acesso e reservas)", inline=False)

    embed.set_footer(text="Sistema UML Simplificado v1.0")
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
        "tipo": "Proprietario"  # Padrão
    }
    db_moradores.append(novo_morador)

    # Interface Visual de Sucesso
    embed = discord.Embed(title="✅ Morador Cadastrado", color=discord.Color.green())
    embed.add_field(name="Nome", value=nome, inline=True)
    embed.add_field(name="Unidade", value=f"{unidade}-{bloco}", inline=True)
    embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/2558/2558054.png")

    await ctx.send(embed=embed)


# 2. Registro de Ponto (Baseado em Funcionario)
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


# 3. Controle de Acesso / Visitante (Baseado em Visitante e RegistroAcesso)
@bot.command()
async def entrada(ctx, nome_visitante: str, cpf_visitante: str, unidade_destino: str):
    # Buscar quem está autorizando (o morador da unidade)
    morador_responsavel = None
    for m in db_moradores:
        if m['unidade'] == unidade_destino:
            morador_responsavel = m
            break

    if not morador_responsavel:
        embed = discord.Embed(title="⛔ Acesso Negado",
                              description=f"A unidade **{unidade_destino}** não possui morador cadastrado ou não existe.",
                              color=discord.Color.red())
        await ctx.send(embed=embed)
        return

    # Registrar Acesso
    hora_atual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    novo_acesso = {
        "visitante": nome_visitante,
        "cpf_visitante": cpf_visitante,
        "autorizado_por": morador_responsavel['nome'],
        "data": hora_atual,
        "tipo": "Entrada Visitante"
    }
    db_acessos.append(novo_acesso)

    # Interface Visual
    embed = discord.Embed(title="🚪 Entrada Liberada", color=discord.Color.green())
    embed.add_field(name="Visitante", value=nome_visitante, inline=True)
    embed.add_field(name="Destino", value=f"Apto {unidade_destino}", inline=True)
    embed.add_field(name="Autorizado por", value=morador_responsavel['nome'], inline=False)
    embed.set_footer(text=f"Registro: {hora_atual}")

    await ctx.send(embed=embed)


# 4. Agendamento de Espaço Comum (Baseado em Agendamento e EspacoComum)
@bot.command()
async def agendar(ctx, espaco: str, data: str, cpf_morador: str):
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

    # 3. Verificar disponibilidade (UML: verificar_disponibilidade)
    for agenda in db_agendamentos:
        if agenda['espaco'] == espaco and agenda['data'] == data:
            await ctx.send(f"⚠️ O espaço **{espaco}** já está reservado para o dia {data}.")
            return

    # 4. Confirmar Reserva
    novo_agendamento = {
        "espaco": espaco,
        "morador": morador['nome'],
        "data": data,
        "status": "Confirmado",
        "taxa": config_espacos[espaco]['taxa']
    }
    db_agendamentos.append(novo_agendamento)

    embed = discord.Embed(title="🗓️ Reserva Confirmada", color=discord.Color.purple())
    embed.add_field(name="Espaço", value=espaco.capitalize(), inline=True)
    embed.add_field(name="Data", value=data, inline=True)
    embed.add_field(name="Morador", value=morador['nome'], inline=False)
    embed.add_field(name="Taxa", value=f"R$ {config_espacos[espaco]['taxa']}", inline=False)

    await ctx.send(embed=embed)


# 5. Relatório Geral (Visualização dos Logs)
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


# --- EXECUÇÃO ---
# Substitua pelo seu TOKEN

bot.run('SEU_TOKEN_AQUI')
