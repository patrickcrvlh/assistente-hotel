from flask import Flask, request, jsonify
import openai
import time

app = Flask(__name__)

# Coloque sua chave secreta aqui
openai.api_key = "SUA_CHAVE_API_AQUI"
assistant_id = "ID_DO_SEU_ASSISTENTE_AQUI"

@app.route("/", methods=["POST"])
def perguntar_ao_joao():
    data = request.json
    pergunta = data.get("mensagem", "")

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

    # 4. Esperar a resposta ficar pronta
    while True:
        run_status = openai.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
        if run_status.status == "completed":
            break
        time.sleep(1)

    # 5. Pegar a resposta
    messages = openai.beta.threads.messages.list(thread_id=thread.id)
    resposta = messages.data[0].content[0].text.value

    return jsonify({"resposta": resposta})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
