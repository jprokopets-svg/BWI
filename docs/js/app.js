/* BAIOE Explorer: static viewer over website/data/*.json
   Every displayed number comes from build_data.py output; nothing is recomputed here
   except bar widths and the contribution share shown as a percentage. */

let YEARS = ["2020", "2021", "2022", "2023", "2024", "2025", "2026"];
const $ = (s, r = document) => r.querySelector(s);
const view = $("#view"), crumbs = $("#crumbs"), tip = $("#tip");

let META = null, OCCS = null, ABILS = null, YEAR = "2026";
const cache = new Map();

const get = async (p) => {
  if (cache.has(p)) return cache.get(p);
  const r = await fetch(p);
  if (!r.ok) throw new Error(`${p}: ${r.status}`);
  const j = await r.json();
  cache.set(p, j);
  return j;
};
const esc = (s) => String(s ?? "").replace(/[&<>"]/g, c =>
  ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
const n2 = (v) => (v === null || v === undefined) ? "n/a" : (+v).toFixed(2);
const n4 = (v) => (v === null || v === undefined) ? "n/a" : (+v).toFixed(4);
const pct = (v) => (v === null || v === undefined) ? "n/a" : (v * 100).toFixed(1) + "%";

/* ---------- sparkline ---------- */
function spark(vals, w = 132, h = 34) {
  const ok = vals.filter(v => v !== null && v !== undefined);
  if (ok.length < 2) return "";
  const lo = Math.min(...ok), hi = Math.max(...ok), rng = (hi - lo) || 1;
  const pts = vals.map((v, i) => v === null ? null : [
    4 + i * (w - 8) / (vals.length - 1),
    h - 4 - (v - lo) / rng * (h - 10)
  ]).filter(Boolean);
  const d = pts.map((p, i) => (i ? "L" : "M") + p[0].toFixed(1) + "," + p[1].toFixed(1)).join(" ");
  const last = pts[pts.length - 1];
  return `<svg class="spark" width="${w}" height="${h}" aria-label="trajectory ${YEARS[0]}-${YEARS[YEARS.length - 1]}">
    <path d="${d}" fill="none" stroke="#2a4b6b" stroke-width="1.6"/>
    <circle cx="${last[0].toFixed(1)}" cy="${last[1].toFixed(1)}" r="2.6" fill="#2a4b6b"/></svg>`;
}

/* ---------- main page: ranked occupation list ----------
   894 rows, virtualized (only the visible window is in the DOM).
   Rank, exposure and quintile all come from the emitted JSON; the only thing
   computed here is bar width. */

const ROW_H = 30, BUFFER = 6;
const LIST = { q: "", grp: "", rows: [], lo: 0, hi: 1 };

function listSlice() {
  const f = LIST.q.trim().toLowerCase();
  const out = [];
  for (const o of OCCS) {
    if (o.y[YEAR][0] === null) continue;
    if (LIST.grp && o.g !== LIST.grp) continue;
    if (f && !o.t.toLowerCase().includes(f)) continue;
    out.push(o);
  }
  return out.sort((a, b) => b.y[YEAR][0] - a.y[YEAR][0]);
}

function rowHTML(o) {
  const [exp, rank, q] = o.y[YEAR];
  // Bars are scaled to the full year range, not from zero, so that differences
  // across a ~9-point spread stay visible. Held constant while filtering.
  const frac = (exp - LIST.lo) / ((LIST.hi - LIST.lo) || 1);
  const w = (4 + frac * 96).toFixed(1);
  return `<div class="row" data-s="${o.s}" style="height:${ROW_H}px">
    <span class="rk">${rank}</span>
    <span class="nm">${esc(o.t)}</span>
    <span class="gp">${esc(o.g)}</span>
    <span class="br"><i class="q${q}" style="width:${w}%"></i></span>
    <span class="sc">${n2(exp)}</span>
  </div>`;
}

function sizeScroller() {
  const sc = $("#scroller");
  if (!sc) return;
  // End the list at the viewport bottom so its own scrollbar can reach the last
  // row without the page also needing to scroll. The footer stays below.
  const top = sc.getBoundingClientRect().top;
  sc.style.height = Math.max(280, innerHeight - top - 16) + "px";
}

function paint() {
  const sc = $("#scroller"), rowsEl = $("#rows");
  if (!sc || !rowsEl) return;
  const total = LIST.rows.length;
  const first = Math.max(0, Math.floor(sc.scrollTop / ROW_H) - BUFFER);
  const count = Math.ceil(sc.clientHeight / ROW_H) + BUFFER * 2;
  const slice = LIST.rows.slice(first, Math.min(total, first + count));
  rowsEl.style.transform = `translateY(${first * ROW_H}px)`;
  rowsEl.innerHTML = slice.map(rowHTML).join("");
}

function refresh() {
  LIST.rows = listSlice();
  const sp = $("#spacer"), sc = $("#scroller");
  if (sp) sp.style.height = LIST.rows.length * ROW_H + "px";
  if (sc) sc.scrollTop = 0;
  const n = LIST.rows.length;
  $("#count").textContent = n === OCCS.length
    ? `${n} occupations`
    : `${n} of ${OCCS.length} occupation${n === 1 ? "" : "s"}`;
  paint();
}

function renderGrid() {
  const v = OCCS.map(o => o.y[YEAR][0]).filter(x => x !== null);
  LIST.lo = Math.min(...v); LIST.hi = Math.max(...v);
  const groups = [...new Set(OCCS.map(o => o.g))].sort();

  view.innerHTML = `
  <div class="controls">
    <input type="search" id="q" placeholder="Search 894 occupations…" value="${esc(LIST.q)}">
    <select id="grp">
      <option value="">All SOC major groups</option>
      ${groups.map(g => `<option value="${esc(g)}"${g === LIST.grp ? " selected" : ""}>${esc(g)}</option>`).join("")}
    </select>
    <div class="yearbtns">${YEARS.map(y =>
      `<button data-y="${y}" class="${y === YEAR ? "on" : ""}">${y}</button>`).join("")}</div>
    <div class="legend"><span>lower</span>
      ${[1, 2, 3, 4, 5].map(q => `<i class="q${q}"></i>`).join("")}<span>higher</span>
    </div>
  </div>

  <div class="listmeta">
    <span id="count"></span>
    <span class="cap">Ranked by ${YEAR} exposure. Bars are scaled to the ${YEAR} range
      ${n2(LIST.lo)} to ${n2(LIST.hi)}, not from zero. Tied scores share a rank.</span>
  </div>

  <div class="listhead">
    <span class="rk">#</span><span class="nm">Occupation</span>
    <span class="gp">SOC major group</span><span class="br"></span>
    <span class="sc">Exposure</span>
  </div>
  <div class="scroller" id="scroller"><div class="spacer" id="spacer">
    <div class="rows" id="rows"></div></div></div>`;

  crumbs.innerHTML = "";

  const q = $("#q");
  q.addEventListener("input", () => { LIST.q = q.value; refresh(); });
  $("#grp").addEventListener("change", e => { LIST.grp = e.target.value; refresh(); });
  view.querySelectorAll(".yearbtns button").forEach(b =>
    b.addEventListener("click", () => { YEAR = b.dataset.y; renderGrid(); }));
  $("#scroller").addEventListener("scroll", paint, { passive: true });
  $("#rows").addEventListener("click", e => {
    const r = e.target.closest(".row");
    if (r) location.hash = "#/occ/" + r.dataset.s;
  });
  addEventListener("resize", () => { sizeScroller(); paint(); });

  sizeScroller();
  refresh();
  q.focus(); q.setSelectionRange(q.value.length, q.value.length);
}

/* ---------- occupation ---------- */
async function renderOcc(soc) {
  const d = await get(`data/occ/${soc}.json`);
  const cy = d.by_year[YEAR], traj = YEARS.map(y => d.by_year[y].exposure);
  // weights are stored once (year-invariant); year-varying fields come from d.years
  const ORD = { kept: 0, dropped: 1, null_this_year: 2, unmapped: 3 };
  const rows = d.abilities.map((a, i) => {
    const [exposure, status, contribution] = d.years[YEAR][i];
    return { ...a, exposure, status, contribution };
  }).sort((a, b) => (ORD[a.status] - ORD[b.status]) || (b.weight - a.weight));

  const kept = rows.filter(r => r.status === "kept");
  const maxC = Math.max(...kept.map(r => r.contribution), 0.001);

  const tr = rows.map(r => {
    const cls = r.status === "kept" ? "kept" :
      r.status === "dropped" ? "dropped" : "nullrow";
    const link = (r.status === "null_this_year" || r.status === "unmapped")
      ? esc(r.ability)
      : `<a href="#/ability/${abilId(r.ability)}">${esc(r.ability)}</a>`;
    const barW = r.status === "kept" ? (r.contribution / maxC * 88).toFixed(1) : 0;
    return `<tr class="${cls}">
      <td class="ab">${link}</td>
      <td class="num">${n4(r.weight)}</td>
      <td class="num">${r.i_norm !== undefined ? n2(r.i_norm * 4 + 1) : "n/a"}</td>
      <td class="num">${r.l_norm !== undefined ? n2(r.l_norm * 7) : "n/a"}</td>
      <td class="num">${n2(r.exposure)}</td>
      <td class="num">${r.status === "kept" ? n2(r.contribution) : "n/a"}</td>
      <td>${r.status === "kept" ? `<span class="bar" style="width:${barW}px"></span>` : ""}</td>
    </tr>`;
  }).join("");

  const sumC = kept.reduce((a, r) => a + r.contribution, 0);

  crumbs.innerHTML = `<a href="#/">All occupations</a><span class="sep">›</span>${esc(d.title)}`;
  view.innerHTML = `
  <div class="head">
    <div class="who">
      <h2>${esc(d.title)}</h2>
      <p><code>${d.soc_code}</code>, ${esc(d.major_group)}</p>
    </div>
    <div class="bignums">
      <div class="bignum"><div class="v">${n2(cy.exposure)}</div><div class="l">${YEAR} exposure</div></div>
      <div class="bignum"><div class="v">${cy.rank ?? "n/a"}<span style="font-size:15px;color:var(--muted)">/894</span></div><div class="l">rank</div></div>
      <div class="bignum"><div class="v">${spark(traj)}</div><div class="l">${YEARS[0]}-${YEARS[YEARS.length - 1]}</div></div>
    </div>
  </div>

  <div class="yearbtns" style="margin-bottom:14px">${YEARS.map(y =>
    `<button data-y="${y}" class="${y === YEAR ? "on" : ""}">${y}</button>`).join("")}</div>

  <div class="note${cy.unmeasured_weight_share > 0.25 ? " warn" : ""}">
    <b>${pct(cy.unmeasured_weight_share)}</b> of this occupation's ability weight is not measured by
    current benchmarks. The ${YEAR} score is computed from the
    <b>${cy.abilities_used}</b> highest-weighted measured abilities that together reach the 90%
    cumulative-weight threshold, <b>${pct(cy.kept_weight_share)}</b> of total ability weight.
    ${cy.abilities_null} rated abilities had no benchmark value this year.
  </div>

  <h3>Ability decomposition, ${YEAR}</h3>
  <p class="cap">weight = I<sub>norm</sub> × L<sub>norm</sub>, where I<sub>norm</sub> = (Importance−1)/4 and
    L<sub>norm</sub> = Level/7. Contribution = exposure × weight ÷ Σ<sub>kept</sub> weight; kept
    contributions sum to ${n2(sumC)} = the score above.</p>
  <table>
    <thead><tr><th>Ability</th><th class="num">Weight</th><th class="num">Import.</th>
      <th class="num">Level</th><th class="num">Exposure</th><th class="num">Contrib.</th><th></th></tr></thead>
    <tbody>${tr}</tbody>
  </table>`;

  view.querySelectorAll(".yearbtns button").forEach(b =>
    b.addEventListener("click", () => { YEAR = b.dataset.y; renderOcc(soc); }));
}

const abilId = (name) => (ABILS.find(a => a.name === name) || {}).ability_id || "";

/* ---------- ability ---------- */
function benchCard(b, y) {
  if (!b) return `<p class="cap">No benchmark for ${y}.</p>`;
  const nm = b.benchmark_id ? `<a href="#/bench/${b.benchmark_id}">${esc(b.name)}</a>` : esc(b.name);
  return `<div class="card">
      <h4>${nm}</h4>
      <div class="kv"><span>Best result</span><b>${b.raw_score ?? "n/a"}</b></div>
      ${b.metric ? `<div class="kv"><span>Metric</span><b>${esc(b.metric)}</b></div>` : ""}
      <div class="kv"><span>System</span><b>${esc(b.model_or_system || "n/a")}</b></div>
      <div class="kv"><span>Capability score (C)</span><b>${b.capability ?? "n/a"}</b></div>
      <div class="kv"><span>Transferability (T)</span><b>${n2(b.transferability)}</b></div>
      <div class="kv"><span>Exposure (C × T)</span><b>${n2(b.exposure)}</b></div>
    </div>`;
}

async function renderAbility(aid) {
  const d = await get(`data/ability/${aid}.json`);
  const cy = d.by_year[YEAR], traj = YEARS.map(y => d.by_year[y].exposure);
  const carried = cy.resolution === "carry_forward";

  const yrRows = YEARS.map(y => {
    const c = d.by_year[y], b = c.benchmark;
    return `<tr><td>${y}</td><td class="num">${n2(c.exposure)}</td>
      <td>${b ? esc(b.name) + (c.source_year !== y ? ` (${c.source_year})` : "") : ""}</td>
      <td class="num">${b && b.capability != null ? b.capability : "n/a"}</td>
      <td class="num">${b ? n2(b.transferability) : "n/a"}</td>
      <td>${esc(c.resolution_label)}</td></tr>`;
  }).join("");

  crumbs.innerHTML = `<a href="#/">All occupations</a><span class="sep">›</span>${esc(d.name)}`;
  view.innerHTML = `
  <div class="head">
    <div class="who"><h2>${esc(d.name)}</h2>
      <p><span class="pill">${esc(d.category)}</span> O*NET ability</p></div>
    <div class="bignums">
      <div class="bignum"><div class="v">${n2(cy.exposure)}</div><div class="l">${YEAR} exposure</div></div>
      <div class="bignum"><div class="v">${spark(traj)}</div><div class="l">${YEARS[0]}-${YEARS[YEARS.length - 1]}</div></div>
    </div>
  </div>
  ${d.definition ? `<p class="cap">${esc(d.definition)}</p>` : ""}

  <div class="yearbtns" style="margin-bottom:14px">${YEARS.map(y =>
    `<button data-y="${y}" class="${y === YEAR ? "on" : ""}">${y}</button>`).join("")}</div>

  <div class="note"><b>${YEAR}:</b> ${esc(cy.resolution_label)}.
    ${esc(META.resolution_labels[cy.resolution] || "")}.</div>

  <h3>${carried ? `Benchmark carried forward from ${cy.source_year}` : `Selected benchmark, ${YEAR}`}</h3>
  <p class="cap">One benchmark is selected per ability and year. Ability exposure is
    capability × transferability (C × T) for that benchmark.</p>
  <div class="cards">${benchCard(cy.benchmark, YEAR)}</div>

  <h3>By year</h3>
  <table><thead><tr><th>Year</th><th class="num">Exposure</th><th>Benchmark</th>
    <th class="num">C</th><th class="num">T</th><th>Status</th></tr></thead><tbody>${yrRows}</tbody></table>

  <h3>Benchmarks selected for this ability</h3>
  <p class="cap">${d.benchmarks_mapped.length} distinct benchmark${d.benchmarks_mapped.length === 1 ? "" : "s"}
    selected across ${YEARS[0]}-${YEARS[YEARS.length - 1]}.</p>
  <div class="cards">${d.benchmarks_mapped.map(b =>
    `<div class="card"><h4>${b.benchmark_id
        ? `<a href="#/bench/${b.benchmark_id}">${esc(b.name)}</a>` : esc(b.name)}</h4>
      <div class="kv"><span>selected</span><b>${b.years_selected.join(", ")}</b></div>
      <div class="kv"><span>rated result</span><b>${b.years_scored.join(", ") || "none"}</b></div>
     </div>`).join("")}</div>`;

  view.querySelectorAll(".yearbtns button").forEach(b =>
    b.addEventListener("click", () => { YEAR = b.dataset.y; renderAbility(aid); }));
}

/* ---------- benchmark ---------- */
async function renderBench(bid) {
  let d;
  try { d = await get(`data/bench/${bid}.json`); }
  catch { view.innerHTML = `<p class="note warn">No transferability record for <code>${esc(bid)}</code>.</p>`; return; }

  const rows = YEARS.filter(y => d.years[y]).map(y => {
    const c = d.years[y];
    return `<tr><td>${y}</td><td class="num">${c.raw_score ?? "n/a"}</td>
      <td>${esc(c.model_or_system || "n/a")}</td>
      <td class="num">${c.capability ?? "n/a"}</td><td class="num">${n2(c.exposure)}</td>
      <td>${esc(c.provenance || "n/a")}</td></tr>`;
  }).join("");

  const f = d.transferability_factors || {};
  const fr = Object.keys(f).map(k =>
    `<div class="kv" title="${esc(f[k].reasoning)}"><span>${esc(k.replace(/_/g, " "))}</span><b>${n2(f[k].score)}</b></div>`).join("");

  crumbs.innerHTML = `<a href="#/">All occupations</a><span class="sep">›</span>
    <a href="#/ability/${d.ability_id}">${esc(d.onet_ability)}</a>
    <span class="sep">›</span>${esc(d.name)}`;
  view.innerHTML = `
  <div class="head">
    <div class="who"><h2>${esc(d.name)}</h2>
      <p>measures <a href="#/ability/${d.ability_id}">${esc(d.onet_ability)}</a>
        &nbsp;<span class="pill">${esc(d.ability_category)}</span></p></div>
    <div class="bignums">
      <div class="bignum"><div class="v">${n2(d.transferability_score)}</div>
        <div class="l">transferability</div></div>
    </div>
  </div>

  ${d.ability_definition ? `<p class="cap">${esc(d.ability_definition)}</p>` : ""}

  <h3>Years this benchmark was selected</h3>
  <table><thead><tr><th>Year</th><th class="num">Best result</th><th>System</th>
    <th class="num">Capability (0-10)</th><th class="num">Exposure (C×T)</th><th>Provenance</th></tr></thead>
    <tbody>${rows || `<tr><td colspan="6" class="cap">No scored years.</td></tr>`}</tbody></table>

  <h3>Transferability factors</h3>
  <div class="cards"><div class="card">${fr || '<span class="cap">Not available.</span>'}</div>
    ${d.transferability_reasoning ? `<div class="card"><h4>Rater's reasoning</h4>
      <p style="font-size:12.5px;margin:0;color:var(--muted)">${esc(d.transferability_reasoning)}</p></div>` : ""}
  </div>`;
}

/* ---------- router ---------- */
function setTab(name) {
  $("#tab-explorer").classList.toggle("on", name === "explorer");
  $("#tab-method").classList.toggle("on", name === "method");
}

async function route() {
  const h = location.hash.replace(/^#\/?/, "");
  tip.hidden = true;
  setTab(h.startsWith("methodology") ? "method" : "explorer");
  try {
    if (h.startsWith("methodology")) await renderMethodology();
    else if (h.startsWith("occ/")) await renderOcc(h.slice(4));
    else if (h.startsWith("ability/")) await renderAbility(h.slice(8));
    else if (h.startsWith("bench/")) await renderBench(h.slice(6));
    else renderGrid();
  } catch (e) {
    view.innerHTML = `<p class="note warn">Could not load: ${esc(e.message)}</p>`;
  }
  scrollTo(0, 0);
}

(async function init() {
  try {
    [META, OCCS, ABILS] = await Promise.all([
      get("data/meta.json"), get("data/occupations.json"), get("data/abilities.json")]);
  } catch (e) {
    view.innerHTML = `<p class="note warn">Data not found. Run
      <code>python3 website/build_data.py</code> first. (${esc(e.message)})</p>`;
    return;
  }
  YEARS = META.years; YEAR = META.latest_year;
  $("#ytd").textContent =
    `${META.latest_year} is year-to-date: it uses benchmark results published up to ` +
    `${META.cutoff}, the date of the run.`;
  $("#buildmeta").textContent =
    `Built ${META.built_utc}. Pipeline ${META.pipeline}, all model stages Claude Opus 5.5. ` +
    `${META.n_occupations} occupations, ${META.n_abilities_mapped} of ${META.n_abilities} abilities ` +
    `mapped, ${META.n_benchmarks} benchmark-ability pairs, ` +
    `cumulative-coverage threshold ${META.cum_coverage_threshold}. ` +
    `Gate (${META.gate.year}): ${META.gate.top_title} ${META.gate.top_score}, ` +
    `mean ${META.gate.mean}, sd ${META.gate.sd}; data match replication ` +
    `${META.gate.replication_commit.slice(0, 7)}.`;
  addEventListener("hashchange", route);
  route();
})();

/* ---------- methodology tab ----------
   Six figures, one per pipeline step, drawn as inline SVG from
   data/methodology.json. No external libraries. */

const PROSE = '<div class="prose-slot">[JAKE: paste methodology text here]</div>';
const V1_MARK = '<span class="prose-slot">[JAKE: v1 text - needs rewrite]</span> ';
const PAL = ["#1f4d6e", "#4f83a8", "#8fb4cd", "#c6d9e6", "#eef3f7"];
// Distinct ramp for the 9 resolution paths, so no two legend swatches repeat.
const PAL9 = ["#16384f", "#1f4d6e", "#356d92", "#4f83a8", "#6d9dbd",
              "#8fb4cd", "#aecbdd", "#c6d9e6", "#e2ecf3"];

function svgWrap(inner, w, h, cls = "") {
  return `<svg class="fig ${cls}" viewBox="0 0 ${w} ${h}" width="100%"
    preserveAspectRatio="xMidYMid meet" role="img">${inner}</svg>`;
}
const tx = (s) => esc(s);

/* Step 1: coverage funnel + resolution-path stacked bar */
function figStep1(d) {
  const W = 720, H = 250;
  const funnel = [
    ["O*NET abilities rated", d.n_rated],
    ["mapped to benchmarks", d.n_mapped],
    [`measured in ${META.latest_year}`, d.n_measured_latest],
  ];
  let s = `<text x="0" y="14" class="ft">Ability coverage</text>`;
  funnel.forEach(([lab, v], i) => {
    const y = 30 + i * 30, w = (v / d.n_rated) * 380;
    s += `<rect x="176" y="${y}" width="${w.toFixed(1)}" height="20" fill="${PAL[i]}"/>
      <text x="168" y="${y + 14}" class="fl" text-anchor="end">${tx(lab)}</text>
      <text x="${(176 + w + 7).toFixed(1)}" y="${y + 14}" class="fv">${v}</text>`;
  });

  const order = Object.entries(d.resolution).sort((a, b) => b[1] - a[1]);
  const tot = order.reduce((a, r) => a + r[1], 0);
  s += `<text x="0" y="152" class="ft">Resolution path, ${tot} ability-years</text>`;
  let x = 0;
  const seg = order.map(([k, v], i) => {
    const w = v / tot * 700;
    const r = `<rect x="${x.toFixed(1)}" y="164" width="${w.toFixed(1)}" height="22"
      fill="${PAL9[i % PAL9.length]}" stroke="#fff" stroke-width="1"><title>${tx(d.resolution_labels[k] || k)}: ${v}</title></rect>`;
    x += w; return r;
  }).join("");
  s += seg;
  // legend
  order.forEach(([k, v], i) => {
    const col = i % 3, row = Math.floor(i / 3);
    s += `<rect x="${col * 240}" y="${200 + row * 17}" width="9" height="9"
        fill="${PAL9[i % PAL9.length]}" stroke="${PAL9[8]}" stroke-width=".5"/>
      <text x="${col * 240 + 14}" y="${208 + row * 17}" class="fl">${tx(d.resolution_labels[k] || k)} (${v})</text>`;
  });
  return svgWrap(s, W, H);
}

/* Step 2: scored observations per year */
function figStep2(d) {
  const W = 720, H = 210, ys = Object.keys(d.per_year), max = Math.max(...Object.values(d.per_year));
  let s = `<text x="0" y="14" class="ft">Scored benchmark-year observations</text>`;
  ys.forEach((y, i) => {
    const v = d.per_year[y], h = v / max * 130, x = 60 + i * 105;
    s += `<rect x="${x}" y="${165 - h}" width="66" height="${h.toFixed(1)}" fill="${PAL[1]}"/>
      <text x="${x + 33}" y="${160 - h}" class="fv" text-anchor="middle">${v}</text>
      <text x="${x + 33}" y="182" class="fl" text-anchor="middle">${y}</text>`;
  });
  s += `<line x1="50" y1="165" x2="700" y2="165" class="ax"/>`;
  return svgWrap(s, W, H);
}

/* Step 3: capability histogram with rubric anchors */
function figStep3(d) {
  const W = 720, H = 230, keys = Object.keys(d.hist).map(Number).sort((a, b) => a - b);
  const max = Math.max(...Object.values(d.hist));
  let s = `<text x="0" y="14" class="ft">Capability score, ${d.n} benchmark-year observations</text>`;
  keys.forEach(k => {
    const v = d.hist[k], h = v / max * 140, x = 48 + k * 60;
    s += `<rect x="${x}" y="${180 - h}" width="46" height="${h.toFixed(1)}" fill="${PAL[0]}"/>
      <text x="${x + 23}" y="${175 - h}" class="fv" text-anchor="middle">${v}</text>
      <text x="${x + 23}" y="196" class="fl" text-anchor="middle">${k}</text>`;
  });
  s += `<line x1="40" y1="180" x2="700" y2="180" class="ax"/>
    <text x="48" y="216" class="fl">0 = no capability</text>
    <text x="352" y="216" class="fl" text-anchor="middle">5 = partial</text>
    <text x="700" y="216" class="fl" text-anchor="end">10 = saturated</text>`;
  return svgWrap(s, W, H);
}

/* Step 4: transferability histogram with mean marked */
function figStep4(d) {
  const W = 720, H = 215;
  const keys = Object.keys(d.hist).map(Number).sort((a, b) => a - b);
  const max = Math.max(...Object.values(d.hist));
  const lo = d.min - 0.5, hi = d.max + 0.5;
  const xf = (t) => 55 + (t - lo) / (hi - lo) * 620;
  let s = `<text x="0" y="14" class="ft">Transferability weight, ${d.n} benchmark-ability pairs</text>`;
  keys.forEach(k => {
    const v = d.hist[k], h = v / max * 130, x = xf(k);
    s += `<rect x="${(x - 20).toFixed(1)}" y="${(165 - h).toFixed(1)}" width="40"
        height="${h.toFixed(1)}" fill="${PAL[1]}"><title>T=${k}: ${v}</title></rect>
      <text x="${x.toFixed(1)}" y="182" class="fl" text-anchor="middle">${k}</text>`;
  });
  const mx = xf(d.mean);
  s += `<line x1="45" y1="165" x2="700" y2="165" class="ax"/>
    <line x1="${mx.toFixed(1)}" y1="28" x2="${mx.toFixed(1)}" y2="165" class="mark"/>
    <text x="${(mx + 6).toFixed(1)}" y="40" class="fv">mean ${d.mean}</text>
    <text x="45" y="202" class="fl">range ${d.min} to ${d.max}</text>`;
  return svgWrap(s, W, H);
}

/* Step 5: 2025 ability exposure dot plot */
function figStep5(d) {
  const rows = d.abilities, W = 720, H = 44 + rows.length * 17;
  const max = Math.max(...rows.map(r => r.exposure));
  let s = `<text x="0" y="14" class="ft">${META.latest_year} exposure, ${rows.length} measured abilities</text>`;
  rows.forEach((r, i) => {
    const y = 34 + i * 17, x = 250 + r.exposure / max * 420;
    s += `<text x="242" y="${y + 4}" class="fl" text-anchor="end">${tx(r.name)}</text>
      <line x1="250" y1="${y}" x2="${x.toFixed(1)}" y2="${y}" class="dl"/>
      <circle cx="${x.toFixed(1)}" cy="${y}" r="3.6" fill="${PAL[0]}">
        <title>${tx(r.name)}: ${r.exposure} from ${tx(r.benchmark)}</title></circle>
      <text x="${(x + 8).toFixed(1)}" y="${y + 4}" class="fv">${r.exposure.toFixed(1)}</text>`;
  });
  return svgWrap(s, W, H);
}

/* Step 6: worked decomposition, contribution waterfall */
function figStep6(d) {
  const rows = d.rows, W = 720, H = 50 + rows.length * 18;
  const max = Math.max(...rows.map(r => r.contribution));
  let s = `<text x="0" y="14" class="ft">${tx(d.title)}: ${rows.length} kept abilities
    sum to ${d.exposure}</text>`;
  let cum = 0;
  rows.forEach((r, i) => {
    const y = 30 + i * 18, w = r.contribution / max * 330;
    cum += r.contribution;
    s += `<text x="212" y="${y + 11}" class="fl" text-anchor="end">${tx(r.ability)}</text>
      <rect x="220" y="${y + 2}" width="${w.toFixed(1)}" height="12" fill="${PAL[1]}">
        <title>weight ${r.weight} x exposure ${r.exposure}</title></rect>
      <text x="${(220 + w + 6).toFixed(1)}" y="${y + 12}" class="fv">${r.contribution.toFixed(2)}</text>
      <text x="700" y="${y + 12}" class="fl" text-anchor="end">${cum.toFixed(2)}</text>`;
  });
  s += `<text x="700" y="18" class="fl" text-anchor="end">cumulative</text>`;
  return svgWrap(s, W, H);
}

const STEPS = [
  ["Step 1", "Ability mapping and judge sweep", figStep1, "step1",
   "52 O*NET abilities are put to three judges, who nominate benchmarks for each ability-year. Coverage narrows at two points: abilities with no benchmark mapping, and mapped abilities with no scored benchmark in a given year.", true],
  ["Step 2", "Benchmark score extraction", figStep2, "step2",
   "Each nominated benchmark is searched for a published best score per year.", true],
  ["Step 3", "Capability rating", figStep3, "step3",
   "Each benchmark-year score is rated 0 to 10 against a rubric anchored on human performance."],
  ["Step 4", "Transferability rating", figStep4, "step4",
   "A three-judge ensemble rates how far each benchmark transfers to the real ability.", true],
  ["Step 5", "Ability-year exposure", figStep5, "step5",
   "Benchmarks resolve to one exposure value per ability-year, T-weighted as sum(C*T^2)/sum(T).", true],
  ["Step 6", "Occupation exposure", figStep6, "step6",
   "O*NET importance and level give each ability a weight. The top-weighted abilities reaching 90% cumulative weight are kept, and their weighted mean is the occupation score."],
];

async function renderMethodology() {
  const d = await get("data/methodology.json");
  crumbs.innerHTML = "";
  view.innerHTML = `
  <article class="paper">
    <h2>How the score is built</h2>
    <p class="lede">Every occupation score traces back through six steps, from AI benchmark
      results to O*NET ability weights. Each figure below is generated from the same
      canonical pipeline outputs the Explorer reads.</p>

    ${STEPS.map(([n, title, fn, key, note, v1]) => `
      <section class="step" id="${key}">
        <h3><span class="stepno">${n}</span> ${tx(title)}</h3>
        ${PROSE}
        <figure>
          ${fn(d[key])}
          <figcaption>${v1 ? V1_MARK : ""}${tx(note)}</figcaption>
        </figure>
      </section>`).join("")}

    <section class="step">
      <h3><span class="stepno">Notes</span> Reproducibility</h3>
      ${PROSE}
    </section>
  </article>`;
}
