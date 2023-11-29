function lerArquivoCSV(callback) {
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function () {
      if (xhr.readyState === XMLHttpRequest.DONE) {
        if (xhr.status === 200) {
          callback(xhr.responseText);
        } else {
          console.error('Erro ao carregar o arquivo CSV');
        }
      }
    };
    xhr.open('GET', 'categorias_mais_compradas.csv', true); // Caminho relativo ao HTML
    xhr.send();
  }

  function criarGraficosAnimados(data, maxItensPorGrafico) {
    var linhas = data.split('\n');
    var cabecalho = linhas[0].split(',');
    var dataset = [];

    for (var i = 1; i < linhas.length; i++) {
      var campos = linhas[i].split(',');
      var obj = {};

      for (var j = 0; j < cabecalho.length; j++) {
        obj[cabecalho[j]] = campos[j];
      }

      dataset.push(obj);
    }

    var totalItens = dataset.length;
    var numGraficos = Math.ceil(totalItens / maxItensPorGrafico);

    for (var k = 0; k < numGraficos; k++) {
      var inicio = k * maxItensPorGrafico;
      var fim = (k + 1) * maxItensPorGrafico;
      var dadosGrafico = dataset.slice(inicio, fim);

      var canvas = document.createElement('canvas');
      canvas.id = 'animatedChart' + k;
      document.getElementById('chartsContainer').appendChild(canvas);

      var ctx = canvas.getContext('2d');
      var chart = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: dadosGrafico.map(item => item.product_category_name),
          datasets: [{
            label: 'Quantidade',
            data: dadosGrafico.map(item => item.quantity),
            backgroundColor: 'rgba(75, 192, 192, 0.2)',
            borderColor: 'rgba(75, 192, 192, 1)',
            borderWidth: 1
          }]
        },
        options: {
          animation: {
            duration: 2000,
            easing: 'easeInOutQuart'
          },
          scales: {
            x: {
              beginAtZero: true
            },
            y: {
              beginAtZero: true
            }
          }
        }
      });
    }
  }

  lerArquivoCSV(function(data) {
    criarGraficosAnimados(data, 25); // Especifique o número desejado de itens por gráfico
  });