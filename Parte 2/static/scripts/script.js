//Função para atualizar a quantidade do range de produtos
function atualizarQtd() {
  var range = document.getElementById('qtd');
  var value = range.value;

  var valor = document.getElementById('qtd_prod');
  valor.textContent = 'Até ' + value + ' Produtos';
}
atualizarValor();
