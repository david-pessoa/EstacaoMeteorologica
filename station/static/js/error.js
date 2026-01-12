import Autocomplete from "./autocomplete.js";

document.addEventListener("DOMContentLoaded", function () {
  const AutocompleteDataList = document.getElementById("AutocompleteDataList");
  const SwitchThemeButton = document.getElementById("flexSwitchCheckDefault");
  const LocalInfoDiv = document.getElementById("local");

  LocalInfoDiv.innerHTML = "";

  const opts = {
    onSelectItem: console.log,
  };

  new Autocomplete(AutocompleteDataList, opts);

  AutocompleteDataList.addEventListener("keydown", (event) => {
    const drop_down_menu = document.getElementById("ac-menu-1");
    if (!SwitchThemeButton.checked) {
      drop_down_menu.classList.add("dropdown-menu-dark");
    } else {
      drop_down_menu.classList.remove("dropdown-menu-dark");
    }

    if (event.key === "Enter") {
      event.preventDefault(); // impede que o autocomplete ou o formulário façam outra ação

      const cidade = AutocompleteDataList.value.trim();

      if (cidade) {
        window.location.href = `/?local=${encodeURIComponent(cidade)}`;
      }
    }
  });

  document.addEventListener("click", function (event) {
    const link = event.target.closest(".dropdown-item");
    if (link) {
      event.preventDefault(); // Impede que o autocomplete só preencha

      const cidade = link.getAttribute("data-value");
      if (cidade) {
        window.location.href = `/?local=${encodeURIComponent(cidade)}`;
      }
    }
  });

  // Troca entre modo claro e escuro
  SwitchThemeButton.addEventListener("click", function (event) {
    const body = document.getElementById("body");
    const boxes = Array.from(document.getElementsByClassName("bg-dark"));
    const drop_down_menu = document.getElementById("ac-menu-1");

    const isDark = !SwitchThemeButton.checked;
    localStorage.setItem("theme", isDark);

    // Modo claro
    if (!isDark) {
      body.style.backgroundColor = "rgb(24, 138, 213)";
      drop_down_menu.classList.remove("dropdown-menu-dark");

      boxes.forEach((el) => {
        el.style.setProperty(
          "background-color",
          "rgb(1, 114, 190)",
          "important"
        );
      });
    }
    // Modo escuro
    else {
      body.style.backgroundColor = "";
      drop_down_menu.classList.add("dropdown-menu-dark");

      boxes.forEach((el) => {
        el.style.setProperty(
          "background-color",
          "rgb(33, 37, 41)",
          "important"
        );
      });
    }
  });

  function toBoolean(string) {
    return string === "true";
  }

  //Coloca o site no tema pré-selecionado
  const theme = localStorage.getItem("theme");
  const isDark = toBoolean(theme) && true;
  if (!isDark) {
    SwitchThemeButton.checked = true;
    SwitchThemeButton.dispatchEvent(new Event("click"));
  }
});
