import datetime

CALENDARIOS = {
    "milho": [
        {"inicio": datetime.date(2026, 1, 1), "fim": datetime.date(2026, 2, 28), "tipo": "desfavoravel"},
        {"inicio": datetime.date(2026, 3, 1), "fim": datetime.date(2026, 4, 30), "tipo": "neutro"},
        {"inicio": datetime.date(2026, 5, 1), "fim": datetime.date(2026, 6, 30), "tipo": "desfavoravel"},
        {"inicio": datetime.date(2026, 7, 1), "fim": datetime.date(2026, 8, 31), "tipo": "neutro"},
        {"inicio": datetime.date(2026, 9, 1), "fim": datetime.date(2026, 10, 31), "tipo": "favoravel"},
        {"inicio": datetime.date(2026, 11, 1), "fim": datetime.date(2026, 12, 31), "tipo": "favoravel"},
    ],
    "soja": [
        {"inicio": datetime.date(2026, 1, 1), "fim": datetime.date(2026, 2, 28), "tipo": "neutro"},
        {"inicio": datetime.date(2026, 3, 1), "fim": datetime.date(2026, 5, 31), "tipo": "desfavoravel"},
        {"inicio": datetime.date(2026, 6, 1), "fim": datetime.date(2026, 8, 31), "tipo": "desfavoravel"},
        {"inicio": datetime.date(2026, 9, 1), "fim": datetime.date(2026, 10, 31), "tipo": "favoravel"},
        {"inicio": datetime.date(2026, 11, 1), "fim": datetime.date(2026, 12, 31), "tipo": "favoravel"},
    ],
    "feijao": [
        {"inicio": datetime.date(2026, 1, 1), "fim": datetime.date(2026, 2, 28), "tipo": "favoravel"},
        {"inicio": datetime.date(2026, 3, 1), "fim": datetime.date(2026, 4, 30), "tipo": "neutro"},
        {"inicio": datetime.date(2026, 5, 1), "fim": datetime.date(2026, 7, 31), "tipo": "desfavoravel"},
        {"inicio": datetime.date(2026, 8, 1), "fim": datetime.date(2026, 9, 30), "tipo": "neutro"},
        {"inicio": datetime.date(2026, 10, 1), "fim": datetime.date(2026, 12, 31), "tipo": "favoravel"},
    ],
    "trigo": [
        {"inicio": datetime.date(2026, 1, 1), "fim": datetime.date(2026, 3, 31), "tipo": "desfavoravel"},
        {"inicio": datetime.date(2026, 4, 1), "fim": datetime.date(2026, 5, 31), "tipo": "favoravel"},
        {"inicio": datetime.date(2026, 6, 1), "fim": datetime.date(2026, 7, 31), "tipo": "favoravel"},
        {"inicio": datetime.date(2026, 8, 1), "fim": datetime.date(2026, 9, 30), "tipo": "neutro"},
        {"inicio": datetime.date(2026, 10, 1), "fim": datetime.date(2026, 12, 31), "tipo": "desfavoravel"},
    ],
    "cafe": [
        {"inicio": datetime.date(2026, 1, 1), "fim": datetime.date(2026, 2, 28), "tipo": "neutro"},
        {"inicio": datetime.date(2026, 3, 1), "fim": datetime.date(2026, 5, 31), "tipo": "favoravel"},
        {"inicio": datetime.date(2026, 6, 1), "fim": datetime.date(2026, 8, 31), "tipo": "neutro"},
        {"inicio": datetime.date(2026, 9, 1), "fim": datetime.date(2026, 10, 31), "tipo": "favoravel"},
        {"inicio": datetime.date(2026, 11, 1), "fim": datetime.date(2026, 12, 31), "tipo": "desfavoravel"},
    ],
}

THRESHOLDS = {
    "milho": {"temp_min": 15, "temp_max": 35, "chuva_min": 3, "chuva_max": 30},
    "soja": {"temp_min": 18, "temp_max": 38, "chuva_min": 4, "chuva_max": 25},
    "feijao": {"temp_min": 16, "temp_max": 30, "chuva_min": 2, "chuva_max": 20},
    "trigo": {"temp_min": 5, "temp_max": 25, "chuva_min": 2, "chuva_max": 15},
    "cafe": {"temp_min": 18, "temp_max": 32, "chuva_min": 3, "chuva_max": 20},
}

CULTURAS_DISPONIVEIS = list(CALENDARIOS.keys())

# ──────────────────────────────────────────────────────────
# Previsão climática (simulação da NASA POWER API)
# ──────────────────────────────────────────────────────────
def gera_previsao_nasa():
    """
    Simula dados climáticos para os próximos 90 dias.
    Em produção, viriam da NASA POWER API.

    Complexidade: O(n), onde n = 90 dias.
    """
    previsao = []
    hoje = datetime.date.today()

    for i in range(1, 91):
        data = hoje + datetime.timedelta(days=i)
        mes = data.month

        if mes in [12, 1, 2]:
            temp = 28 + (i % 7)
            chuva = 12 + (i % 15)
        elif mes in [3, 4, 5]:
            temp = 20 + (i % 8)
            chuva = 5 + (i % 8)
        elif mes in [6, 7, 8]:
            temp = 10 + (i % 8)
            chuva = 1 + (i % 4)
        else:
            temp = 22 + (i % 8)
            chuva = 7 + (i % 12)

        previsao.append({"data": data, "temp": temp, "chuva": chuva})

    return previsao

# ──────────────────────────────────────────────────────────
# 1. Busca binária – O(log n)
# ──────────────────────────────────────────────────────────
def busca_janela_plantio(calendario, data_alvo):
    """
    Busca binária que localiza a janela de plantio de uma data.

    Complexidade: O(log n) – descarta metade das janelas a cada iteração.
    """
    inicio = 0
    fim = len(calendario) - 1

    while inicio <= fim:
        meio = (inicio + fim) // 2
        janela = calendario[meio]

        if janela["inicio"] <= data_alvo <= janela["fim"]:
            return janela
        elif data_alvo < janela["inicio"]:
            fim = meio - 1
        else:
            inicio = meio + 1

    if inicio < len(calendario):
        return calendario[inicio]

    return None

# ──────────────────────────────────────────────────────────
# 2. Recursão – O(n)
# ──────────────────────────────────────────────────────────
def conta_dias_em_risco(previsao, threshold):
    """
    Conta recursivamente os dias cujo clima ultrapassa o threshold da cultura.

    Caso base: lista vazia → retorna 0
    Caso recursivo: verifica o primeiro dia e chama com o resto (lista[1:])

    Complexidade: O(n) – cada dia é visitado exatamente uma vez.
    """
    if len(previsao) == 0:
        return 0

    primeiro = previsao[0]
    resto = previsao[1:]

    em_risco = (
        primeiro["temp"] < threshold["temp_min"]  or
        primeiro["temp"] > threshold["temp_max"]  or
        primeiro["chuva"] < threshold["chuva_min"] or
        primeiro["chuva"] > threshold["chuva_max"]
    )

    return (1 if em_risco else 0) + conta_dias_em_risco(resto, threshold)

def calcula_nivel_risco(cultura, previsao, dias):
    """
    Calcula o nível de risco (ALTO / MEDIO / BAIXO) de uma cultura
    para os próximos 'dias' dias usando conta_dias_em_risco.

    Complexidade: O(n), onde n = dias analisados.
    """
    threshold = THRESHOLDS[cultura]
    previsao_recorte = previsao[:dias]
    dias_em_risco = conta_dias_em_risco(previsao_recorte, threshold)
    proporcao = dias_em_risco / dias

    if proporcao >= 0.5:
        return "ALTO"
    elif proporcao >= 0.25:
        return "MEDIO"
    else:
        return "BAIXO"

# ──────────────────────────────────────────────────────────
# 3. Pilha com UNDO – push e pop são O(1)
# ──────────────────────────────────────────────────────────
def cria_perfil():
    """
    Cria o perfil vazio do produtor com lista de culturas e pilha de UNDO.

    Complexidade: O(1)
    """
    return {
        "culturas": [],
        "pilha_undo": []
    }

def perfil_adicionar(perfil, cultura):
    """
    Adiciona cultura ao perfil e empilha a operação inversa para UNDO.

    Complexidade: O(1) – append e push são O(1).
    """
    if cultura in perfil["culturas"]:
        print(f"  '{cultura}' já está no perfil.")
        return

    perfil["pilha_undo"].append(("remover", cultura))
    perfil["culturas"].append(cultura)
    print(f"  ✔ '{cultura}' adicionada ao perfil.")

def perfil_remover(perfil, cultura):
    """
    Remove cultura do perfil e empilha a operação inversa para UNDO.

    Complexidade: O(n) – list.remove percorre a lista.
    """
    if cultura not in perfil["culturas"]:
        print(f"  '{cultura}' não está no perfil.")
        return

    perfil["pilha_undo"].append(("adicionar", cultura))
    perfil["culturas"].remove(cultura)
    print(f"  ✔ '{cultura}' removida do perfil.")

def perfil_undo(perfil):
    """
    Desfaz a última operação executando a operação inversa guardada na pilha.

    Complexidade: O(1) para o pop + O(n) para executar o inverso.
    """
    if len(perfil["pilha_undo"]) == 0:
        print("  Nada para desfazer.")
        return False

    operacao, cultura = perfil["pilha_undo"].pop()

    if operacao == "remover":
        perfil["culturas"].remove(cultura)
        print(f"  ↩ UNDO: '{cultura}' removida do perfil.")
    else:
        perfil["culturas"].append(cultura)
        print(f"  ↩ UNDO: '{cultura}' reinserida no perfil.")

    return True

# ──────────────────────────────────────────────────────────
# Interface
# ──────────────────────────────────────────────────────────
MENU = """
╔══════════════════════════════════════════════════════╗
║          SafePlant – Inteligência Climática          ║
║          Recomendações e Risco por Cultura           ║
╠══════════════════════════════════════════════════════╣
║  1 – Adicionar cultura ao perfil                     ║
║  2 – Remover cultura do perfil                       ║
║  3 – Ver recomendações de plantio (30 / 60 / 90 dias)║
║  4 – Ver indicador de risco por cultura              ║
║  5 – Desfazer última operação (UNDO)                 ║
║  0 – Sair                                            ║
╚══════════════════════════════════════════════════════╝"""

ICONE_TIPO = {
    "favoravel":    "🟢 FAVORÁVEL",
    "neutro":       "🟡 NEUTRO",
    "desfavoravel": "🔴 DESFAVORÁVEL",
}

ICONE_RISCO = {
    "BAIXO": "🟢 BAIXO",
    "MEDIO": "🟡 MÉDIO",
    "ALTO":  "🔴 ALTO",
}

def exibe_culturas_disponiveis():
    print("\n  Culturas disponíveis na SafePlant:")
    for i, c in enumerate(CULTURAS_DISPONIVEIS, 1):
        print(f"    {i}. {c}")

def exibe_recomendacoes(perfil):
    if len(perfil["culturas"]) == 0:
        print("\n  Nenhuma cultura no perfil.")
        return

    hoje = datetime.date.today()
    print(f"\n  {'─'*55}")
    print(f"  Recomendações de Plantio – base: {hoje.strftime('%d/%m/%Y')}")
    print(f"  {'─'*55}")

    for cultura in perfil["culturas"]:
        calendario = CALENDARIOS[cultura]
        print(f"\n  {cultura.upper()}")

        for dias in [30, 60, 90]:
            data_alvo = hoje + datetime.timedelta(days=dias)
            janela    = busca_janela_plantio(calendario, data_alvo)
            situacao  = ICONE_TIPO[janela["tipo"]] if janela else "sem dados"
            print(f"     +{dias: > 2} dias ({data_alvo.strftime('%d/%m/%Y')}) → {situacao}")

    print(f"\n  {'─'*55}")

def exibe_risco(perfil, previsao):
    if len(perfil["culturas"]) == 0:
        print("\n  Nenhuma cultura no perfil.")
        return

    print(f"\n  {'─'*50}")
    print("  Indicador de Risco Climático – próximos 30 dias")
    print(f"  {'─'*50}")

    for cultura in perfil["culturas"]:
        nivel     = calcula_nivel_risco(cultura, previsao, 30)
        threshold = THRESHOLDS[cultura]
        print(f"  {cultura:<10}  {ICONE_RISCO[nivel]}")
        print(f"       Faixa segura: {threshold['temp_min']} – {threshold['temp_max']}°C  |  "
              f"chuva {threshold['chuva_min']} – {threshold['chuva_max']} mm/dia")

    print(f"  {'─'*50}")

def le_cultura(lista):
    """Lê nome ou número de uma cultura e retorna o nome, ou None se inválido."""
    entrada = input("  Nome ou número: ").strip().lower()

    if entrada.isdigit():
        idx = int(entrada) - 1
        if 0 <= idx < len(lista):
            return lista[idx]
        print("  Número fora do intervalo.")
        return None

    return entrada

def main():
    perfil = cria_perfil()
    previsao = gera_previsao_nasa()

    perfil["culturas"] = ["milho", "soja"]
    print("\n  SafePlant iniciado.")
    print(f"  Culturas de demonstração: {perfil['culturas']}")
    print(f"  Previsão: próximos {len(previsao)} dias (NASA POWER API simulada).")

    while True:
        print(MENU)
        opcao = input("  Escolha uma opção: ").strip()

        if opcao == "1":
            exibe_culturas_disponiveis()
            cultura = le_cultura(CULTURAS_DISPONIVEIS)
            if cultura is not None:
                if cultura not in CULTURAS_DISPONIVEIS:
                    print(f"  Cultura '{cultura}' não disponível.")
                else:
                    perfil_adicionar(perfil, cultura)

        elif opcao == "2":
            if len(perfil["culturas"]) == 0:
                print("\n  Nenhuma cultura cadastrada.")
            else:
                print("\n  Culturas no perfil:")
                for i, c in enumerate(perfil["culturas"], 1):
                    print(f"    {i}. {c}")
                cultura = le_cultura(perfil["culturas"])
                if cultura is not None:
                    perfil_remover(perfil, cultura)

        elif opcao == "3":
            exibe_recomendacoes(perfil)

        elif opcao == "4":
            exibe_risco(perfil, previsao)

        elif opcao == "5":
            print(f"\n  Operações para desfazer: {len(perfil['pilha_undo'])}")
            perfil_undo(perfil)
            print(f"  Perfil atual: {perfil['culturas']}")

        elif opcao == "0":
            print("\n  Encerrando SafePlant. Boas colheitas!")
            break

        else:
            print("  Opção inválida.")

main()