import pymysql.cursors, json, os
from flask import Flask,request, jsonify

try:
    banco=pymysql.connect(
        host='',
        user='',
        password='',
        db='',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
except:
    print('error ao conectar com o banco de dados')

#Função para obter o TEC específicado na barra de tarefa para determinado latxlon e ano
def retornaTEC(ano,lat, dia_i, dia_f):
    tecs = []
    linha_i = dia_i*13
    linha_f = dia_f*13
    dbName = str(ano)+'_'+str(lat)
    try:
        with banco.cursor() as cursor:
            cursor.execute("SELECT * FROM `"+dbName+"` ORDER BY id ASC LIMIT "+str(linha_i-13)+","+str(linha_f)+"")
            tecs = cursor.fetchall()
    except:
        print("SELECT * FROM `"+dbName+"` ORDER BY id ASC LIMIT "+str(linha_i-13)+","+str(linha_f)+"")
        print('erro ao listar os TECs para o bando de dados:', dbName)

    return tecs

#Início do código desenvolvido para a construção da API
app = Flask(__name__)
app.config["DEBUG"] = True
###HOME---------------------------------------------------------------------
@app.route('/', methods=['GET'])
def home():
    return "<h1>API para obter dados TEC</h1><p>Atualmente o Banco de dados está alimentado com dados dos anos de 2018 e 2019 - Atualizações estão sendo feitas</p><p><span style='font-style: italic'>Andres Benoit</span> - andres.benoit7@gmail.com</p>"

@app.route('/tec/', methods=['GET'])
def obterTECdeBD():
    if 'ano' in request.args:
        ano = int(request.args['ano'])
        lat = float(request.args['lat'])
        dia_i = int(request.args['dia_i'])
        dia_f = int(request.args['dia_f'])
    else:
        return "Error: Existem dados faltantes. Você deve especificar o ano, a latitude(lat) e de que dia a que dia quer obter os dados. Ex: /tec?ano=2019&lat=87.5&dia_i=-1&dia_f=10"
    
    resultados = []
    for tec in retornaTEC(ano, lat, dia_i, dia_f):
        resultados.append(tec)
    
    return jsonify(resultados)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

