// Contrôle des chiffres du dashboard.
//   node tools/check_aggregates.mjs            -> affiche les agrégats et recoupe les chiffres écrits en dur
//   node tools/check_aggregates.mjs --write    -> régénère tools/reference_aggregates.json
//   node tools/check_aggregates.mjs --check    -> échoue si les agrégats diffèrent de la référence
import { readFileSync, writeFileSync, existsSync } from 'node:fs';
import vm from 'node:vm';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const ctx = { window: {} };
vm.createContext(ctx);
vm.runInContext(readFileSync(path.join(root, 'data/rixensart_data.js'), 'utf8'), ctx);
const data = ctx.window.TELRAAM_RIXENSART;
const hist = ctx.window.TELRAAM_HISTORY;

// --- Même logique que l'index.html actuel (speedStatus) ---
// --- Écarts à la tendance communale : le code est lu dans index.html (entre les repères <timeline>) ---
const html = readFileSync(path.join(root, 'index.html'), 'utf8');
const tl = html.match(/\/\/ <timeline>([\s\S]*?)\/\/ <\/timeline>/);
const tlCtx = {};
vm.createContext(tlCtx);
if (tl) vm.runInContext(tl[1] + '\nthis.buildTimeline = buildTimeline;', tlCtx);
const refTl = JSON.parse(readFileSync(path.join(root, 'tools/reference_timeline.json'), 'utf8'));
function checkTimeline() {
  if (!tlCtx.buildTimeline) return ['buildTimeline introuvable dans index.html'];
  const T = JSON.parse(JSON.stringify(tlCtx.buildTimeline(hist)));
  const errs = [];
  refTl.trend.forEach((t, j) => { if (Math.abs(T.trend[j] - t) > 1) errs.push(`tendance ${refTl.dates[j]} : ${T.trend[j]} au lieu de ${t}`); });
  for (const r of refTl.streets) {
    const g = T.streets.find(x => x.id === r.id);
    if (!g) { errs.push(`rue absente : ${r.street}`); continue; }
    r.values.forEach((v, j) => {
      const w = g.values[j];
      if (v == null || w == null) { if (v !== w) errs.push(`${r.street} ${refTl.dates[j]} : ${w} au lieu de ${v}`); }
      else if (Math.abs(w - v) > 1) errs.push(`${r.street} ${refTl.dates[j]} : ${w.toFixed(1)} au lieu de ${v}`);
    });
    const sus = (refTl.suspect[r.street] || []);
    g.suspect.forEach((f, j) => { if (f !== sus.includes(j)) errs.push(`${r.street} ${refTl.dates[j]} : drapeau « suspect » ${f}`); });
  }
  return errs;
}

const speedStatus = (v85, limit) => {
  if (!v85) return 'none';
  const d = v85 - limit;
  return d > 5 ? 'high' : d > 2 ? 'warn' : 'ok';
};
const r1 = n => (n == null ? null : Math.round(n * 10) / 10);

// --- Agrégats de référence (tableaux 1 et 4, calculés en JS dans la page) ---
const streets = data.map(s => {
  const nov = s.nov2024 || {};
  const v85 = (nov.speed || {}).avg_v85 || null;
  const limit = s.speed_limit || 50;
  return {
    id: s.id, street: s.street, limit, v85,
    delta: v85 ? r1(v85 - limit) : null,
    status: speedStatus(v85, limit),
    dailyTotal: nov.daily_total || 0,
    dailyBikes: nov.daily_bikes || 0,
    bikePct: nov.bike_pct || 0,
    pedPct: nov.ped_pct || 0,
    activePct: nov.active_pct ?? null,
    // V85 récente (21 août – 4 sept. 2026) : null si le capteur n'a rien mesuré
    recentV85: (s.recent2026 || {}).avg_v85 ?? null,
    recentDelta: (s.recent2026 || {}).avg_v85 ? r1(s.recent2026.avg_v85 - limit) : null,
    recentStatus: speedStatus((s.recent2026 || {}).avg_v85 || null, limit),
  };
});
const zone30 = streets.filter(s => s.limit === 30 && s.v85);
const worst = zone30.reduce((a, b) => (b.v85 > a.v85 ? b : a));
const hero = { worst: worst.street, v85: worst.v85, over5: zone30.filter(z => z.v85 - 30 > 5).length, of: zone30.length };

// Comparaison saisonnière issue de yoy_analysis
const yoy = hist.yoy_analysis;
const pick = k => ({ label: yoy[k].label, sensors: yoy[k].constant_sensors_count ?? null, totals: yoy[k].totals });
const seasonal = { autumn: pick('autumn'), spring: pick('spring') };

const reference = { streets, hero, seasonal };

// --- Année glissante : change à chaque mise à jour, donc contrôlée avec des tolérances, pas à l'identique ---
const yearNow = Object.fromEntries(data.filter(s => s.year).map(s => [s.id, {
  street: s.street, v85: s.year.v85 ?? null, coverage: s.year.coverage ?? 0, vehicles: (s.year.per_day || {}).vehicles ?? null,
}]));
const yearRefPath = path.join(root, 'tools/reference_year.json');
const YEAR_TOL = { v85: 6, vehiclesPct: 35 };   // km/h ; % d'écart tolérés entre deux mises à jour
function checkYear() {
  const errs = [];
  const n = Object.keys(yearNow).length;
  if (n < 10) errs.push(`année glissante présente pour ${n} capteurs seulement (attendu : 10 au moins)`);
  for (const [id, y] of Object.entries(yearNow)) {
    if (y.v85 != null && (y.v85 < 10 || y.v85 > 120)) errs.push(`${y.street} : V85 annuelle invraisemblable (${y.v85})`);
    if (y.coverage < 0 || y.coverage > 1) errs.push(`${y.street} : couverture hors 0-1 (${y.coverage})`);
    if (y.coverage > 0 && !y.vehicles) errs.push(`${y.street} : aucun véhicule malgré une couverture de ${y.coverage}`);
  }
  if (existsSync(yearRefPath)) {
    const ref = JSON.parse(readFileSync(yearRefPath, 'utf8'));
    for (const [id, r] of Object.entries(ref)) {
      const y = yearNow[id];
      if (!y) { errs.push(`${r.street} : année glissante absente`); continue; }
      if (r.v85 != null && y.v85 != null && Math.abs(y.v85 - r.v85) > YEAR_TOL.v85) errs.push(`${r.street} : V85 annuelle ${y.v85} (référence ${r.v85})`);
      if (r.vehicles && y.vehicles && Math.abs(y.vehicles - r.vehicles) / r.vehicles * 100 > YEAR_TOL.vehiclesPct) errs.push(`${r.street} : ${y.vehicles} véh./j (référence ${r.vehicles})`);
    }
  }
  return errs;
}
const refPath = path.join(root, 'tools/reference_aggregates.json');
const arg = process.argv[2];

if (arg === '--write') {
  writeFileSync(refPath, JSON.stringify(reference, null, 2) + '\n');
  writeFileSync(yearRefPath, JSON.stringify(yearNow, null, 2) + '\n');
  console.log('Référence écrite :', refPath);
  process.exit(0);
}
if (arg === '--check') {
  const tlErrs = checkTimeline();
  if (tlErrs.length) { console.log('ÉCART écarts à la tendance :\n - ' + tlErrs.join('\n - ')); process.exit(1); }
  const yErrs = checkYear();
  if (yErrs.length) { console.log('ÉCART année glissante :\n - ' + yErrs.join('\n - ')); process.exit(1); }
  const expected = JSON.parse(readFileSync(refPath, 'utf8'));
  const same = JSON.stringify(expected) === JSON.stringify(JSON.parse(JSON.stringify(reference)));
  console.log(same ? 'OK : aucun écart avec la référence.' : 'ÉCART avec tools/reference_aggregates.json');
  process.exit(same ? 0 : 1);
}

// --- Recoupement des chiffres écrits en dur (tableaux 2 et 3 de l'index.html actuel) ---
const by = name => data.find(s => s.street.startsWith(name));
const sum = (period, key) => data.reduce((t, s) => t + ((s.history_periods || {})[period]?.[key] || 0), 0);
const rows = [];
const claim = (label, written, computed, note = '') => rows.push({ label, écrit: written, calculé: computed, note });

const tot = k => ['cars', 'pedestrians', 'bikes', 'heavy'].reduce((t, m) => t + sum(k, m), 0);
for (const p of ['nov2024', 'jan2025', 'may2025', 'nov2025', 'may2026']) {
  const t = tot(p);
  console.log(`Répartition ${p} (tous capteurs, ${t.toLocaleString('fr-FR')} passages) :`,
    ['cars', 'pedestrians', 'bikes', 'heavy'].map(m => `${m} ${(100 * sum(p, m) / t).toFixed(1)}%`).join(' · '));
}
const jan = sum('jan2025', 'bikes'), may = sum('may2025', 'bikes');
claim('Vélos janvier 2025 (tous capteurs)', 20574, jan);
claim('Vélos mai 2025 (tous capteurs)', 60501, may);
claim('Hausse jan→mai', '+194 %', `${r1(100 * (may - jan) / jan)} %`);

const gare = by('Rue de la Gare'), til = by('Rue du Tilleul'), bou = by('Avenue de Boulogne');
const g = gare.nov2024, t = til.nov2024, b = bou.nov2024;
claim('Gare V85', 44.5, g.speed.avg_v85);
claim('Gare écart à 30', '+14,5', r1(g.speed.avg_v85 - 30));
claim('Gare mobilités actives', '17,1 %', g.active_pct + ' %');
claim('Gare vélos / jour', 154, g.daily_bikes);
claim('Tilleul V85', 37.2, t.speed.avg_v85);
claim('Tilleul écart à 30', '+7,2', r1(t.speed.avg_v85 - 30));
claim('Tilleul mobilités actives', '22,3 %', t.active_pct + ' %');
claim('Tilleul part vélos', '11,4 %', t.bike_pct + ' %');
claim('Tilleul part piétons', '10,9 %', t.ped_pct + ' %');
claim('Boulogne V85', 59.2, b.speed.avg_v85);
claim('Boulogne pointes (max V85)', 61, b.speed.max_v85);
claim('Boulogne mobilités actives', '8,0 %', b.active_pct + ' %');
console.table(rows);
console.log('Hero :', hero);
console.log('Saisonnier :', JSON.stringify(seasonal.spring.totals));
