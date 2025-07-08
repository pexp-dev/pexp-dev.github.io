const PROJECTS = [
  {
    id: "media-classifier",
    url: "https://github.com/pexp-dev/media-classifier"
  },
  {
    id: "freight-estimator",
    url: "https://github.com/pexp-dev/freight-estimator"
  }
];

let currentLang = localStorage.getItem("pexp-lang") || "pt";

function loadLanguage(lang) {
  fetch(`lang/${lang}.json`)
    .then(res => res.json())
    .then(data => {
      document.getElementById("projects-title").innerText = data.projectsTitle;const PROJECTS = [
  {
    id: "media-classifier"
  },
  {
    id: "freight-estimator"
  }
];

let currentLang = detectBrowserLang();

function detectBrowserLang() {
  const stored = localStorage.getItem("pexp-lang");
  if (stored) return stored;

  const browserLang = navigator.language || navigator.userLanguage;
  const langCode = browserLang.toLowerCase().split('-')[0];

  // Definir PT como padrão para pt-pt, pt-br, etc.
  if (langCode === 'pt') return 'pt';
  return 'en';
}

function loadLanguage(lang) {
  fetch(`lang/${lang}.json`)
    .then(res => res.json())
    .then(data => {
      document.getElementById("projects-title").innerText = data.projectsTitle;
      document.getElementById("footer-text").innerText = data.footer;
      document.getElementById("subtitle").innerText = data.subtitle;

      const list = document.getElementById("project-list");
      list.innerHTML = "";

      PROJECTS.forEach(p => {
        const t = data.projects[p.id];
        const item = document.createElement("li");
        item.className = "project";
        item.innerHTML = `
          <strong>${t.title}</strong><br />
          <span>${t.desc}</span><br />
          <em>${t.status}</em><br />
          <del>${t.linkText}</del>
        `;
        list.appendChild(item);
      });
    });
}

function switchLang(lang) {
  currentLang = lang;
  localStorage.setItem("pexp-lang", lang);
  loadLanguage(lang);
}

document.addEventListener("DOMContentLoaded", () => {
  document.getElementById("langSelect").value = currentLang;
  loadLanguage(currentLang);
});

      document.getElementById("footer-text").innerText = data.footer;

      const list = document.getElementById("project-list");
      list.innerHTML = "";

      PROJECTS.forEach(p => {
        const t = data.projects[p.id];
        const item = document.createElement("li");
        item.className = "project";
        item.innerHTML = `
          <strong>${t.title}</strong><br />
          <span>${t.desc}</span><br />
          <em>${t.status}</em><br />
          <a href="${p.url}" target="_blank">${t.linkText}</a>
        `;
        list.appendChild(item);
      });
    });
}

function switchLang(lang) {
  currentLang = lang;
  localStorage.setItem("pexp-lang", lang);
  loadLanguage(lang);
}

document.addEventListener("DOMContentLoaded", () => {
  document.getElementById("langSelect").value = currentLang;
  loadLanguage(currentLang);
});

