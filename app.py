import datetime
import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify, g
import psycopg2

load_dotenv()

app = Flask(__name__)

# Função para obter a conexão com o banco de dados PostgreSQL
def get_db_connection():
    if 'db_conn' not in g:
        g.db_conn = psycopg2.connect(
            host='localhost',
            database='cafedatabase',
            user=os.environ['DB_USERNAME'],
            password=os.environ['DB_PASSWORD']
        )
    return g.db_conn

# Fecha a conexão de acordo com a documentação do PostgreSQL
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, 'db_conn', None)
    if db is not None:
        db.close()

@app.route("/")
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM tb_usuario;')
    tb_usuario = cur.fetchall()
    cur.close()
    return render_template('index.html', tb_usuario=tb_usuario)

def getUsuarios():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tb_usuario')
    resultset = cursor.fetchall()
    usuarios = []
    for linha in resultset:
        id = linha[0]
        nome = linha[1]
        nascimento = linha[2]
        usuarioDict = {
            "id": id,
            "nome": nome,
            "nascimento": nascimento.strftime('%Y-%m-%d') if isinstance(nascimento, datetime.date) else nascimento
        }
        usuarios.append(usuarioDict)
    conn.close()
    return usuarios


def setUsuario(data):
    nome = data.get('nome')
    nascimento = data.get('nascimento')

    # Verificar se 'nascimento' está no formato correto
    if isinstance(nascimento, str):
        nascimento = nascimento[:10]  # Considerando que o formato é 'YYYY-MM-DD'
    else:
        # Converte a data para string no formato desejado
        nascimento = nascimento.strftime('%Y-%m-%d')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO tb_usuario(nome, nascimento) VALUES (%s, %s)', (nome, nascimento))
    conn.commit()
    cursor.execute('SELECT LASTVAL()')  # Recupera o último ID inserido
    id = cursor.fetchone()[0]
    data['id'] = id
    conn.close()
    return data


@app.route("/usuarios", methods=['GET', 'POST'])
def usuarios():
    if request.method == 'GET':
        usuarios = getUsuarios()
        return jsonify(usuarios), 200
    elif request.method == 'POST':
        data = request.json
        response = setUsuario(data)
        if isinstance(response, tuple):
            return response  # retorna o erro se houver
        return jsonify(response), 201

def getUsuarioById(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tb_usuario WHERE id = %s', (id,))
    linha = cursor.fetchone()
    cursor.close()
    if linha:
        usuarioDict = {
            "id": linha[0],
            "nome": linha[1],
            "nascimento": linha[2].strftime('%Y-%m-%d') if linha[2] else None
        }
        return usuarioDict
    return None

def updateUsuario(id, data):
    nome = data.get('nome')
    nascimento = data.get('nascimento')

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            'UPDATE tb_usuario SET nome = %s, nascimento = %s WHERE id = %s', (nome, nascimento, id))
        conn.commit()
        rowupdate = cursor.rowcount
    except psycopg2.Error as e:
        conn.rollback()
        return str(e), 500
    finally:
        cursor.close()
    return rowupdate

def deleteUsuario(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('DELETE FROM tb_usuario WHERE id = %s', (id,))
        conn.commit()
        rowdelete = cursor.rowcount
    except psycopg2.Error as e:
        conn.rollback()
        return str(e), 500
    finally:
        cursor.close()
    return rowdelete

@app.route("/usuarios/<int:id>", methods=['GET', 'DELETE', 'PUT'])
def usuario(id):
    if request.method == 'GET':
        usuario = getUsuarioById(id)
        if usuario is not None:
            return jsonify(usuario), 200
        else:
            return {}, 404
    elif request.method == 'PUT':
        data = request.json
        rowupdate = updateUsuario(id, data)
        if isinstance(rowupdate, tuple):
            return rowupdate  # retorna o erro se houver
        if rowupdate != 0:
            return jsonify(data), 201
        else:
            return jsonify(data), 304
    elif request.method == 'DELETE':
        rowdelete = deleteUsuario(id)
        if isinstance(rowdelete, tuple):
            return rowdelete  # retorna o erro se houver
        if rowdelete != 0:
            return {}, 204
        else:
            return {}, 404
