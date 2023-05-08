function saveTableData() {
    console.log('Start');
    const table = document.querySelector('.responsive-table')
    const tbody = table.querySelector('tbody')
    const rows = tbody.querySelectorAll('tr')
    const dataList =[]
  
    rows.forEach((row) => {
      const productName = row.querySelector('.productName').textContent.replace(/\s*\n\s*/g, "");
      const productCount = row.querySelector('.countInput').value.replace(/\s*\n\s*/g, "");
      const productPrice = row.querySelector('.productPrice').textContent.replace(/\s*\n\s*/g, "");
      const totalPrice = row.querySelector('.totalPrice').textContent.replace(/\s*\n\s*/g, "");
      dataList.push({productName, productCount, productPrice, totalPrice });
    })
    
    const data = {'data':dataList,'table_name':'Table' + Math.random()}
    console.log(data);
    const csrftoken = getCookie('csrftoken');
    fetch('save-table-data/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken,
      },
      body: JSON.stringify(data),
    })
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.error(error))
  }
  
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
  }