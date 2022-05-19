from PyQt5 import uic, QtWidgets
import mysql.connector


numero_id = 0

banco = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    passwd = '',
    database= 'cadastro_produtos'
)

def alterar_dados():
    global numero_id
    linha = segunda_tela.tableWidget.currentRow()

    cursor = banco.cursor()
    cursor.execute('SELECT id FROM produtos')
    dados_lidos = cursor.fetchall()
    valor_id = dados_lidos[linha][0]
    cursor.execute('SELECT * FROM produtos WHERE id='+ str(valor_id))
    produto = cursor.fetchall()
    tela_editar.show()

    numero_id = valor_id
    
    tela_editar.lineEdit.setText(str(produto[0][0]))
    tela_editar.lineEdit_2.setText(str(produto[0][1]))
    tela_editar.lineEdit_3.setText(str(produto[0][2]))
    tela_editar.lineEdit_4.setText(str(produto[0][3]))
    tela_editar.lineEdit_5.setText(str(produto[0][4]))


def salvar_dados_editados():
    #pegar o numero do ID
    global numero_id
    #valor digitado nos lineEdits
    codigo = tela_editar.lineEdit_2.text()
    descricao = tela_editar.lineEdit_3.text()
    preco = tela_editar.lineEdit_4.text()
    categoria = tela_editar.lineEdit_5.text()
    #atualizar aos dados no banco
    cursor = banco.cursor()
    cursor.execute('UPDATE produtos SET codigo= "{}", descricao= "{}", preco= "{}", catergoria= "{}" WHERE id = {}'.format(codigo, descricao, preco, categoria, numero_id))
    #atualizar as janelas
    tela_editar.close()
    segunda_tela.close()
    chama_segunda_tela()


def excluir_dados():
    linha = segunda_tela.tableWidget.currentRow()
    segunda_tela.tableWidget.removeRow(linha)

    cursor = banco.cursor()
    cursor.execute('SELECT id FROM produtos')
    dados_lidos = cursor.fetchall()
    valor_id = dados_lidos[linha][0]
    cursor.execute('DELETE FROM produtos WHERE id='+ str(valor_id))
    
    

def funcao_principal():
    linha1 = formulario.lineEdit.text()
    linha2 = formulario.lineEdit_2.text()
    linha3 = formulario.lineEdit_3.text()
    categoria = ''


    if formulario.radioButton.isChecked() :
        print('Categoria Informática foi selecionado')
        categoria = 'informatica'
    elif formulario.radioButton_2.isChecked() :
        print('Categoria Alimentos foi selecionado')
        categoria = 'alimentos'
    else :
        print('Categoria Eletrônicos foi selecionado')
        categoria = 'eletronicos'


    print('Código: ', linha1)
    print('Descrição: ', linha2)
    print('Preço: ', linha3)

    cursor = banco.cursor()
    comando_SQL = "INSERT INTO produtos (codigo, descricao, preco, catergoria) VALUES (%s, %s, %s, %s)"
    dados = (str(linha1)), str((linha2)), str((linha3)), categoria
    cursor.execute(comando_SQL, dados)
    banco.commit()
    formulario.lineEdit.setText('')
    formulario.lineEdit_2.setText('')
    formulario.lineEdit_3.setText('')


def chama_segunda_tela():
    segunda_tela.show()

    cursor = banco.cursor()
    comando_SQL = 'SELECT * FROM PRODUTOS;'
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()

    segunda_tela.tableWidget.setRowCount(len(dados_lidos))
    segunda_tela.tableWidget.setColumnCount(5)

    for i in range(0, len(dados_lidos)):
        for j in range(0, 5):
            segunda_tela.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))


app=QtWidgets.QApplication([])
formulario=uic.loadUi('formulario.ui')
segunda_tela=uic.loadUi('listar_dados.ui')
tela_editar=uic.loadUi('menu_alterar.ui')
formulario.pushButton.clicked.connect(funcao_principal)
formulario.pushButton_2.clicked.connect(chama_segunda_tela)
segunda_tela.pushButton.clicked.connect(excluir_dados)
segunda_tela.pushButton_2.clicked.connect(alterar_dados)
tela_editar.pushButton.clicked.connect(salvar_dados_editados)

formulario.show()
app.exec()