// Temporary storage (later replaced by Firebase)
let reports = JSON.parse(localStorage.getItem("reports")) || [];

function submitReport(e) {
  e.preventDefault();

  const report = {
    type: document.getElementById("type").value,
    item: document.getElementById("item").value,
    description: document.getElementById("description").value,
    contact: document.getElementById("contact").value,
    status: "open"
  };

  reports.push(report);
  localStorage.setItem("reports", JSON.stringify(reports));

  alert("Report submitted successfully!");
  window.location.href = "index.html";
}

function searchItems() {
  const input = document.getElementById("searchInput").value.toLowerCase();
  const results = document.getElementById("results");

  results.innerHTML = "";

  reports.filter(r => r.item.toLowerCase().includes(input))
    .forEach(r => {
      results.innerHTML += `
        <div class="card">
          <strong>${r.item}</strong><br>
          Type: ${r.type}<br>
          Description: ${r.description}<br>
          Status: ${r.status}
        </div>`;
    });
}

// Admin load
if (document.getElementById("adminList")) {
  const adminList = document.getElementById("adminList");
  reports.forEach((r, i) => {
    adminList.innerHTML += `
      <div class="card">
        <strong>${r.item}</strong> (${r.type})<br>
        ${r.description}<br>
        Contact: ${r.contact}<br>
        Status: ${r.status}<br>
        <button onclick="markClaimed(${i})">Mark Claimed</button>
      </div>`;
  });
}

function markClaimed(index) {
  reports[index].status = "claimed";
  localStorage.setItem("reports", JSON.stringify(reports));
  location.reload();
}
