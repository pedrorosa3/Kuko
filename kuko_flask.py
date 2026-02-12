"""
Aplicações Distribuídas - Projeto 3 - kuko_client.py
Grupo: 40
Números de aluno: 60294 60270
"""

from flask import Flask, request, make_response, g
import json
import sqlite3
from os.path import isfile
import ssl
from kazoo.client import KazooClient



def connect_db(dbname):
    db_is_created = isfile(dbname) # Existe ficheiro da base de dados?
    connection = sqlite3.connect('kuko.db')
    cursor = connection.cursor()
    if not db_is_created:
        cursor.execute('PRAGMA foreign_keys = ON')
        cursor.execute("CREATE TABLE question(id_question INTEGER PRIMARY KEY AUTOINCREMENT, question TEXT NOT NULL, answers TEXT NOT NULL, k INT NOT NULL);")
        cursor.execute("CREATE TABLE qset(id_qset INTEGER PRIMARY KEY AUTOINCREMENT, questions TEXT NOT NULL);")
        cursor.execute("CREATE TABLE quiz(id_quiz INTEGER PRIMARY KEY AUTOINCREMENT, id_qset INT,state VARCHAR(50), points TEXT, timestamp_p DATETIME, timestamp_e DATETIME, question_i INT, participants TEXT, FOREIGN KEY (id_qset) REFERENCES qset(id_qset));")
        cursor.execute("CREATE TABLE results(id_quiz INT , question_i INT , participant INT , answer INT, PRIMARY KEY (id_quiz, question_i, participant) ,FOREIGN KEY (id_quiz) REFERENCES quiz(id_quiz));")
        connection.commit()
        variasperguntas=[("What is the capital of France?","Paris;Berlim;London;Madrid",1),
        ("Who wrote 'Romeo and Juliet'","William;Jose;Antonio;Manel",1),
        ("What is the chemical symbol of silver","Au;Ag;Fe;Cu",1),
        ("What is the capital of Italy","Rome;Berlin;Paris;Madrid",1)]

        #variosqsets=[("1;2"),("2;3")]
        cursor.executemany('INSERT INTO question VALUES (NULL,?, ?, ?)', variasperguntas)
        connection.commit()


    return connection, cursor

app = Flask(__name__)

@app.before_request
def before_request():
	g.db = connect_db('kuko.db')

@app.teardown_appcontext
def close_connection(exception):
	db = getattr(g, '_kuko', None)
	if db is not None:
		db[0].close()
                

#########################################################

@app.route('/question', methods = ["POST"])
@app.route('/question/<int:id>', methods = ["GET"])
def question(id = None):
    if request.method == "GET":
    # Ler dados da questao com id na base de dados
        cursor=g.db[1].execute("SELECT * FROM question WHERE id_question=?",(int(id),))
        linha=cursor.fetchall()
        
        if len(linha) != 0:
            corpo_resposta={"ans":linha[0][1]}
            r = make_response()
            r.set_data(json.dumps(corpo_resposta))
        else:

            r=make_response()
            corpo_resposta={"ans":"NOK"}
            r.set_data(json.dumps(corpo_resposta))
            
        return r
    if request.method == "POST":
        dados=request.json
        dadosresposta=""
        if int(dados["respostacorreta"]) > len(dados["respostas"]):
            corpo_resposta={"ans": "ERRO: k="+str(int(dados["respostacorreta"]))+" > "+ str(len(dados["respostas"]))+" = number of answers"}
        else:
             

            for i in range(len(dados["respostas"])):
                if i == (len(dados["respostas"])-1):
                    
                    dadosresposta=dadosresposta+dados["respostas"][i]
                else:
                    dadosresposta=dadosresposta+dados["respostas"][i]+";"
                    

            valor = ( dados['questao'], dadosresposta, int(dados['respostacorreta']),)
            g.db[1].execute('INSERT INTO question VALUES(NULL,?,?,?)', valor)
            g.db[0].commit()
            g.db[1].execute('SELECT COUNT(*) FROM question')
            g.db[0].commit()
            db_ans=g.db[1].fetchall()
            corpo_resposta={"ans":"nova pergunta: "+str(db_ans[0][0])}
        r = make_response()
        r.set_data(json.dumps(corpo_resposta))
        return r
    
    
    
#########################################################
        
    

@app.route('/qset', methods = ["POST"])
def qset():
    if request.method == "POST":
        dados=request.json
        flag=True
        questoeslista=dados["questoes"].split(";")
        for i in questoeslista:
            valor2=(i,)
            g.db[1].execute("SELECT * FROM question WHERE id_question=?",valor2)
            g.db[0].commit()
            linha=g.db[1].fetchall()
            if len(linha)==0:
                flag=False
        if flag==False:
             corpo_resposta={"ans":"ERRO: One or more question IDs do not exist in the question table."}
        else:
            valor = ( dados['questoes'],)
            g.db[1].execute('INSERT INTO qset VALUES(NULL,?)', valor)
            g.db[0].commit()
            g.db[1].execute('SELECT COUNT(*) FROM qset')
            g.db[0].commit()
            db_ans=g.db[1].fetchall()
            corpo_resposta={"ans":"novo qset: "+str(db_ans[0][0])}
        r = make_response()
        r.set_data(json.dumps(corpo_resposta))
        return r


#########################################################
# 
#    
@app.route('/quiz/', methods = ['POST'])
@app.route('/quiz/<int:id>', methods = ['GET'])

def quiz(id = None):
    if request.method == "GET":
        cursor = g.db[1].execute("SELECT quiz.state FROM quiz WHERE id_quiz=?", (int(id),))
        linha = cursor.fetchall()
        if len(linha) != 0 :
            r = make_response()
            corpo_resposta={"ans":linha[0][0]}
            r.set_data(json.dumps(corpo_resposta))
        else:
            r = make_response()
            corpo_resposta={"ans":"ERRO: Dont exist any quiz with that ID in the quiz table."}
            r.set_data(json.dumps(corpo_resposta))
                    
                    
        return r
    if request.method == "POST":
        dados=request.json
        valor1=(dados["id_qset"],)
        g.db[1].execute("SELECT qset.questions FROM qset WHERE id_qset=?", valor1)
        g.db[0].commit()
        db_ans=g.db[1].fetchall()
        questoeslista=db_ans[0][0].split(";")
        pontoslista=dados["points"].split(";")
        if len(questoeslista)!=len(pontoslista):
            corpo_resposta={"ans":"ERRO: Number of points does not match the number of questions in qset."}
        else:
             
            state="PREPARED"
            valor = (dados['id_qset'],state, dados['points'],)
            g.db[1].execute('INSERT INTO quiz VALUES(NULL,?,?,?,current_timestamp,NULL,0,NULL)', valor)
            g.db[0].commit()
            g.db[1].execute('SELECT COUNT(*) FROM quiz')
            g.db[0].commit()
            db_ans=g.db[1].fetchall()
            corpo_resposta={"ans":"Novo quiz: "+str(db_ans[0][0])}
        r = make_response()
        r.set_data(json.dumps(corpo_resposta))
        return r

#########################################################

@app.route('/launch/', methods = ['PUT'])
def launch():
    if request.method == "PUT":
        #dados = json.loads(request.data)
        dados=request.json
        state="ONGOING"
        valor1=(dados["id_quiz"],)
        g.db[1].execute('SELECT * FROM quiz WHERE id_quiz = ?', valor1)
        g.db[0].commit()
        db_ans=g.db[1].fetchall()
        if len(db_ans)==0:
             corpo_resposta={"ans":"ERRO: Quiz is not PREPARED"}
        else:
            if db_ans[0][2]=="ONGOING":
                corpo_resposta={"ans":"ERRO: Quiz is already ONGOING"}
            else:
                valor = (state,dados['id_quiz'],)
                g.db[1].execute('UPDATE quiz SET state=? WHERE id_quiz = ?', valor)
                g.db[0].commit()
                valor2=(1,dados["id_quiz"])
                g.db[1].execute('UPDATE quiz SET question_i=? WHERE id_quiz = ?', valor2)
                g.db[0].commit()
                corpo_resposta={"ans":"OK"}
        r = make_response()
        r.set_data(json.dumps(corpo_resposta))
        return r
    

#########################################################

@app.route('/next/', methods = ['PUT'])

def next():
    if request.method == "PUT":
        #dados = json.loads(request.data)
        dados=request.json
        valor = (dados['id_quiz'],)
        g.db[1].execute('SELECT * FROM quiz WHERE id_quiz = ?', valor)
        g.db[0].commit()
        db_ans=g.db[1].fetchall()
        numberquestions=len(db_ans[0][3].split(";"))
        if int(db_ans[0][6]+1<=numberquestions):
            valor1 = (int(db_ans[0][6])+1,dados['id_quiz'],)
            g.db[1].execute('UPDATE quiz SET question_i=? WHERE id_quiz = ?', valor1)
            g.db[0].commit()
            corpo_resposta={"ans":"total qsets:"+str(numberquestions)+" current: "+str(db_ans[0][6])+"\nA Passar da "+str(db_ans[0][6])+" para a "+str(int(db_ans[0][6])+1)}
        else:
            corpo_resposta={"ans":"total qsets:"+str(numberquestions)+" current: "+str(db_ans[0][6])+"\nclosing!"}
            valor2=("ENDED",dados['id_quiz'],)
            g.db[1].execute('UPDATE quiz SET state=? WHERE id_quiz = ?', valor2)
            g.db[0].commit()
            valor3=(dados['id_quiz'],)
            g.db[1].execute('UPDATE quiz SET timestamp_e = current_timestamp WHERE id_quiz = ?', valor3)
            g.db[0].commit()


        r = make_response()
        r.set_data(json.dumps(corpo_resposta))
        return r

#########################################################

@app.route('/reg/', methods = ['PUT'])

def reg():
    if request.method == "PUT":
        #dados = json.loads(request.data)
        dados=request.json
        valor = (dados['id_quiz'],)
        g.db[1].execute('SELECT * FROM quiz WHERE id_quiz = ?', valor)
        g.db[0].commit()
        db_ans=g.db[1].fetchall()
        if len(db_ans)==0:
            corpo_resposta={"ans":"ERRO: Quiz is not PREPARED"}
        else:
            participants=db_ans[0][7]
            flag=True

            if participants == None:
                participants=""
            else:
                participantslista=participants.split(";")
                
                if dados["id_utilizador"] in participantslista:
                    flag=False

            

            if flag==False:
                corpo_resposta={"ans":"ERRO: Player "+str(dados["id_utilizador"])+" is already registed for quiz "+str(dados["id_quiz"])}
            else:
                

                state=db_ans[0][2]
                if state=="PREPARED":
                    if len(participants)==0:
                        
                        participants=participants+str(dados["id_utilizador"])
                    else:
                        participants=participants+";"+str(dados["id_utilizador"])
                        
                    valor1 = (participants,dados['id_quiz'],)
                    g.db[1].execute('UPDATE quiz SET participants=? WHERE id_quiz = ?', valor1)
                    g.db[0].commit()
                    corpo_resposta={"ans":"OK"}
                
                else:
                    corpo_resposta={"ans":"ERRO: Quiz is not PREPARED"}
        r = make_response()
        r.set_data(json.dumps(corpo_resposta))
        return r
       
#########################################################

@app.route('/get/<int:id>', methods = ['GET'])

def get(id=None):
    if request.method == "GET":
        dados=request.json
        valor=(dados["id_quiz"],)
        g.db[1].execute("SELECT quiz.question_i,quiz.id_qset,quiz.state,quiz.participants FROM quiz WHERE id_quiz=?", valor)
        g.db[0].commit()
        db_ans=g.db[1].fetchall()
        if len(db_ans)==0:
                corpo_resposta={"ans":"ERRO: Quiz is not PREPARED"}
        else:

            idqset=db_ans[0][1]
            questaoatual=db_ans[0][0]
            estadoquiz=db_ans[0][2]
            participants=db_ans[0][3]
            participantslista=participants.split(";")
            if estadoquiz!="ONGOING":
                corpo_resposta={"ans":"ERRO: Quiz is not ONGOING"}
            else:
                if dados["id_utilizador"] not in participantslista:
                    corpo_resposta={"ans":"ERRO: Participant "+str(dados["id_utilizador"])+" is not registered in quiz "+str(dados["id_quiz"])}
                else:

                    valor1=(idqset,)
                    g.db[1].execute("SELECT qset.questions FROM qset WHERE id_qset=?", valor1)
                    g.db[0].commit()
                    db_ans=g.db[1].fetchall()
                    questoes=db_ans[0][0]
                    questoes=questoes.split(";")		
                    idquestaoatual=int(questoes[questaoatual-1])
                    valor2=(idquestaoatual,)
                    g.db[1].execute("SELECT * FROM question WHERE id_question=?", valor2)
                    g.db[0].commit()
                    db_ans=g.db[1].fetchall()
                    questao=db_ans[0][1]
                    respostas=db_ans[0][2]
                    respostas=respostas.split(";")
                    respostadict={"question":questao,"answers":respostas}
                    corpo_resposta={"ans":"Pergunta: "+str(respostadict)}
        r = make_response()
        r.set_data(json.dumps(corpo_resposta))
        return r
    
#########################################################


@app.route('/ans/', methods = ['POST'])

def ans():
	if request.method == "POST":
		
		dados=request.json
		valor=(dados["id_quiz"],)
		g.db[1].execute("SELECT quiz.question_i,quiz.id_qset FROM quiz WHERE id_quiz=?", valor)
		g.db[0].commit()
		db_ans=g.db[1].fetchall()
		idqset=db_ans[0][1]
		questaoatual=int(db_ans[0][0])
		valor1=(idqset,)
		g.db[1].execute("SELECT qset.questions FROM qset WHERE id_qset=?", valor1)
		g.db[0].commit()
		db_ans=g.db[1].fetchall()
		questoes=db_ans[0][0]
		questoes=questoes.split(";")		
		idquestaoatual=int(questoes[questaoatual-1])
		valor2=(idquestaoatual,)
		g.db[1].execute("SELECT * FROM question WHERE id_question=?", valor2)
		g.db[0].commit()
		db_ans=g.db[1].fetchall()
		#respostacorreta=db_ans[0][3]
		respostautilizador=int(dados["resposta"])
		idutilizador=int(dados["id_utilizador"])
			


		valor3 = (dados['id_quiz'],questaoatual,idutilizador,respostautilizador,)
		g.db[1].execute('INSERT INTO results VALUES(?,?,?,?)', valor3)
		g.db[0].commit()

		corpo_resposta={"ans":"OK"}
		r = make_response()
		r.set_data(json.dumps(corpo_resposta))
		return r


#########################################################

@app.route('/rel/<int:id>', methods = ['GET'])

def rel(id=None):
    if request.method == "GET":
        dados=request.json
        valor=(dados["id_quiz"],)
        g.db[1].execute("SELECT quiz.question_i,quiz.id_qset,quiz.points,quiz.state FROM quiz WHERE id_quiz=?", valor)
        g.db[0].commit()

        db_ans=g.db[1].fetchall()
        idqset=db_ans[0][1]
        pontos=db_ans[0][2]
        state=db_ans[0][3]
        if state!="ENDED":
            corpo_resposta={"ans":"ERRO: Quiz is not ENDED"}
        else:

            valor1=(idqset,)
            g.db[1].execute("SELECT qset.questions FROM qset WHERE id_qset=?", valor1)
            g.db[0].commit()
            db_ans=g.db[1].fetchall()
            questoes=db_ans[0][0]
            questoes=questoes.split(";")
            pontuacao=0
            respostascertas=0
            respostasdoquiz=0
            pontos=pontos.split(";")
            for i in range(len(questoes)):
                valor2=(questoes[i],)
                g.db[1].execute("SELECT * FROM question WHERE id_question=?", valor2)
                g.db[0].commit()
                db_ans=g.db[1].fetchall()
                respostacorreta=db_ans[0][3]
                valor3=(int(dados["id_quiz"]),i+1,int(dados["id_utilizador"]),)
                g.db[1].execute("SELECT * FROM results WHERE id_quiz=? AND question_i=? AND participant=?", valor3)
                g.db[0].commit()
                db_ans=g.db[1].fetchall()
                respostautilizador=int(db_ans[0][3])
                if respostautilizador==respostacorreta:
                    respostascertas=respostascertas+1
                    pontuacao=pontuacao+int(pontos[i])
                respostasdoquiz=respostasdoquiz+1
            respostadict={"n_correct":respostascertas,"n_questions":respostasdoquiz,"score":pontuacao}
            corpo_resposta={"ans":"Relatório: "+str(respostadict)}
        r = make_response()
        r.set_data(json.dumps(corpo_resposta))
        return r

		
if __name__ == '__main__':

    #zh = KazooClient(hosts="localhost:5000")
    #zh = KazooClient()
    #zh.start()

    conn, cursor = connect_db('kuko.db')
    #cursor.execute('SELECT * FROM question') # Fazer query e obter todos
    #todos = cursor.fetchall() # os resultados
    #print ("QUESTÕES: ", todos)
    #cursor.execute('SELECT * FROM qset') # Fazer query e obter todos
    #todos = cursor.fetchall() # os resultados
    #print ("QSETS: ", todos)
    #cursor.execute('SELECT * FROM quiz') # Fazer query e obter todos
    #todos = cursor.fetchall() # os resultados
    #print ("QUIZS: ", todos)
    #cursor.execute('SELECT * FROM results') # Fazer query e obter todos
    #todos = cursor.fetchall() # os resultados
    #print ("RESULTS: ", todos)
    #context = ssl.SSLContext(protocol=ssl.PROTOCOL_TLS_SERVER)
    #context.verify_mode = ssl.CERT_REQUIRED
    #context.load_verify_locations(cafile='Servidor/root.pem')
    #context.load_cert_chain(certfile='Servidor/serv.crt',keyfile='Servidor/serv.key')
    #app.run('localhost', ssl_context=context, debug = True)

    app.run(debug = True)
    #zh.stop()
    #zh.close()