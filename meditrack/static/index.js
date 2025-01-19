function deleteNote(noteId) {
    fetch("/delete-note", {
      method: "POST",
      body: JSON.stringify({ noteId: noteId }),
    }).then((_res) => {
      window.location.href = "/";
    });
  }
  // Add this to your existing script
function loadRecords() {
  fetch('/get-records')
      .then(response => response.json())
      .then(records => {
          const tbody = document.querySelector('#recordsModal tbody');
          tbody.innerHTML = records.map(record => `
              <tr>
                  <td>${record.date}</td>
                  <td>${record.patientName}</td>
                  <td>${record.phoneNumber}</td>
                  <td>${record.note}</td>
                  <td>${record.paymentMethod}</td>
                  <td>KES ${record.amount}</td>
                  <td>
                      <button class="btn btn-sm btn-outline-danger" onclick="deleteRecord(${record.id})">
                          <i class="fas fa-trash"></i>
                      </button>
                  </td>
              </tr>
          `).join('');
      });
}

document.getElementById('recordsModal').addEventListener('show.bs.modal', loadRecords);

