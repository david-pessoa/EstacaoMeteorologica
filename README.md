# Estação Meteorológica

Aplicação web em Django que exibe um dashboard meteorológico com dados atuais e previsão dos próximos dias. O usuário pode pesquisar uma cidade, visualizar temperatura, sensação térmica, condição do tempo, vento, umidade, pressão, previsão horária do dia e resumo dos dias seguintes.

Os dados meteorológicos são obtidos pela WeatherAPI e apresentados em uma interface com Bootstrap, ícones SVG e gráfico de temperatura com Chart.js.

## Funcionalidades

- Consulta de clima por cidade usando o parâmetro `local` na URL.
- Cidade padrão: `São Paulo`.
- Exibição de temperatura atual, sensação térmica, condição do tempo, vento, umidade e pressão.
- Gráfico com a temperatura hora a hora do dia atual.
- Previsão resumida dos próximos dias, com chance de chuva, ícone do tempo, máxima e mínima.
- Autocomplete com cidades cadastradas no banco.
- Alternância visual entre tema escuro e claro.
- Área administrativa do Django para gerenciar cidades.
- Páginas de erro para local inexistente e erros HTTP.

## Principais ferramentas utilizadas

- **Django 5**: framework principal do projeto. Foi escolhido por oferecer estrutura completa para rotas, templates, views, models, administração e configuração de arquivos estáticos.
- **WeatherAPI**: fonte dos dados meteorológicos em tempo real e de previsão. Permite consultar cidades e retornar informações detalhadas de clima.
- **SQLite**: banco de dados usado na configuração atual, suficiente para um projeto pequeno e simples de executar localmente.
- **python-decouple**: leitura de variáveis sensíveis a partir do arquivo `.env`, evitando credenciais diretamente no código.
- **requests**: biblioteca usada para fazer as requisições HTTP para a WeatherAPI.
- **pytz**: tratamento de fuso horário da estação meteorológica retornada pela API.
- **Bootstrap e django-bootstrap5**: base visual da interface, com componentes responsivos e integração com templates Django.
- **Chart.js**: renderização do gráfico de temperatura do dia.
- **Gunicorn**: servidor WSGI usado no container para executar a aplicação Django em ambiente de produção.
- **Nginx**: proxy reverso na frente do Gunicorn, recebendo as requisições HTTP na porta 80.
- **WhiteNoise**: suporte para servir arquivos estáticos da aplicação Django.
- **Docker e Docker Compose**: empacotamento da aplicação e do proxy em containers, simplificando a execução em servidor.

## Rotas

| Rota | Descrição |
| --- | --- |
| `/` | Dashboard principal. Sem parâmetros, consulta `São Paulo`. |
| `/?local=<cidade>` | Dashboard principal consultando a cidade informada. Exemplo: `/?local=Rio%20de%20Janeiro`. |
| `/admin/` | Painel administrativo do Django para gerenciar registros, incluindo cidades cadastradas. |

Quando a WeatherAPI retorna erro para a cidade pesquisada, a aplicação renderiza a página `local_inexistente.html`.

## Pré-requisitos

- Python 3.11 ou superior.
- Chave de API da WeatherAPI.
- Docker e Docker Compose, caso prefira executar com containers.

## Configuração local com ambiente virtual

### 1. Clone o repositório

```bash
git clone https://github.com/david-pessoa/EstacaoMeteorologica.git
cd EstacaoMeteorologica
```

### 2. Crie e ative o ambiente virtual

```bash
python3 -m venv venv
```

Linux ou macOS:

```bash
source venv/bin/activate
```

Windows PowerShell:

```powershell
venv\Scripts\Activate.ps1
```

Windows CMD:

```bat
venv\Scripts\activate.bat
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto. Você pode usar o `.env.example` como base.

Para gerar uma `SECRET_KEY`, execute:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Exemplo de `.env`:

```env
SECRET_KEY='sua-chave-secreta'
DEBUG=True
API_KEY='sua-chave-da-weatherapi'
```

### 5. Prepare o banco de dados

```bash
python manage.py migrate
```

Opcionalmente, crie um usuário administrador:

```bash
python manage.py createsuperuser
```

### 6. Execute o servidor local

```bash
python manage.py runserver
```

Acesse:

```text
http://127.0.0.1:8000/
```

## Configuração com Docker

O Dockerfile cria a imagem da aplicação Django, instala as dependências do `requirements.txt` e executa o projeto com Gunicorn. O `docker-compose.yml` sobe dois serviços:

- `web`: aplicação Django/Gunicorn na porta interna `8000`.
- `nginx`: proxy reverso exposto na porta `80`, encaminhando requisições para o serviço `web`.

### 1. Configure o `.env`

Antes de subir os containers, crie o arquivo `.env` na raiz do projeto:

```env
SECRET_KEY='sua-chave-secreta'
DEBUG=False
API_KEY='sua-chave-da-weatherapi'
```

Em produção, prefira `DEBUG=False`.

### 2. Construa a imagem

Com Docker Compose v2:

```bash
docker compose build
```

Se estiver usando a versão antiga do Compose:

```bash
docker-compose build
```

### 3. Suba os containers

```bash
docker compose up -d
```

Ou, com a versão antiga:

```bash
docker-compose up -d
```

### 4. Rode as migrações dentro do container

```bash
docker compose exec web python manage.py migrate
```

Opcionalmente, crie um superusuário:

```bash
docker compose exec web python manage.py createsuperuser
```

### 5. Colete os arquivos estáticos, se necessário

```bash
docker compose exec web python manage.py collectstatic --noinput
```

### 6. Verifique se os containers estão rodando

```bash
docker compose ps
```

A aplicação ficará disponível em:

```text
http://localhost/
```

Em uma instância EC2 ou servidor remoto, acesse pelo IP público ou domínio configurado no `nginx.conf` e em `ALLOWED_HOSTS`.

## Atualizando o projeto em produção com Docker

Depois de atualizar o código no servidor:

```bash
docker compose down
docker compose build
docker compose up -d
docker compose exec web python manage.py migrate
docker compose exec web python manage.py collectstatic --noinput
```

Se precisar recriar tudo do zero, incluindo containers órfãos e volumes:

```bash
docker compose down --volumes --remove-orphans
docker compose build --no-cache
docker compose up -d
```

Use `--volumes` com cuidado, pois ele remove volumes gerenciados pelo Docker. No estado atual do projeto, o banco SQLite fica no arquivo `db.sqlite3` da raiz, que é montado no container pelo volume `.:/app`.

## Estrutura resumida

```text
project/                 Configurações principais do Django
station/                 App da estação meteorológica
station/templates/       Templates HTML
station/static/          CSS, JavaScript e ícones
Dockerfile               Imagem da aplicação Django/Gunicorn
docker-compose.yml       Serviços web e nginx
nginx.conf               Configuração do proxy reverso
requirements.txt         Dependências Python
```
