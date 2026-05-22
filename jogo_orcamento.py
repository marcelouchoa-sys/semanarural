import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import json, os



ARQUIVO_DADOS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dados_orcamento.json")

st.set_page_config(page_title="🏛️ Eu Sou o Governo!", page_icon="🏛️",
                   layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fredoka+One&family=Nunito:wght@400;600;700;800&display=swap');

/* ── TEMA DARK NAVY GLOBAL ── */
html, body {
    background-color:#0d1b2a !important;
    overflow-x:hidden !important;
}
[class*="css"], [data-testid="stAppViewContainer"],
[data-testid="stMain"], .main {
    font-family:'Nunito',sans-serif !important;
    background-color:#0d1b2a !important;
    color:#e2e8f0 !important;
    max-width:100% !important;
    overflow-x:hidden !important;
}
.block-container {
    background-color:#0d1b2a !important;
    max-width:900px !important;
    padding:1rem 1rem 5rem !important;
    margin:0 auto !important;
}
@media(max-width:640px){
    .block-container{padding:.5rem .5rem 4rem !important;}
}
[data-testid="stSidebar"] { background:#0a1628 !important; }
[data-testid="stHeader"]  { background:#0d1b2a !important; border-bottom:1px solid rgba(255,255,255,.06); }

/* scrollbar */
::-webkit-scrollbar{width:6px;height:6px;}
::-webkit-scrollbar-track{background:#0d1b2a;}
::-webkit-scrollbar-thumb{background:#334155;border-radius:3px;}
/* smooth scroll on mobile */
html{scroll-behavior:smooth;-webkit-overflow-scrolling:touch;}

h1,h2,h3{font-family:'Fredoka One',cursive!important;color:#f1f5f9!important;}

/* Título arco-íris */
.titulo-jogo{
  font-family:'Fredoka One',cursive;font-size:2.6rem;text-align:center;
  background:linear-gradient(90deg,#e8315b,#f97316,#eab308,#22c55e,#3b82f6,#8b5cf6);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;margin-bottom:0;
}
.subtitulo{text-align:center;font-size:1.05rem;color:#94a3b8;font-weight:700;margin-top:0;}

/* Chips de alerta */
.chip-verde{background:rgba(34,197,94,.15);border:1.5px solid #22c55e;border-radius:12px;
            padding:.7rem 1rem;color:#4ade80;font-weight:700;margin:.3rem 0;}
.chip-ambar{background:rgba(251,191,36,.12);border:1.5px solid #fbbf24;border-radius:12px;
            padding:.7rem 1rem;color:#fbbf24;font-weight:700;margin:.3rem 0;}
.chip-verm{background:rgba(239,68,68,.12);border:1.5px solid #ef4444;border-radius:12px;
           padding:.7rem 1rem;color:#f87171;font-weight:700;margin:.3rem 0;}

/* Inputs e selects */
[data-testid="stTextInput"] input,
[data-testid="stNumberInput"] input,
[data-testid="stSelectbox"] select,
div[data-baseweb="select"] > div {
    background:#1e293b !important;
    border:1.5px solid #334155 !important;
    border-radius:10px !important;
    color:#e2e8f0 !important;
}
[data-testid="stTextInput"] label,
[data-testid="stNumberInput"] label,
[data-testid="stSelectbox"] label,
[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] li { color:#cbd5e1 !important; }

/* Tabs */
[data-testid="stTabs"] [data-baseweb="tab-list"] {
    background:#1e293b !important; border-radius:12px; padding:4px;
    border:1px solid #334155;
}
[data-testid="stTabs"] [data-baseweb="tab"] {
    background:transparent !important; color:#94a3b8 !important;
    font-family:'Fredoka One',cursive; font-size:.95rem; border-radius:8px;
}
[data-testid="stTabs"] [aria-selected="true"] {
    background:linear-gradient(135deg,#3b82f6,#2563eb) !important;
    color:white !important;
}
[data-testid="stTabs"] [data-baseweb="tab-panel"] {
    background:#0d1b2a !important; padding-top:1rem;
}

/* Dataframe */
[data-testid="stDataFrame"] { background:#1e293b !important; border-radius:12px; }

/* Divisor */
hr { border-color:#1e293b !important; }

/* Botões Streamlit */
.stButton>button {
    font-family:'Fredoka One',cursive !important;
    font-size:1.05rem !important;
    border-radius:12px !important;
    padding:.6rem 1.5rem !important;
    border:none !important;
    transition:all .2s !important;
    background:linear-gradient(135deg,#3b82f6,#2563eb) !important;
    color:white !important;
    box-shadow:0 4px 16px rgba(59,130,246,.3) !important;
}
.stButton>button:hover { transform:translateY(-2px) scale(1.02) !important;
    box-shadow:0 8px 24px rgba(59,130,246,.45) !important; }

/* Métricas */
div[data-testid="metric-container"] {
    background:#1e293b !important; border-radius:14px;padding:1rem;
    border:1px solid #334155; box-shadow:0 4px 16px rgba(0,0,0,.3);
}
div[data-testid="metric-container"] label,
div[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color:#e2e8f0 !important;
}

/* Warnings / info */
[data-testid="stAlert"] {
    background:#1e293b !important; border-radius:12px;
    border:1px solid #334155 !important; color:#e2e8f0 !important;
}
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# TOTAL: 10 cartões
# Cada setor tem uma escala de 0 a 4+ cartões com efeitos não-lineares
# Referência: LOA 2025 + COFOG 2024 (proporções reais do Brasil)
# ═══════════════════════════════════════════════════════════════
TOTAL_CARTOES = 5

# real_pct: distribuição real do Brasil (em % dos 10 cartões)
# Nível de serviço por quantidade de cartões: 0=colapso, 1=sobrevivendo, 2=funcionando, 3=ideal, 4+=excesso
GASTOS = {
    "🏫 Educação": {
        "cor": "#3b82f6",
        "descricao": "Escolas, professores, bolsas e livros",
        "real_pct": 13,
        "crise_emoji": "📚❌", "crise_msg": "Escolas fechando por falta de verba!",
        "niveis": {
            0: ("💀 Colapso total",      "#7f1d1d",
                "Zero investimento em educação. Para Kalecki, isso é catastrófico: sem qualificação, os trabalhadores ficam presos em empregos de baixíssima remuneração, o consumo popular desaba e a economia entra em estagnação permanente. Não há crescimento sustentável possível sem base educacional."),
            1: ("🔴 Crise grave",         "#ef4444",
                "Um cartão apenas — o sistema sobrevive no limite. Kalecki diria que esse gasto mínimo não move o multiplicador educacional: professores mal pagos, evasão escolar alta, sem materiais. A economia não consegue absorver tecnologia nem ampliar produtividade."),
            2: ("🟡 Funcionando precariamente", "#f59e0b",
                "Dois cartões: dá pra manter as portas abertas, mas com qualidade baixa. Para Kalecki, é o ponto onde o gasto público começa a ter algum efeito de multiplicação — salários de professores entram no consumo local — mas ainda insuficiente para reduzir desigualdade."),
            3: ("🟢 Funcionamento ideal",  "#22c55e",
                "Três cartões: o ponto ótimo kaleckiano. O gasto em educação aqui maximiza o multiplicador: cada real investido gera mais de um real de renda na economia, via salários de professores, fornecedores de material, construção de escolas. A desigualdade começa a cair de forma consistente."),
            4: ("🔵 Excesso relativo",     "#3b82f6",
                "Quatro ou mais cartões em educação: bom, mas com retornos decrescentes no curto prazo. Kalecki alertaria que esse recurso extra poderia ser redistributivo em outras frentes — o excesso aqui significa falta em saúde ou transferência de renda, que têm impacto imediato sobre a demanda agregada."),
        },
    },
    "🏥 Saúde": {
        "cor": "#ef4444",
        "descricao": "Hospitais, médicos, remédios e UBSs",
        "real_pct": 14,
        "crise_emoji": "🏥❌", "crise_msg": "Filas imensas, hospitais lotados!",
        "niveis": {
            0: ("💀 Colapso total",      "#7f1d1d",
                "Sem saúde pública, trabalhadores doentes não produzem e morrem cedo. Kalecki seria direto: saúde é o gasto que preserva a força de trabalho — base de toda produção capitalista. Sem ela, até os lucros empresariais despencam. É o pior cenário para qualquer economia."),
            1: ("🔴 Emergências apenas",  "#ef4444",
                "Um cartão: só atendimento de emergência. Kalecki destacava que saúde preventiva evita gastos maiores depois — o custo de não investir se multiplica. Com apenas emergências, a população trabalha doente, a produtividade cai e o consumo doméstico encolhe."),
            2: ("🟡 Sistema sob pressão", "#f59e0b",
                "Dois cartões: o sistema funciona, mas na corda bamba. Filas longas, falta de remédios. Para Kalecki, é insuficiente: os trabalhadores de baixa renda — que dependem do SUS — continuam vulneráveis, o que mantém alta a desigualdade e baixo o consumo popular."),
            3: ("🟢 SUS funcionando",     "#22c55e",
                "Três cartões: o ponto ótimo. Kalecki via a saúde pública como redistribuição disfarçada: as famílias pobres não precisam gastar com plano privado e médicos, liberando renda para consumo de outros bens. Isso aquece a demanda agregada e reduz a desigualdade diretamente."),
            4: ("🔵 Excesso relativo",    "#3b82f6",
                "Quatro ou mais: retornos decrescentes. O sistema já está bem servido — mais cartões aqui melhoram pouco a saúde mas poderiam ampliar muito o consumo popular se fossem para transferência de renda. Kalecki preferiria redistribuir esse excesso."),
        },
    },
    "🏠 Habitação": {
        "cor": "#f97316",
        "descricao": "Moradia popular e urbanização",
        "real_pct": 5,
        "crise_emoji": "🏚️❌", "crise_msg": "Favelas crescendo, sem moradia digna!",
        "niveis": {
            0: ("💀 Sem moradia popular", "#7f1d1d",
                "Zero em habitação. Kalecki adorava obras públicas: construção civil é o setor que mais emprega trabalhadores sem qualificação avançada — pedreiros, carpinteiros, eletricistas. Sem esse investimento, o desemprego de base explode e o consumo popular despenca."),
            1: ("🔴 Insuficiente",        "#ef4444",
                "Um cartão: programas mínimos, sem escala. O efeito kaleckiano de multiplicação — cada obra pública contrata trabalhadores que consomem localmente — não se realiza. A especulação imobiliária domina e a população de baixa renda paga aluguel caro, reduzindo consumo de outros bens."),
            2: ("🟡 Programas básicos",   "#f59e0b",
                "Dois cartões: começa a funcionar. Kalecki diria que aqui o multiplicador da construção civil já aparece: salários de trabalhadores da obra entram no comércio local, o consumo aquece, e famílias realocadas de favelas passam a gastar melhor sua renda."),
            3: ("🟢 Programa robusto",    "#22c55e",
                "Três cartões: o ideal. Kalecki via grandes programas habitacionais como política anticíclica perfeita — em crises, o governo constrói casas, gera emprego de base e sustenta a demanda. Reduz desigualdade, libera renda das famílias e aquece cadeias produtivas inteiras."),
            4: ("🔵 Excesso relativo",    "#3b82f6",
                "Quatro ou mais: habitação já resolvida — mais cartões aqui têm retorno marginal baixo. Kalecki sugeriria redirecionar para transferência de renda, que tem efeito imediato e mais direto sobre o consumo popular."),
        },
    },
    "🎭 Cultura": {
        "cor": "#ec4899",
        "descricao": "Museus, teatro, esporte e lazer",
        "real_pct": 1,
        "crise_emoji": "🎭❌", "crise_msg": "Museus e teatros fechando!",
        "niveis": {
            0: ("💀 Cultura zerada",      "#7f1d1d",
                "Sem cultura pública, o lazer vira mercadoria cara e exclusiva. Para Kalecki, isso aumenta a desigualdade de bem-estar: ricos frequentam espetáculos privados, trabalhadores não têm acesso a nada. A coesão social se fragiliza e a qualidade de vida dos mais pobres piora muito."),
            1: ("🔴 Só o básico",         "#ef4444",
                "Um cartão: sobrevivência mínima — alguns eventos públicos, praças. Kalecki veria esse gasto como semente: pequeno, mas os salários de artistas, técnicos e gestores culturais entram no consumo local. O multiplicador cultural é real, mesmo que menor que educação e saúde."),
            2: ("🟡 Razoável",            "#f59e0b",
                "Dois cartões: programas regulares, equipamentos culturais abertos. Para Kalecki, cultura é consumo popular democratizado — quando o Estado fornece lazer gratuito ou barato, as famílias pobres têm mais dinheiro livre para outras necessidades."),
            3: ("🟢 Boa oferta cultural", "#22c55e",
                "Três cartões: cultura acessível e diversificada. Kalecki diria que aqui o gasto público em cultura começa a ter efeito de identidade e coesão social — além do multiplicador econômico. Trabalhadores mais satisfeitos são mais produtivos e consomem mais."),
            4: ("🔵 Excesso relativo",    "#3b82f6",
                "Quatro ou mais em cultura com 10 cartões totais é muito. Kalecki priorizaria isso apenas após resolver saúde, educação e transferência de renda — esses têm multiplicadores maiores e impacto imediato sobre desigualdade."),
        },
    },
    "🛡️ Segurança e Defesa": {
        "cor": "#8b5cf6",
        "descricao": "Polícia, bombeiros e forças armadas",
        "real_pct": 9,
        "crise_emoji": "🚨❌", "crise_msg": "Violência sem controle!",
        "niveis": {
            0: ("💀 Caos e violência",    "#7f1d1d",
                "Sem segurança, a economia paralisa. Kalecki reconhecia que ordem pública é pré-condição para qualquer atividade econômica — empresas não investem, trabalhadores não se deslocam, comércio fecha cedo. O custo econômico da violência recai desproporcionalmente sobre os mais pobres."),
            1: ("🔴 Segurança precária",  "#ef4444",
                "Um cartão: força policial mínima. Kalecki era crítico do excesso de gasto em segurança, mas reconhecia o mínimo necessário. Com apenas isso, a violência ainda é alta e afeta o consumo: as famílias pobres, que moram nas áreas mais vulneráveis, são as mais prejudicadas."),
            2: ("🟡 Controle básico",     "#f59e0b",
                "Dois cartões: segurança funcionando. Para Kalecki, esse é o nível adequado — o Estado garante a ordem sem desperdiçar recursos que poderiam ir para saúde, educação ou transferência de renda, que têm multiplicadores sociais muito maiores."),
            3: ("🟢 Segurança adequada",  "#22c55e",
                "Três cartões: segurança bem estruturada. Kalecki aceitaria esse nível, mas alertaria: segurança não reduz desigualdade por si só — ela apenas protege o que existe. O investimento social em educação e renda é que ataca as causas da violência, não o policiamento."),
            4: ("🔵 Excesso — risco autoritário", "#8b5cf6",
                "Quatro ou mais em segurança e defesa é o ponto de alerta kaleckiano: gasto militar/policial excessivo não gera consumo popular, não reduz desigualdade e pode comprimir liberdades. Para Kalecki, isso representa transferência de recursos dos trabalhadores para setores que não os beneficiam."),
        },
    },
    "🤝 Transferência de Renda": {
        "cor": "#22c55e",
        "descricao": "Bolsa Família, Pé-de-Meia, BPC",
        "real_pct": 17,
        "crise_emoji": "😢❌", "crise_msg": "Fome e pobreza extrema!",
        "niveis": {
            0: ("💀 Pobreza extrema",     "#7f1d1d",
                "Zero em transferência de renda. Kalecki era contundente: sem renda nas mãos de quem mais precisa, o consumo popular colapsa. A demanda agregada cai, empresas vendem menos, demitem mais — uma espiral recessiva que afeta toda a economia, não só os pobres."),
            1: ("🔴 Alcance mínimo",      "#ef4444",
                "Um cartão: atinge só as famílias em extrema miséria. Para Kalecki, é insuficiente: famílias pobres têm propensão a consumir quase 100% da renda que recebem — cada real de transferência vira consumo imediato. Com pouco, o efeito multiplicador não se realiza em escala."),
            2: ("🟡 Redução parcial",     "#f59e0b",
                "Dois cartões: melhora, mas ainda limitado. Kalecki diria que aqui o consumo popular começa a responder: mais famílias comprando no comércio local, mais demanda por bens básicos. O multiplicador kaleckiano da transferência de renda começa a aparecer na economia."),
            3: ("🟢 Programa efetivo",    "#22c55e",
                "Três cartões: o ideal kaleckiano por excelência. Transferência de renda é o gasto com maior propensão a virar consumo imediato — quem recebe Bolsa Família gasta tudo no comércio local. Kalecki diria que esse é o multiplicador mais poderoso para aquecer a demanda e reduzir desigualdade."),
            4: ("🔵 Alto impacto",        "#10b981",
                "Quatro ou mais: impacto muito positivo. Kalecki apoiaria — transferência de renda tem o maior multiplicador de curto prazo. A única ressalva é equilibrar com saúde e educação, que garantem os multiplicadores de longo prazo. Mas em contexto de crise, mais transferência é sempre bem-vindo."),
        },
    },
    "💰 Serviço da Dívida": {
        "cor": "#6b7280",
        "descricao": "Juros e pagamento de dívidas do governo",
        "real_pct": 41,
        "crise_emoji": "📉❌", "crise_msg": "Calote — governo sem crédito!",
        "niveis": {
            0: ("🔴 Calote",              "#ef4444",
                "Zero na dívida significa calote. Kalecki reconhecia que algum pagamento é necessário para manter o crédito do Estado — sem isso, o governo perde capacidade de financiar seus gastos futuros. Mas ele também dizia: a dívida pública é riqueza dos credores, não uma obrigação sagrada."),
            1: ("🟡 Pagamento mínimo",    "#f59e0b",
                "Um cartão: só os juros mínimos. Para Kalecki, esse é um bom sinal — significa que o governo priorizou saúde, educação e renda em vez de remunerar rentistas. A dívida pública, para Kalecki, é sobretudo um mecanismo de transferência de renda dos trabalhadores para os mais ricos."),
            2: ("🟢 Equilíbrio",          "#22c55e",
                "Dois cartões: pagamento razoável que mantém a credibilidade fiscal sem sacrificar o social. Kalecki diria que esse é o ponto de equilíbrio — honrar compromissos sem transformar o orçamento num veículo de enriquecimento de credores às custas dos serviços públicos."),
            3: ("🟡 Acima do necessário", "#f59e0b",
                "Três cartões: já está acima do ideal kaleckiano. Cada cartão a mais aqui é um cartão a menos em saúde ou transferência de renda. Para Kalecki, isso representa uma escolha política de favorecer rentistas em detrimento dos trabalhadores — exatamente o que o Brasil real faz com seus 44%."),
            4: ("🔴 Prioridade invertida","#ef4444",
                "Quatro ou mais em dívida — a escolha do Brasil real. Kalecki denunciaria isso como captura do Estado pelo capital financeiro: o governo usa recursos públicos para remunerar quem já é rico, em vez de investir nos multiplicadores que geram emprego e reduzem desigualdade. É o anti-Kalecki."),
        },
    },
}

REAL_CARTOES = {k: round(v["real_pct"] / 100 * TOTAL_CARTOES) for k, v in GASTOS.items()}
diff = TOTAL_CARTOES - sum(REAL_CARTOES.values())
if diff != 0:
    REAL_CARTOES["💰 Serviço da Dívida"] += diff

# ── Scores kaleckianos por nível (0-4+) ─────────────────────────────────────
# Cada indicador tem score 0-100 para cada nível de cartão
# Reflete mudança brusca: 0→1 é enorme; 3→4 é marginal ou negativo
SCORES_POR_NIVEL = {
    # emprego, consumo, desigualdade(redução), investimento, divida(controle)
    "🏫 Educação": {
        0: {"emprego":0, "consumo":0, "desigualdade":0, "investimento":0, "divida":50},
        1: {"emprego":20,"consumo":15,"desigualdade":15,"investimento":25,"divida":50},
        2: {"emprego":45,"consumo":35,"desigualdade":35,"investimento":55,"divida":50},
        3: {"emprego":80,"consumo":65,"desigualdade":70,"investimento":90,"divida":50},
        4: {"emprego":85,"consumo":68,"desigualdade":75,"investimento":92,"divida":45},
    },
    "🏥 Saúde": {
        0: {"emprego":5, "consumo":0, "desigualdade":0, "investimento":5, "divida":50},
        1: {"emprego":25,"consumo":20,"desigualdade":20,"investimento":20,"divida":50},
        2: {"emprego":50,"consumo":45,"desigualdade":50,"investimento":40,"divida":50},
        3: {"emprego":75,"consumo":70,"desigualdade":80,"investimento":65,"divida":50},
        4: {"emprego":78,"consumo":73,"desigualdade":82,"investimento":67,"divida":45},
    },
    "🏠 Habitação": {
        0: {"emprego":0, "consumo":5, "desigualdade":5, "investimento":5, "divida":50},
        1: {"emprego":30,"consumo":25,"desigualdade":20,"investimento":25,"divida":50},
        2: {"emprego":60,"consumo":50,"desigualdade":45,"investimento":50,"divida":50},
        3: {"emprego":85,"consumo":70,"desigualdade":65,"investimento":70,"divida":50},
        4: {"emprego":87,"consumo":72,"desigualdade":67,"investimento":72,"divida":45},
    },
    "🎭 Cultura": {
        0: {"emprego":0, "consumo":0, "desigualdade":0, "investimento":0, "divida":50},
        1: {"emprego":15,"consumo":20,"desigualdade":15,"investimento":10,"divida":50},
        2: {"emprego":30,"consumo":40,"desigualdade":30,"investimento":25,"divida":50},
        3: {"emprego":45,"consumo":55,"desigualdade":45,"investimento":35,"divida":50},
        4: {"emprego":47,"consumo":57,"desigualdade":47,"investimento":37,"divida":45},
    },
    "🛡️ Segurança e Defesa": {
        0: {"emprego":0, "consumo":0, "desigualdade":0, "investimento":0, "divida":50},
        1: {"emprego":25,"consumo":10,"desigualdade":5, "investimento":10,"divida":50},
        2: {"emprego":45,"consumo":20,"desigualdade":10,"investimento":20,"divida":50},
        3: {"emprego":55,"consumo":22,"desigualdade":10,"investimento":22,"divida":45},
        4: {"emprego":55,"consumo":15,"desigualdade":5, "investimento":15,"divida":35},
    },
    "🤝 Transferência de Renda": {
        0: {"emprego":0, "consumo":0, "desigualdade":0, "investimento":10,"divida":50},
        1: {"emprego":20,"consumo":40,"desigualdade":45,"investimento":15,"divida":50},
        2: {"emprego":35,"consumo":65,"desigualdade":70,"investimento":20,"divida":50},
        3: {"emprego":50,"consumo":90,"desigualdade":95,"investimento":30,"divida":45},
        4: {"emprego":55,"consumo":95,"desigualdade":98,"investimento":32,"divida":40},
    },
    "💰 Serviço da Dívida": {
        0: {"emprego":20,"consumo":40,"desigualdade":60,"investimento":20,"divida":0},
        1: {"emprego":40,"consumo":50,"desigualdade":50,"investimento":35,"divida":40},
        2: {"emprego":50,"consumo":50,"desigualdade":40,"investimento":45,"divida":65},
        3: {"emprego":40,"consumo":35,"desigualdade":20,"investimento":35,"divida":75},
        4: {"emprego":20,"consumo":15,"desigualdade":5, "investimento":15,"divida":80},
    },
}

INDICADORES = {
    "👷 Emprego":         ("emprego",       "#3b82f6"),
    "🛒 Consumo Popular": ("consumo",       "#22c55e"),
    "⚖️ Desigualdade↓":  ("desigualdade",  "#ec4899"),
    "📈 Investimento":    ("investimento",  "#f97316"),
    "📉 Controle Dívida": ("divida",        "#8b5cf6"),
}

def calcular_scores(dist):
    """Soma os scores de cada área pelo número de cartões, com cap em nível 4."""
    totais = {k: 0.0 for k in ["emprego","consumo","desigualdade","investimento","divida"]}
    n_areas = len(GASTOS)
    for area, qtd in dist.items():
        if area not in SCORES_POR_NIVEL: continue
        nivel = min(int(round(qtd)), 4)
        s = SCORES_POR_NIVEL[area][nivel]
        for ind in totais:
            totais[ind] += s[ind]
    # Média entre as áreas → normaliza para 0-100
    return {k: min(100, int(v / n_areas)) for k, v in totais.items()}

def nivel_label(area, qtd):
    niveis = GASTOS[area]["niveis"]
    n = min(qtd, 4)
    return niveis[n]

def carregar_dados():
    if os.path.exists(ARQUIVO_DADOS):
        with open(ARQUIVO_DADOS,"r",encoding="utf-8") as f: return json.load(f)
    return []

def salvar_dados(registro):
    dados = carregar_dados(); dados.append(registro)
    with open(ARQUIVO_DADOS,"w",encoding="utf-8") as f: json.dump(dados,f,ensure_ascii=False,indent=2)

# ── Session state ───────────────────────────────────────────────
for k,v in [("pagina","inicio"),("nome",""),("idade",""),("escolaridade",""),
            ("distribuicao",{k:0 for k in GASTOS}),("enviado",False),("reset_key",0)]:
    if k not in st.session_state: st.session_state[k]=v

# ═══════════════════════════════════════════════════════════════
# PÁGINA 1 — INÍCIO
# ═══════════════════════════════════════════════════════════════
if st.session_state.pagina == "inicio":
    # ── Hero banner ──────────────────────────────────────────────
    st.markdown("""
    <div style="background:linear-gradient(135deg,#1e3a5f 0%,#0f2744 60%,#0d1b2a 100%);
         border-radius:24px;padding:2.5rem 2rem 2rem;margin-bottom:1.5rem;
         border:1px solid rgba(74,144,217,.3);
         box-shadow:0 8px 40px rgba(0,0,0,.5);text-align:center;">
      <div style="font-family:'Fredoka One',cursive;font-size:3rem;
           background:linear-gradient(90deg,#f97316,#eab308,#22c55e,#3b82f6,#8b5cf6);
           -webkit-background-clip:text;-webkit-text-fill-color:transparent;
           background-clip:text;margin-bottom:.3rem;">🏛️ Eu Sou o Governo!</div>
      <div style="color:#93c5fd;font-size:1.1rem;font-weight:700;">
           Jogo do Orçamento Público &nbsp;·&nbsp; Semana Rural</div>
    </div>
    """, unsafe_allow_html=True)

    col_form, col_info = st.columns([1, 1], gap="large")

    with col_form:
        st.markdown("""
        <div style="background:#1e293b;border-radius:20px;padding:1.8rem 1.5rem 1rem;
             border:1px solid #334155;box-shadow:0 8px 32px rgba(0,0,0,.4);margin-bottom:1rem;">
        <div style="font-family:'Fredoka One',cursive;font-size:1.4rem;color:#ffd700;
             margin-bottom:1.2rem;text-align:center;">👋 Antes de começar</div>
        </div>""", unsafe_allow_html=True)

        nome = st.text_input("Seu nome:", placeholder="Ex: João Silva", key="in_nome")
        if nome.strip():
            st.markdown(
                f'<div style="background:linear-gradient(135deg,#1e40af,#7c3aed);'
                f'border-radius:12px;padding:.7rem 1rem;text-align:center;margin:.2rem 0 .4rem;">'
                f'<span style="font-family:Fredoka One,cursive;font-size:1.2rem;color:#ffd700;">'
                f'Olá, {nome.strip()}! 👋</span><br>'
                f'<span style="font-size:.82rem;color:rgba(255,255,255,.8);">'
                f'Pronto(a) para ser governante?</span></div>',
                unsafe_allow_html=True)
        idade = st.number_input("Sua idade:", min_value=8, max_value=80, value=15, step=1, key="in_idade")
        escolaridade = st.selectbox("Nível de escolaridade:", [
            "— selecione —",
            "Ensino Fundamental II (6º ao 9º ano)",
            "Ensino Médio",
            "Graduação",
            "Pós-graduação / Mestrado / Doutorado",
        ], key="in_esc")

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🚀 Começar o Jogo!", use_container_width=True):
            if nome.strip()=="" or escolaridade=="— selecione —":
                st.warning("⚠️ Preencha seu nome e escolaridade!")
            else:
                st.session_state.nome = nome.strip()
                st.session_state.idade = int(idade)
                st.session_state.escolaridade = escolaridade
                st.session_state.distribuicao = {k:0 for k in GASTOS}
                st.session_state.enviado = False
                st.session_state.pagina = "jogo"
                st.rerun()

    with col_info:
        st.markdown(f"""
        <div style="background:rgba(59,130,246,.08);border:1.5px solid rgba(59,130,246,.3);
             border-radius:20px;padding:1.8rem 1.6rem;height:100%;
             box-shadow:0 8px 32px rgba(0,0,0,.3);">
          <div style="font-family:'Fredoka One',cursive;color:#93c5fd;font-size:1.3rem;margin-bottom:1rem;">
               📖 Como funciona?</div>

          <div style="display:flex;align-items:flex-start;gap:12px;margin-bottom:1rem;">
            <div style="font-size:1.8rem;line-height:1;">🃏</div>
            <div style="font-size:.9rem;color:#cbd5e1;line-height:1.6;">
              Você recebe <b style="color:#ffd700">{TOTAL_CARTOES} cartões</b> representando
              todo o orçamento do governo. É pouco — de propósito.
            </div>
          </div>

          <div style="display:flex;align-items:flex-start;gap:12px;margin-bottom:1rem;">
            <div style="font-size:1.8rem;line-height:1;">🎯</div>
            <div style="font-size:.9rem;color:#cbd5e1;line-height:1.6;">
              Distribua os cartões nas <b style="color:#4ade80">7 áreas de gasto</b>.
              Cada real a mais em um lugar é um real a menos em outro — você não pode deixar tudo no máximo.
            </div>
          </div>

          <div style="display:flex;align-items:flex-start;gap:12px;margin-bottom:1rem;">
            <div style="font-size:1.8rem;line-height:1;">🔍</div>
            <div style="font-size:.9rem;color:#cbd5e1;line-height:1.6;">
              No final, veja <b style="color:#a78bfa">o que acontece com a economia</b>
              com base nas suas escolhas — na visão do economista Kalecki.
            </div>
          </div>

          <div style="display:flex;align-items:flex-start;gap:12px;">
            <div style="font-size:1.8rem;line-height:1;">🏦</div>
            <div style="font-size:.9rem;color:#cbd5e1;line-height:1.6;">
              Descubra o <b style="color:#fbbf24">paradoxo do orçamento público</b>:
              o governo emite a própria moeda — então por que a restrição existe?
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# PÁGINA 2 — JOGO
# ═══════════════════════════════════════════════════════════════
elif st.session_state.pagina == "jogo":
    import streamlit.components.v1 as components

    st.markdown(f'''
    <div style="background:linear-gradient(135deg,#1e3a5f,#0f2744);border-radius:16px;
         padding:1rem 1.5rem;margin-bottom:.5rem;border:1px solid rgba(74,144,217,.3);
         box-shadow:0 4px 20px rgba(0,0,0,.4);display:flex;align-items:center;justify-content:space-between;">
      <div>
        <div style="font-family:'Fredoka One',cursive;font-size:1.6rem;color:#ffd700;">🏛️ Monte seu Orçamento!</div>
        <div style="font-size:.85rem;color:#93c5fd;">Governante: <b style="color:white">{st.session_state.nome}</b></div>
      </div>
      <div style="text-align:right;">
        <div style="font-family:'Fredoka One',cursive;font-size:2rem;color:#4ade80;">{TOTAL_CARTOES}</div>
        <div style="font-size:.72rem;color:#94a3b8;">cartões totais</div>
      </div>
    </div>''', unsafe_allow_html=True)

    st.markdown("""<style>
    div[data-testid="stTextInput"]:has(input[aria-label="dist hidden"]) {
        position:fixed !important;bottom:-9999px !important;
        opacity:0 !important;pointer-events:none !important;height:0 !important;
    }
    </style>""", unsafe_allow_html=True)
    resultado_raw = st.text_input("dist hidden", key="drag_result", label_visibility="collapsed")

    if resultado_raw and resultado_raw.startswith("{"):
        try:
            dec = json.loads(resultado_raw)
            for k in GASTOS: st.session_state.distribuicao[k] = dec.get(k,0)
            salvar_dados({"nome":st.session_state.nome,"idade":st.session_state.idade,
                          "escolaridade":st.session_state.escolaridade,
                          "timestamp":datetime.now().isoformat(),
                          "distribuicao":dict(st.session_state.distribuicao)})
            st.session_state.enviado=True; st.session_state.pagina="resultado"; st.rerun()
        except Exception as e: st.error(f"Erro: {e}")

    gastos_json = json.dumps({
        k: {"cor":v["cor"],"descricao":v["descricao"],
            "nivel0":v["niveis"][0][0],"nivel1":v["niveis"][1][0],
            "nivel2":v["niveis"][2][0],"nivel3":v["niveis"][3][0],
            "nivel4":v["niveis"][4][0],
            "nivel0cor":v["niveis"][0][1],"nivel1cor":v["niveis"][1][1],
            "nivel2cor":v["niveis"][2][1],"nivel3cor":v["niveis"][3][1],
            "nivel4cor":v["niveis"][4][1]}
        for k,v in GASTOS.items()}, ensure_ascii=False)
    dist_ini = json.dumps(st.session_state.distribuicao, ensure_ascii=False)
    n = len(GASTOS)
    altura = 1080

    html = f"""<!DOCTYPE html><html lang="pt-BR"><head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no">
<link href="https://fonts.googleapis.com/css2?family=Fredoka+One&family=Nunito:wght@400;600;700;800&display=swap" rel="stylesheet">
<style>
*{{box-sizing:border-box;margin:0;padding:0;}}
body{{font-family:'Nunito',sans-serif;
  background:linear-gradient(135deg,#0f172a 0%,#1e293b 100%);
  padding:16px 20px 28px;color:white;user-select:none;}}

/* ── LAYOUT MASTER: sidebar esquerda + conteúdo direita ── */
#master{{display:grid;grid-template-columns:180px 1fr;gap:16px;align-items:start;}}

/* ── SIDEBAR: banco + contador + btn ── */
#sidebar{{display:flex;flex-direction:column;gap:12px;position:sticky;top:16px;}}

/* HEADER (acima do master, full-width) */
#header{{display:flex;align-items:center;justify-content:space-between;
  background:linear-gradient(135deg,#1e3a5f,#0f2744);
  border-radius:16px;padding:14px 20px;margin-bottom:14px;
  border:1px solid rgba(74,144,217,.4);box-shadow:0 4px 24px rgba(0,0,0,.4);}}
#header-left h1{{font-family:'Fredoka One',cursive;font-size:1.25rem;color:#ffd700;margin-bottom:2px;}}
#header-left p{{font-size:.72rem;color:#93c5fd;}}
#header-right{{text-align:right;}}
#contador-resto{{font-family:'Fredoka One',cursive;font-size:2.6rem;color:#ffd700;line-height:1;}}
#contador-label{{font-size:.68rem;color:#93c5fd;}}

/* PROGRESSO */
#prog-wrap{{margin-bottom:14px;}}
#prog-bg{{background:rgba(255,255,255,.1);border-radius:20px;height:12px;overflow:hidden;}}
#prog-bar{{height:100%;border-radius:20px;
  background:linear-gradient(90deg,#ef4444,#f97316,#eab308,#22c55e);
  background-size:400% 100%;
  transition:width .5s cubic-bezier(.34,1.56,.64,1);
  box-shadow:0 0 12px rgba(34,197,94,.5);}}

/* AVISO */
#aviso{{text-align:center;font-size:.82rem;font-weight:700;border-radius:10px;
  padding:8px 10px;margin-bottom:14px;transition:all .3s;}}
.av-f{{background:rgba(251,191,36,.15);color:#fbbf24;border:1.5px solid rgba(251,191,36,.4);}}
.av-ok{{background:rgba(34,197,94,.15);color:#4ade80;border:1.5px solid rgba(34,197,94,.4);}}

/* BANCO (sidebar) */
#banco{{background:linear-gradient(135deg,#1e3a5f,#162d4a);border-radius:14px;
  padding:14px;border:1.5px solid rgba(74,144,217,.35);
  box-shadow:0 4px 20px rgba(0,0,0,.3);}}
#banco h2{{font-family:'Fredoka One',cursive;color:#ffd700;font-size:.95rem;margin-bottom:3px;}}
#banco-sub{{font-size:.65rem;color:#93c5fd;margin-bottom:8px;line-height:1.4;}}
#banco-cards{{display:flex;flex-wrap:wrap;gap:7px;min-height:55px;padding:8px;
  border-radius:10px;background:rgba(255,255,255,.05);
  border:2px dashed rgba(255,255,255,.15);transition:all .2s;}}
#banco-cards.drag-over{{background:rgba(255,215,0,.1);border-color:#ffd700;
  box-shadow:0 0 0 3px rgba(255,215,0,.2);}}

/* CARTÃO */
.cartao{{width:48px;height:64px;
  background:linear-gradient(145deg,#fbbf24,#f59e0b);
  border-radius:10px;border:2px solid #d97706;cursor:grab;
  display:flex;align-items:center;justify-content:center;font-size:1.5rem;
  box-shadow:0 4px 10px rgba(0,0,0,.4),inset 0 1px 0 rgba(255,255,255,.3);
  transition:transform .15s,box-shadow .15s;position:relative;}}
.cartao::after{{content:'';position:absolute;inset:3px;border-radius:6px;
  border:1px solid rgba(255,255,255,.25);pointer-events:none;}}
.cartao:hover{{transform:translateY(-6px) rotate(-4deg);box-shadow:0 12px 28px rgba(0,0,0,.5);}}
.cartao.dragging{{opacity:.2;transform:scale(.88);}}

/* BOTÃO CONFIRMAR (sidebar) */
#btn{{display:block;width:100%;padding:13px;
  font-family:'Fredoka One',cursive;font-size:1rem;
  border:none;border-radius:12px;cursor:pointer;
  transition:all .25s;position:relative;overflow:hidden;}}
#btn:enabled{{background:linear-gradient(135deg,#22c55e,#16a34a);color:white;
  box-shadow:0 6px 20px rgba(34,197,94,.4);}}
#btn:enabled::before{{content:'';position:absolute;top:0;left:-100%;width:100%;height:100%;
  background:linear-gradient(90deg,transparent,rgba(255,255,255,.2),transparent);transition:left .5s;}}
#btn:enabled:hover::before{{left:100%;}}
#btn:enabled:hover{{transform:translateY(-2px);box-shadow:0 10px 28px rgba(34,197,94,.55);}}
#btn:enabled:active{{transform:scale(.97);}}
#btn:disabled{{background:rgba(255,255,255,.08);color:rgba(255,255,255,.3);
  cursor:not-allowed;border:1.5px solid rgba(255,255,255,.1);box-shadow:none;}}

/* GRID (conteúdo principal) */
#grid{{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;}}

/* CAIXA */
.caixa{{border-radius:16px;padding:18px 10px 16px;
  display:flex;flex-direction:column;align-items:center;
  border:2px solid transparent;
  transition:transform .2s,border-color .2s,box-shadow .2s,filter .2s;
  min-height:160px;position:relative;overflow:hidden;cursor:default;}}
.caixa:hover{{transform:translateY(-3px);filter:brightness(1.08);}}
.caixa.drag-over{{
  border-color:rgba(255,255,255,.8)!important;
  box-shadow:0 0 0 4px rgba(255,255,255,.3),0 10px 32px rgba(0,0,0,.3)!important;
  transform:scale(1.06)!important;filter:brightness(1.15)!important;}}
.caixa.zero{{filter:grayscale(.4) brightness(.72);}}
.c-emoji{{font-size:2.2rem;margin-bottom:6px;filter:drop-shadow(0 2px 6px rgba(0,0,0,.35));}}
.c-nome{{font-family:'Fredoka One',cursive;font-size:.82rem;color:white;text-align:center;
  text-shadow:0 1px 4px rgba(0,0,0,.5);line-height:1.25;margin-bottom:8px;}}
.c-cnt{{font-family:'Fredoka One',cursive;font-size:2rem;color:white;
  background:rgba(0,0,0,.3);border-radius:50%;width:52px;height:52px;
  display:flex;align-items:center;justify-content:center;
  box-shadow:0 3px 12px rgba(0,0,0,.35),inset 0 1px 0 rgba(255,255,255,.15);
  transition:transform .25s cubic-bezier(.34,1.56,.64,1);
  border:2px solid rgba(255,255,255,.2);margin-bottom:8px;}}
.c-cnt.bump{{transform:scale(1.5);}}
.c-touch-btns{{display:none;}}

/* MINI CARTÕES */
.c-pilha{{display:flex;flex-wrap:wrap;gap:3px;justify-content:center;padding:2px 4px 0;}}
.mini{{width:14px;height:20px;background:linear-gradient(145deg,#fbbf24,#f59e0b);
  border-radius:3px;border:1px solid #d97706;cursor:grab;
  box-shadow:0 1px 4px rgba(0,0,0,.4);transition:transform .1s;}}
.mini:hover{{transform:translateY(-3px);}}
</style></head><body>

<div id="header">
  <div id="header-left">
    <h1>🏛️ Monte seu Orçamento</h1>
    <p>Você tem apenas {TOTAL_CARTOES} cartões — cada um conta!</p>
  </div>
  <div id="header-right">
    <div id="contador-resto">{TOTAL_CARTOES}</div>
    <div id="contador-label">cartões restantes</div>
  </div>
</div>

<div id="prog-wrap">
  <div id="prog-bg"><div id="prog-bar" style="width:0%"></div></div>
</div>
<div id="aviso" class="av-f">💡 Distribua todos os {TOTAL_CARTOES} cartões para confirmar!</div>

<div id="master">
  <div id="sidebar">
    <div id="banco">
      <h2>💳 Banco</h2>
      <div id="banco-sub">Arraste para as caixas. Devolva arrastando aqui.</div>
      <div id="banco-cards"></div>
    </div>
    <button id="btn" disabled>Distribuir todos ✋</button>
  </div>
  <div id="grid"></div>
</div>

<script>
const GASTOS={gastos_json};
const TOTAL={TOTAL_CARTOES};
const DIST_INI={dist_ini};
const estado={{}};
Object.keys(GASTOS).forEach(k=>estado[k]=DIST_INI[k]||0);
let dragSource=null,touchDragging=null,touchClone=null,touchSourceArea=null;

function totalDist(){{return Object.values(estado).reduce((a,b)=>a+b,0);}}
function restantes(){{return TOTAL-totalDist();}}
function cid(s){{return s.replace(/[^a-zA-Z0-9]/g,'_');}}

/* BANCO */
function renderBanco(){{
  const el=document.getElementById('banco-cards');el.innerHTML='';
  for(let i=0;i<restantes();i++){{
    const card=criarCartao('banco');el.appendChild(card);
  }}
}}
function criarCartao(source){{
  const c=document.createElement('div');
  c.className='cartao';c.draggable=true;c.dataset.source=source;
  c.innerHTML='💵';
  c.addEventListener('dragstart',onDS);c.addEventListener('dragend',onDE);
  c.addEventListener('touchstart',onTouchStart,{{passive:false}});
  c.addEventListener('touchmove',onTouchMove,{{passive:false}});
  c.addEventListener('touchend',onTouchEnd);
  return c;
}}

/* GRID */
function initGrid(){{
  const grid=document.getElementById('grid');
  Object.entries(GASTOS).forEach(([nome,info])=>{{
    const emoji=nome.split(' ')[0];
    const label=nome.split(' ').slice(1).join(' ');
    const div=document.createElement('div');
    div.className='caixa zero';div.dataset.area=nome;
    div.style.background=`linear-gradient(160deg,${{info.cor}}cc,${{info.cor}}77)`;
    div.style.boxShadow=`0 4px 20px ${{info.cor}}44`;
    div.innerHTML=`
      <div class="c-emoji">${{emoji}}</div>
      <div class="c-nome">${{label}}</div>
      <div class="c-cnt" id="cnt-${{cid(nome)}}">0</div>
      <div class="c-touch-btns" id="tbtn-${{cid(nome)}}">
        <button class="c-btn-minus" onclick="touchBtn('${{nome}}',-1)" disabled>−</button>
        <button class="c-btn-plus"  onclick="touchBtn('${{nome}}',+1)">＋</button>
      </div>
      <div class="c-pilha" id="pilha-${{cid(nome)}}"></div>`;
    div.addEventListener('dragover',onDO);div.addEventListener('dragleave',onDL);div.addEventListener('drop',onDrop);
    grid.appendChild(div);
  }});
}}

function renderCaixas(){{
  Object.entries(estado).forEach(([nome,qtd])=>{{
    const cnt=document.getElementById('cnt-'+cid(nome));
    const pilha=document.getElementById('pilha-'+cid(nome));
    const tbtn=document.getElementById('tbtn-'+cid(nome));
    const caixa=document.querySelector(`[data-area="${{nome}}"]`);
    if(cnt) cnt.textContent=qtd;
    if(tbtn){{
      tbtn.querySelector('.c-btn-minus').disabled=(qtd<=0);
      tbtn.querySelector('.c-btn-plus').disabled=(restantes()<=0);
    }}
    if(pilha){{
      pilha.innerHTML='';
      for(let i=0;i<Math.min(qtd,5);i++){{
        const m=document.createElement('div');m.className='mini';m.draggable=true;
        m.dataset.source=nome;
        m.addEventListener('dragstart',onDS);m.addEventListener('dragend',onDE);
        m.addEventListener('touchstart',onTouchStart,{{passive:false}});
        m.addEventListener('touchmove',onTouchMove,{{passive:false}});
        m.addEventListener('touchend',onTouchEnd);
        pilha.appendChild(m);
      }}
    }}
    if(caixa) caixa.classList.toggle('zero',qtd===0);
  }});
}}

function touchBtn(area,delta){{
  if(delta>0&&restantes()<=0) return;
  if(delta<0&&estado[area]<=0) return;
  estado[area]+=delta; atualizar();
}}

/* DRAG MOUSE */
function onDS(e){{dragSource=e.target.dataset.source;setTimeout(()=>e.target.classList.add('dragging'),0);e.dataTransfer.effectAllowed='move';}}
function onDE(e){{e.target.classList.remove('dragging');dragSource=null;}}
function onDO(e){{e.preventDefault();e.currentTarget.classList.add('drag-over');}}
function onDL(e){{e.currentTarget.classList.remove('drag-over');}}
function onDrop(e){{
  e.preventDefault();e.currentTarget.classList.remove('drag-over');
  const dest=e.currentTarget.dataset.area;
  if(!dragSource||dragSource===dest) return;
  if(dragSource!=='banco'){{if(estado[dragSource]<=0) return;estado[dragSource]--;}}
  else{{if(restantes()<=0) return;}}
  estado[dest]++;atualizar();
}}
const bancoEl=document.getElementById('banco-cards');
bancoEl.addEventListener('dragover',e=>{{e.preventDefault();bancoEl.classList.add('drag-over');}});
bancoEl.addEventListener('dragleave',()=>bancoEl.classList.remove('drag-over'));
bancoEl.addEventListener('drop',e=>{{
  e.preventDefault();bancoEl.classList.remove('drag-over');
  if(!dragSource||dragSource==='banco') return;
  if(estado[dragSource]<=0) return;
  estado[dragSource]--;atualizar();
}});

/* DRAG TOUCH */
function onTouchStart(e){{
  if(e.touches.length!==1) return;e.preventDefault();
  touchDragging=e.currentTarget;touchSourceArea=e.currentTarget.dataset.source;
  touchClone=touchDragging.cloneNode(true);
  touchClone.style.cssText=`position:fixed;z-index:9999;opacity:.85;pointer-events:none;
    width:${{touchDragging.offsetWidth}}px;height:${{touchDragging.offsetHeight}}px;
    transform:scale(1.15) rotate(-5deg);transition:none;`;
  document.body.appendChild(touchClone);
  moveTouchClone(e.touches[0]);
  touchDragging.classList.add('touching');
}}
function moveTouchClone(t){{if(!touchClone) return;touchClone.style.left=(t.clientX-touchClone.offsetWidth/2)+'px';touchClone.style.top=(t.clientY-touchClone.offsetHeight/2)+'px';}}
function onTouchMove(e){{
  if(!touchDragging||e.touches.length!==1) return;e.preventDefault();
  moveTouchClone(e.touches[0]);
  document.querySelectorAll('.caixa,#banco-cards').forEach(el=>el.classList.remove('touch-over'));
  const tgt=document.elementFromPoint(e.touches[0].clientX,e.touches[0].clientY);
  if(tgt){{const cx=tgt.closest('[data-area]');if(cx) cx.classList.add('touch-over');const bk=tgt.closest('#banco-cards');if(bk) bk.classList.add('touch-over');}}
}}
function onTouchEnd(e){{
  if(!touchDragging) return;
  touchDragging.classList.remove('touching');
  if(touchClone){{touchClone.remove();touchClone=null;}}
  document.querySelectorAll('.caixa,#banco-cards').forEach(el=>el.classList.remove('touch-over'));
  const t=e.changedTouches[0];
  const tgt=document.elementFromPoint(t.clientX,t.clientY);
  if(tgt){{
    const cx=tgt.closest('[data-area]');const bk=tgt.closest('#banco-cards');
    const dest=cx?cx.dataset.area:(bk?'banco':null);
    if(dest&&dest!==touchSourceArea){{
      if(touchSourceArea!=='banco'){{if(estado[touchSourceArea]<=0){{touchDragging=null;return;}}estado[touchSourceArea]--;}}
      else{{if(restantes()<=0){{touchDragging=null;return;}}}}
      if(dest!=='banco') estado[dest]++;
      atualizar();
    }}
  }}
  touchDragging=null;touchSourceArea=null;
}}

/* ATUALIZAR */
function atualizar(){{
  const dist=totalDist();const rest=TOTAL-dist;
  document.getElementById('prog-bar').style.width=(dist/TOTAL*100)+'%';
  document.getElementById('contador-resto').textContent=rest;
  const av=document.getElementById('aviso');
  if(rest===0){{av.innerHTML='🎉 <b>Perfeito!</b> Todos os cartões distribuídos!';av.className='av-ok';}}
  else{{av.innerHTML='💡 Faltam <b>'+rest+'</b> cartão'+(rest>1?'s':'')+' para distribuir!';av.className='av-f';}}
  const btn=document.getElementById('btn');
  btn.disabled=rest!==0;
  btn.textContent=rest===0?'✅ Confirmar minha escolha!':'Distribua todos os cartões ✋';
  renderBanco();renderCaixas();
  Object.keys(estado).forEach(nome=>{{
    const cnt=document.getElementById('cnt-'+cid(nome));
    if(cnt){{cnt.classList.remove('bump');void cnt.offsetWidth;cnt.classList.add('bump');setTimeout(()=>cnt.classList.remove('bump'),350);}}
  }});
}}

/* CONFIRMAR */
document.getElementById('btn').addEventListener('click',()=>{{
  const payload=JSON.stringify(estado);
  const inputs=window.parent.document.querySelectorAll('input[type="text"]');
  for(const inp of inputs){{
    if(inp.getAttribute('aria-label')==='dist hidden'){{
      const setter=Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype,'value').set;
      setter.call(inp,payload);
      inp.dispatchEvent(new Event('input',{{bubbles:true}}));
      inp.dispatchEvent(new KeyboardEvent('keydown',{{key:'Enter',keyCode:13,bubbles:true}}));
      inp.dispatchEvent(new KeyboardEvent('keypress',{{key:'Enter',keyCode:13,bubbles:true}}));
      inp.dispatchEvent(new KeyboardEvent('keyup',{{key:'Enter',keyCode:13,bubbles:true}}));
      break;
    }}
  }}
}});

initGrid();atualizar();
</script></body></html>"""

    components.html(html + f"<!-- reset:{st.session_state.reset_key} -->", height=700, scrolling=False)

    col_v1,col_v2,col_v3=st.columns([1,1,1])
    with col_v1:
        if st.button("↩️ Voltar para o início", use_container_width=True):
            st.session_state.pagina="inicio"; st.rerun()
    with col_v2:
        if st.button("🔄 Zerar tudo", use_container_width=True):
            st.session_state.distribuicao={k:0 for k in GASTOS}
            st.session_state.reset_key = st.session_state.get("reset_key",0)+1
            st.rerun()

elif st.session_state.pagina == "resultado":
    dist   = st.session_state.distribuicao
    nome   = st.session_state.nome
    scores = calcular_scores(dist)

    s_educ  = dist.get("🏫 Educação",0)
    s_saude = dist.get("🏥 Saúde",0)
    s_hab   = dist.get("🏠 Habitação",0)
    s_cult  = dist.get("🎭 Cultura",0)
    s_seg   = dist.get("🛡️ Segurança e Defesa",0)
    s_trans = dist.get("🤝 Transferência de Renda",0)
    s_div   = dist.get("💰 Serviço da Dívida",0)

    def nivel_n(area): return min(dist.get(area,0),4)

    st.markdown(f'''
    <div style="background:linear-gradient(135deg,#1e3a5f,#0f2744);border-radius:16px;
         padding:1.2rem 1.8rem;margin-bottom:1rem;border:1px solid rgba(74,144,217,.3);
         box-shadow:0 4px 20px rgba(0,0,0,.4);display:flex;align-items:center;gap:16px;">
      <div style="font-size:2.8rem;">🏙️</div>
      <div>
        <div style="font-family:'Fredoka One',cursive;font-size:1.8rem;
             background:linear-gradient(90deg,#f97316,#eab308,#22c55e);
             -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;">
          Como ficou sua cidade?</div>
        <div style="font-size:.9rem;color:#93c5fd;">Governo de <b style="color:#ffd700">{nome}</b> — análise kaleckiana completa</div>
      </div>
    </div>''', unsafe_allow_html=True)


    # ══════════════════════════════════════════════════════════════
    # NARRATIVA KALECKIANA — sem níveis, baseada no mix de escolhas
    # ══════════════════════════════════════════════════════════════

    def bloco(emoji, titulo, cor, texto):
        return (f'<div style="margin-bottom:1.1rem;">'
                f'<div style="font-family:Fredoka One,cursive;font-size:1rem;'
                f'color:{cor};margin-bottom:.4rem;">{emoji} {titulo}</div>'
                f'<div style="font-size:.9rem;color:#e2e8f0;line-height:1.8;">{texto}</div>'
                f'</div>')

    def card_narrativa(blocos_html):
        return (f'<div style="background:linear-gradient(135deg,#1a2744 0%,#0f1e38 100%);'
                f'border-radius:18px;padding:1.6rem 1.8rem;'
                f'border:1.5px solid rgba(99,179,237,.25);'
                f'box-shadow:0 8px 32px rgba(0,0,0,.5);margin-bottom:1.2rem;position:relative;">'
                f'<div style="position:absolute;top:-1px;left:0;right:0;height:3px;'
                f'border-radius:18px 18px 0 0;'
                f'background:linear-gradient(90deg,#3b82f6,#8b5cf6,#ec4899);"></div>'
                f'{blocos_html}</div>')

    # ── Dados base ───────────────────────────────────────────────
    sc        = calcular_scores(dist)
    areas_ord = sorted(dist.items(), key=lambda x: -x[1])
    areas_com = [(a, v) for a, v in areas_ord if v > 0]
    areas_sem = [a for a, v in dist.items() if v == 0 and a != "💰 Serviço da Dívida"]

    s_div   = dist.get("💰 Serviço da Dívida", 0)
    s_trans = dist.get("🤝 Transferência de Renda", 0)
    s_educ  = dist.get("🏫 Educação", 0)
    s_saude = dist.get("🏥 Saúde", 0)
    s_hab   = dist.get("🏠 Habitação", 0)
    s_seg   = dist.get("🛡️ Segurança e Defesa", 0)
    s_cult  = dist.get("🎭 Cultura", 0)

    # ── Perfil geral ─────────────────────────────────────────────
    social = sc["consumo"] + sc["desigualdade"] + sc["emprego"]
    if social >= 180:         perfil = "progressista"
    elif social >= 120:       perfil = "equilibrado"
    elif sc["divida"] >= 70:  perfil = "fiscal-conservador"
    else:                     perfil = "fragmentado"

    # ── BLOCO 1: O que suas escolhas movimentam na economia ──────
    partes_eco = []

    if s_trans > 0:
        partes_eco.append(
            f"Ao destinar <b style='color:#22c55e'>{s_trans} cartão(ões) à Transferência de Renda</b>, "
            "você colocou dinheiro diretamente nas mãos de quem mais consome proporcionalmente. "
            "Para Kalecki, esse é o multiplicador mais imediato: famílias pobres gastam quase tudo "
            "que recebem — em comida, transporte, roupa — aquecendo o comércio local e gerando "
            "empregos em cascata."
        )

    if s_educ > 0 and s_saude > 0:
        partes_eco.append(
            f"A combinação de <b style='color:#3b82f6'>Educação ({s_educ})</b> e "
            f"<b style='color:#ef4444'>Saúde ({s_saude})</b> é o que Kalecki chamava de "
            "investimento no trabalhador: trabalhadores saudáveis produzem mais, "
            "qualificados ganham mais — e quem ganha mais consome mais. "
            "É o multiplicador de longo prazo que reduz desigualdade de forma estrutural."
        )
    elif s_educ > 0:
        partes_eco.append(
            f"Com <b style='color:#3b82f6'>{s_educ} cartão(ões) em Educação</b>, você investiu "
            "no multiplicador de longo prazo: trabalhadores mais qualificados ganham mais, "
            "consomem mais e reduzem a desigualdade ao longo do tempo."
        )
    elif s_saude > 0:
        partes_eco.append(
            f"Com <b style='color:#ef4444'>{s_saude} cartão(ões) em Saúde</b>, você preservou "
            "a força de trabalho. Para Kalecki, saúde pública é redistribuição disfarçada: "
            "famílias pobres não precisam gastar com plano privado e liberam renda "
            "para consumir outras coisas."
        )

    if s_hab > 0:
        partes_eco.append(
            f"Os <b style='color:#f97316'>{s_hab} cartão(ões) em Habitação</b> ativaram "
            "o multiplicador da construção civil — o setor que mais emprega trabalhadores "
            "sem qualificação avançada. Cada obra contrata pedreiros, eletricistas e engenheiros "
            "que gastam seu salário no comércio local."
        )

    if s_div > 0:
        partes_eco.append(
            f"Destinar <b style='color:#6b7280'>{s_div} cartão(ões) ao Serviço da Dívida</b> "
            "significa transferir recursos públicos para credores — bancos e investidores. "
            "Para Kalecki, esse dinheiro sai da economia produtiva: quem recebe juros tende "
            "a poupar, não a consumir. O multiplicador é negativo do ponto de vista social."
        )

    if s_seg > 0 and s_trans == 0 and s_educ == 0:
        partes_eco.append(
            f"Com <b style='color:#8b5cf6'>{s_seg} cartão(ões) em Segurança e Defesa</b> "
            "e nada em renda ou educação, você apostou na contenção em vez da prevenção. "
            "Kalecki diria: segurança sem investimento social é tratar o sintoma, "
            "não a causa — a desigualdade."
        )

    if not partes_eco:
        partes_eco.append(
            "Suas escolhas ficaram muito dispersas para gerar um multiplicador claro. "
            "Para Kalecki, concentrar recursos nos setores de maior impacto — "
            "renda, saúde, educação — é mais eficiente do que distribuir pouco em tudo."
        )

    economia_texto = " ".join(partes_eco[:3])

    # ── BLOCO 2: O que ficou de fora e o custo disso ─────────────
    custo_partes = []
    if s_trans == 0:
        custo_partes.append(
            "Sem <b style='color:#22c55e'>Transferência de Renda</b>, o consumo popular "
            "ficou sem base. Para Kalecki, é aqui que começa a recessão: famílias sem renda "
            "não consomem, empresas vendem menos, demitem mais — uma espiral que começa "
            "embaixo e sobe."
        )
    if s_educ == 0 and s_saude == 0:
        custo_partes.append(
            "Não investir em <b style='color:#3b82f6'>Educação</b> nem em "
            "<b style='color:#ef4444'>Saúde</b> ao mesmo tempo significa abandonar "
            "os dois pilares do multiplicador de longo prazo. "
            "A economia pode até funcionar no curto prazo, "
            "mas sem base humana, o crescimento não se sustenta."
        )
    if areas_sem:
        nomes_sem = ", ".join([
            f"<b style='color:{GASTOS[a]["cor"]}'>{a.split(" ",1)[1]}</b>"
            for a in areas_sem[:3]
        ])
        custo_partes.append(
            f"Você não alocou nada em {nomes_sem}. "
            "Para Kalecki, investimento zero não significa apenas serviço ausente — "
            "significa que o multiplicador daquele setor foi completamente desperdiçado."
        )

    if not custo_partes:
        custo_partes.append(
            "Você distribuiu cartões em todas as áreas — o que mostra consciência de que "
            "tudo importa. O desafio agora é concentrar mais onde o multiplicador é maior."
        )

    custo_texto = " ".join(custo_partes[:2])

    # ── BLOCO 3: Restrição orçamentária — visão de Kalecki ───────
    restricao = (
        "Você teve apenas <b style='color:#ffd700'>5 cartões</b> para distribuir entre "
        f"{len(GASTOS)} áreas. Isso não é acidente — é a representação de uma escolha política "
        "chamada <b style='color:#a78bfa'>restrição orçamentária</b>.<br><br>"
        "Para Kalecki, o ponto central é este: o governo emite a própria moeda. "
        "Ele nunca 'fica sem dinheiro' no sentido que uma família fica. "
        "O limite existe porque o Estado <b style='color:#f472b6'>escolhe criá-lo</b> — "
        "por meio de regras fiscais, leis de responsabilidade e acordos políticos.<br><br>"
        "O argumento kaleckiano mais profundo não é sobre inflação ou dívida. "
        "É sobre <b style='color:#4ade80'>poder</b>: manter o orçamento apertado significa "
        "manter o desemprego como ameaça permanente aos trabalhadores. "
        "Quem tem medo de perder o emprego não reivindica salário, não faz greve, "
        "não organiza sindicato. Para Kalecki, a austeridade fiscal não é técnica — "
        "é uma <b style='color:#f472b6'>disciplina social imposta pelo capital sobre o trabalho</b>. "
        "Na vida real, o Brasil destina mais de 40% do orçamento ao serviço da dívida — "
        "enquanto saúde, educação e habitação brigam pelo restante."
    )

    # ── BLOCO 4: Frase final ──────────────────────────────────────
    frases = {
        "progressista":
            f'"<i>{nome} entendeu o que poucos governantes aceitam: '
            'a economia cresce quando quem tem menos passa a ter mais. '
            'O multiplicador não começa no topo — começa na base.</i>"',
        "fiscal-conservador":
            f'"<i>Honrar a dívida tem seu lugar. Mas quando os credores recebem '
            'antes das crianças irem à escola, isso não é responsabilidade fiscal — '
            'é uma escolha sobre quem importa mais, {nome}.</i>"',
        "equilibrado":
            f'"<i>{nome} tentou distribuir bem com pouco. '
            'Mas em economia, meio investimento em tudo '
            'frequentemente significa resultado fraco em nada. '
            'Priorizar é a essência da política.</i>"',
        "fragmentado":
            f'"<i>O orçamento de {nome} não teve coragem de escolher. '
            'E orçamento sem escolha é política sem projeto — '
            'os recursos se perdem sem mover nada de verdade.</i>"',
    }

    # ── Renderiza ─────────────────────────────────────────────────
    st.markdown('''
    <div style="font-family:Fredoka One,cursive;font-size:1.3rem;
        color:#ffd700;margin:.2rem 0 .4rem;">📖 A história do seu governo</div>
    <div style="font-size:.78rem;color:#64748b;margin-bottom:.9rem;">
        Análise kaleckiana baseada no mix das suas escolhas
    </div>''', unsafe_allow_html=True)

    st.markdown(card_narrativa(
        bloco("📈", "O que suas escolhas movimentam na economia", "#93c5fd", economia_texto) +
        bloco("⚠️", "O que ficou de fora — e o custo disso", "#fbbf24", custo_texto) +
        bloco("🏦", "A restrição orçamentária — na visão de Kalecki", "#a78bfa", restricao) +
        bloco("💬", "O que Kalecki diria sobre seu governo", "#f472b6", frases[perfil])
    ), unsafe_allow_html=True)
    st.markdown("---")

    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Minha Escolha",
        "🌍 Impacto Kaleckiano",
        "👥 Coletivo da Semana Rural",
        "📋 Dados",
    ])

    # ── TAB 1 ────────────────────────────────────────────────────────────────
    with tab1:
        st.markdown('<div style="font-family:Fredoka One,cursive;font-size:1.3rem;color:#ffd700;margin-bottom:.8rem;">📊 Como você distribuiu seus cartões</div>', unsafe_allow_html=True)

        labels = [k.split(" ",1)[1] if " " in k else k for k in GASTOS]
        minha  = [dist.get(k,0) for k in GASTOS]
        cores  = [GASTOS[k]["cor"] for k in GASTOS]

        fig_minha = go.Figure(go.Bar(
            x=labels, y=minha, marker_color=cores,
            text=minha, textposition="outside",
        ))
        fig_minha.update_layout(
            title="Seus cartões por área",
            title_font=dict(family="Fredoka One",size=17,color="#ffd700"),
            plot_bgcolor="rgba(30,41,59,0.4)", paper_bgcolor="rgba(13,27,42,0)",
            font=dict(family="Nunito",size=12,color="#e2e8f0"),
            xaxis_title="", yaxis_title="Cartões",
            xaxis=dict(tickfont=dict(color="#94a3b8"),gridcolor="rgba(148,163,184,.1)"),
            yaxis=dict(tickfont=dict(color="#94a3b8"),gridcolor="rgba(148,163,184,.1)",range=[0, max(minha)+2]),
            showlegend=False,
        )
        st.plotly_chart(fig_minha, use_container_width=True)

        st.markdown('<div style="font-family:Fredoka One,cursive;font-size:1.1rem;color:#93c5fd;margin:1rem 0 .6rem;">🎯 Status kaleckiano de cada setor</div>', unsafe_allow_html=True)
        cols_s = st.columns(len(GASTOS))
        for i,(area,info) in enumerate(GASTOS.items()):
            qtd = dist.get(area,0)
            n   = min(qtd,4)
            lbl, cor, _ = info["niveis"][n]
            emoji_s = {0:"💀",1:"🔴",2:"🟡",3:"🟢",4:"🔵"}[n]
            label_curto = area.split(" ",1)[1] if " " in area else area
            with cols_s[i]:
                st.markdown(
                    f'<div style="background:{cor}22;border:2px solid {cor};border-radius:12px;'
                    f'padding:.5rem .3rem;text-align:center;">'
                    f'<div style="font-size:1.4rem">{area.split()[0]}</div>'
                    f'<div style="font-family:Fredoka One,cursive;font-size:.7rem;color:{cor}">{label_curto}</div>'
                    f'<div style="font-size:1.2rem">{emoji_s}</div>'
                    f'<div style="font-size:.7rem;color:#94a3b8;font-weight:700;margin-top:2px;">{qtd} cartões</div>'
                    f'<div style="font-size:.6rem;color:{cor};font-weight:700">{lbl}</div>'
                    f'</div>', unsafe_allow_html=True)

    # ── TAB 2 ────────────────────────────────────────────────────────────────
    with tab2:
        st.markdown('<div style="font-family:Fredoka One,cursive;font-size:1.3rem;color:#ffd700;margin-bottom:.8rem;">🌍 O que Kalecki diria sobre seu governo?</div>', unsafe_allow_html=True)
        st.markdown('''
        <div style="background:rgba(59,130,246,.1);border:1.5px solid rgba(59,130,246,.35);
             border-radius:14px;padding:1rem 1.2rem;margin-bottom:1rem;">
          <div style="font-family:Fredoka One,cursive;color:#93c5fd;font-size:1rem;margin-bottom:.4rem;">
               📚 Quem foi Kalecki?</div>
          <div style="font-size:.88rem;color:#cbd5e1;line-height:1.6;">
            <b style="color:#fbbf24">Michal Kalecki</b> (1899–1970) foi o economista que mostrou que
            <b>onde</b> o governo gasta importa tanto quanto <b>quanto</b> gasta.
            Para ele, gastos em saúde, educação e transferência de renda têm
            <b style="color:#4ade80">multiplicadores muito maiores</b> do que gastos em dívida ou defesa.
          </div>
        </div>''', unsafe_allow_html=True)

        # Indicadores visuais
        col_r, col_g = st.columns([1,1])
        with col_r:
            ind_labels = list(INDICADORES.keys())
            ind_vals   = [scores[v[0]] for v in INDICADORES.values()]
            fig_radar = go.Figure(go.Scatterpolar(
                r=ind_vals+[ind_vals[0]], theta=ind_labels+[ind_labels[0]],
                fill='toself', fillcolor='rgba(59,130,246,0.2)',
                line=dict(color='#3b82f6',width=3),
            ))
            fig_radar.update_layout(
                polar=dict(radialaxis=dict(visible=True,range=[0,100],tickfont=dict(size=9,color="#94a3b8"),gridcolor="rgba(148,163,184,.2)",linecolor="rgba(148,163,184,.2)"),angularaxis=dict(tickfont=dict(color="#cbd5e1"),gridcolor="rgba(148,163,184,.15)")),
                title="Perfil econômico",
                title_font=dict(family="Fredoka One",size=16,color="#ffd700"),
                paper_bgcolor="rgba(13,27,42,0)", font=dict(family="Nunito",color="#e2e8f0"),
                height=320, margin=dict(t=50,b=10,l=30,r=30),
            )
            st.plotly_chart(fig_radar, use_container_width=True)
        with col_g:
            st.markdown("**Indicadores do seu governo:**")
            for label,(chave,cor) in INDICADORES.items():
                v = scores[chave]
                emoji_v = "🟢" if v>=65 else "🟡" if v>=35 else "🔴"
                st.markdown(
                    f'<div style="margin-bottom:9px;">'
                    f'<div style="font-size:.85rem;font-weight:700;color:#374151">{emoji_v} {label}</div>'
                    f'<div style="background:#e5e7eb;border-radius:20px;height:22px;overflow:hidden;">'
                    f'<div style="background:{cor};width:{v}%;height:100%;border-radius:20px;'
                    f'display:flex;align-items:center;padding-left:8px;">'
                    f'<span style="font-size:.75rem;font-weight:800;color:white;text-shadow:0 1px 3px rgba(0,0,0,.5);">{v}%</span>'
                    f'</div></div></div>', unsafe_allow_html=True)

        st.markdown("---")
        st.markdown('<div style="font-family:Fredoka One,cursive;font-size:1.1rem;color:#93c5fd;margin:.8rem 0 .4rem;">📖 Análise kaleckiana — área por área</div>', unsafe_allow_html=True)
        st.markdown('<div style="font-size:.8rem;color:#64748b;margin-bottom:.8rem;">Cada área recebe um diagnóstico baseado exatamente em quantos cartões você colocou.</div>', unsafe_allow_html=True)

        areas_ord = sorted(dist.items(), key=lambda x:-x[1])
        for area, qtd in areas_ord:
            info = GASTOS[area]
            n    = min(qtd,4)
            lbl, cor, texto = info["niveis"][n]
            emoji_s = {0:"💀",1:"🔴",2:"🟡",3:"🟢",4:"🔵"}[n]
            pct = int(qtd/TOTAL_CARTOES*100)
            st.markdown(
                f'<div style="border-radius:14px;padding:1rem;margin-bottom:.8rem;background:linear-gradient(135deg,#1e293b,#162032);'
                f'border-left:6px solid {cor};box-shadow:0 4px 20px rgba(0,0,0,.4);">'
                f'<div style="display:flex;align-items:center;gap:10px;margin-bottom:6px;">'
                f'<span style="font-size:1.6rem">{area.split()[0]}</span>'
                f'<div style="flex:1">'
                f'<strong style="color:{cor};font-size:.95rem">{area}</strong>'
                f'<span style="font-size:1rem;margin-left:6px">{emoji_s}</span><br>'
                f'<span style="font-size:.75rem;color:#94a3b8">{qtd} cartão(ões) · {pct}% do orçamento · '
                f'<b style="color:{cor}">{lbl}</b></span>'
                f'</div></div>'
                f'<p style="font-size:.87rem;color:#cbd5e1;line-height:1.65;margin:0">{texto}</p>'
                f'</div>', unsafe_allow_html=True)

        # Alertas globais kaleckianos
        st.markdown("---")
        if s_div >= 4:
            st.markdown('<div class="chip-verm">⚠️ <b>Alerta Kaleckiano:</b> Você repetiu o erro do Brasil real — mais de 40% para a dívida. Kalecki chamaria isso de captura do Estado pelo capital financeiro.</div>', unsafe_allow_html=True)
        if s_trans >= 3:
            st.markdown('<div class="chip-verde">🌟 <b>Elogio Kaleckiano:</b> Excelente aposta em transferência de renda! É o gasto com maior multiplicador de curto prazo segundo Kalecki.</div>', unsafe_allow_html=True)
        if s_educ >= 3 and s_saude >= 3:
            st.markdown('<div class="chip-verde">🌟 <b>Elogio Kaleckiano:</b> Investir bem em saúde E educação é a combinação que mais reduz desigualdade no longo prazo.</div>', unsafe_allow_html=True)
        if s_educ == 0 or s_saude == 0:
            st.markdown('<div class="chip-verm">💀 <b>Colapso Kaleckiano:</b> Zerar saúde ou educação é catastrófico. Kalecki diria que sem esses pilares, não há demanda agregada sustentável.</div>', unsafe_allow_html=True)

    # ── TAB 3 ────────────────────────────────────────────────────────────────
    with tab3:
        dados = carregar_dados()
        if not dados:
            st.info("Nenhum participante ainda.")
        else:
            st.markdown(f'<div style="font-family:Fredoka One,cursive;font-size:1.3rem;color:#ffd700;margin-bottom:.8rem;">👥 {len(dados)} participante(s) já jogaram!</div>', unsafe_allow_html=True)
            totais={k:0 for k in GASTOS}
            for reg in dados:
                for area,val in reg["distribuicao"].items():
                    if area in totais: totais[area]+=val

            df_col=pd.DataFrame({"Área":list(totais.keys()),"Total":list(totais.values())}).sort_values("Total",ascending=False)

            col_p,col_b2=st.columns(2)
            with col_p:
                fig_pizza=px.pie(df_col,names="Área",values="Total",color="Área",
                    color_discrete_map={k:GASTOS[k]["cor"] for k in GASTOS},
                    title="Prioridades coletivas",hole=0.35)
                fig_pizza.update_traces(textposition="inside",textinfo="percent+label",textfont_size=11)
                fig_pizza.update_layout(font=dict(family="Nunito",color="#e2e8f0"),
                    title_font=dict(family="Fredoka One",size=16,color="#ffd700"),
                    paper_bgcolor="rgba(13,27,42,0)",showlegend=False)
                st.plotly_chart(fig_pizza, use_container_width=True)
            with col_b2:
                n_jog=len(dados)
                dist_media={k:totais[k]/n_jog for k in GASTOS}
                sc_t=calcular_scores(dist_media)
                ind_l2=list(INDICADORES.keys())
                ind_v2=[sc_t[v[0]] for v in INDICADORES.values()]
                fig_r2=go.Figure(go.Scatterpolar(
                    r=ind_v2+[ind_v2[0]],theta=ind_l2+[ind_l2[0]],
                    fill='toself',fillcolor='rgba(236,72,153,0.2)',
                    line=dict(color='#ec4899',width=3),
                ))
                fig_r2.update_layout(
                    polar=dict(radialaxis=dict(visible=True,range=[0,100],tickfont=dict(color="#94a3b8"),gridcolor="rgba(148,163,184,.2)",linecolor="rgba(148,163,184,.2)"),angularaxis=dict(tickfont=dict(color="#cbd5e1"),gridcolor="rgba(148,163,184,.15)")),
                    title="Perfil coletivo (Kalecki)",
                    title_font=dict(family="Fredoka One",size=16,color="#ffd700"),
                    paper_bgcolor="rgba(13,27,42,0)",font=dict(family="Nunito",color="#e2e8f0"),
                    height=310,margin=dict(t=50,b=10,l=30,r=30),
                )
                st.plotly_chart(fig_r2, use_container_width=True)

            campeao=df_col.iloc[0]
            st.markdown(f'<div class="chip-verde" style="margin-top:.8rem;">🏆 Área mais escolhida: <b>{campeao["Área"]}</b> com <b>{int(campeao["Total"])} cartões no total</b>. Assim funciona a política real — as prioridades emergem da decisão coletiva.</div>', unsafe_allow_html=True)

            if any("escolaridade" in r for r in dados):
                st.markdown("#### 📚 Prioridade principal por escolaridade")
                rows2=[]
                for reg in dados:
                    if "escolaridade" not in reg: continue
                    ma=max(reg["distribuicao"],key=reg["distribuicao"].get)
                    rows2.append({"Escolaridade":reg["escolaridade"].split("(")[0].strip(),"Prioridade":ma})
                if rows2:
                    df_esc=pd.DataFrame(rows2)
                    fig_esc=px.histogram(df_esc,x="Escolaridade",color="Prioridade",
                        color_discrete_map={k:GASTOS.get(k,{"cor":"#999"})["cor"] for k in GASTOS},
                        title="Maior prioridade por escolaridade",barmode="stack")
                    fig_esc.update_layout(paper_bgcolor="rgba(13,27,42,0)",plot_bgcolor="rgba(30,41,59,0.4)",
                        font=dict(family="Nunito",color="#e2e8f0"),title_font=dict(family="Fredoka One",size=16,color="#ffd700"))
                    st.plotly_chart(fig_esc, use_container_width=True)

    # ── TAB 4 ────────────────────────────────────────────────────────────────
    with tab4:
        dados=carregar_dados()
        if dados:
            rows=[]
            for reg in dados:
                row={"Nome":reg["nome"],"Idade":reg.get("idade","—"),
                     "Escolaridade":reg.get("escolaridade","—"),
                     "Hora":reg["timestamp"][:16].replace("T"," ")}
                row.update(reg["distribuicao"]); rows.append(row)
            df_tab=pd.DataFrame(rows)
            st.dataframe(df_tab,use_container_width=True,hide_index=True)
            csv=df_tab.to_csv(index=False).encode("utf-8")
            st.download_button("⬇️ Baixar dados da Semana Rural (CSV)",data=csv,file_name="orcamento_semana_rural.csv",mime="text/csv")
        else:
            st.info("Nenhuma resposta ainda.")

    # ══════════════════════════════════════════════════════════════
    # BLOCO EDUCATIVO — Arcabouço Fiscal, Restrição e Kalecki
    # ══════════════════════════════════════════════════════════════
    st.markdown("---")
    st.markdown('''<div style="font-family:Fredoka One,cursive;font-size:1.4rem;
        color:#ffd700;margin-bottom:.8rem;">🏦 Para pensar além do jogo</div>''',
        unsafe_allow_html=True)

    def card_edu(emoji, titulo, cor_borda, conteudo):
        return f'''<div style="background:linear-gradient(135deg,#1e293b,#0f172a);
            border-radius:16px;padding:1.4rem 1.6rem;margin-bottom:1rem;
            border-left:5px solid {cor_borda};
            box-shadow:0 4px 20px rgba(0,0,0,.4);">
          <div style="font-family:Fredoka One,cursive;font-size:1.05rem;
               color:{cor_borda};margin-bottom:.7rem;">{emoji} {titulo}</div>
          <div style="font-size:.9rem;color:#cbd5e1;line-height:1.75;">{conteudo}</div>
        </div>'''

    bloco1 = card_edu("🖨️", "O governo emite a própria moeda — então por que tem limite?", "#3b82f6", """
O governo brasileiro emite o <b style='color:#ffd700'>Real</b>. Diferente de você ou de uma empresa,
ele nunca pode "ficar sem dinheiro" na própria moeda — ele a cria. Isso é chamado de
<b style='color:#93c5fd'>soberania monetária</b>: o Estado é o emissor, não o usuário da moeda.<br><br>
Então por que o jogo tem apenas 5 cartões? Porque o governo
<b style='color:#f472b6'>escolhe se impor um limite</b>. Esse limite é uma decisão política,
não uma lei da natureza — e entender isso muda tudo na discussão sobre orçamento público.
""")

    bloco2 = card_edu("📜", "O que é o Arcabouço Fiscal?", "#8b5cf6", """
O <b style='color:#a78bfa'>Arcabouço Fiscal</b> é o conjunto de regras que o governo brasileiro
adotou em 2023 para limitar seus gastos. Ele define que as despesas só podem crescer até
<b style='color:#ffd700'>70% da variação da receita</b> e que o déficit primário precisa ser
zerado num prazo determinado.<br><br>
Na prática: mesmo que o governo queira gastar mais em saúde ou educação,
o arcabouço <b style='color:#f87171'>proíbe</b> — a menos que a arrecadação cresça primeiro.
É como se você tivesse dinheiro no bolso mas uma regra impedisse de usá-lo.<br><br>
Apoiadores dizem que isso <b style='color:#4ade80'>gera confiança dos investidores</b> e
controla a inflação. Críticos dizem que é uma
<b style='color:#f87171'>camisa de força que sacrifica serviços públicos</b>
para agradar ao mercado financeiro.
""")

    bloco3 = card_edu("⚖️", "A restrição orçamentária: lei da natureza ou escolha política?", "#ec4899", """
Quando um político diz <i>"não tem dinheiro para saúde"</i>, isso é
<b style='color:#f472b6'>tecnicamente falso</b> para um governo emissor de moeda.
O que existe é uma <b style='color:#fbbf24'>restrição política escolhida</b>: regras, leis e
acordos que o próprio Estado criou e pode modificar.<br><br>
A discussão real é outra: <b style='color:#93c5fd'>gastar mais gera inflação?</b>
Depende. Se há capacidade produtiva ociosa — trabalhadores desempregados, fábricas paradas —
gastar mais gera emprego e renda <i>sem</i> inflação. Se a economia já está no limite,
gastar mais sobe preços. Esse é o verdadeiro debate, não "tem ou não tem dinheiro".
""")

    bloco4 = card_edu("🔬", "O que Kalecki diria sobre tudo isso?", "#22c55e", """
Michal Kalecki (1899–1970) foi um dos primeiros economistas a perceber que
<b style='color:#4ade80'>o pleno emprego é tecnicamente possível</b> — mas politicamente indesejável
para parte da elite econômica.<br><br>
Seu argumento central: se o governo gasta e mantém pleno emprego,
os trabalhadores <b style='color:#fbbf24'>perdem o medo de serem demitidos</b> e passam a
reivindicar mais salários e direitos. Isso <i>reduz o poder dos patrões</i>.
Por isso, para Kalecki, a preferência pelo "equilíbrio fiscal" não é técnica —
é <b style='color:#f472b6'>uma escolha de classe</b>: manter o desemprego como disciplinador
da força de trabalho.<br><br>
O arcabouço fiscal, nessa leitura, não é neutro. É um mecanismo que
<b style='color:#93c5fd'>prioriza a confiança do mercado financeiro</b> em detrimento do
investimento público que reduziria desigualdade e ampliaria o consumo popular —
exatamente os multiplicadores que Kalecki mais valorizava.
""")

    bloco5 = card_edu("💡", "O que o jogo não consegue mostrar — mas a vida real mostra", "#fbbf24", """
No jogo, você tinha 5 cartões fixos e 7 áreas. Na vida real, o governo pode
<b style='color:#ffd700'>criar mais cartões</b> — mas escolhe não fazer isso por razões políticas.<br><br>
O Brasil gasta hoje mais de <b style='color:#f87171'>40% do orçamento com juros e amortização da dívida</b>.
Isso significa que, a cada R$1 arrecadado em impostos, quase R$0,45 vai para bancos e
investidores antes de chegar em saúde, educação ou moradia.<br><br>
A pergunta que Kalecki deixou para a história não é técnica.
É política: <b style='color:#a78bfa'>"A quem serve o orçamento público?"</b><br>
<i style='color:#64748b'>Essa é a pergunta que este jogo quer te ajudar a fazer.</i>
""")

    st.markdown(bloco1 + bloco2 + bloco3 + bloco4 + bloco5, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div style="background:#1e293b;border-radius:14px;padding:.8rem 1.2rem;border:1px solid #334155;margin-bottom:.5rem;"><div style="font-family:Fredoka One,cursive;color:#94a3b8;font-size:.85rem;text-align:center;margin-bottom:.6rem;">O que deseja fazer agora?</div></div>', unsafe_allow_html=True)
    col_r1,col_r2=st.columns(2)
    with col_r1:
        if st.button("🔄 Jogar de novo", use_container_width=True):
            st.session_state.pagina="inicio"
            st.session_state.distribuicao={k:0 for k in GASTOS}
            st.session_state.enviado=False; st.rerun()
    with col_r2:
        if st.button("🔁 Atualizar resultado coletivo", use_container_width=True):
            st.rerun()