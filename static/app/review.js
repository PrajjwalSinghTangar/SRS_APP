document.addEventListener('DOMContentLoaded', function() {

    document.querySelector('#id_table').addEventListener('submit', deck_table);

  });


async function deck_table(){

  const deckname = document.querySelector('#id_deck').value

  fetch(`review_table/${deckname}`)
  .then(response => response.json())
  .then(tableData => {
    const data = JSON.parse(tableData);
    let id=0

    const table = document.createElement('table')
    table.setAttribute('class',`table`)
    table.setAttribute('id',`${deckname}`)
    document.querySelector("[id='table']").appendChild(table)
    const tr_head = document.createElement('tr')
      tr_head.style.display = 'flex';
      tr_head.style.justifyContent = 'space-between';
    const th_id = document.createElement('th')
      th_id.setAttribute('id','th_id')
    const th_front = document.createElement('th')
      th_front.setAttribute('id','th_front')
    const th_back = document.createElement('th')
      th_back.setAttribute('id','th_back')
    const th_revision = document.createElement('th')
      th_revision.setAttribute('id','th_revision')

      document.querySelector('.table').style.display = 'none';
      document.getElementById(`${deckname}`).style.display = 'block';

      table.appendChild(tr_head)
      tr_head.appendChild(th_id)
      tr_head.appendChild(th_front)
      tr_head.appendChild(th_back)
      tr_head.appendChild(th_revision)

        th_id.innerHTML = 'id'
        th_front.innerHTML = 'front'
        th_back.innerHTML = 'back'
        th_revision.innerHTML = 'last revision'

  

    for(let value of data) {
      queryvalue = value.fields
      id += 1;
      const tr = document.createElement('tr')
      tr.style.display = 'flex';
      tr.style.justifyContent = 'space-between';
      table.appendChild(tr)
      const td_id = document.createElement('td')
      const td_front = document.createElement('td')
      const td_back = document.createElement('td')
      const td_revision = document.createElement('td')
        tr.appendChild(td_id)
        tr.appendChild(td_front)
        tr.appendChild(td_back)
        tr.appendChild(td_revision)
          td_id.innerHTML = id
          td_front.innerHTML = queryvalue.front
          td_back.innerHTML = queryvalue.back
          td_revision.innerHTML = queryvalue.revision
        }
  })
  document.querySelector('table').remove();
}