const target = "https://x9-bot.herokuapp.com/"
//const target = "http://localhost:8080/"

const file_button = document.getElementById("submit-btn");
const soundtrack_button = document.getElementById("submit-soundtrack-btn");

file_button.addEventListener("click", async (_) => {
  const input = document.querySelector('input[type="file"][id="file-input"]');

  file_button
    .querySelector("span.spinner-border")
    .classList.remove("display-none");
  file_button.querySelector("span.text-btn").innerHTML = "Carregando...";

  var data = new FormData();
  data.append("file", input.files[0]);

  await sendFile(data, "file");

  file_button.querySelector("span").classList.add("display-none");
  file_button.querySelector("span.text-btn").innerHTML = "Enviar";
});

soundtrack_button.addEventListener("click", async (_) => {
  const input = document.querySelector('input[type="file"][id="soundtrack-input"]');

  soundtrack_button
    .querySelector("span.spinner-border")
    .classList.remove("display-none");
  soundtrack_button.querySelector("span.text-btn").innerHTML = "Carregando...";

  var data = new FormData();
  data.append("file", input.files[0]);

  await sendFile(data, "soundtrack");

  soundtrack_button.querySelector("span").classList.add("display-none");
  soundtrack_button.querySelector("span.text-btn").innerHTML = "Enviar";
});

async function sendFile(file, path) {
  const response = await fetch(target + path, {
    method: "POST",
    body: file,
  });
  
  response.ok
    ? swal({
      title: "Contribuição enviada com sucesso!",
      text: "Agora é só aguardar a aprovação do PR :)",
      icon: "success",
    })
    : swal({
      title: "Opa...",
      text: "Houve algum erro ao efetuar sua solicitação :(",
      icon: "error",
    });
}