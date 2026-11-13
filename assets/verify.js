/* Vérifie dans le navigateur l'instantané signé du registre de démonstration.
   Rien n'est envoyé : les deux fichiers sont lus sur ce site, la signature Ed25519
   est contrôlée par le navigateur (WebCrypto). Même règle que amr.public_registry. */
(function () {
  "use strict";
  var root = document.getElementById("checker");
  if (!root) return;
  var text = JSON.parse(document.getElementById("checker-text").textContent);
  var input = document.getElementById("mandate-id");
  var tamper = document.getElementById("tamper");
  var outcome = document.getElementById("outcome");
  var files = null;

  function bytes(b64u) {
    var b64 = b64u.replace(/-/g, "+").replace(/_/g, "/");
    while (b64.length % 4) b64 += "=";
    var bin = atob(b64), out = new Uint8Array(bin.length);
    for (var i = 0; i < bin.length; i++) out[i] = bin.charCodeAt(i);
    return out;
  }
  function b64u(str) {
    var raw = new TextEncoder().encode(str), bin = "";
    for (var i = 0; i < raw.length; i++) bin += String.fromCharCode(raw[i]);
    return btoa(bin).replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, "");
  }
  function utf8(b) { return new TextDecoder().decode(b); }
  function el(tag, cls, content) {
    var node = document.createElement(tag);
    if (cls) node.className = cls;
    if (content !== undefined) node.textContent = content;
    return node;
  }
  function icon(kind) {
    var tpl = document.getElementById("icon-" + kind);
    return tpl.content.firstElementChild.cloneNode(true);
  }
  function day(iso) {
    var d = new Date(iso);
    return isNaN(d) ? iso : d.toLocaleDateString(text.locale, { day: "numeric", month: "long", year: "numeric" });
  }
  function step(kind, title, lines) {
    var box = el("div", "step step-" + kind);
    box.appendChild(icon(kind === "ok" ? "ok" : kind === "no" ? "no" : "idle"));
    var body = el("div");
    body.appendChild(el("h2", "", title));
    (lines || []).forEach(function (line) {
      if (typeof line === "string") body.appendChild(el("p", "", line)); else body.appendChild(line);
    });
    box.appendChild(body);
    return box;
  }
  function dl(pairs) {
    var list = el("dl");
    pairs.forEach(function (pair) {
      list.appendChild(el("dt", "", pair[0]));
      var dd = el("dd");
      if (Array.isArray(pair[1])) {
        var ul = el("ul");
        pair[1].forEach(function (item) { ul.appendChild(el("li", "", item)); });
        dd.appendChild(ul);
      } else dd.textContent = pair[1];
      list.appendChild(dd);
    });
    return list;
  }

  /* Statut d'un mandat à l'instant présent : lui-même, puis toute sa chaîne. */
  function evaluate(index, id, now) {
    var m = index[id];
    if (!m) return { status: "unknown" };
    var result = { status: "active" };
    if (m.revoked_at) result.status = "revoked";
    else if (m.recorded_status !== "active") result.status = "inactive";
    else if (new Date(m.expires_at).getTime() <= now) result.status = "expired";
    var parentId = m.parent_mandate_id, depth = 0;
    while (parentId) {
      var p = index[parentId];
      var broken = depth >= 10 || !p || p.revoked_at || p.recorded_status !== "active" ||
        new Date(p.expires_at).getTime() <= now;
      if (broken) { if (result.status === "active") result.status = "cut_by_parent"; break; }
      parentId = p.parent_mandate_id; depth++;
    }
    return result;
  }

  /* Le registre public ne publie pas le nom du mandant, seulement une empreinte.
     Celui qui connaît l'identifiant annoncé la recalcule et compare. */
  async function matches(announced, ref) {
    var digest = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(announced));
    var hex = Array.prototype.map.call(new Uint8Array(digest), function (b) { return ("0" + b.toString(16)).slice(-2); }).join("");
    return "sha256:" + hex === ref;
  }

  async function verify(jws, jwk) {
    var parts = jws.trim().split(".");
    if (parts.length !== 3) return { ok: false };
    var header = JSON.parse(utf8(bytes(parts[0])));
    if (header.alg !== "EdDSA" || header.kid !== jwk.kid) return { ok: false };
    var key = await crypto.subtle.importKey("jwk", { kty: "OKP", crv: "Ed25519", x: jwk.x }, { name: "Ed25519" }, false, ["verify"]);
    var ok = await crypto.subtle.verify({ name: "Ed25519" }, key, bytes(parts[2]), new TextEncoder().encode(parts[0] + "." + parts[1]));
    return { ok: ok, payload: ok ? JSON.parse(utf8(bytes(parts[1]))) : null };
  }

  function falsify(jws) {
    var parts = jws.trim().split(".");
    var payload = utf8(bytes(parts[1])).replace(/("max_amount":\s*")100(")/, "$1100000$2");
    return parts[0] + "." + b64u(payload) + "." + parts[2];
  }

  async function run() {
    outcome.replaceChildren();
    if (!files) { outcome.appendChild(step("no", text.loadError)); return; }
    var id = input.value.trim();
    var jws = tamper.checked ? falsify(files.jws) : files.jws;
    var started = performance.now(), checked;
    try { checked = await verify(jws, files.key.jwk); }
    catch (err) { outcome.appendChild(step("idle", text.unsupported, [text.unsupportedHelp])); return; }
    var ms = Math.max(1, Math.round(performance.now() - started));
    if (!checked.ok) {
      outcome.appendChild(step("no", text.sigBad, [tamper.checked ? text.sigBadTampered : text.sigBadOther]));
      return;
    }
    var reg = checked.payload.amr_public_registry;
    outcome.appendChild(step("ok", text.sigOk, [dl([
      [text.key, files.key.key_id],
      [text.snapshot, day(reg.generated_at)],
      [text.count, String(reg.mandates.length)],
      [text.time, text.timeValue.replace("{ms}", ms)]
    ])]));
    if (!id) { outcome.appendChild(step("idle", text.needId)); return; }
    var index = {};
    reg.mandates.forEach(function (m) { index[m.id] = m; });
    var verdict = evaluate(index, id, Date.now());
    if (verdict.status === "unknown") { outcome.appendChild(step("no", text.unknown, [text.unknownHelp])); return; }
    var m = index[id], per = m.perimeter || {};
    var announced = files.announced[id], who = m.principal_ref.slice(0, 23) + "...";
    if (announced) who = announced + " " + ((await matches(announced, m.principal_ref)) ? text.principalMatch : text.principalMismatch);
    var pairs = [
      [announced ? text.principalAnnounced : text.principal, who],
      [text.signed, m.principal_signed ? text.signedYes.replace("{key}", m.principal_key_id) : text.signedNo],
      [text.agent, m.agent_id],
      [text.created, day(m.created_at)],
      [m.revoked_at ? text.revokedOn : text.expires, day(m.revoked_at || m.expires_at)]
    ];
    if (per.allowed_actions) pairs.push([text.may, per.allowed_actions]);
    if (per.forbidden_actions) pairs.push([text.never, per.forbidden_actions]);
    if (per.max_amount) pairs.push([text.ceiling, per.max_amount + " " + (per.currency || "")]);
    var active = verdict.status === "active";
    outcome.appendChild(step(active ? "ok" : "no", text.status[verdict.status], [dl(pairs)]));
  }

  root.classList.add("ready");
  document.getElementById("checker-nojs").hidden = true;
  document.getElementById("checker-form").hidden = false;
  document.getElementById("checker-form").addEventListener("submit", function (event) { event.preventDefault(); run(); });
  tamper.addEventListener("change", run);
  Array.prototype.forEach.call(document.querySelectorAll(".pick"), function (button) {
    button.addEventListener("click", function () { input.value = button.getAttribute("data-id"); run(); });
  });

  Promise.all([
    fetch("/assets/demo/registry-snapshot.jws").then(function (r) { if (!r.ok) throw new Error(); return r.text(); }),
    fetch("/assets/demo/registry-key.json").then(function (r) { if (!r.ok) throw new Error(); return r.json(); }),
    fetch("/assets/demo/lock-demo.json").then(function (r) { return r.ok ? r.json() : {}; }).catch(function () { return {}; })
  ]).then(function (got) { files = { jws: got[0], key: got[1], announced: got[2].announced_principals || {} }; run(); })
    .catch(function () { run(); });
})();
