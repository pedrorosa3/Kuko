<div align="center">

# 🦉 Kuko — Sistema Distribuído de Quizzes

**Um jogo de perguntas e respostas em tempo real, inspirado no *Kahoot!***

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-REST%20API-000000?logo=flask&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-3-003B57?logo=sqlite&logoColor=white)
![Estado](https://img.shields.io/badge/estado-concluído-success)

👥 **Autores:** Pedro Rosa e Daniel Cabanilhas &nbsp;·&nbsp; 📅 **Entrega:** 14 de maio de 2024 &nbsp;·&nbsp; 🎓 **FCUL — 2023/2024**

</div>

---

## 📖 Sobre o projeto

O **Kuko** é um sistema distribuído desenvolvido no âmbito da unidade curricular de **Aplicações Distribuídas** da Faculdade de Ciências da Universidade de Lisboa (FCUL), no ano letivo 2023/2024, como trabalho de grupo (Grupo 40) de **Pedro Rosa** e **Daniel Cabanilhas**, entregue a **14 de maio de 2024**.

Um **Gestor** cria perguntas, conjuntos de perguntas e quizzes; os **Participantes** inscrevem-se num quiz ativo e respondem às perguntas à medida que o gestor avança no jogo. No final, cada participante pode consultar a sua pontuação.

## 🏗️ Arquitetura

```
┌──────────────────┐        HTTP / JSON         ┌───────────────────┐        ┌────────────┐
│  kuko_client.py  │  ───────────────────────▶  │   kuko_flask.py   │  ───▶  │  kuko.db   │
│  (cliente CLI)   │  ◀───────────────────────  │  (API REST Flask) │        │  (SQLite)  │
└──────────────────┘                            └───────────────────┘        └────────────┘
```

| Componente | Descrição |
|---|---|
| 🖥️ **Servidor** (`kuko_flask.py`) | API REST em Flask com toda a lógica de perguntas, quizzes e resultados |
| 💾 **Base de dados** (`kuko.db`) | SQLite, criada automaticamente com 4 perguntas de exemplo |
| ⌨️ **Cliente** (`kuko_client.py`) | Interface de linha de comandos que comunica com a API via `requests` |
| 🔐 **Certificados** (`*.crt`, `*.key`, `root.pem`) | Certificados para TLS com autenticação mútua (ver [Notas](#-notas)) |

## ✨ Funcionalidades

**👤 Gestor**
- Criar perguntas, conjuntos de perguntas (*QSets*) e quizzes
- Lançar um quiz e avançar para a pergunta seguinte
- Consultar o estado de um quiz

**👥 Participante**
- Inscrever-se num quiz ativo
- Obter a pergunta atual e submeter respostas
- Consultar o relatório final (respostas certas e pontuação)

## 🚀 Como executar

### 1. Pré-requisitos

- Python **3.10** ou superior
- `pip`

### 2. Instalar dependências

```bash
pip install flask requests kazoo
```

### 3. Iniciar o servidor

```bash
python kuko_flask.py
```

O servidor fica disponível em **http://localhost:5000**. Na primeira execução é criado o ficheiro `kuko.db` com 4 perguntas de exemplo (IDs 1 a 4).

> 💡 Opcionalmente, pode criar a base de dados antes de arrancar o servidor com `python setup_db.py`.

### 4. Iniciar o cliente

Noutro terminal:

```bash
python kuko_client.py
```

Aparece a linha de comandos `comando >`. Os argumentos de cada comando são separados por `;`.

## ⌨️ Comandos do cliente

| Comando | Formato | Descrição |
|---|---|---|
| `QUESTION` | `QUESTION;<pergunta>;<resp1>;<resp2>;...;<k>` | Cria uma pergunta (`k` = índice da resposta certa) |
| `QUESTIONGET` | `QUESTIONGET;<id_questao>` | Mostra uma pergunta |
| `QSET` | `QSET;<id_q1>;<id_q2>;...` | Cria um conjunto de perguntas |
| `QUIZ` | `QUIZ;<id_qset>;<pts1>;<pts2>;...` | Cria um quiz com a pontuação de cada pergunta |
| `QUIZGET` | `QUIZGET;<id_quiz>` | Mostra o estado de um quiz |
| `LAUNCH` | `LAUNCH;<id_quiz>` | Lança o quiz |
| `NEXT` | `NEXT;<id_quiz>` | Avança para a pergunta seguinte |
| `REG` | `REG;<id_quiz>;<id_utilizador>` | Inscreve um participante |
| `GET` | `GET;<id_quiz>;<id_utilizador>` | Obtém a pergunta atual |
| `ANS` | `ANS;<id_quiz>;<resposta>;<id_utilizador>` | Submete uma resposta |
| `REL` | `REL;<id_quiz>;<id_utilizador>` | Mostra o relatório final |
| `EXIT` | `EXIT` | Sai do cliente |

### 🎮 Exemplo de uma partida

```text
comando > QSET;1;2;3              # conjunto com as perguntas 1, 2 e 3
comando > QUIZ;1;10;20;30         # quiz sobre o QSet 1 com 10, 20 e 30 pontos
comando > REG;1;123               # o participante 123 inscreve-se no quiz 1
comando > LAUNCH;1                # o gestor lança o quiz
comando > GET;1;123               # o participante vê a pergunta atual
comando > ANS;1;1;123             # e responde com a opção 1
comando > NEXT;1                  # o gestor avança para a próxima pergunta
   ...
comando > REL;1;123               # relatório final do participante
```

## 🌐 Endpoints da API

| Método | Endpoint | Descrição |
|---|---|---|
| `POST` | `/question` | Criar pergunta |
| `GET` | `/question/<id>` | Obter pergunta |
| `POST` | `/qset` | Criar conjunto de perguntas |
| `POST` | `/quiz/` | Criar quiz |
| `GET` | `/quiz/<id>` | Estado do quiz |
| `PUT` | `/launch/` | Lançar quiz |
| `PUT` | `/next/` | Próxima pergunta |
| `PUT` | `/reg/` | Inscrever participante |
| `GET` | `/get/<id>` | Pergunta atual |
| `POST` | `/ans/` | Submeter resposta |
| `GET` | `/rel/<id>` | Relatório de resultados |

## 📁 Estrutura do repositório

```
Kuko/
├── kuko_flask.py     # Servidor (API REST)
├── kuko_client.py    # Cliente de linha de comandos
├── setup_db.py       # Criação da base de dados com dados de exemplo
├── schema.sql        # Esquema SQL das tabelas
├── *.crt / *.key     # Certificados e chaves TLS (servidor, cliente)
└── root.pem          # Certificado da autoridade de certificação (CA)
```

## 📝 Notas

- O suporte a **HTTPS/TLS com autenticação mútua** e a integração com **Apache ZooKeeper** (biblioteca `kazoo`) estão preparados no código mas encontram-se comentados; na versão atual a comunicação é feita por HTTP simples em `localhost:5000`.
- As chaves privadas incluídas no repositório servem apenas para fins académicos — não devem ser usadas em produção.

---

<div align="center">

Feito com ☕ por **Pedro Rosa** e **Daniel Cabanilhas** · FCUL · Aplicações Distribuídas · maio de 2024

</div>
