import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import os
from datetime import datetime

# Configuração
st.set_page_config(page_title="Acompanhamento de Produção REDE 150", layout="wide")

def listar_arquivos_json(pasta='data'):
    """Lista todos os arquivos JSON na pasta"""
    if not os.path.exists(pasta):
        os.makedirs(pasta, exist_ok=True)
    
    arquivos = [f for f in os.listdir(pasta) if f.endswith('.json')]
    return sorted(arquivos, reverse=True)  # Mais recentes primeiro

def carregar_dados(arquivo):
    """Carrega dados do arquivo JSON selecionado"""
    try:
        with open(f'data/{arquivo}', 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Erro ao carregar {arquivo}: {str(e)}")
        return None

def criar_novo_arquivo():
    """Cria um novo arquivo JSON com dados padrão"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nome_arquivo = f"producao_{timestamp}.json"
    
    dados_padrao = {
        "periodo": {
            "inicio": datetime.now().strftime("%d/%m/%Y"),
            "fim": datetime.now().strftime("%d/%m/%Y")
        },
        "totais_periodo": {
            "producao_mil": 0,
            "receita_mil": 0
        },
        "equipes": {
            "PAULO": {
                "rede": "150",
                "producao_total": 0,
                "receita_total": 0,
                "meta_mes_percentual": 0,
                "producao_diaria": [0] * 31,
                "ativo": False
            },
            "ELANIO": {
                "rede": "150", 
                "producao_total": 0,
                "receita_total": 0,
                "meta_mes_percentual": 0,
                "producao_diaria": [0] * 31,
                "ativo": False
            },
            "HUMBERTO": {
                "rede": "150",
                "producao_total": 0,
                "receita_total": 0,
                "meta_mes_percentual": 0,
                "producao_diaria": [0] * 31,
                "ativo": False
            },
            "FABIO": {
                "rede": "150",
                "producao_total": 0,
                "receita_total": 0,
                "meta_mes_percentual": 0,
                "producao_diaria": [0] * 31,
                "ativo": False
            }
        },
        "configuracoes": {
            "meta_diaria_minima": 40,
            "meta_diaria_boa": 60,
            "meta_mensal_target": 90,
            "cores": {
                "baixa": "#ef4444",
                "media": "#fbbf24",
                "alta": "#22c55e"
            }
        }
    }
    
    with open(f'data/{nome_arquivo}', 'w', encoding='utf-8') as f:
        json.dump(dados_padrao, f, indent=2, ensure_ascii=False)
    
    return nome_arquivo

def criar_card_equipe(nome, dados, config):
    """Cria card individual da equipe"""
    
    # Filtrar apenas os dias com dados (não zero)
    dias_com_dados = [i for i, v in enumerate(dados['producao_diaria'], 1) if v > 0]
    valores_com_dados = [v for v in dados['producao_diaria'] if v > 0]
    
    if not valores_com_dados:
        dias_com_dados = list(range(1, 8))  # Mostrar 7 dias por padrão
        valores_com_dados = [0] * 7
    
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
        yaxis=dict(title="Produção", range=[0, max(120, max(valores_com_dados) + 20) if valores_com_dados else 120]),
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
    # Sidebar para seleção de arquivo
    with st.sidebar:
        st.header("📁 Gerenciar Arquivos")
        
        # Listar arquivos JSON
        arquivos = listar_arquivos_json()
        
        if not arquivos:
            st.warning("Nenhum arquivo JSON encontrado na pasta 'data'")
            if st.button("➕ Criar Primeiro Arquivo"):
                nome_novo = criar_novo_arquivo()
                st.success(f"Arquivo {nome_novo} criado!")
                st.rerun()
            return
        
        # Seletor de arquivo
        arquivo_selecionado = st.selectbox(
            "📄 Selecionar Arquivo",
            arquivos,
            help="Escolha o arquivo JSON com os dados a exibir"
        )
        
        # Botões de ação
        col1, col2 = st.columns(2)
        with col1:
            if st.button("➕ Novo"):
                nome_novo = criar_novo_arquivo()
                st.success(f"Arquivo {nome_novo} criado!")
                st.rerun()
        
        with col2:
            if st.button("🔄 Recarregar"):
                st.rerun()
        
        # Upload de arquivo
        st.subheader("📤 Upload JSON")
        arquivo_upload = st.file_uploader(
            "Carregar arquivo JSON",
            type=['json'],
            help="Faça upload de um arquivo JSON com dados de produção"
        )
        
        if arquivo_upload:
            try:
                dados_upload = json.load(arquivo_upload)
                nome_arquivo = f"upload_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                
                with open(f'data/{nome_arquivo}', 'w', encoding='utf-8') as f:
                    json.dump(dados_upload, f, indent=2, ensure_ascii=False)
                
                st.success(f"Arquivo salvo como {nome_arquivo}")
                st.rerun()
            except Exception as e:
                st.error(f"Erro no upload: {str(e)}")
    
    # Carregar dados do arquivo selecionado
    if not arquivos:
        return
        
    dados = carregar_dados(arquivo_selecionado)
    if not dados:
        return

    # Header principal
    periodo_texto = f"{dados['periodo']['inicio']} - {dados['periodo']['fim']}"
    st.markdown(f"""
    <div style="background: linear-gradient(90deg, #1e3a8a 0%, #3b82f6 100%); padding: 20px; border-radius: 10px; margin-bottom: 20px;">
        <h1 style="color: white; margin: 0; font-size: 28px;">🏗️ Acompanhamento de Produção REDE 150</h1>
        <p style="color: #e0e7ff; margin: 5px 0 0 0;">{periodo_texto}</p>
        <p style="color: #bfdbfe; margin: 5px 0 0 0; font-size: 14px;">📄 Arquivo: {arquivo_selecionado}</p>
    </div>
    """, unsafe_allow_html=True)

    # Métricas principais
    col1, col2 = st.columns(2)
    with col1:
        st.metric("🎯 Produção Total do Período", f"{dados['totais_periodo']['producao_mil']} Mil", delta="Metros")
    with col2:
        st.metric("💰 Receita Total do Período", f"R$ {dados['totais_periodo']['receita_mil']} Mil", delta="Reais")

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
                if equipe_dados['ativo']:
                    st.metric("Produção", f"{equipe_dados['producao_total']:.2f}", delta="Metros")
                else:
                    st.metric("Produção", "(Em branco)", delta="Metros")
            
            with col_rec:
                if equipe_dados['ativo']:
                    st.metric("Receita", f"R$ {equipe_dados['receita_total']:.3f}", delta="Mil")
                else:
                    st.metric("Receita", "(Em branco)", delta="Mil")
            
            # Gráficos
            if equipe_dados['ativo']:
                fig_barras, fig_gauge = criar_card_equipe(nome, equipe_dados, dados['configuracoes'])
                
                st.plotly_chart(fig_barras, use_container_width=True, key=f"barras_{nome}_{arquivo_selecionado}")
                
                # Métricas adicionais
                col_prod2, col_rec2 = st.columns(2)
                with col_prod2:
                    st.metric("Produção do mês", f"{equipe_dados['producao_total']:.2f}")
                with col_rec2:
                    st.metric("Receita do mês", f"R$ {equipe_dados['receita_total']:.2f} Mil")
                
                st.plotly_chart(fig_gauge, use_container_width=True, key=f"gauge_{nome}_{arquivo_selecionado}")
            else:
                # Para equipes em branco
                st.markdown("""
                <div style="height: 200px; background: #f8fafc; border: 2px dashed #cbd5e1; border-radius: 8px; 
                            display: flex; align-items: center; justify-content: center; margin: 20px 0;">
                    <p style="color: #64748b; font-size: 16px;">(Em branco)</p>
                </div>
                """, unsafe_allow_html=True)
                
                st.metric("Produção do mês", "(Em branco)")
                st.metric("Receita do mês", "(Em branco)")
                
                st.markdown("""
                <div style="height: 180px; background: #f8fafc; border: 2px dashed #cbd5e1; border-radius: 8px; 
                            display: flex; align-items: center; justify-content: center;">
                    <p style="color: #64748b;">(Em branco)</p>
                </div>
                """, unsafe_allow_html=True)

    # Resumo consolidado
    st.divider()
    st.subheader("📊 Resumo Consolidado")

    col1, col2, col3 = st.columns(3)

    with col1:
        # Ranking de produção
        ranking_prod = [(nome, equipe['producao_total']) for nome, equipe in dados['equipes'].items() if equipe['ativo']]
        ranking_prod.sort(key=lambda x: x[1], reverse=True)
        
        st.markdown("**🏆 Ranking Produção**")
        for i, (nome, prod) in enumerate(ranking_prod):
            st.write(f"{i+1}. {nome}: {prod:.0f}m")

    with col2:
        # Ranking de receita
        ranking_rec = [(nome, equipe['receita_total']) for nome, equipe in dados['equipes'].items() if equipe['ativo']]
        ranking_rec.sort(key=lambda x: x[1], reverse=True)
        
        st.markdown("**💰 Ranking Receita**")
        for i, (nome, rec) in enumerate(ranking_rec):
            st.write(f"{i+1}. {nome}: R$ {rec:.1f}k")

    with col3:
        # Performance geral
        total_prod_equipes = sum([equipe['producao_total'] for equipe in dados['equipes'].values() if equipe['ativo']])
        total_rec_equipes = sum([equipe['receita_total'] for equipe in dados['equipes'].values() if equipe['ativo']])
        equipes_ativas = len([equipe for equipe in dados['equipes'].values() if equipe['ativo']])
        
        st.markdown("**📈 Performance Geral**")
        st.write(f"Total Produção: {total_prod_equipes:.0f}m")
        st.write(f"Total Receita: R$ {total_rec_equipes:.1f}k")
        st.write(f"Equipes Ativas: {equipes_ativas}/{len(dados['equipes'])}")

    # Mostrar estrutura JSON
    with st.expander("📄 Ver JSON do arquivo atual"):
        st.json(dados)

if __name__ == "__main__":
    main()