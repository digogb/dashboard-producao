import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import os
from datetime import datetime

# Configuração
st.set_page_config(page_title="Acompanhamento de Produção REDE 150", layout="wide")

# Dados embutidos (já que Vercel não suporta upload de arquivos)
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
        },
        "configuracoes": {
            "meta_diaria_minima": 40, "meta_diaria_boa": 60,
            "meta_mensal_target": 90,
            "cores": {"baixa": "#ef4444", "media": "#fbbf24", "alta": "#22c55e"}
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
        },
        "configuracoes": {
            "meta_diaria_minima": 40, "meta_diaria_boa": 60,
            "meta_mensal_target": 90,
            "cores": {"baixa": "#ef4444", "media": "#fbbf24", "alta": "#22c55e"}
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
        },
        "configuracoes": {
            "meta_diaria_minima": 40, "meta_diaria_boa": 60,
            "meta_mensal_target": 90,
            "cores": {"baixa": "#ef4444", "media": "#fbbf24", "alta": "#22c55e"}
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
        },
        "configuracoes": {
            "meta_diaria_minima": 40, "meta_diaria_boa": 60,
            "meta_mensal_target": 90,
            "cores": {"baixa": "#ef4444", "media": "#fbbf24", "alta": "#22c55e"}
        }
    }
}

def criar_card_equipe(nome, dados, config):
    """Cria card individual da equipe"""
    valores_com_dados = dados['producao_diaria']
    if not valores_com_dados or all(v == 0 for v in valores_com_dados):
        valores_com_dados = [0]
    
    dias_com_dados = list(range(1, len(valores_com_dados) + 1))
    
    fig_barras = go.Figure()
    
    # Cores baseadas nas metas
    cores = []
    for x in valores_com_dados:
        if x < config['meta_diaria_minima']:
            cores.append(config['cores']['baixa'])
        elif x < config['meta_diaria_boa']:
            cores.append(config['cores']['media'])
        else:
            cores.append(config['cores']['alta'])
    
    fig_barras.add_trace(go.Bar(
        x=dias_com_dados,
        y=valores_com_dados,
        marker_color=cores,
        showlegend=False
    ))
    
    fig_barras.update_layout(
        height=200,
        margin=dict(l=0, r=0, t=0, b=30),
        xaxis=dict(title="Dias", tickmode='linear'),
        yaxis=dict(title="Produção", range=[0, max(120, max(valores_com_dados) + 20)]),
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    
    # Gauge de meta
    fig_gauge = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = dados['meta_mes_percentual'],
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "% da Meta do Mês"},
        delta = {'reference': 100},
        gauge = {
            'axis': {'range': [None, 100]},
            'bar': {'color': config['cores']['alta'] if dados['meta_mes_percentual'] > 80 else 
                             config['cores']['media'] if dados['meta_mes_percentual'] > 60 else 
                             config['cores']['baixa']},
            'steps': [
                {'range': [0, 50], 'color': "#fee2e2"},
                {'range': [50, 80], 'color': "#fef3c7"},
                {'range': [80, 100], 'color': "#dcfce7"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': config['meta_mensal_target']
            }
        }
    ))
    
    fig_gauge.update_layout(
        height=180,
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor='white'
    )
    
    return fig_barras, fig_gauge

def main():
    # Sidebar para seleção de período
    with st.sidebar:
        st.header("📅 Selecionar Período")
        
        periodos_disponiveis = list(dados_exemplo.keys())
        nomes_periodos = [dados_exemplo[p]['periodo']['inicio'] for p in periodos_disponiveis]
        
        periodo_selecionado = st.selectbox(
            "Escolha o período:",
            periodos_disponiveis,
            format_func=lambda x: dados_exemplo[x]['periodo']['inicio']
        )
        
        st.info("💡 Dashboard rodando no Vercel com dados de exemplo")

    # Carregar dados do período selecionado
    dados = dados_exemplo[periodo_selecionado]

    # Header principal
    periodo_texto = f"{dados['periodo']['inicio']} - {dados['periodo']['fim']}"
    st.markdown(f"""
    <div style="background: linear-gradient(90deg, #1e3a8a 0%, #3b82f6 100%); padding: 20px; border-radius: 10px; margin-bottom: 20px;">
        <h1 style="color: white; margin: 0; font-size: 28px;">🏗️ Acompanhamento de Produção REDE 150</h1>
        <p style="color: #e0e7ff; margin: 5px 0 0 0;">{periodo_texto}</p>
        <p style="color: #bfdbfe; margin: 5px 0 0 0; font-size: 14px;">🌐 Deploy Vercel</p>
    </div>
    """, unsafe_allow_html=True)

    # Métricas principais
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("🎯 Rede Diária", f"{dados['totais_diarios']['rede']} m")
    with col2:
        st.metric("🔗 Ligações Diárias", dados['totais_diarios']['ligacao'])
    with col3:
        st.metric("📊 PV Diário", dados['totais_diarios']['pv'])
    with col4:
        st.metric("📈 Rede Total", f"{dados['producao_acumulada']['rede_total']} m")

    st.divider()

    # Cards das equipes
    num_equipes = len(dados['equipes'])
    cols = st.columns(num_equipes)
    
    for i, (nome, equipe_dados) in enumerate(dados['equipes'].items()):
        with cols[i]:
            # Header da equipe
            st.markdown(f"""
            <div style="background: #f8fafc; padding: 15px; border-radius: 8px; border-left: 4px solid #3b82f6; margin-bottom: 15px;">
                <h3 style="margin: 0; color: #1e40af; font-size: 20px;">{nome}</h3>
                <p style="margin: 5px 0 0 0; color: #64748b; font-size: 14px;">Rede {equipe_dados['rede']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Métricas principais
            col_prod, col_rec = st.columns(2)
            with col_prod:
                st.metric("Rede", f"{equipe_dados['producao_total']} m")
            with col_rec:
                st.metric("Ligações", equipe_dados['ligacao'])
            
            # PV e observações
            if equipe_dados['pv'] > 0:
                st.metric("PV", equipe_dados['pv'])
            
            if equipe_dados['observacoes']:
                st.info(f"📝 {equipe_dados['observacoes']}")
            
            # Gráficos
            if equipe_dados['ativo'] and equipe_dados['producao_total'] > 0:
                fig_barras, fig_gauge = criar_card_equipe(nome, equipe_dados, dados['configuracoes'])
                st.plotly_chart(fig_barras, use_container_width=True, key=f"barras_{nome}_{periodo_selecionado}")

    # Resumo consolidado
    st.divider()
    st.subheader("📊 Resumo do Período")

    col1, col2, col3 = st.columns(3)

    with col1:
        # Ranking de produção
        ranking_prod = [(nome, equipe['producao_total']) for nome, equipe in dados['equipes'].items() if equipe['producao_total'] > 0]
        ranking_prod.sort(key=lambda x: x[1], reverse=True)
        
        st.markdown("**🏆 Ranking Rede**")
        for i, (nome, prod) in enumerate(ranking_prod):
            st.write(f"{i+1}. {nome}: {prod}m")

    with col2:
        # Ligações
        ranking_lig = [(nome, equipe['ligacao']) for nome, equipe in dados['equipes'].items() if equipe['ligacao'] > 0]
        ranking_lig.sort(key=lambda x: x[1], reverse=True)
        
        st.markdown("**🔗 Ranking Ligações**")
        for i, (nome, lig) in enumerate(ranking_lig):
            st.write(f"{i+1}. {nome}: {lig}")

    with col3:
        # PVs
        ranking_pv = [(nome, equipe['pv']) for nome, equipe in dados['equipes'].items() if equipe['pv'] > 0]
        ranking_pv.sort(key=lambda x: x[1], reverse=True)
        
        st.markdown("**📊 Ranking PV**")
        for i, (nome, pv) in enumerate(ranking_pv):
            st.write(f"{i+1}. {nome}: {pv}")

    # Dados do período
    with st.expander("📄 Dados completos do período"):
        st.json(dados)

if __name__ == "__main__":
    main()