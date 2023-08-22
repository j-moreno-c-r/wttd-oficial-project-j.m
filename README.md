# Eventex

sistema de Eventos encomendado ficionalmente pela Morena 
no curso WTTD.

## como desenvolver?

1. Clone o repositório.
2. Crie um virtualenv com o python 3.10.12
3. ative a virtualenv.
4. instale as dependências.
5.  Configure a instância com o .env
6. execute os testes.

`console
git clone clone https://github.com/j-moreno-c-r/wttd-deploy-linux
cd wttd
python -m venv .wttd
source .wttd/bin/acctivate
pip install -r requirements.txt
cp contrib/env-sample .env
python manage.py test 
``

## deploy 
Segue em anexo o tutorial do desenvolvedor https://github.com/mconrado

Vou deixar aqui um guia rápido para migrar suas aplicações Django para plataforma PythonAnywhere (Anaconda 🐍 ).

Como disse é um guia rápido e não tão profundo, baseado na doc do próprio PythonAnywhere.

Ideal para:
Quem assim como eu ficou órfão do Heroku depois das mudanças e quer continuar seus estudos do projeto da Morena/Eventex.
Para quem quer testar a plataforma e já tem um projetinho Django.

Pequenos requisitos:
Seu projeto em dia.
Projeto commitado no GitHub.
Existência do requirements.txt para contemplar as dependências do projeto.
Conta criada no PythonAnywhere.com.

1️⃣  Subindo o seu código para PythonAnywhere:
 Na aba Console e em Start New Console clique em Bash e clone seu repositório:
  
git clone https://github.com/seu-usuario/projeto-django-a-clonar.git
 

  Ainda no Bash e dentro do diretório raiz do seu projeto crie a venv:
mkvirtualenv --python=/usr/bin/python3.9 wttd-virtualenv
 
 
python3.9 = substitua pela versão que você usa na venv do seu projeto.
wttd-virtualenv = aqui serve para nomear sua venv então usei este nome como exemplo, mas guarde este nome, vamos precisar.


  Certifique que seu console tenha entrado na venv criada, caso não, dê o activate e ele deve parecer algo assim:
  (mysite-virtualenv)$

  Finalize instalando as dependências:
  
pip install -r requirements.txt

  Este processo pode demorar um pouco. 
mconrado
AP
 — 18/04/2023 14:28
2️⃣  Criando sua Web app e configurando o arquivo WSGI

  Saindo da Bash e voltando no painel do PythonAnywhere clique no item Web do menu superior a direita, na próxima página clique em Manual Configuration (including virtualenvs).

  Aqui lembra do nome da venv que eu pedi para guardar? Então é aqui que vamos usar.

No setor de Virtualenv, clique no link do endereço da venv e ele se tornará um campo editável, edite e logo ele deve parecer com isso:
/home/nome-do-seu-user/.virtualenvs/nome-da-sua-venv


  No item Code certifique-se que os itens estejam configurados da seguinte forma:
Source Code: /home/nome-do-seu-user/pasta-raiz-do-projeto (aqui deve apontar onde está o manage.py)
 
Working directory: /home/nome-do-seu-user/pasta-raiz-do-projeto/pasta-da-app-principal (aqui deve apontar onde está o settings.py)
  
 
  
WSGI configuration file: /var/www/nome-do-seu-user_pythonanywhere_com_wsgi.py
  
 
Python version: a versão do Python que você tem rodado o seu projeto e que foi pedido para instalar na venv

  Agora precisamos configurar o o arquivo WSGI e para isso clique nesta mesma seção Code no link do arquivo 
 
   
/var/www/nome-do-seu-user_pythonanywhere_com_wsgi.py

  Ao abrir o arquivo altere as seguintes linhas e caso estejam comentadas, remova o comentário:
path = '/home/nome-do-seu-user/pasta-raiz-do-projeto'

os.environ['DJANGO_SETTINGS_MODULE'] = 'nome-da-sua-app-principal.settings'

    aqui no meu caso ficou assim:
os.environ['DJANGO_SETTINGS_MODULE'] = 'eventex.settings' (*lembrando do nome da pasta onde contem o settings.py)

  Clique no botão Save para salvar este arquivo. 
mconrado
AP
 — 18/04/2023 14:35
3️⃣  Configurando as variáveis de ambiente e rodando o migrate.

  Nota: Aqui estou levando em conta que assim como no projeto Eventex você esteja usando:
    
Decouple para leitura das variáveis de ambiente.
Gunicorn para contornar o serviço de arquivos estáticos.
Django secret key generator.

  Antes de fazer o migrate do banco é preciso configurar as variáveis de ambiente e para isso existe algumas formas de se fazer isso.
  Aqui vou focar só em uma:
  Abra o console de preferência com virtualenv ativo, na aba Web existe um atalho direto para abrir um console com a venv já ativa, clique em Start a console in this virtualenv.

  Gere a a secret key pelo Django secret key generator:
python contrib/secret_gen.py

  Copie a hash gerada.

  Crie um arquivo chamado .env com o seguinte conteúdo:

  Aqui vale um adendo: se você usa serviço de envio de e-mail na sua app utilizando as variáveis de ambiente é interessante já colar as configs neste arquivo.
  Neste caso seu arquivo deve se parecer com isso:
SECRET_KEY=cole aqui a hash gerada
DEBUG=False
ALLOWED_HOSTS=nome-do-seu-user.pythonanywhere.com

EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=endereco-smtp-do-seu-provedor-de-email (ex: Gmail = smtp.gmail.com)
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=seu-email
EMAIL_HOST_PASSWORD=senha-do-email

  Outra dica: na hash que você colou da SECRET_KEY remova caracteres como "()/&" que possam estar dentro da mesma. 
  Isso porque no passo a frente pode gerar algum erro, e eu não consegui contornar o mesmo.
  🤦‍♂️  Não, eu não me orgulho disso!

  Feito todo passo até aqui, salve esse arquivo .env.

  De volta no console precisamos registrar estas configs na venv com o seguinte comando:
echo 'set -a; source ~/pasta-raiz-do-projeto/.env; set +a' >> ~/.virtualenvs/nome-da-sua-virtual/bin/postactivate
 
mconrado
AP
 — 18/04/2023 14:44
3️⃣ Continuação...

  Se tudo deu certo verifique se as variáveis de ambiente estão registradas, dando um echo na mesma como exemplo abaixo:
echo $SECRET_KEY

  A saída deverá ser o valor que você preencheu no .env


  Rode as migrações do banco:
python manage.py migrate
 
mconrado
AP
 — 18/04/2023 14:53
4️⃣  Rodando collectstatic e configurando a rota para os arquivos estáticos.

    Ainda na bash/console é preciso rodar o collectstatic para gerar os arquivos estáticos na pasta configurada do projeto.
    
python manage.py collectstatic

    Se tudo ocorreu bem até aqui, volte para o menu Web e em Static files adicione a rota dos arquivos estáticos.

      Onde cada campo deverá ter seu respectivo valor assim como:

      Na coluna URL clique em Enter URL e adicione:
      
/static/


      Na coluna Directory clique Enter Path e adicione:
      
/home/seu-usuario/pasta-raiz-do-projeto/staticfiles/


    Lembrando: aqui usei os valores para quem acompanhou o projeto Eventex, caso seja um projeto pessoal e diferente fique atento as suas configurações e diretórios dos arquivos estáticos da forma como está no seu projeto.

    Para finalizar nesta mesma seção Web vá até o topo da página e clique no botão em verde:

      Reload seu-usuario.pythonanywhere.com

    Se tudo saiu pelos conformes você pode acessar o endereço:

    
seu-usuario.pythonanywhere.com



Dica final: se ao acessar apresentar algum erro, você pode verificar o log no menu Web > Log Files > e acessar Error log e descer até o final da página para ver o que há de errado e tentar corrigir. 




# wttd_fenix
http://joaomcr.pythonanywhere.com/

