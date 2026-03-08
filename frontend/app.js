const API_URL = "http://localhost:5000/api/calculate";

const form = document.getElementById("loan-form");
const resultSection = document.getElementById("result");
const errorSection = document.getElementById("error");

const resPrincipal = document.getElementById("res-principal");
const resRate = document.getElementById("res-rate");
const resFrequency = document.getElementById("res-frequency");
const resDuration = document.getElementById("res-duration");
const resPayment = document.getElementById("res-payment");
const amortTableBody = document.querySelector("#amort-table tbody");
const errorMsg = document.getElementById("error-msg");

function formatMoney(value) {
  return value.toLocaleString("fr-FR", {
    style: "currency",
    currency: "EUR",
    minimumFractionDigits: 2,
  });
}

function buildDuration(periods, frequency) {
  if (!Number.isFinite(periods)) return "-";

  const periodsPerYear = frequency === "mensuelle" ? 12 : frequency === "trimestrielle" ? 4 : 1;
  const years = Math.floor(periods / periodsPerYear);
  const remainder = periods - years * periodsPerYear;
  const months = frequency === "mensuelle" ? remainder : frequency === "trimestrielle" ? remainder * 3 : 0;

  const parts = [];
  if (years) parts.push(`${years} an(s)`);
  if (months) parts.push(`${months} mois`);
  return parts.length ? parts.join(" et ") : `${periods} période(s)`;
}

function showError(message) {
  errorMsg.textContent = message;
  errorSection.classList.remove("hidden");
  resultSection.classList.add("hidden");
}

function showResult(data) {
  errorSection.classList.add("hidden");
  resultSection.classList.remove("hidden");

  resPrincipal.textContent = formatMoney(data.input.principal);
  resRate.textContent = `${data.input.annual_rate.toFixed(2)} %`;
  resFrequency.textContent = data.input.frequency;
  resDuration.textContent = buildDuration(data.input.periods, data.input.frequency);
  resPayment.textContent = formatMoney(data.input.payment);

  amortTableBody.innerHTML = "";
  data.schedule.forEach((row) => {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${row.period}</td>
      <td>${formatMoney(row.balance_before)}</td>
      <td>${formatMoney(row.interest)}</td>
      <td>${formatMoney(row.principal)}</td>
      <td>${formatMoney(row.payment)}</td>
      <td>${formatMoney(row.balance_after)}</td>
    `;
    amortTableBody.appendChild(tr);
  });
}

async function onSubmit(event) {
  event.preventDefault();

  const formData = new FormData(form);
  const principal = parseFloat(formData.get("principal"));
  const annual_rate = parseFloat(formData.get("annual_rate"));
  const years = parseInt(formData.get("years"), 10);
  const months = parseInt(formData.get("months"), 10);
  const payment = parseFloat(formData.get("payment"));
  const frequency = formData.get("frequency");

  if (Number.isNaN(principal) || Number.isNaN(annual_rate) || principal <= 0 || annual_rate < 0) {
    showError("Veuillez fournir un capital et un taux annuel valides.");
    return;
  }

  const payload = {
    principal,
    annual_rate,
    frequency,
  };

  // Si l'utilisateur a complété les champs année/mois, on envoie la durée.
  const periodCount = (() => {
    if (!Number.isNaN(years) && years > 0) {
      const periodsPerYear = frequency === "mensuelle" ? 12 : frequency === "trimestrielle" ? 4 : 1;
      return years * periodsPerYear + (Number.isFinite(months) && months > 0 ? months * (periodsPerYear / 12) : 0);
    }
    return null;
  })();

  if (Number.isFinite(periodCount) && periodCount > 0) {
    payload.periods = Math.round(periodCount);
  }

  if (!Number.isNaN(payment) && payment > 0) {
    payload.payment = payment;
  }

  try {
    const res = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    const json = await res.json();

    if (!res.ok) {
      showError(json.error || "Erreur lors du calcul.");
      return;
    }

    showResult(json);
  } catch (err) {
    showError(err.message || "Impossible de contacter le serveur.");
  }
}

form.addEventListener("submit", onSubmit);
