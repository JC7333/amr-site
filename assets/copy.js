/* Bouton « copier » de la page cahier des charges. Sans ce script, le bouton reste caché et le texte se sélectionne à la main. */
(function () {
  "use strict";
  function lines(list) {
    var items = list.querySelectorAll("li"), out = [];
    for (var i = 0; i < items.length; i++) out.push((i + 1) + ". " + items[i].textContent.replace(/\s+/g, " ").trim());
    return out.join("\n");
  }
  function fallback(text) {
    var area = document.createElement("textarea");
    area.value = text;
    area.setAttribute("readonly", "");
    area.className = "copy-buffer";
    document.body.appendChild(area);
    area.select();
    area.setSelectionRange(0, text.length);
    var ok = false;
    try { ok = document.execCommand("copy"); } catch (e) { ok = false; }
    document.body.removeChild(area);
    return ok;
  }
  var buttons = document.querySelectorAll("button.copy[data-copy]");
  for (var i = 0; i < buttons.length; i++) {
    (function (button) {
      var list = document.getElementById(button.getAttribute("data-copy"));
      if (!list) return;
      var label = button.textContent;
      button.hidden = false;
      function done(ok) {
        if (!ok) return;
        button.textContent = button.getAttribute("data-done") || label;
        window.setTimeout(function () { button.textContent = label; }, 2000);
      }
      button.addEventListener("click", function () {
        var text = lines(list);
        if (navigator.clipboard && window.isSecureContext) {
          navigator.clipboard.writeText(text).then(function () { done(true); }, function () { done(fallback(text)); });
        } else {
          done(fallback(text));
        }
      });
    })(buttons[i]);
  }
})();
