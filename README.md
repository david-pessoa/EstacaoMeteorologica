# Endereço na Internet
 * http://3.149.124.111/

# Passo a passo para configuração do ambiente virtual

## Pré-requisitos:
 * Python 3.12 ou superior
 * Possuir uma chave para a API da WeatherAPI (é possível utilizar o plano gratuito)


## 1) Clone o repositório
```
git clone https://github.com/david-pessoa/EstacaoMeteorologica.git
```

## 2) Entre no diretório raíz do projeto, instale o ambiente virtual venv e ative-o
```
python3 -m venv venv
```

### No Linux ou MacOS
```
source venv/bin/activate
```

### No Windows powershell
```
source venv/Scripts/Activate.ps1
```

### No Windows cmd
```
source venv/Scripts/Activate.bat
```

## 3) Instale todos os pacotes necessários
```
pip install -r requirements.txt
```

## 4) Crie um arquivo .env na mesma pasta e gere uma SECRET_KEY 
```
python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

## 5) Agora preencha o arquivo .env com as informações a seguir substituindo os respectivos valores
```
SECRET_KEY='sua senha secreta'

API_KEY="chave da API"

DEBUG=True
```

## 6) Crie um novo super usuário
```
python manage.py createsuperuser
```

## 7) Agora rode o migrate e o servidor
```
python manage.py migrate
python manage.py runserver
```

# Configurando o Docker no ambiente de produção
## 0) Se você está apenas atualizando o código na instância, rode
```
sudo docker-compose down --volumes --remove-orphans
sudo docker-compose up -d
```

## 1) Se você estiver criando as imagens do zero, prepare-as com docker compose
```
sudo docker-compose build --no-cache
```

## 2) Rode os containers em segundo plano
```
sudo docker-compose up -d
```

### Se esse passo falhar, digite os comandos a seguir e tente de novo
```
sudo docker-compose down --volumes --remove-orphans
sudo docker image prune -a
```

## 3) Verifique os containers
```
sudo docker ps
```
