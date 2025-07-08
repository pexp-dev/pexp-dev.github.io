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
      // Preencher o título (se existir no JSON)
      if (data.title) {
        document.querySelector(".title").innerText = data.title;
      } else {
        document.querySelector(".title").innerText = "Project Experimental by Pirika";
      }
      // Preencher o subtítulo
      document.getElementById("subtitle").innerText = data.subtitle;

      // Restantes traduções
      document.getElementById("projects-title").innerText = data.projectsTitle;
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
