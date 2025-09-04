##Dashboard de Análise de Produção Industrial##

Este projeto consiste em um dashboard web interativo para a análise de dados de produção de uma indústria automotiva. A aplicação foi construída inteiramente em Python, utilizando o framework Dash, e permite a visualização dinâmica de KPIs e a performance de máquinas e operadores.

O objetivo é transformar dados brutos e distribuídos em múltiplos arquivos CSV em uma ferramenta centralizada, visual e acionável para suportar a tomada de decisões estratégicas.

📱 Visualização do Dashboard

Aqui está uma prévia de como o dashboard se parece em um dispositivo móvel. O design é totalmente responsivo e se adapta a qualquer tamanho de tela.

https://iili.io/KBLIFKN.png

Instrução: Para que sua imagem apareça aqui, tire uma captura de tela do seu dashboard, envie para um site como o Imgur e substitua o link acima pelo link direto da sua imagem.

⚙️ Funcionalidades

· KPls Dinâmicos: Cards que exibem em tempo real o total produzido, total de defeitos, a taxa de defeito média e o número de operadores ativos no período selecionado.
· Filtros Interativos: Filtre os dados por um intervalo de datas, por fábrica ou por equipe para uma análise mais granular.
· Gráficos Detalhados:
  · Acompanhe a produção e os defeitos ao longo do tempo.
  · Analise a proporção de peças boas vs. peças defeituosas.
  · Compare a produtividade total por máquina e por operador.
· Design Moderno e Responsivo: Interface com tema escuro construída com Dash Bootstrap Components que se ajusta perfeitamente a desktops, tablets e celulares.

💻 Tecnologias Utilizadas

· Linguagem: Python 3.11+
· Manipulação de Dados: Pandas
· Dashboard e Visualização: Dash, Plotly
· Componentes e Estilo: Dash Bootstrap Components
· Servidor Web (para deploy): Gunicorn

🚀 Rodando o Projeto Localmente

Siga os passos abaixo para executar o dashboard na sua própria máquina.

Pré-requisitos

· Git instalado.
· Python 3.11 ou superior instalado.

Passo a Passo

1. Clone o repositório:

```bash
git clone https://github.com/seu-usuario/nome-do-seu-repositorio.git
```

1. Navegue até a pasta do projeto:

```bash
cd nome-do-seu-repositorio
```

1. Crie e ative um ambiente virtual (Virtual Environment):

Um ambiente virtual isola as dependências do seu projeto, o que é uma boa prática.

```bash
# Criar o ambiente
python -m venv venv

# Ativar no Windows
\venv\Scripts\activate

# Ativar no macOS/Linux
source venv/bin/activate
```

1. Instale as bibliotecas necessárias:

```bash
pip install -r requirements.txt
```

1. Execute o aplicativo:

```bash
python dashboard.py
```

1. Acesse no seu navegador: Abra seu navegador e vá para o endereçohttp://127.0.0.1:8050.

📁 Estrutura de Arquivos

```
dashboard.py           # Script principal da aplicação Dash
dados_consolidados.csv # Arquivo de dados unificado (usado pelo script)
requirements.txt       # Lista de dependências Python para instalação
README.md              # Este arquivo
```

🌐 Como Fazer o Deploy (Publicar na Web)

Este projeto está pronto para ser publicado na web usando plataformas como o Render.

1. Garanta que os 3 arquivos (dashboard.py, dados_consolidados.csv, requirements.txt) estejam no seu repositório do GitHub.
2. Crie uma conta em uma plataforma como o Render.com.
3. Crie um novo "Web Service" e conecte seu repositório do GitHub.
4. Use os seguintes comandos nas configurações:
   · Build Command: pip install -r requirements.txt
   · Start Command: gunicorn dashboard:app.server

Em poucos minutos, seu dashboard estará online com um link compartilhável!

👨‍💻 Autor

Feito com dedicação por José Bernardo

https://www.linkedin.com/in/jos%C3%A9moraesbernardo?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app
