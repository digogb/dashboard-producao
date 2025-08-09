from flask import Flask, render_template_string
import plotly.graph_objects as go
import plotly.express as px
from plotly.utils import PlotlyJSONEncoder
import json

app = Flask(__name__)

# Dados embutidos
dados_exemplo = {
    "producao_01_08_2025": {
        "periodo": {"inicio": "01/08/2025", "fim": "01/08/2025"},
        "totais_periodo": {"producao_mil": 0.084, "receita_mil": 0},
        "equipes": {
            "PAULO": {
                "rede": "150", "producao_total": 66, "receita_total": 0,
                "meta_mes_percentual": 0, "producao_diaria": [66],
                "ligacao": 0, "pv": 0, "observacoes": "", "ativo": True
            },
            "ERLANIO": {
                "rede": "150", "producao_total": 18, "receita_total": 0,
                "meta_mes_percentual": 0, "producao_diaria": [18],
                "ligacao": 0, "pv": 0, "observacoes": "", "ativo": True
            },
            "HUMBERTO": {
                "rede": "150", "producao_total": 0, "receita_total": 0,
                "meta_mes_percentual": 0, "producao_diaria": [0],
                "ligacao": 0, "pv": 1, "observacoes": "", "ativo": True
            },
            "JUAREZ": {
                "rede": "150", "producao_total": 0, "receita_total": 0,
                "meta_mes_percentual": 0, "producao_diaria": [0],
                "ligacao": 6, "pv": 0, "observacoes": "", "ativo": True
            },
            "FABIO": {
                "rede": "150", "producao_total": 0, "receita_total": 0,
                "meta_mes_percentual": 0, "producao_diaria": [0],
                "ligacao": 0, "pv": 2, "observacoes": "", "ativo": True
            }
        },
        "totais_diarios": {"rede": 84, "ligacao": 6, "pv": 3},
        "producao_acumulada": {
            "rede_total": 6724, "rede_agosto": 84,
            "ligacao_total": 470, "ligacao_julho": 6
        }
    },
    "producao_04_08_2025": {
        "periodo": {"inicio": "04/08/2025", "fim": "04/08/2025"},
        "totais_periodo": {"producao_mil": 0.054, "receita_mil": 0},
        "equipes": {
            "PAULO": {
                "rede": "150", "producao_total": 0, "receita_total": 0,
                "meta_mes_percentual": 0, "producao_diaria": [0],
                "ligacao": 0, "pv": 0, "observacoes": "Regularização de trecho", "ativo": True
            },
            "ERLANIO": {
                "rede": "150", "producao_total": 6, "receita_total": 0,
                "meta_mes_percentual": 0, "producao_diaria": [6],
                "ligacao": 0, "pv": 0, "observacoes": "", "ativo": True
            },
            "HUMBERTO": {
                "rede": "150", "producao_total": 48, "receita_total": 0,
                "meta_mes_percentual": 0, "producao_diaria": [48],
                "ligacao": 0, "pv": 0, "observacoes": "", "ativo": True
            },
            "JUAREZ": {
                "rede": "150", "producao_total": 0, "receita_total": 0,
                "meta_mes_percentual": 0, "producao_diaria": [0],
                "ligacao": 10, "pv": 0, "observacoes": "", "ativo": True
            },
            "FABIO": {
                "rede": "150", "producao_total": 0, "receita_total": 0,
                "meta_mes_percentual": 0, "producao_diaria": [0],
                "ligacao": 0, "pv": 1, "observacoes": "", "ativo": True
            }
        },
        "totais_diarios": {"rede": 54, "ligacao": 10, "pv": 1},
        "producao_acumulada": {
            "rede_total": 6778, "rede_agosto": 138,
            "ligacao_total": 480, "ligacao_julho": 16
        }
    },
    "producao_05_08_2025": {
        "periodo": {"inicio": "05/08/2025", "fim": "05/08/2025"},
        "totais_periodo": {"producao_mil": 0.170, "receita_mil": 0},
        "equipes": {
            "PAULO": {
                "rede": "150", "producao_total": 36, "receita_total": 0,
                "meta_mes_percentual": 0, "producao_diaria": [36],
                "ligacao": 0, "pv": 0, "observacoes": "", "ativo": True
            },
            "ERLANIO": {
                "rede": "150", "producao_total": 0, "receita_total": 0,
                "meta_mes_percentual": 0, "producao_diaria": [0],
                "ligacao": 0, "pv": 1, "observacoes": "", "ativo": True
            },
            "HUMBERTO": {
                "rede": "150", "producao_total": 66, "receita_total": 0,
                "meta_mes_percentual": 0, "producao_diaria": [66],
                "ligacao": 0, "pv": 0, "observacoes": "", "ativo": True
            },
            "JUAREZ": {
                "rede": "150", "producao_total": 0, "receita_total": 0,
                "meta_mes_percentual": 0, "producao_diaria": [0],
                "ligacao": 6, "pv": 0, "observacoes": "", "ativo": True
            },
            "FABIO": {
                "rede": "150", "producao_total": 68, "receita_total": 0,
                "meta_mes_percentual": 0, "producao_diaria": [68],
                "ligacao": 0, "pv": 0, "observacoes": "", "ativo": True
            }
        },
        "totais_diarios": {"rede": 170, "ligacao": 6, "pv": 1},
        "producao_acumulada": {
            "rede_total": 6821, "rede_agosto": 306,
            "ligacao_total": 486, "ligacao_julho": 22
        }
    },
    "producao_06_08_2025": {
        "periodo": {"inicio": "06/08/2025", "fim": "06/08/2025"},
        "totais_periodo": {"producao_mil": 0.072, "receita_mil": 0},
        "equipes": {
            "PAULO": {
                "rede": "150", "producao_total": 18, "receita_total": 0,
                "meta_mes_percentual": 0, "producao_diaria": [18],
                "ligacao": 0, "pv": 0, "observacoes": "", "ativo": True
            },
            "ERLANIO": {
                "rede": "150", "producao_total": 6, "receita_total": 0,
                "meta_mes_percentual": 0, "producao_diaria": [6],
                "ligacao": 0, "pv": 0, "observacoes": "", "ativo": True
            },
            "HUMBERTO": {
                "rede": "150", "producao_total": 48, "receita_total": 0,
                "meta_mes_percentual": 0, "producao_diaria": [48],
                "ligacao": 0, "pv": 0, "observacoes": "", "ativo": True
            },
            "JUAREZ": {
                "rede": "150", "producao_total": 0, "receita_total": 0,
                "meta_mes_percentual": 0, "producao_diaria": [0],
                "ligacao": 10, "pv": 0, "observacoes": "", "ativo": True
            },
            "FABIO": {
                "rede": "150", "producao_total": 0, "receita_total": 0,
                "meta_mes_percentual": 0, "producao_diaria": [0],
                "ligacao": 0, "pv": 0, "observacoes": "Ajuda com limpeza de trecho", "ativo": True
            }
        },
        "totais_diarios": {"rede": 72, "ligacao": 10, "pv": 0},
        "producao_acumulada": {
            "rede_total": 6893, "rede_agosto": 378,
            "ligacao_total": 496, "ligacao_julho": 32
        }
    }
}

def criar_graficos(dados):
    """Cria gráficos para o dashboard"""
    graficos = {}
    
    # Gráfico de barras - produção por equipe
    equipes = []
    rede_valores = []
    ligacao_valores = []
    
    for nome, equipe in dados['equipes'].items():
        equipes.append(nome)
        rede_valores.append(equipe['producao_total'])
        ligacao_valores.append(equipe['ligacao'])
    
    fig_barras = go.Figure()
    fig_barras.add_trace(go.Bar(x=equipes, y=rede_valores, name='Rede (m)', marker_color='lightblue'))
    fig_barras.add_trace(go.Bar(x=equipes, y=ligacao_valores, name='Ligações', marker_color='lightgreen'))
    fig_barras.update_layout(title='Produção por Equipe', barmode='group', height=400)
    
    graficos['barras'] = json.dumps(fig_barras, cls=PlotlyJSONEncoder)
    
    # Gráfico de pizza - distribuição da rede
    equipes_rede = [nome for nome, equipe in dados['equipes'].items() if equipe['producao_total'] > 0]
    valores_rede = [equipe['producao_total'] for equipe in dados['equipes'].values() if equipe['producao_total'] > 0]
    
    if valores_rede:
        fig_pizza = px.pie(values=valores_rede, names=equipes_rede, title='Distribuição da Rede')
        graficos['pizza'] = json.dumps(fig_pizza, cls=PlotlyJSONEncoder)
    else:
        graficos['pizza'] = None
    
    return graficos

@app.route('/')
def dashboard():
    # Por padrão, mostrar o primeiro período
    dados = dados_exemplo['producao_01_08_2025']
    graficos = criar_graficos(dados)
    
    return render_template_string(TEMPLATE_HTML, 
                                dados=dados, 
                                graficos=graficos,
                                periodos=dados_exemplo,
                                periodo_atual='producao_01_08_2025')

@app.route('/periodo/<periodo_id>')
def dashboard_periodo(periodo_id):
    if periodo_id in dados_exemplo:
        dados = dados_exemplo[periodo_id]
        graficos = criar_graficos(dados)
        
        return render_template_string(TEMPLATE_HTML, 
                                    dados=dados, 
                                    graficos=graficos,
                                    periodos=dados_exemplo,
                                    periodo_atual=periodo_id)
    else:
        return "Período não encontrado", 404

# Template HTML
TEMPLATE_HTML = '''
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard de Produção REDE 150</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
    <style>
        .gradient-bg {
            background: linear-gradient(90deg, #1e3a8a 0%, #3b82f6 100%);
        }
    </style>
</head>
<body class="bg-gray-100">
    <div class="container mx-auto px-4 py-6">
        <!-- Header -->
        <div class="gradient-bg rounded-lg p-6 mb-6 text-white">
            <h1 class="text-3xl font-bold mb-2">🏗️ Acompanhamento de Produção REDE 150</h1>
            <p class="text-blue-200">{{dados.periodo.inicio}} - {{dados.periodo.fim}}</p>
            <p class="text-blue-300 text-sm">🌐 Deploy Vercel com Flask</p>
        </div>

        <!-- Seletor de Período -->
        <div class="bg-white rounded-lg p-4 mb-6">
            <h3 class="text-lg font-semibold mb-3">📅 Selecionar Período:</h3>
            <div class="flex gap-2 flex-wrap">
                {% for periodo_id, periodo_data in periodos.items() %}
                <a href="/periodo/{{periodo_id}}" 
                   class="px-4 py-2 rounded {% if periodo_id == periodo_atual %}bg-blue-500 text-white{% else %}bg-gray-200 text-gray-700 hover:bg-blue-100{% endif %}">
                    {{periodo_data.periodo.inicio}}
                </a>
                {% endfor %}
            </div>
        </div>

        <!-- Métricas Principais -->
        <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
            <div class="bg-blue-500 text-white rounded-lg p-4">
                <h3 class="text-lg font-semibold">🎯 Rede Diária</h3>
                <p class="text-2xl font-bold">{{dados.totais_diarios.rede}} m</p>
            </div>
            <div class="bg-green-500 text-white rounded-lg p-4">
                <h3 class="text-lg font-semibold">🔗 Ligações Diárias</h3>
                <p class="text-2xl font-bold">{{dados.totais_diarios.ligacao}}</p>
            </div>
            <div class="bg-purple-500 text-white rounded-lg p-4">
                <h3 class="text-lg font-semibold">📊 PV Diário</h3>
                <p class="text-2xl font-bold">{{dados.totais_diarios.pv}}</p>
            </div>
            <div class="bg-orange-500 text-white rounded-lg p-4">
                <h3 class="text-lg font-semibold">📈 Rede Total</h3>
                <p class="text-2xl font-bold">{{dados.producao_acumulada.rede_total}} m</p>
            </div>
        </div>

        <!-- Cards das Equipes -->
        <div class="grid grid-cols-1 md:grid-cols-5 gap-4 mb-6">
            {% for nome, equipe in dados.equipes.items() %}
            <div class="bg-white rounded-lg p-4 border-l-4 border-blue-500">
                <h3 class="text-xl font-bold text-blue-800">{{nome}}</h3>
                <p class="text-gray-600 text-sm mb-3">Rede {{equipe.rede}}</p>
                
                <div class="space-y-2">
                    <div class="flex justify-between">
                        <span class="text-gray-600">Rede:</span>
                        <span class="font-semibold">{{equipe.producao_total}} m</span>
                    </div>
                    <div class="flex justify-between">
                        <span class="text-gray-600">Ligações:</span>
                        <span class="font-semibold">{{equipe.ligacao}}</span>
                    </div>
                    {% if equipe.pv > 0 %}
                    <div class="flex justify-between">
                        <span class="text-gray-600">PV:</span>
                        <span class="font-semibold">{{equipe.pv}}</span>
                    </div>
                    {% endif %}
                    {% if equipe.observacoes %}
                    <div class="bg-blue-50 p-2 rounded text-sm">
                        <strong>📝 Obs:</strong> {{equipe.observacoes}}
                    </div>
                    {% endif %}
                </div>
            </div>
            {% endfor %}
        </div>

        <!-- Gráficos -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
            <div class="bg-white rounded-lg p-6">
                <div id="grafico-barras"></div>
            </div>
            {% if graficos.pizza %}
            <div class="bg-white rounded-lg p-6">
                <div id="grafico-pizza"></div>
            </div>
            {% endif %}
        </div>

        <!-- Resumo -->
        <div class="bg-white rounded-lg p-6">
            <h3 class="text-xl font-semibold mb-4">📊 Resumo do Período</h3>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div>
                    <h4 class="font-semibold text-blue-800 mb-2">🏆 Ranking Rede</h4>
                    {% set ranking_rede = dados.equipes.items() | selectattr('1.producao_total', '>', 0) | sort(attribute='1.producao_total', reverse=true) | list %}
                    {% for nome, equipe in ranking_rede %}
                    <p>{{loop.index}}. {{nome}}: {{equipe.producao_total}}m</p>
                    {% endfor %}
                </div>
                <div>
                    <h4 class="font-semibold text-green-800 mb-2">🔗 Ranking Ligações</h4>
                    {% set ranking_ligacao = dados.equipes.items() | selectattr('1.ligacao', '>', 0) | sort(attribute='1.ligacao', reverse=true) | list %}
                    {% for nome, equipe in ranking_ligacao %}
                    <p>{{loop.index}}. {{nome}}: {{equipe.ligacao}}</p>
                    {% endfor %}
                </div>
                <div>
                    <h4 class="font-semibold text-purple-800 mb-2">📊 Ranking PV</h4>
                    {% set ranking_pv = dados.equipes.items() | selectattr('1.pv', '>', 0) | sort(attribute='1.pv', reverse=true) | list %}
                    {% for nome, equipe in ranking_pv %}
                    <p>{{loop.index}}. {{nome}}: {{equipe.pv}}</p>
                    {% endfor %}
                </div>
            </div>
        </div>
    </div>

    <script>
        // Renderizar gráfico de barras
        var graficoBarra = {{graficos.barras|safe}};
        Plotly.newPlot('grafico-barras', graficoBarra.data, graficoBarra.layout);

        // Renderizar gráfico de pizza se existir
        {% if graficos.pizza %}
        var graficoPizza = {{graficos.pizza|safe}};
        Plotly.newPlot('grafico-pizza', graficoPizza.data, graficoPizza.layout);
        {% endif %}
    </script>
</body>
</html>
'''

if __name__ == '__main__':
    app.run(debug=True)