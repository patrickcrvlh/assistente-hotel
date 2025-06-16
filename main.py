from flask import Flask, request, jsonify
import openai
import os
import time

app = Flask(__name__)

# Chave da API OpenAI e ID do Assistant
openai.api_key = os.environ["OPENAI_API_KEY"]
assistant_id = "asst_CE2zEjsJHGKghvvGLeUORTzh"

@app.route("/perguntar", methods=["POST"])
def perguntar_ao_joao():
    data = request.json
    pergunta = data.get("mensagem", "")

    try:
        # 1. Criar um thread novo
        thread = openai.beta.threads.create()

        # 2. Adicionar a mensagem no thread
        openai.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=pergunta
        )

        # 3. Mandar o assistente rodar
        run = openai.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=assistant_id
        )

        # 4. Esperar a resposta ficar pronta com timeout de segurança
        tempo_maximo = 60  # segundos
        tempo_inicial = time.time()

        while True:
            run_status = openai.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id
            )

            if run_status.status == "completed":
                break

            if time.time() - tempo_inicial > tempo_maximo:
                return jsonify({"erro": "Tempo limite atingido aguardando resposta do Assistant."}), 504

            time.sleep(1)

        # 5. Pegar a resposta
        messages = openai.beta.threads.messages.list(thread_id=thread.id)
        resposta = messages.data[0].content[0].text.value

        return jsonify({"resposta": resposta})

    except Exception as e:
        return jsonify({"erro": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
