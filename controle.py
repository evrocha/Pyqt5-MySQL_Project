# quando nao cadastra o botao de voltar nao funciona
#sistema de favorito com order by fav
# ordenar o pdf pelo cantor  -- order by singer, nomemusica
# fazer um sistema de search usando o like p buscar musicas do banco de dados
#USAR O SUM P DAR O TEMPO TOTAL DA PLAYLIST

# tive que alterar o tipo de duracao para VARCHAR pq quando, da tela de login (inicial), chamava a funcao_principal pelo botao, dava o erro "data truncated for column "duracao" at row 1
    # com o varchar  dá certo, mas nao vou mais conseguir usar a funcao SQL SUM p retornar o tempo total da playlist
import mailbox
from PyQt5 import uic, QtWidgets
import mysql.connector
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A1, A4, A3, A2
 # variavel q recebe a conexao do código com o banco de dados MySQL
banco = mysql.connector.connect(
    host='localhost',
    database='cadastro_produtos',
    user='root',
    passwd='')


def excluirDados():
    
    linha = listData.tableWidget.currentRow() # recebe a linha clicada
    listData.tableWidget.removeRow(linha)

    cursor = banco.cursor()

    cursor.execute("SELECT id FROM musicas")
    data = cursor.fetchall()
    valorId = data[linha][0]
    cursor.execute("DELETE FROM musicas WHERE id = "+ str(valorId))
    banco.commit()
    
def gerarPDF():
    sucPDF.show()
   
    cursor = banco.cursor()

    comando_SQL = "SELECT nomeMusica,cantor,compositor,ano,duracao,GENERO from musicas;"
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()
        
    y=0

    pdf = canvas.Canvas("Playlist_Música.pdf", pagesize= A2)
    pdf.setFont("Times-Bold", 25)
    pdf.drawString(450,1600, "Músicas cadastradas: ") 
    pdf.setFont("Times-Bold", 18)
    

    pdf.drawString(10, 1550, "Música")
    pdf.drawString(90, 1550, "Cantor")
    pdf.drawString(310, 1550, "Compositor")
    pdf.drawString(510, 1550, "Ano")
    pdf.drawString(710, 1550, "Duração")
    pdf.drawString(910, 1550, "Gênero")
   

    for i in range(0, len(dados_lidos)):
        y = y +50
        pdf.drawString(10, 1530 -y, str(dados_lidos[i][0]))
        pdf.drawString(230, 1530 -y, str(dados_lidos[i][1]))
        pdf.drawString(410, 1530 -y, str(dados_lidos[i][2]))
        pdf.drawString(610, 1530 -y, str(dados_lidos[i][3]))
        pdf.drawString(910, 1530 -y, str(dados_lidos[i][4]))
        pdf.drawString(1010, 1530 -y, str(dados_lidos[i][5]))
    pdf.save()
   
def closeSucPDF():
    sucPDF.close()
    formulario.close()
    # callSecScreen.close()

def sucCadastrar():
    sucMsgCadastrar.show()

def cadastrar():
    nomeCompleto = str(cadastrarScreen.lineEdit.text().upper().replace(" ", ""))
    nomeUsr = str(cadastrarScreen.lineEdit_2.text().upper().replace(" ", ""))
    telUsr = str(cadastrarScreen.lineEdit_3.text().upper().replace(" ", ""))
    emailUsr = str(cadastrarScreen.lineEdit_4.text().upper().replace(" ", ""))
    senhaUsr = str(cadastrarScreen.lineEdit_5.text().upper().replace(" ", ""))
    senha2Usr = str(cadastrarScreen.lineEdit_6.text().upper().replace(" ", ""))

    print("Nome Completo" + nomeCompleto)
    print("nome usr" + nomeUsr )
    print("tel" + telUsr )
    print("email" + emailUsr)
    print("senha" + senhaUsr)
    print("senha2: " + senha2Usr)
# condições 
    # 1. se o nomeUsr ou o emailusr tiver cadastro no banco, nao fazer
    # 2. sesenhaUsr == SenhaUsr2: cadastrar
    # o campo do email tem q ter o @
    cursor3 = banco.cursor()
    cursor4= banco.cursor()
    cursor5= banco.cursor()

    querySql_nome = ("SELECT nomeUsr from cadastrousr WHERE nomeUsr ='{}'".format(nomeUsr))
    cursor3.execute(querySql_nome)
    qtdNomeUsr = cursor3.fetchall()

    querySql_email = ("SELECT email from cadastrousr WHERE email ='{}'".format(emailUsr))
    cursor4.execute(querySql_email)
    qtdEmail = cursor4.fetchall()

    querySql_emailValidar = ("SELECT email FROM cadastrousr where email = '{}' NOT LIKE '%_@_%._%';".format(emailUsr)) 
    cursor5.execute(querySql_emailValidar)
    qtdEmailValidado = cursor5.fetchall() 
   

    if cursor3.rowcount<1 and cursor4.rowcount<1:
        if cursor5.rowcount<1:
            cadastrarScreen.label_8.setText("Digite um e-mail válido")
        else:
            if senhaUsr==senha2Usr:
                command_SQL = "INSERT INTO cadastrousr (nomeCompleto,nomeUsr,tel,email,senha) VALUES (%s,%s,%s,%s,%s)"
                data = (str(nomeCompleto), str(nomeUsr), str(telUsr), str(emailUsr), str(senhaUsr))
                cursor3.execute(command_SQL, data)
                banco.commit()
                cadastrarScreen.label_8.setText("Conta cadastrada com sucesso!")
            else:
                print("As senhas não correspondem!")
    else:
        cadastrarScreen.label_8.setText("Nome de usuário ou e-mail já cadastrados")

def logar():
    # conferir se o email/nome de usr e a senha batem com a senha no banco de dados
    # se sim -> entrar
    email = str(loginScreen.lineEdit.text().upper().replace(" ", ""))
    nomeUsr = str(loginScreen.lineEdit.text().upper().replace(" ", ""))
    senha =  str(loginScreen.lineEdit_2.text().upper().replace(" ", ""))

    cursor= banco.cursor()
    cursor2= banco.cursor()
    cursor3= banco.cursor(buffered=True)
     

# email
    qSql_email = "SELECT * FROM cadastrousr where email = '{}'".format(email)
    cursor.execute(qSql_email)
    Qtdemail = cursor.fetchall()
    cursor.close()

# nome de usuario
    qSql_NomeUsr = "SELECT * FROM cadastrousr WHERE nomeUsr = '{}'".format(nomeUsr)
    cursor2.execute(qSql_NomeUsr)
    QtdNomeUsr = cursor2.fetchall()
    cursor2.close()
# senha

    qSql_senha = "SELECT senha FROM cadastrousr WHERE nomeUsr = '{}' email ='{}'".format(nomeUsr, email)
    # TERMINAR AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA PARTE DA SENHAA A A A A A A A AA A 
    cursor3.execute(qSql_senha)
    QtdSenha = cursor.fetchall
    cursor3.close()
    print(QtdSenha, "AJDIOASOADASJDIJADJOASJDASODAOJIOAJD")

    if cursor.rowcount ==1 or cursor2.rowcount ==1:
        
        print("nome de usr ou email correspondentes")
        funcao_principal()
    else:
        loginScreen.label_4.setText("Email ou Nome de Usuário não encontrado")
    
    # print(QtdNomeUsr[0][0], "XXXXXXXXXXXXXXXXXX")
    # print(Qtdemail[0][0], " !AAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
    # print(email, " 000000000000000000000000")

    # if email == str(Qtdemail[0][0]):
    #     print("nome de usr ou email correspondentes")
    #     funcao_principal()
    # elif nomeUsr == str(QtdNomeUsr[0][0]):
    #     print("nome de usr ou email correspondentes!!!!!!!!!!!!!!!")
    #     funcao_principal()
    # else:
    #     print("emailsd nao verificcadaoasasas")

    


def callCadastrarScreen():
    cadastrarScreen.show()

def funcao_principal():
    # o problema do tool button esta aqui
    # tem q fazer algum laço p ele abrir sempre q for chamado
    # listData.close()
    formulario.show()

    # le os inputs do arquivo formulario
    musicInput = str(formulario.lineEdit_5.text()).upper().replace(" ", "")
    singerInput = str((formulario.lineEdit.text()).upper()).replace(" ", "")
    composerInput = str((formulario.lineEdit_2.text()).upper()).replace(" ", "")
    yearInput = formulario.lineEdit_3.text()
    timeInput = formulario.lineEdit_4.text()
    
    genero = ""

    if formulario.radioButton.isChecked():
        genero = "Rap/Trap"
    elif formulario.radioButton_2.isChecked():
        genero = "Classico"
    elif formulario.radioButton_3.isChecked():
        genero = "Rock"
    elif formulario.radioButton_4.isChecked():
        genero = "Rock"    
    elif formulario.radioButton_5.isChecked():
        genero = "MPB"
    elif formulario.radioButton_6.isChecked():
        genero = "Samba"

    print("Música ", musicInput)
    print("Cantor " + singerInput)
    print("Compositor " + composerInput)
    print("Ano " + yearInput)
    print("Duração " + timeInput)
    print("Gênero " + genero) 

    
# logica usada p teste do nome e email de cadastro
    cursor = banco.cursor()
    cursor2= banco.cursor()
    consulta_sql_musica = ("SELECT nomeMusica from musicas WHERE nomeMusica = '{}'".format(musicInput))
    cursor.execute(consulta_sql_musica)
    qtdMusica = cursor.fetchall()

    consulta_sql_linha = ("SELECT * from musicas;")
    cursor2.execute(consulta_sql_linha)
    qtdMusica = cursor2.fetchall()


    if cursor2.rowcount < 30:
        if cursor.rowcount >= 1:
            formulario.label_8.setText("b")
        else:
            command_SQL = "INSERT INTO musicas (nomeMusica,cantor,compositor,ano,duracao, GENERO) VALUES (%s,%s,%s,%s,%s,%s)"
            data = (str(musicInput), str(singerInput), str(composerInput), str(yearInput), str(timeInput), genero) 
            cursor.execute(command_SQL, data)
            banco.commit()
            formulario.label_8.setText("Música adicionada com sucesso!")
    else:    
        formulario.label_8.setText("Quantidade máxima de músicas atingida!!!")


def callSecScreen():
    # formulario.close()
    listData.show()
   
   # coletando info do banco
    cursor = banco.cursor()
    comando_SQL = "SELECT nomeMusica,cantor,compositor,ano,duracao,GENERO from musicas;"
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()
   
    listData.tableWidget.setRowCount(len(dados_lidos))
    listData.tableWidget.setColumnCount(6)

    for i in range(0, len(dados_lidos)):
        for j in range(0,6):
            listData.tableWidget.setItem(i,j,QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))

app = QtWidgets.QApplication([]) # cria app

formulario = uic.loadUi("formulario.ui") # obj q carrega o arquivo principal
erro01 = uic.loadUi("erro_MusicaJaInserida.ui") # obj q carrega a tela do erro da musica ja add
listData = uic.loadUi("listar_dados.ui")
sucPDF = uic.loadUi("successMsg_PDF.ui")
loginScreen = uic.loadUi("loginScreen.ui")
cadastrarScreen = uic.loadUi("criarContaScreen.ui")
sucMsgCadastrar = uic.loadUi("sucMsgCadastro.ui")


formulario.pushButton.clicked.connect(funcao_principal)  #pushButton = botao Cadastrar. Ao ser acionado chamara a funcao principal
formulario.pushButton_2.clicked.connect(callSecScreen)  
erro01.pushButton.clicked.connect(funcao_principal)
listData.pushButton.clicked.connect(gerarPDF)
listData.pushButton_2.clicked.connect(excluirDados)
sucPDF.pushButton.clicked.connect(closeSucPDF)
listData.toolButton.clicked.connect(funcao_principal) # retorno da lista p inicial
loginScreen.pushButton.clicked.connect(logar) ########
loginScreen.pushButton_2.clicked.connect(callCadastrarScreen)
cadastrarScreen.pushButton.clicked.connect(cadastrar)
sucMsgCadastrar.pushButton.clicked.connect(funcao_principal)
loginScreen.show() # o certo é abrir na tela de login, sempre

app.exec()