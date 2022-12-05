from flask import Flask, render_template, request
import time
import csv

app = Flask(__name__)

@app.route('/')
def home():
    return show_products()

@app.route('/create', methods=['POST'])
def create():
    
    nome = request.form['nome']         
    quantidade = request.form['quantidade'] 
    preco = request.form['preco']
    id = int(time.time() * 1000)

    with open('produtos.csv', 'a', newline = '') as file_out:
        fieldnames = ['Id', 'Nome','Quantidade','Preco']
        writer = csv.DictWriter(file_out, fieldnames=fieldnames)

        writer.writerow({'Id': id, 'Nome': nome, 'Quantidade': quantidade, 'Preco': preco})

    return home()

@app.route('/delete/<id>')
def delete(id):

    produtos_list = []

    with open('produtos.csv', 'rt') as file_in:
        produtos = csv.DictReader(file_in)
        for produto in produtos:
            produtos_list.append(produto)

    print('produtos_list', produtos_list)           

    with open('produtos.csv', 'wt', newline='') as file_out:

        fieldnames = ['Id', 'Nome','Quantidade','Preco']
        writer = csv.DictWriter(file_out, fieldnames=fieldnames)

        writer.writeheader()
        writer = csv.writer(file_out)
        for produto in produtos_list:
            if produto['Id'] != id:
                print('Produto dif', f"{produto['Id']},{produto['Nome']},{produto['Quantidade']},{produto['Preco']}")
                writer.writerow([produto['Id'], produto['Nome'], produto['Quantidade'], produto['Preco']])
    
    return home()
    

@app.route('/update/<id>/<nome>/<quantidade>/<preco>')
def update(id, nome, quantidade, preco):
    lista = {
        "id": id,
        "nome": nome,
        "quantidade": quantidade,
        "preco": preco
    }

    return render_template('update.html', lista=lista)


#salva os forms que foram modificados do /update/
@app.route('/saveup', methods=['POST'])
def saveup():

    #obtem as novas variaveis
    id = request.form['id'] # o id esta ocultado na pagina
    nome = request.form['nome']         
    data = request.form['data'] 
    preco = request.form['preco']

    #abre o dataframe do .csv
    data = pd.read_csv("compras.csv")

    #cria um novo dataframe apartir das novas variaveis
    new_df = pd.DataFrame({'Id': [id],'Nome': [nome],'Data': [dat],'Preco': [preco]})

    #seta os index's para a coluna 'Id'
    #n sei se isso é necessario mas na minha mente faz sentido 
    data = data.set_index("Id")
    new_df = new_df.set_index("Id")

    #atualiza os dados do data frame antigo com o novo
    data.update(new_df)

    #salva o arquivo
    data.to_csv('compras.csv')

    #redireciona para "/"
    with open('compras.csv', 'rt') as file_in:
        compras = csv.DictReader(file_in)
        return render_template('index.html', compras=compras)

def show_products():
    with open('produtos.csv', 'rt') as file_in:
        produtos = csv.DictReader(file_in)
        return render_template('home.html', produtos=produtos)

app.run(debug=True)