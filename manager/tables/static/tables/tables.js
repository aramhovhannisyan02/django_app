const inputs = document.querySelectorAll('input[type="number"]');

inputs.forEach(input => {
  input.addEventListener('change', () => {
    const row = input.parentNode.parentNode;
    const inputValue = parseFloat(input.value);
    const constantCell = row.cells[2];
    const constantValue = parseFloat(constantCell.textContent);
    const result = inputValue * constantValue;
    const resultCell = row.cells[3];
    if (!result) {
      result = 10
    }
    resultCell.textContent = result.toString();
  });
});

function sumLastCells() {
  let total = 0;

  const rows = document.querySelectorAll('tbody tr');

  rows.forEach(row => {
    const lastCell = row.lastElementChild;
    const value = parseFloat(lastCell.textContent);
    if (!isNaN(value)) {
      total += value;
    }
  });

  return total;
}

function updateTotalSum() {
  const totalSum = sumLastCells();

  const totalSumCell = document.getElementById('total-sum');
  totalSumCell.textContent = totalSum.toString();
  // 
  // 
}

const inputElements = document.querySelectorAll('tbody td:nth-child(2) input');
inputElements.forEach(input => {
  input.onchange = function () {
    updateTotalSum();
  };
});

updateTotalSum();

