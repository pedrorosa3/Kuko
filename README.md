# Kuko - Distributed Quiz System 🦉❓

## About the Project
**Kuko** is a distributed software system inspired by the popular game *Kahoot!*. It was developed as the capstone project for the **Distributed Applications** (Aplicações Distribuídas) course at the Faculty of Sciences, University of Lisbon (FCUL) in 2023/2024.

The project evolved through multiple stages, culminating in a robust **RESTful Web Service** that allows a "Manager" to create quizzes and "Participants" to answer questions in real-time.

## System Architecture
The final solution implements a secure Client-Server architecture with the following components:

* **Web Server (REST API):** Built with **Python/Flask**, serving as the core logic to manage quizzes, questions, and sessions.
* **Database:** **SQLite** integration for persistent storage of Question Sets, Active Quizzes, and Results.
* **Client:** A Python-based CLI client that interacts with the server using the `requests` library.
* **Security:** Communication is encrypted using **SSL/TLS v1.3** (HTTPS) with mutual authentication (Client and Server certificates).
* **Coordination:** Integration with **Apache ZooKeeper** to handle distributed event notifications (e.g., notifying participants when the manager advances to the next question).

## Key Features

### 👤 Manager (Gestor)
* **Content Creation:** Create Questions, Question Sets (QSets), and Quizzes via the API.
* **Game Control:** Launch quizzes and advance questions (`NEXT` command) in real-time.
* **Monitoring:** View quiz status and verify completion.

### 👥 Participant (Participante)
* **Game Lobby:** Register for active quizzes using a unique Quiz ID.
* **Gameplay:** Fetch current questions (`GET`) and submit answers (`ANS`) synchronously.
* **Feedback:** Receive real-time updates when the quiz state changes (via ZooKeeper watches) and view final score reports (`REL`).

## Technologies Used
* **Language:** Python 3.10+
* **Framework:** Flask (Web Service)
* **Database:** SQLite3
* **Networking:** HTTP/REST, Python `requests`, Python `ssl`
* **Distributed Coordination:** Apache ZooKeeper (`kazoo` library)
* **Serialization:** JSON

## How to Run

### Prerequisites
* Python 3.10+
* Apache ZooKeeper running on `localhost:2181`
* Valid SSL Certificates (for server and client)

### 1. Server Setup
Initialize the database and start the Flask server (HTTPS):
```bash
python3 kuko_server.py localhost 5000


2. Client Usage
Run the client application to interact with the server:

Bash
# Syntax: python3 kuko_client.py <participant_id>
python3 kuko_client.py 123
