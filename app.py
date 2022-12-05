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
@app.route('/updateProduct', methods=['POST'])
def updateProduct():

    #print('Entrou na rota')

    id = request.form['id']
    nome = request.form['nome']         
    quantidade = request.form['quantidade'] 
    preco = request.form['preco']

    #print(id, nome, quantidade, preco)

    produtos_list = []

    with open('produtos.csv', 'rt') as file_in:
        produtos = csv.DictReader(file_in)
        for produto in produtos:
            produtos_list.append(produto)

        with open('produtos.csv', 'wt', newline='') as file_out:

            fieldnames = ['Id', 'Nome','Quantidade','Preco']
            writer = csv.DictWriter(file_out, fieldnames=fieldnames)

            writer.writeheader()
            writer = csv.writer(file_out)
            for index, produto in enumerate(produtos_list):
                if produto['Id'] == id:
                    print('NORMAL', produto)
                    writer.writerow([id, nome, quantidade, preco])
                else:
                    print('UP', produto)
                    writer.writerow([produtos_list[index]['Id'], produtos_list[index]['Nome'], produtos_list[index]['Quantidade'], produtos_list[index]['Preco']])
    
    return home()

def show_products():
    with open('produtos.csv', 'rt') as file_in:
        produtos = csv.DictReader(file_in)
        return render_template('home.html', produtos=produtos)

app.run(debug=True)