"""
Aplicações Distribuídas - Projeto 3 - kuko_client.py
Grupo: 40
Números de aluno: 60294 60270
"""

import requests,json
import ssl




### código do programa principal ###

def main():
    """
    Função principal para execução do cliente Kuko.
    """
    #idcliente=sys.argv[1]
    #context = ssl.SSLContext(protocol=ssl.PROTOCOL_TLS_CLIENT)
    #context.verify_mode = ssl.CERT_REQUIRED
    #context.check_hostname = False
    #context.load_verify_locations(cafile='Servidor/root.pem')
    #context.load_cert_chain(certfile='Servidor/cli.crt', keyfile='Servidor/cli.key')
    
    
    #sslsock = context.wrap_socket(sock, server_hostname=HOST)


    connected=True

    while connected:
            
        try:

            
            msg=str(input("comando >"))

            if msg.lower()=="exit":
                print("Encerrou o programa!")
                connected=False
            
            else:

                    
                    

                
                pedido=msg.split(";")
                
                if len(pedido)==0:
                    print("Comando Incorreto!")


                elif pedido[0].upper()=="QUESTION":
                    questao=pedido[1]
                    respostas=pedido[2:-1]
                    k=pedido[-1]
                    url=("http://localhost:5000/question")
                    dados={"questao":questao,"respostas":respostas,"respostacorreta":k}
                    #dados=json.dumps({"pegunta":questao,"respostas":respostas,"respostacorreta":k})
                    #resp=requests.post(url,json=dados,verify="./Servidor/root.pem",cert=("./Servidor/cli.crt","./Servidor/cli.key"))
                    resp=requests.post(url,json=dados)
                    #print(resp)
                    #print(resp.url)
                    #print(resp.content.decode())
                    print(resp.json()["ans"])
                
                
                elif pedido[0].upper()=="QUESTIONGET":
                    idquestao=pedido[1]
                    url=("http://localhost:5000/question/"+str(idquestao))
                    #dados=json.dumps({"idcliente":idcliente,"idquestao":idquestao})
                    dados={"idquestao":idquestao}
                    resp=requests.get(url,json=dados)
                    #print(resp)
                    #print(resp.url)
                    #print(resp)
                    #print(resp.content.decode())
                    print(resp.json()["ans"])

                elif pedido[0].upper()=="QSET":
                    questoes=pedido[1:]
                    stringquestoes=""
                    for i in range(len(questoes)):
                        if i == (len(questoes)-1):
                            stringquestoes=stringquestoes+str(questoes[i])
                        else:

                            stringquestoes=stringquestoes+str(questoes[i])+";"
                    url=("http://localhost:5000/qset")

                    #dados=json.dumps({"peguntas":stringquestoes})
                    dados={"questoes":stringquestoes}
                    resp=requests.post(url,json=dados)
                    #print(resp)
                    #print(resp.url)
                    #print(resp.content.decode())
                    print(resp.json()["ans"])

                elif pedido[0].upper()=="QUIZ":
                    #if len(pedido)==2:
                        #idquiz=pedido[1]
                        #url=("http://localhost:5000/quiz/"+str(idquiz))
                        #dados=json.dumps({"idquiz":idquiz})
                        #dados={"idquiz":idquiz}
                        #resp=requests.get(url,json=dados)
                        #print(resp)
                        #print(resp.url)
                        #print(resp.content)
                        #print(resp.json()["ans"])
                    #else:
                        qset=pedido[1]
                        points=pedido[2:]
                        stringpoints=""
                        for i in range(len(points)):
                            if i == (len(points)-1):
                                stringpoints=stringpoints+str(points[i])
                            else:

                                stringpoints=stringpoints+str(points[i])+";"
                        url=("http://localhost:5000/quiz")
                        dados={"id_qset":qset,"points":stringpoints}
                        #dados=json.dumps({"id_qset":qset,"points":stringpoints})
                        resp=requests.post(url,json=dados)
                        #print(resp)
                        #print(resp.url)
                        #print(resp.content)
                        print(resp.json()["ans"])
                
                elif pedido[0].upper()=="QUIZGET":
                    idquiz=pedido[1]
                    url=("http://localhost:5000/quiz/"+str(idquiz))
                    #dados=json.dumps({"idcliente":idcliente,"idquestao":idquestao})
                    dados={"idquiz":idquiz}
                    resp=requests.get(url,json=dados)
                    #print(resp)
                    #print(resp.url)
                    #print(resp)
                    #print(resp.content.decode())
                    print(resp.json()["ans"])

                elif pedido[0].upper()=="LAUNCH":

                    id_quiz=pedido[1]
                    url=("http://localhost:5000/launch")
                    #dados=json.dumps({"id_quiz":id_quiz})
                    dados={"id_quiz":id_quiz}
                    resp=requests.put(url,json=dados)
                    #print(resp)
                    #print(resp.url)
                    #print(resp.content)
                    print(resp.json()["ans"])

                elif pedido[0].upper()=="NEXT":
                    id_quiz=pedido[1]
                    url=("http://localhost:5000/next")
                    #dados=json.dumps({"id_quiz":id_quiz})
                    dados={"id_quiz":id_quiz}
                    resp=requests.put(url,json=dados)
                    #print(resp)
                    #print(resp.url)
                    #print(resp.content)
                    print(resp.json()["ans"])

                elif pedido[0].upper()=="REG":
                    id_quiz=pedido[1]
                    id_utilizador=pedido[2]
                    url=("http://localhost:5000/reg")
                    #dados=json.dumps({"id_quiz":id_quiz,"id_utilizador":idcliente})
                    dados={"id_quiz":id_quiz,"id_utilizador":id_utilizador}
                    resp=requests.put(url,json=dados)
                    #print(resp)
                    #print(resp.url)
                    #print(resp.content)
                    print(resp.json()["ans"])

                
                elif pedido[0].upper()=="GET":
                    if len(pedido)!=3:
                        print("ERRO: list index out of range\n")
                    id_quiz=pedido[1]
                    id_utilizador=pedido[2]
                    url=("http://localhost:5000/get/"+str(pedido[1]))
                    #dados=json.dumps({"id_quiz":id_quiz,"id_utilizador":idcliente})
                    dados={"id_quiz":id_quiz,"id_utilizador":id_utilizador}
                    resp=requests.get(url,json=dados)
                    #print(resp)
                    #print(resp.url)
                    #print(resp.content)
                    print(resp.json()["ans"])

                elif pedido[0].upper()=="ANS":
                    id_quiz=pedido[1]
                    resposta=pedido[2]
                    id_utilizador=pedido[3]
                    url=("http://localhost:5000/ans")
                    #dados=json.dumps({"id_quiz":id_quiz,"id_utilizador":idcliente,"resposta":resposta})
                    dados={"id_quiz":id_quiz,"id_utilizador":id_utilizador,"resposta":resposta}
                    resp=requests.post(url,json=dados)
                    #print(resp)
                    #print(resp.url)
                    #print(resp.content)
                    print(resp.json()["ans"])

                elif pedido[0].upper()=="REL":

                    id_quiz=int(pedido[1])
                    id_utilizador=int(pedido[2])
                    url=("http://localhost:5000/rel/"+str(id_quiz))
                    #dados=json.dumps({"id_quiz":id_quiz,"id_utilizador":idcliente})
                    dados={"id_quiz":id_quiz,"id_utilizador":id_utilizador}
                    resp=requests.get(url,json=dados)
                    #print(resp)
                    #print(resp.url)
                    #print(resp.content)
                    print(resp.json()["ans"])
                else:
                    print("INVALID COMMAND!")
                    
        
            
        except KeyboardInterrupt:
            
            print("Programa encerrado manualmente!")
            exit()
        except Exception as e:
            print("ERROR:")
            print(e)
    



        

if __name__ == "__main__":
    main()