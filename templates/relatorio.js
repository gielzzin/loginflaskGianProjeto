document.addEventListener('DOMContentLoaded', function() {
    const tabelaEntrada = document.querySelector('.tabelaEntrada');
    const tabelaSaida = document.querySelector('.tabelaSaida');
  
    document.getElementById('btnEntrada').addEventListener('click', function() {
      if (tabelaEntrada.style.display === 'none') {
        tabelaEntrada.style.display = 'table'; // mostra a tabela
      } else {
        tabelaEntrada.style.display = 'none'; // esconde a tabela
      }
    });
  
    document.getElementById('btnSaida').addEventListener('click', function() {
      if (tabelaSaida.style.display === 'none') {
        tabelaSaida.style.display = 'table'; // mostra a tabela
      } else {
        tabelaSaida.style.display = 'none'; // esconde a tabela
      }
    });
  });