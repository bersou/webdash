import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import dash_bootstrap_components as dbc
import plotly.io as pio

# --- CORREÇÃO FINAL: Usar o tema escuro padrão 'plotly_dark' ---
pio.templates.default = "plotly_dark"
# ----------------------------------------------------------------

# --- 1. Carregar e Preparar os Dados ---
try:
    df = pd.read_csv('dados_consolidados.csv')
    df['Data'] = pd.to_datetime(df['Data'])
except FileNotFoundError:
    print("ERRO: O arquivo 'dados_consolidados.csv' não foi encontrado.")
    print("Por favor, crie o arquivo usando o código de preparação de dados.")
    exit()

# --- 2. Inicializar o App Dash ---
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.VAPOR],
                meta_tags=[{'name': 'viewport', 'content': 'width=device-width, initial-scale=1.0'}])
app.title = 'Dashboard de Produção Industrial'

# --- 3. Layout do Dashboard ---
app.layout = dbc.Container([
    dbc.Row(
        dbc.Col(html.H1("Dashboard de Análise de Produção Industrial",
                        className='text-center text-primary, mb-4'), width=12)
    ),
    dbc.Row([
        dbc.Col([
            html.H5("Filtro por Data", className='text-light'),
            dcc.DatePickerRange(
                id='date-picker-range',
                min_date_allowed=df['Data'].min(),
                max_date_allowed=df['Data'].max(),
                initial_visible_month=df['Data'].min(),
                start_date=df['Data'].min(),
                end_date=df['Data'].max(),
                className='w-100'
            )
        ], width=12, lg=4),
        dbc.Col([
            html.H5("Filtro por Fábrica", className='text-light'),
            dcc.Dropdown(
                id='fabrica-dropdown',
                options=[{'label': f, 'value': f} for f in df['Fabrica'].unique()],
                multi=True,
                placeholder="Selecione as fábricas"
            )
        ], width=12, lg=4),
        dbc.Col([
            html.H5("Filtro por Equipe", className='text-light'),
            dcc.Dropdown(
                id='equipe-dropdown',
                options=[{'label': e, 'value': e} for e in df['Equipe'].unique()],
                multi=True,
                placeholder="Selecione as equipes"
            )
        ], width=12, lg=4)
    ], className='mb-4'),
    dbc.Row(id='kpi-cards-row', className='mb-4'),
    dbc.Row([
        dbc.Col(dcc.Graph(id='producao-tempo-graph'), width=12, lg=8),
        dbc.Col(dcc.Graph(id='defeitos-pie-chart'), width=12, lg=4)
    ], className='mb-4'),
    dbc.Row([
        dbc.Col(dcc.Graph(id='producao-maquina-graph'), width=12, lg=6),
        dbc.Col(dcc.Graph(id='producao-operador-graph'), width=12, lg=6)
    ])
], fluid=True)

# --- 4. Callbacks para Interatividade ---
@app.callback(
    [Output('kpi-cards-row', 'children'),
     Output('producao-tempo-graph', 'figure'),
     Output('defeitos-pie-chart', 'figure'),
     Output('producao-maquina-graph', 'figure'),
     Output('producao-operador-graph', 'figure')],
    [Input('date-picker-range', 'start_date'),
     Input('date-picker-range', 'end_date'),
     Input('fabrica-dropdown', 'value'),
     Input('equipe-dropdown', 'value')]
)
def update_dashboard(start_date, end_date, selected_fabricas, selected_equipes):
    dff = df[
        (df['Data'] >= start_date) & (df['Data'] <= end_date)
    ]
    if selected_fabricas:
        dff = dff[dff['Fabrica'].isin(selected_fabricas)]
    if selected_equipes:
        dff = dff[dff['Equipe'].isin(selected_equipes)]

    if dff.empty:
        kpi_cards = dbc.Row([
            dbc.Col(dbc.Card(dbc.CardBody(html.H4("Sem dados para os filtros selecionados", className="text-danger"))))
        ])
        empty_fig = go.Figure().update_layout(
            xaxis={"visible": False}, 
            yaxis={"visible": False}, 
            annotations=[{"text": "Sem dados", "xref": "paper", "yref": "paper", "showarrow": False, "font": {"size": 20}}]
        )
        return kpi_cards, empty_fig, empty_fig, empty_fig, empty_fig

    total_produzido = dff['QuantidadeProduzida'].sum()
    total_defeitos = dff['QuantidadeDefeitos'].sum()
    taxa_defeito_media = (total_defeitos / total_produzido) * 100 if total_produzido > 0 else 0
    num_operadores = dff['ID_Operador'].nunique()
    
    kpi_cards = [
        dbc.Col(dbc.Card(dbc.CardBody([
            html.H5("Total Produzido", className="card-title"),
            html.H2(f"{total_produzido:,.0f}", className="card-text text-success")
        ])), width=6, md=3),
        dbc.Col(dbc.Card(dbc.CardBody([
            html.H5("Total de Defeitos", className="card-title"),
            html.H2(f"{total_defeitos:,.0f}", className="card-text text-danger")
        ])), width=6, md=3),
        dbc.Col(dbc.Card(dbc.CardBody([
            html.H5("Taxa de Defeito Média", className="card-title"),
            html.H2(f"{taxa_defeito_media:.2f}%", className="card-text text-warning")
        ])), width=6, md=3),
        dbc.Col(dbc.Card(dbc.CardBody([
            html.H5("Operadores Ativos", className="card-title"),
            html.H2(f"{num_operadores}", className="card-text text-info")
        ])), width=6, md=3)
    ]
    
    df_tempo = dff.groupby('Data').agg(
        Producao=('QuantidadeProduzida', 'sum'),
        Defeitos=('QuantidadeDefeitos', 'sum')
    ).reset_index()
    fig_tempo = px.line(df_tempo, x='Data', y=['Producao', 'Defeitos'],
                        title='Produção e Defeitos ao Longo do Tempo',
                        labels={'value': 'Quantidade', 'variable': 'Métrica'},
                        color_discrete_map={'Producao': '#00CFD8', 'Defeitos': '#FF4B4B'})
    fig_tempo.update_layout(title_x=0.5)

    total_ok = total_produzido - total_defeitos
    fig_pie = px.pie(
        names=['Peças OK', 'Peças com Defeito'],
        values=[total_ok, total_defeitos],
        title='Proporção Produzido vs. Defeitos',
        hole=0.4,
        color_discrete_sequence=['#00CFD8', '#FF4B4B']
    )
    fig_pie.update_layout(title_x=0.5)
    
    df_maquina = dff.groupby('NomeMaquina')['QuantidadeProduzida'].sum().sort_values(ascending=False).reset_index()
    fig_maquina = px.bar(df_maquina, x='QuantidadeProduzida', y='NomeMaquina',
                         orientation='h', title='Produção Total por Máquina',
                         color='QuantidadeProduzida', color_continuous_scale=px.colors.sequential.Teal)
    fig_maquina.update_layout(title_x=0.5, yaxis={'title': ''})

    df_operador = dff.groupby('NomeOperador')['QuantidadeProduzida'].sum().sort_values(ascending=False).reset_index()
    fig_operador = px.bar(df_operador, x='QuantidadeProduzida', y='NomeOperador',
                          orientation='h', title='Produção Total por Operador',
                          color='QuantidadeProduzida', color_continuous_scale=px.colors.sequential.Purp)
    fig_operador.update_layout(title_x=0.5, yaxis={'title': ''})

    return kpi_cards, fig_tempo, fig_pie, fig_maquina, fig_operador

# --- 5. Rodar o Servidor Local ---
if __name__ == '__main__':
    app.run(debug=True)
