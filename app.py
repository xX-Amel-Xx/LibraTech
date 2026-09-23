from flask import Flask,url_for, session,flash,render_template, request, redirect
from models import db, Livro, Leitor, Emprestimo, Categoria,Usuario
from datetime import date, datetime, timedelta

app=Flask(__name__)
app.secret_key = 'chave_secreta' 
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///lista.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
with app.app_context():
        db.create_all()

        if Categoria.query.count() == 0:
             db.session.add_all([
            Categoria(nome="Romance"),
            Categoria(nome="Fantasia"),
            Categoria(nome="Terror"),
            Categoria(nome="Ficção Científica")
        ])
        db.session.commit()
# ===================== FUNÇÃO AUXILIAR =====================
def carregar_dados_emprestimo():
    return {
        "livros": Livro.query.all(),
        "usuarios": Leitor.query.all(),
        "emprestimos": Emprestimo.query.all()
    }
#=====================PAGINA INICIAL=====================
@app.route("/inicial")
def inicio():
        return render_template("inicial.html")

#=====================PAGINA CADASTRAR=====================
@app.route("/cadastrar")
def cadastrar():
        registros=Livro.query.all()
        return render_template("cadastrar.html",
                            registros=registros)


#=====================ROTA REGISTRAR=====================
@app.route("/registrar",methods=["POST"])
def registrar():
            titulo = request.form.get("titulo", "").strip()
            autor = request.form.get("autor", "").strip()
            editora = request.form.get("editora", "").strip()
            ano_publicacao = request.form.get("ano_publicacao", "").strip()
            categoria_id = request.form.get("categoria_id")
            if titulo == "" or autor == "" or editora == "" or not categoria_id:
                    return render_template(
                    "cadastrar.html",
                    erro="Insira uma mensagem antes de salvar."
                    
                )
            if len(ano_publicacao)!=4:
             return render_template(
              "cadastrar.html",
              erro2="O ano deve 4 caracteres"      
             )
            novo_livro = Livro(
                titulo=titulo,
                autor=autor,
                editora=editora,
                ano_publicacao=ano_publicacao,
                categoria_id=categoria_id)
            db.session.add(novo_livro)
            db.session.commit()
            return redirect("/cadastrar")
    


#=====================ROTA DELETAR LIVROS======================
@app.route("/deletar/<int:id>")
def deletar(id):
    emprestimo = Emprestimo.query.filter_by(leitor_id=id).first()
    if emprestimo:
     return render_template("erro_user.html")
    registro = Livro.query.get(id)
    
    if registro:
            db.session.delete(registro)
            db.session.commit()
    return redirect("/cadastrar")

#===================== ROTA CADASTRAR USUÁRIO =====================
@app.route("/cad_user")
def cad_user():
       registros=Leitor.query.all()
       return render_template("cad_user.html",
                                registros=registros)

#=====================ROTA REGISTRAR LEITOR=====================
@app.route("/registrar_leitor",methods=["POST"])
def registrar_leitor():
       nome=request.form.get("nome","").strip()
       email=request.form.get("email","").strip()
       telefone=request.form.get("telefone","").strip()
       data_cadastro=request.form.get("data_cadastro"," ").strip()

       
       if nome=="" or email=="" or telefone=="" or data_cadastro=="":
              return render_template("cad_user.html")

       #tratamento de exceção para caso o usuário digite uma data inválida
       try:
           data_cadastro=datetime.strptime(data_cadastro, "%Y-%m-%d").date()
       except ValueError:
              return render_template(
                    "cad_user.html",
                    erro_data2="Digite uma data válida"
              )
       
       leitor = Leitor.query.filter_by(email=email).first()
       if leitor:
                    return render_template(
                     "cad_user.html",
                     erro3="O email já foi cadastrado, adicione outro email...")
       
     #Convertendo a informação do usuário para formato data 
       dia=date.today()

       #mensagem de erro para caso o usuário digite uma data atual
       #realizando a validação e exibindo mensagem de erro
       if data_cadastro!=dia:
               return render_template(
                "cad_user.html",
               erro_data="Adicione a data atual ")
              
    #salvando novas informações    
       novo_leitor= Leitor(
        nome=nome,
        email=email,
        telefone=telefone,
        data_cadastro=data_cadastro)

       db.session.add(novo_leitor)
       db.session.commit()
       return redirect("/emprestar")

#=====================ROTA DELETAR USUÁRIOS======================
@app.route("/deletar_user/<int:id>")
def deletar_user(id):
        registro = Leitor.query.get(id)
        
        emprestimo = Emprestimo.query.filter_by(leitor_id=id).first()
        if emprestimo:
         return render_template("erro_user.html")
        if registro:
                db.session.delete(registro)
                db.session.commit()
        return redirect("/cad_user")


#===================== ROTA EMPRESTAR =====================
@app.route("/emprestar")
def emprestar():
        return render_template("emprestar.html",
                               **carregar_dados_emprestimo())
        

#==================ROTA REGISTRAR EMPRESTIMO==========================
@app.route("/novo_emprestimo",methods=["POST"])
def novo_emprestimo():
        livro_id=request.form.get("livro_id","").strip()
        leitor_id=request.form.get("leitor_id","").strip()
        data_emprestimo=request.form.get("data_emprestimo","").strip()
        data_prevista=request.form.get("data_prevista","").strip()


        #Valida se o usuário adicionou as informações válidas
        if livro_id == "" or leitor_id == "" or data_emprestimo == "" or data_prevista == "":
                    return render_template(
                    "emprestar.html",
                    erro_registros="Insira os registrojs.",
                    **carregar_dados_emprestimo()
                    
                )

        #Valida e converte as datas informadas pelo usuário para o formato date  
        try:
                data_emprestimo=datetime.strptime(data_emprestimo, "%Y-%m-%d").date()
                data_prevista=datetime.strptime(data_prevista, "%Y-%m-%d").date()
        except ValueError:
                        return render_template(
                    "emprestar.html",
                    erro_data="Digite uma data válida",
                    **carregar_dados_emprestimo()
              ) 


        #validando se o usuário digitou a data atual
        dia=date.today()
        if data_emprestimo !=dia:
                return render_template(
                "emprestar.html",
                erro_data_emprestimo="Adicione a data atual",
                **carregar_dados_emprestimo()
                )

        #validando se a data prevista é menor que a data de emprestimo
        if data_prevista<data_emprestimo:
                return render_template(
                        "emprestar.html",
                        erro_data_prevista="A data prevista deve ser maior ou igual a data de emprestimo",
                         **carregar_dados_emprestimo()
                )
        emprestimo = Emprestimo(
        livro_id=livro_id,
        leitor_id=leitor_id,
        data_emprestimo=data_emprestimo,
        data_prevista=data_prevista)
            
        db.session.add(emprestimo)
        db.session.commit()
        return redirect("/emprestar")

#==================ROTA DELETAR EMPRESTIMO==========================
@app.route("/deletar_emprestimo/<int:id>")
def deletar_emprestimo(id):
        emprestimo = Emprestimo.query.get(id)
        if emprestimo:
               db.session.delete(emprestimo)
               db.session.commit()
        return redirect("/emprestar")

#==================ROTA DEVOLVER LIVROS==========================
@app.route("/devolver")
def tela_devolver():

    # Verificando o status entrega dos empréstimos
    # Busca emprestimos que ainda não foram devolvidos
    emprestimos = Emprestimo.query.filter_by(
        data_devolucao=None
    ).all()

    #Data atual
    dia=date.today()

     # Verifica o status de cada empréstimo
    for emprestimo in emprestimos:
        if emprestimo.data_prevista<dia:
            emprestimo.status="Emprétimo atrasado"
        elif emprestimo.data_prevista==dia:
             emprestimo.status="Devolução prevista para hoje" 
        else:
            emprestimo.status="Dentro do prazo" 
    return render_template(
        "devolver.html",
        emprestimos=emprestimos
    )

    # Rota para devolver livros
@app.route("/devolver/<int:id>")
def devolver(id):
    emprestimos = Emprestimo.query.get(id)
    if emprestimos:
           emprestimos.data_devolucao=date.today()
           db.session.commit()
    return redirect("/devolver")

#==================ROTA LIVROS DISPONÍVEIS=========================
@app.route("/li_disponiveis", methods=["GET","POST"])
def livros_disponiveis():

    #Acessando as informaões do Html
    pesquisa=request.form.get("pesquisa", "").strip()
    categoria=request.form.get("categoria_id", "").strip()
    autor=request.form.get("autor","").strip()
    editora=request.form.get("editora","").strip()
    livros = Livro.query.all()

    #Pegando as informações do bando de dados
    categorias = Categoria.query.all()
    autor_livro = Livro.query.all()
    editora_livro = Livro.query.all()

    emprestimos = Emprestimo.query.filter_by(data_devolucao=None).all()

    livros_emprestados = [emprestimo.livro_id for emprestimo in emprestimos]
    
    livros_disponiveis = [
        livro for livro in livros
        if livro.id not in livros_emprestados
    ]

    livros_pesquisados = [
      livro for livro in livros_disponiveis
    if pesquisa.lower() in livro.titulo.lower() or
     pesquisa.lower() in livro.autor.lower() or
     pesquisa.lower() in livro.editora.lower()
     ]
    
    # Filtro por categoria
    if categoria:
        livros_pesquisados = [
        livro
        for livro in livros_pesquisados
        if livro.categoria_id == int(categoria)
    ]

    #Filtro por autor
    if autor:
           livros_pesquisados=[
           livro
           for livro in livros_pesquisados
           if livro.autor == autor
           ]

    #Filtro por editora
    if editora:
           livros_pesquisados=[
           livro
           for livro in livros_pesquisados
           if livro.editora == editora
           ]

    return render_template(
        "disponiveis.html", livros=livros_pesquisados,
    pesquisa=pesquisa,
    categorias=categorias,
     autor_livro= autor_livro,
    editora_livro=editora_livro
    )

@app.route("/historico",methods=["GET","POST"])
def historico_emprestio():
    emprestimos=Emprestimo.query.all()
    dia=date.today()

    #Acessando as informações do Html
    pesquisa=request.form.get("pesquisa","").strip()
    usuario=request.form.get("usuario","").strip()
    status=request.form.get("status","").strip()
    livros=request.form.get("livros","").strip()
    
    data_inicial = request.form.get("data_inicial", "").strip()
    data_final = request.form.get("data_final", "").strip()

        
    #Verificando o Status de cada emprestimo 
    for emprestimo in emprestimos:
        if emprestimo.data_devolucao:
              emprestimo.status="Devolvido"
        elif emprestimo.data_prevista <dia:
              emprestimo.status="Atrasado"
        else:
           emprestimo.status="Em aberto" 

   #itens da pesquisa 
    itens_pesquisados = [
    emprestimo for emprestimo in emprestimos
    if pesquisa.lower() in emprestimo.leitor.nome.lower()
    or pesquisa.lower() in emprestimo.livro.titulo.lower()
    or pesquisa.lower() in emprestimo.status.lower()
]
    # Pegando as datas do formulário
    try:

        if data_inicial:
            if len(data_inicial) == 4:
                ano = int(data_inicial)

                data_inicial = date(ano, 1, 1)

            elif len(data_inicial) == 7:
                data = datetime.strptime(data_inicial, "%m/%Y")

                data_inicial = date(data.year, data.month, 1)

            elif len(data_inicial) == 10:
                data_inicial = datetime.strptime(
                    data_inicial, "%d/%m/%Y"
                ).date()

            else:
                raise ValueError


        if data_final:
            if len(data_final) == 4:
                ano = int(data_final)

                data_final = date(ano, 12, 31)

            elif len(data_final) == 7:
                data = datetime.strptime(data_final, "%m/%Y")

                if data.month == 12:
                    data_final = date(data.year, 12, 31)
                else:
                    proximo_mes = date(data.year, data.month + 1, 1)
                    data_final = proximo_mes - timedelta(days=1)

            elif len(data_final) == 10:
                data_final = datetime.strptime(
                    data_final, "%d/%m/%Y"
                ).date()

            else:
                raise ValueError


        # Filtro por data inicial
        if data_inicial:
            emprestimos = [
                emprestimo
                for emprestimo in emprestimos
                if emprestimo.data_emprestimo >= data_inicial
            ]


        # Filtro por data final
        if data_final:
            emprestimos = [
                emprestimo
                for emprestimo in emprestimos
                if emprestimo.data_emprestimo <= data_final
            ]


    except ValueError:
        return render_template(
            "historico.html",
            erro_data_historico="Digite um ano, mês/ano ou uma data válida",
            **carregar_dados_emprestimo()
        )

   
    #Filtro por status
    if status:
            itens_pesquisados=[
                emprestimo for emprestimo in itens_pesquisados
                            if emprestimo.status==status ]

    return render_template("historico.html", emprestimos=itens_pesquisados,
                           pesquisa=pesquisa,usuario=usuario,livros=livros  )

#==================ROTA LOGIN=========================
@app.route("/login",methods=['GET', 'POST'])
def login():

        # Verifica se já existe uma sessão de login
            if 'id' in session:
                flash("Você já está logado!", "info")
                
                return redirect('/inicial')

        
            if request.method=='POST':
                email_digitado=request.form.get('email')
                senha_digitada=request.form.get('senha')


        # Busca o usuário no banco de dados 
                usuario=Usuario.query.filter_by(email=email_digitado).first()

        # Verificando se o usuário já possui cadastro
                if usuario is None:
                    flash("Usuário não cadastrado!", "info")
                    return render_template("login.html")

                
                # Criando Sessão do usuário
                if usuario and usuario.senha== senha_digitada:
                        session['id']=usuario.id
                        session['usuario_nome']=usuario.nome
                        print("SESSÃO CRIADA:",dict(session))
                        return redirect('/inicial')
                else:
                            flash('E-mail ou senha incorretos!','erro')
                            return render_template('login.html')
            
            return render_template('login.html')

#==================ROTA LOGOUT==================================
@app.route("/logout")
def logout():
    session.clear()
    flash("Você saiu da sua conta.", "info")
    return redirect(url_for("login"))
      
#==================ROTA RECUPERAR SENHA=========================
@app.route("/recuperar_senha",methods=['GET','POST'])
def recuperar_senha():

    if request.method == 'POST':
        email = request.form.get('email')

        usuario = Usuario.query.filter_by(email=email).first()

        if usuario:
            return render_template(
                'nova_senha.html',
                usuario_id=usuario.id
            )

        else:
            return render_template(
                'recuperar_senha.html',
                erro="E-mail não encontrado"
            )

    return render_template('recuperar_senha.html')


#==================ROTA NOVA SENHA=================================
@app.route("/nova_senha", methods=['GET', 'POST'])
def nova_senha():

    if request.method == 'POST':

        usuario_id = request.form.get('usuario_id')
        nova_senha = request.form.get('nova_senha')
        confirmar_senha = request.form.get('confirmar_senha')

        print("ID:", usuario_id)
        print("NOVA SENHA:", nova_senha)
        print("CONFIRMAÇÃO:", confirmar_senha)

        if nova_senha != confirmar_senha:
            flash("As senhas não coincidem", "erro")
            return render_template(
                "nova_senha.html",
                usuario_id=usuario_id
            )

        usuario = db.session.get(Usuario, usuario_id)

        print("USUÁRIO:", usuario)

        if usuario:
            usuario.senha = nova_senha
            db.session.commit()

            print("SENHA ALTERADA!")

            flash("Senha alterada com sucesso!", "sucesso")
            return redirect(url_for("login"))

    return render_template("nova_senha.html")

#==================ROTA TELA CADASTRAR USUARIO======================
@app.route("/tela_cadastrar", methods=['GET','POST'])
def tela_cadastrar():
      if request.method=='POST':
        nome=request.form.get('nome')
        email=request.form.get('email')
        senha=request.form.get('senha')
        confirmar_senha=request.form.get("confirmar_senha")
        telefone=request.form.get("telefone")

    # Confirmar Senha
        if senha!= confirmar_senha:
         flash("As senhas não coincidem","erro")
         return render_template("tela_cadastrar.html")

    # verificar se já existe um e-mail cadastrado

        email_existente=Usuario.query.filter_by(email=email).first()
        if email_existente:
              flash("O email já possui cadastro","erro")
              return render_template("tela_cadastrar.html")
        
    # Verificar se já existe número cadastrado

        numero_existente=Usuario.query.filter_by(telefone=telefone).first()
        if numero_existente:
              flash("O telefone já possui cadastro","erro")
              return render_template("tela_cadastrar.html")

    # Adicionando no banco de dados 
        novo_usuario=Usuario(nome=nome,email=email,senha=senha,telefone=telefone)
        db.session.add(novo_usuario)
        db.session.commit()

        flash("Cadastro realizado com sucesso, faça seu login","susesso")
        return redirect(url_for("login"))
      return render_template("tela_cadastrar.html")
    



if __name__ == "__main__":
        app.run(debug=True)
    
