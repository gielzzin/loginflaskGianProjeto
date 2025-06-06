document.addEventListener('DOMContentLoaded', () => {

  // Funções para alternar a visibilidade das tabelas (mantidas)
  window.botaoEntrada = function() {
      const visivelEntrada = document.getElementById('visivelEntrada');
      // Alterna entre block e none, mas pode interferir com o filtro de ID
      visivelEntrada.style.display = visivelEntrada.style.display === 'none' ? 'block' : 'none';
  };

  window.botaoSaida = function() {
      const visivelSaida = document.getElementById('visivelSaida');
      // Alterna entre block e none, mas pode interferir com o filtro de ID
      visivelSaida.style.display = visivelSaida.style.display === 'none' ? 'block' : 'none';
  };

  // Função para filtrar as tabelas por ID
  window.filterById = function() {
      const idToSearch = document.getElementById('idSearch').value.trim(); // .trim() remove espaços em branco

      const tables = [
          { id: 'tbodyEntrada', selector: '#tbodyEntrada tr' },
          { id: 'tbodySaida', selector: '#tbodySaida tr' },
          { id: 'tbodyJustificativa', selector: '#tbodyJustificativa tr' }
      ];

      tables.forEach(tableInfo => {
          const rows = document.querySelectorAll(tableInfo.selector);
          rows.forEach(row => {
              const rowId = row.dataset.id; // Pega o ID da linha do atributo data-id
              
              if (idToSearch === '') {
                  // Se o campo de busca estiver vazio, esconde todas as linhas
                  row.style.display = 'none'; 
              } else if (rowId === idToSearch) {
                  // Se o ID da linha corresponder ao ID buscado, mostra a linha
                  row.style.display = ''; // Volta ao display padrão (table-row, block, etc.)
              } else {
                  // Se não corresponder, esconde a linha
                  row.style.display = 'none'; 
              }
          });
      });
  };

  // NOVO: Chamar filterById() uma vez quando a página é carregada
  // para que as tabelas comecem vazias/ocultas.
  filterById(); 

  // Opcional: Adicionar um listener para o evento 'input' no campo de busca
  // Assim, o filtro é aplicado em tempo real enquanto você digita.
  document.getElementById('idSearch').addEventListener('input', filterById);

});