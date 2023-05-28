const getConfidence = (probabilities) => {
  return (
    (probabilities.true === 0 && probabilities.false === 0)
    || (probabilities.true !== 0 && probabilities.false !== 0)
  ) ? 'Unsure'
    : 'Confident'
}

const makeIntoTable = (data) => {
  const table = document.createElement('table');
  table.classList.add('table')

  const thead = document.createElement('thead');
  const tr = document.createElement('tr');
  const th1 = document.createElement('th');
  th1.appendChild(document.createTextNode('Result'));
  const th2 = document.createElement('th');
  th2.appendChild(document.createTextNode('Confidence'));
  tr.appendChild(th1);
  tr.appendChild(th2);
  thead.appendChild(tr);
  table.appendChild(thead);

  const tbody = document.createElement('tbody');
  data.forEach(function (row) {
    const [result, probabilities] = row;

    const tr = document.createElement('tr');
    const resultTD = document.createElement('td');
    const confidenceTD = document.createElement('td');

    resultTD.appendChild(document.createTextNode(result));


    confidenceTD.appendChild(document.createTextNode(getConfidence(probabilities)))

    tr.appendChild(resultTD);
    tr.appendChild(confidenceTD);
    tbody.appendChild(tr);
  });

  table.appendChild(tbody);

  return table;
}

const getPieChart = (data) => {
  let trueCount = 0;
  let falseCount = 0;

  data.forEach(([result, probabilities]) => {
    if (getConfidence(probabilities) === 'Unsure') return;
    result ? trueCount++ : falseCount++;
  });

  const chartUrl = 'https://quickchart.io/chart?c=' + encodeURIComponent(`{
    type:'pie',
    data:{
      labels:['True','False'],
      datasets:[{
        data:[${trueCount},${falseCount}]
      }]
    },
    options: {
      plugins: {
        datalabels: {
          color: '#ffffff'
        }
      }
    }
  }`);

  const image = document.createElement('img');
  image.src = chartUrl;
  return image;
}

const removeAllChildren = (element) => {
  while (element.firstChild) {
    element.removeChild(element.firstChild);
  }
}


document.getElementById('review-form').addEventListener('submit', function (e) {
  e.preventDefault();

  const url = document.getElementById('url').value;

  fetch('/get-results', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ 'url': url }),
  })
    .then(response => response.json())
    .then(data => {
      if ('error' in data) {
        const results = document.getElementById("results")
        removeAllChildren(results);
        results.appendChild(document.createTextNode(data.error));
        return;
      }
      const results = document.getElementById("results")
      removeAllChildren(results);
      results.appendChild(makeIntoTable(data));

      const pieResults = document.getElementById("pie-results")
      removeAllChildren(pieResults);
      pieResults.appendChild(getPieChart(data));
    })
    .catch((error) => {
      console.error('Error:', error);
    });
});
