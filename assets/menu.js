/* Referme le menu mobile après un choix, sur Échap ou sur un clic ailleurs. Sans ce script, le menu marche quand même. */
(function () {
  "use strict";
  var menu = document.querySelector("details.menu");
  if (!menu) return;
  menu.addEventListener("click", function (event) { if (event.target.closest("a")) menu.open = false; });
  document.addEventListener("keydown", function (event) { if (event.key === "Escape") menu.open = false; });
  document.addEventListener("click", function (event) { if (menu.open && !menu.contains(event.target)) menu.open = false; });
})();
