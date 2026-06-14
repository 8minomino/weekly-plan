const plan = window.MEAL_PLAN_DATA;
const selected = { index: 0 };

function formatRange() {
  const start = new Date(`${plan.weekStart}T00:00:00`);
  const end = new Date(`${plan.weekEnd}T00:00:00`);
  return `${start.getFullYear()}/${start.getMonth() + 1}/${start.getDate()} - ${end.getMonth() + 1}/${end.getDate()}`;
}

function storageKey(itemId) {
  return `meal-plan:${plan.weekStart}:${itemId}`;
}

function renderTabs() {
  const tabs = document.getElementById("dayTabs");
  tabs.innerHTML = plan.dinners.map((dinner, index) => `
    <button type="button" aria-selected="${index === selected.index}" data-index="${index}">
      <b>${dinner.day}</b><span>${dinner.date}</span>
    </button>
  `).join("");

  tabs.querySelectorAll("button").forEach((button) => {
    button.addEventListener("click", () => {
      selected.index = Number(button.dataset.index);
      renderTabs();
      renderMeal();
    });
  });
}

function renderMeal() {
  const dinner = plan.dinners[selected.index];
  const card = document.getElementById("mealCard");
  card.innerHTML = `
    <div class="meal-card__head">
      <span>${dinner.day}曜日の夕食</span>
      <h2>${dinner.main}</h2>
      <a class="source-link" href="${dinner.sourceUrl}" target="_blank" rel="noopener">${dinner.sourceName}</a>
    </div>
    <div class="set-grid">
      ${setItem("ごはん", dinner.rice, "授乳中なので主食は抜かず、量は体調と空腹感で調整。")}
      ${setItem("汁物", dinner.soup, "味噌汁やスープで水分と野菜を足す。")}
      ${setItem("野菜", dinner.vegetable, "主菜に足りない野菜を補う。")}
      ${setItem("主菜", dinner.main, "夕食2名 + 翌日弁当1名分を目安。")}
    </div>
    <div class="timeline">
      ${timelineRow("作業時間", `${dinner.work} / 入浴・授乳 約60分`)}
      ${timelineRow("入浴前", dinner.before)}
      ${timelineRow("入浴後", dinner.after)}
    </div>`;
}

function setItem(type, title, note) {
  return `<article class="set-item">
    <div class="set-item__type">${type}</div>
    <div><strong>${title}</strong><p>${note}</p></div>
  </article>`;
}

function timelineRow(label, value) {
  return `<div class="timeline__row"><b>${label}</b><span>${value}</span></div>`;
}

function renderShopping() {
  const root = document.getElementById("shoppingList");
  root.innerHTML = Object.entries(plan.shopping).map(([day, groups]) => `
    <article class="shop-day">
      <h3>${day}</h3>
      ${Object.entries(groups).map(([group, items]) => `
        <div class="shop-group">
          <h4>${group}</h4>
          <ul>${items.map((item, index) => checklistItem(day, group, item, index)).join("")}</ul>
        </div>
      `).join("")}
    </article>
  `).join("");

  root.querySelectorAll("input[type='checkbox']").forEach((checkbox) => {
    checkbox.checked = localStorage.getItem(storageKey(checkbox.id)) === "1";
    checkbox.addEventListener("change", () => {
      if (checkbox.checked) {
        localStorage.setItem(storageKey(checkbox.id), "1");
      } else {
        localStorage.removeItem(storageKey(checkbox.id));
      }
    });
  });
}

function checklistItem(day, group, item, index) {
  const id = `${day}-${group}-${item[0]}-${index}`.replace(/\s+/g, "-");
  return `<li class="check-item">
    <input id="${id}" type="checkbox">
    <label for="${id}">
      <span>${item[0]}<b>${item[1]}</b></span>
      <small>${item[2]}</small>
    </label>
  </li>`;
}

function renderWeekTable() {
  const table = document.getElementById("weekTable");
  table.innerHTML = plan.dinners.map((dinner) => `
    <div class="week-row">
      <b>${dinner.day}<small>${dinner.date}</small></b>
      <span>${dinner.main}</span>
    </div>
  `).join("");
}

function setupWeekToggle() {
  const button = document.getElementById("toggleWeek");
  const panel = document.getElementById("weekPanel");
  button.addEventListener("click", () => {
    const expanded = button.getAttribute("aria-expanded") === "true";
    button.setAttribute("aria-expanded", String(!expanded));
    button.textContent = expanded ? "1週間分の献立を見る" : "1週間分の献立を閉じる";
    panel.hidden = expanded;
  });
}

function registerServiceWorker() {
  if (!("serviceWorker" in navigator)) return;
  navigator.serviceWorker.register("./sw.js").catch(() => {});
}

document.getElementById("weekRange").textContent = formatRange();
setupWeekToggle();
renderTabs();
renderMeal();
renderWeekTable();
renderShopping();
registerServiceWorker();
