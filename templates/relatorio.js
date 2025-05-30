

function botaoEntrada() {
  let tabelaEntrada = document.getElementById("tabelaEntrada");
  tabelaEntrada.id('tabelaEntrada')
  botaoEntrada.parentNode.replaceChild(botaoEntrada, botaoSaida);
}
function botaoSaida() {
  let tabelaSaida = document.getElementById("tabelaSaida");
  tabelaSaida.id('tabelaSaida')
  botaoEntrada.parentNode.replaceChild(botaoSaida, botaoEntrada);
}
