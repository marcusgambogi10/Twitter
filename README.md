# PROJETO TWITTER

### Instalando as dependências
```
pip install -r requirements.txt
```
### Execução
Criando Migração

```
python manage.py makemigrations
```
Sincronizando com banco de dados
```
python manage.py migrate
```
Criar um superusuário com privilégios administrativos
```
python manage.py createsuperuser
```

Inicia o servidor
```
python manage.py runserver
```