import pymysql.cursors, json
from flask import Flask,request, jsonify

try:
    banco=pymysql.connect(
        host='sql112.epizy.com',
        user='epiz_25900474',
        password='4EZ75R0pZc1LR',
        db='epiz_25900474_spaceapps_en',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
except:
    print('error ao conectar com o banco de dados')

#Função para obter o TEC específicado na barra de tarefa para determinado latxlon e ano
def retornaTEC(lat,lon,ano):
    dbName = str(ano)+'_'+str(lat)+'_'+str(lon)
    try:
        with banco.cursor() as cursor:
            cursor.execute("SELECT * FROM `"+dbName+"` ORDER BY dia ASC")
            tecs = cursor.fetchall()
    except:
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
        lon = int(request.args['lon'])
    else:
        return "Error: Existem dados faltantes. Você deve especificar o ano, a latitude(lat) e a longitude(lon). Ex: tec/?ano=2019&lat=87.5&lon=-170"
    
    resultados = [retornaTEC(lat,lon,ano)]
    
    return jsonify(resultados)

app.run()

