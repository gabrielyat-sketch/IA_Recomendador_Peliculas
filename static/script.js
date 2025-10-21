const messagesEl = document.getElementById("messages");
const sendBtn = document.getElementById("send");

function appendBubble(text, who="bot"){
  const div = document.createElement("div");
  div.className = "bubble " + (who === "user" ? "user" : "bot");
  div.textContent = text;
  messagesEl.appendChild(div);
  messagesEl.scrollTop = messagesEl.scrollHeight;
}

sendBtn.addEventListener("click", async () => {
  const tipo = document.getElementById("tipo").value;
  const genero = document.getElementById("genero").value;
  const estado = document.getElementById("estado").value;
  const anio = document.getElementById("anio").value;

  // Mensaje usuario
  const userText = `Pref: tipo=${tipo || "cualquiera"}, genero=${genero || "cualquiera"}, estado=${estado || "cualquiera"}, año=${anio || "cualquiera"}`;
  appendBubble(userText, "user");

  // Enviar al backend
  appendBubble("Procesando tu solicitud...", "bot");
  try {
    const resp = await fetch("/api/recommend", {
      method: "POST",
      headers: {"Content-Type":"application/json"},
      body: JSON.stringify({ tipo, genero, estado_animo: estado, anio, cantidad: 5 })
    });
    const data = await resp.json();
    // quitar el "Procesando"
    const last = messagesEl.querySelectorAll(".bot");
    if(last.length) last[last.length - 1].remove();

    if(data && data.ok){
      appendBubble(data.message, "bot");
    } else {
      appendBubble("Lo siento, no pude procesar la solicitud.", "bot");
    }
  } catch (e) {
    const last = messagesEl.querySelectorAll(".bot");
    if(last.length) last[last.length - 1].remove();
    appendBubble("Error de conexión al servidor.", "bot");
    console.error(e);
  }
});
