# SafePlant – Recomendações de Plantio e Indicador de Risco por Cultura

Plataforma de inteligência climática agrícola desenvolvida como parte da **Global Solution 2026 – FIAP**.

## Integrantes

| Nome | RM |
|------|----|
| Camila Martins | 561492 |
| Luís Felipe Scacchetti | 562241 |
| Gabriel Amara | 561403 |
| Guilherme Godoy | 564417 |
| Pedro Lucas Almeida | 566256 |

## Sobre o projeto

A SafePlant ajuda produtores rurais a tomarem melhores decisões de plantio com base em previsões climáticas. O sistema cruza o calendário agrícola de cada cultura com dados climáticos simulados da NASA POWER API para recomendar se um período é favorável, neutro ou desfavorável ao plantio, e calcular o nível de risco climático.

## Funcionalidades

- **Recomendações de plantio** nos horizontes de 30, 60 e 90 dias por cultura
- **Indicador de risco climático** (BAIXO / MÉDIO / ALTO) com base na previsão dos próximos 30 dias
- **Gerenciamento de culturas** no perfil do produtor com suporte a UNDO

## Técnicas implementadas

| Técnica | Onde | Complexidade |
|---------|------|-------------|
| Busca binária | `busca_janela_plantio` – localiza a janela de plantio de uma data no calendário ordenado | O(log n) |
| Recursão | `conta_dias_em_risco` – conta recursivamente os dias fora da faixa segura da cultura | O(n) |
| Pilha com UNDO | `perfil_adicionar` / `perfil_remover` / `perfil_undo` – desfaz a última operação no perfil | O(1) push/pop |

## Como executar

```bash
python safeplant.py
```

Não há dependências externas, apenas a biblioteca padrão do Python (`datetime`).

## Culturas disponíveis

- Milho
- Soja
- Feijão
- Trigo
- Café

## Observação sobre os dados climáticos

Os dados de temperatura e precipitação são simulados seguindo as estações do Brasil (Sul/Sudeste). Em produção, seriam obtidos via **NASA POWER API** por coordenada geográfica da propriedade.
