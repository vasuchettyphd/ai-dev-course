// Built by Claude Code (Sonnet) with the Anatomy skill on 2026-10-22, after the follow-up prompt.
// Paths changed to relative so it runs from demo/practice/skill-figure/figure-src/: node figure-src/build.mjs
import { writeFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import * as k from "../.claude/skills/anatomy/kit/iso-kit.mjs";
import { kitScript } from "../.claude/skills/anatomy/scripts/inline-kit.mjs";

const OUT = fileURLToPath(new URL("../figure/skill-use.html", import.meta.url));
const WIDTH = 760, HEIGHT = 460;

// facts from brief.md
const SKILLS = 7, REFS = 10, BODY_LINES = 185, DESC_MAX = "1,024";

const PLATE = { x: -158, y: -72, w: 316, d: 144, r: 8 };
const PLATE_H = 12, FOOT_H = 5;
const RACK = { x: -124, y: -34, w: 216, d: 68, r: 2 };
const RIM = 20;
const FX0 = -112, FSTEP = 30;
const FX = (i) => FX0 + FSTEP * i;
const FW = 9, FOLD_Z = 4, FOLD_TOP = 34, LIFT = 22;
const TRAY = { x: 104, y: -27, w: 46, d: 54, r: 2 };
const TRAY_RIM = 12;
const SY0 = -22, SSTEP = 4.8;
const SY = (j) => SY0 + SSTEP * j;
const SHEET_TOP = 19, SHEET_LIFT = 18;
const RAIL_Y = 52, BEAM_Z = 78, HEAD_TIP = 62, HOME_X = -140;

const P = k.fitProjection(
  [...k.boxCorners(PLATE, -PLATE_H - FOOT_H, 0), [HOME_X, 0, BEAM_Z + 14], [150, 0, BEAM_Z + 14]],
  WIDTH, HEIGHT, { pad: 34, azimuth: 40 },
);
const at = (p) => k.iso(p, P);
const S = (paths, style) => k.solidSvg(paths, style);
const L = (d, style) => k.lineSvg(d, style);
const D = (pts, style) => k.dotsSvg(pts, style);
const dep = (x, y) => k.depthOf([x, y, 0], P);
const frontIsPosY = dep(0, 70) > dep(0, -70);
const slab = (plan, z, h, tone = "mid", bevel = 0.6, extra = {}) => S(k.slabOf(plan, z, h, P, 3, bevel), { tone, ...extra });

function plate() {
  const out = [`<path class="iso-halo" d="${k.haloOf(PLATE, -PLATE_H - FOOT_H, PLATE_H, P)}"/>`];
  const feet = [...k.corners(PLATE, 22)].sort((a, b) => dep(a[0], a[1]) - dep(b[0], b[1]));
  for (const [x, y] of feet) {
    out.push(S(k.cylinder(x, y, 7, -PLATE_H - FOOT_H, 1.6, P, 28), { tone: "lo" }));
    out.push(S(k.cylinder(x, y, 5.4, -PLATE_H - FOOT_H + 1.6, FOOT_H - 1.6, P, 28), { tone: "mid" }));
  }
  out.push(S(k.slabOf(PLATE, -PLATE_H, PLATE_H, P, 8, 1.6), { tone: "mid" }));
  out.push(L(k.planOutline(k.insetPlan(PLATE, 5), 0, P), { tone: "lo" }));
  const sc = k.corners(PLATE, 10);
  out.push(L(sc.map(([x, y]) => k.ring(x, y, 2.2, 0, P, 16)).join(""), { tone: "lo" }));
  out.push(D(sc.map(([x, y]) => at([x, y, 0])), { size: 0.5 }));
  const strip = { x: -140, y: PLATE.y + 6, w: 280, d: 7, r: 1 };
  out.push(S(k.slabOf(strip, 0, 0.6, P, 3), { tone: "lo", crease: "none" }));
  const t = k.topTicks(strip.x + 4, strip.x + strip.w - 4, 4, 5, strip.y + 0.8, 0.6, [2, 3.6], P);
  out.push(L(t.minor, { tone: "lo" }), L(t.major, { tone: "mid" }));
  out.push(D([at([strip.x + 2, strip.y + 3.5, 0.6]), at([strip.x + strip.w - 2, strip.y + 3.5, 0.6])], { size: 0.45 }));
  return out.join("");
}

function rails() {
  const out = [];
  for (const y of [-RAIL_Y, RAIL_Y]) {
    out.push(slab({ x: -150, y: y - 2.5, w: 300, d: 5, r: 1 }, 0, 3, "mid", 0.4));
    out.push(L(k.lineOnTop([-148, y], [148, y], 3, P), { tone: "faint" }));
    out.push(D([-143, 143].map((x) => at([x, y, 3])), { size: 0.4 }));
  }
  return out.join("");
}

const wall = (plan, side) => ({ x: plan.x, y: side < 0 ? plan.y : plan.y + plan.d - 3, w: plan.w, d: 3, r: 0.6 });
const farSide = frontIsPosY ? -1 : 1;

function rack(part) {
  if (part === "back") {
    const out = [slab(RACK, 0, 3, "lo")];
    out.push(slab(wall(RACK, farSide), 3, RIM - 3));
    for (const x of [RACK.x, RACK.x + RACK.w - 3]) out.push(slab({ x, y: RACK.y + 3, w: 3, d: RACK.d - 6, r: 0.6 }, 3, RIM - 3));
    return out.join("");
  }
  const near = wall(RACK, -farSide);
  const out = [slab(near, 3, RIM - 3)];
  out.push(L(k.lineOnTop([near.x + 2, near.y + 1.5], [near.x + near.w - 2, near.y + 1.5], RIM, P), { tone: "faint" }));
  out.push(D([6, 50, 90, 130, 170, 210].map((dx) => at([RACK.x + dx, near.y + 1.5, RIM])), { size: 0.4, tone: "lo" }));
  return out.join("");
}

function folder(i) {
  const out = [];
  out.push(slab({ x: FX(i), y: -29, w: FW, d: 58, r: 1 }, FOLD_Z, FOLD_TOP - FOLD_Z, "mid", 0.5));
  out.push(slab({ x: FX(i) - 0.5, y: -9, w: FW + 1, d: 18, r: 1 }, FOLD_TOP, 7, "hi", 0.5));
  for (const y of [-5, 0, 5]) out.push(L(k.lineOnTop([FX(i) + 2, y], [FX(i) + FW - 2, y], FOLD_TOP + 7, P), { tone: "lo" }));
  return out.join("");
}
function folders() {
  const order = [...Array(SKILLS).keys()].sort((a, b) => dep(FX(a), 0) - dep(FX(b), 0));
  return order.map((i) => `<g data-folder="${i}" transform="${k.translateAlong(P, [0, 0, 0])}">${folder(i)}</g>`).join("");
}

function tray(part) {
  if (part === "back") return slab(TRAY, 0, 3, "lo") + slab(wall(TRAY, farSide), 3, TRAY_RIM - 3);
  const near = wall(TRAY, -farSide);
  return slab(near, 3, TRAY_RIM - 3) + D([8, 38].map((dx) => at([TRAY.x + dx, near.y + 1.5, TRAY_RIM])), { size: 0.4, tone: "lo" });
}
function sheets() {
  const order = [...Array(REFS).keys()].sort((a, b) => dep(0, SY(a)) - dep(0, SY(b)));
  return order.map((j) => {
    const plan = { x: TRAY.x + 4, y: SY(j), w: 38, d: 2.2, r: 0.5 };
    const body = slab(plan, 3, SHEET_TOP - 3, "mid", 0.3) + L(k.lineOnTop([plan.x + 3, plan.y + 1.1], [plan.x + 24, plan.y + 1.1], SHEET_TOP, P), { tone: "lo" });
    return `<g data-sheet="${j}" transform="${k.translateAlong(P, [0, 0, 0])}">${body}</g>`;
  }).join("");
}

// gantry, built at x = 0
function post(y) {
  return slab({ x: -8, y: y - 6, w: 16, d: 12, r: 2 }, 3, 6) + slab({ x: -3, y: y - 3, w: 6, d: 6, r: 1 }, 9, BEAM_Z - 9, "mid", 0.5)
    + D([at([-5, y, 9]), at([5, y, 9])], { size: 0.4, tone: "lo" });
}
function gantryFar() { return post(frontIsPosY ? -RAIL_Y : RAIL_Y); }
function gantryNear() {
  const out = [post(frontIsPosY ? RAIL_Y : -RAIL_Y)];
  out.push(slab({ x: -4, y: -RAIL_Y - 4, w: 8, d: 2 * RAIL_Y + 8, r: 1.5 }, BEAM_Z, 7, "mid", 0.6));
  for (const x of [-2, 2]) out.push(L(k.lineOnTop([x, -RAIL_Y], [x, RAIL_Y], BEAM_Z + 7, P), { tone: "faint" }));
  return out.join("");
}
function head() {
  const out = [slab({ x: -7, y: -9, w: 14, d: 18, r: 2 }, BEAM_Z + 7, 7, "mid", 0.6)];
  out.push(D([at([-4, -5, BEAM_Z + 14]), at([4, 5, BEAM_Z + 14])], { size: 0.45 }));
  out.push(S(k.cylinder(0, 0, 4.5, BEAM_Z - 6, 6, P, 24), { tone: "hi" }));
  out.push(S(k.cylinder(0, 0, 3, HEAD_TIP + 3, BEAM_Z - 9 - HEAD_TIP, P, 20), { tone: "hi", crease: "none", lit: true }));
  out.push(S(k.cylinder(0, 0, 3.8, HEAD_TIP, 3, P, 20), { tone: "hi", lit: true }));
  return out.join("");
}

const svg = k.figureSvg({
  width: WIDTH, height: HEIGHT,
  label: `A reading gantry over a rack of ${SKILLS} skill folders. It scans the tabs (the short descriptions), lifts the one matching folder out of the rack (the SKILL.md body, about ${BODY_LINES} lines), then reaches a tray of ${REFS} reference sheets and lifts just one.`,
  body: [
    plate(), rails(),
    `<g data-part="gantry-far">${gantryFar()}</g>`,
    rack("back"), folders(), rack("front"),
    tray("back"), sheets(), tray("front"),
    `<g data-part="gantry-near">${gantryNear()}<g data-part="head">${head()}</g></g>`,
  ],
});

const live = `
const P = ${JSON.stringify(P)};
const SKILLS = ${SKILLS}, REFS = ${REFS};
const FX = (i) => ${FX0} + ${FSTEP} * i + ${FW / 2};
const SY = (j) => ${SY0} + ${SSTEP} * j + 1.1;
const LIFT = ${LIFT}, SHEET_LIFT = ${SHEET_LIFT}, HOME = ${HOME_X}, TRAY_X = ${TRAY.x + 23};
const stage = document.querySelector(".iso-stage");
const svg = stage.querySelector("svg");
const q = (s) => svg.querySelector(s);
const gf = q('[data-part="gantry-far"]'), gn = q('[data-part="gantry-near"]'), hd = q('[data-part="head"]');
const folders = [...Array(SKILLS).keys()].map((i) => q('[data-folder="' + i + '"]'));
const sheets = [...Array(REFS).keys()].map((j) => q('[data-sheet="' + j + '"]'));
const readout = document.querySelector("[data-readout]");
const still = matchMedia("(prefers-reduced-motion: reduce)");
const ease = (t) => (t <= 0 ? 0 : t >= 1 ? 1 : t * t * (3 - 2 * t));
const seg = (t, a, b) => ease((t - a) / (b - a));
const PICKS = [3, 5, 1, 4, 2, 6, 0];
let frame = 0, visible = false, litIdx = -1, litSheet = -1, lastText = "", cycle = 0, start = 0;
function plan(m, from) {
  const r = 0;
  const a = 0.8 + Math.abs(FX(m) - from) / 38, b = a + 0.9, c = b + 1.0, d = c + 1.6, e = d + 1.2, f = e + 1.4, g = f + 1.6;
  return { m, r, from, a, b, c, d, e, f, g };
}
let cur = plan(PICKS[0], HOME), touring = true, userPick = -1, idleTimer = 0, lastGx = HOME;
function state(t, p) {
  let gx = p.from, hy = 0, fl = 0, sl = 0, text;
  const tabX = FX(p.m);
  if (t < p.a) {
    gx = p.from + (tabX - p.from) * ease(t / p.a);
    const seen = Math.min(SKILLS - 1, Math.max(0, Math.round((gx - FX(0)) / 30)));
    text = "1 · tab " + (seen + 1) + " of " + SKILLS + " · ≤ ${DESC_MAX} chars";
  } else if (t < p.b) { gx = tabX; text = "match · skill " + (p.m + 1) + " of " + SKILLS; }
  else if (t < p.c) { gx = tabX; fl = seg(t, p.b, p.c); text = "2 · SKILL.md · ~${BODY_LINES} lines"; }
  else if (t < p.e) {
    fl = 1; gx = tabX + (TRAY_X - tabX) * seg(t, p.c, p.d); hy = SY(p.r) * seg(t, p.c + 0.5, p.d); sl = seg(t, p.d, p.e);
    text = sl > 0 ? "3 · reference " + (p.r + 1) + " of ${REFS}" : "body points to a reference";
  } else if (t < p.f) { fl = 1; sl = 1; gx = TRAY_X; hy = SY(p.r); text = "loaded: 1 body + 1 reference"; }
  else { const u = seg(t, p.f, p.g); fl = 1 - u; sl = 1 - u; gx = TRAY_X + (HOME - TRAY_X) * u; hy = SY(p.r) * (1 - u); text = "back to descriptions only"; }
  return { gx, hy, fl, sl, text };
}
function draw(s) {
  const T = translateAlong(P, [s.gx, 0, 0]);
  gf.setAttribute("transform", T); gn.setAttribute("transform", T);
  hd.setAttribute("transform", translateAlong(P, [0, s.hy, 0]));
  folders.forEach((f, i) => f.setAttribute("transform", translateAlong(P, [0, 0, i === cur.m ? LIFT * s.fl : 0])));
  sheets.forEach((f, j) => f.setAttribute("transform", translateAlong(P, [0, 0, j === cur.r ? SHEET_LIFT * s.sl : 0])));
  const want = s.fl > 0.5 ? cur.m : -1, wantSheet = s.sl > 0.5 ? cur.r : -1;
  if (want !== litIdx || wantSheet !== litSheet) {
    const mark = (list, on) => list.forEach((f, i) => f.querySelectorAll(".iso-solid").forEach((g) => (i === on ? g.setAttribute("data-lit", "") : g.removeAttribute("data-lit"))));
    mark(folders, want); mark(sheets, wantSheet);
    litIdx = want; litSheet = wantSheet;
  }
  if (s.text !== lastText) { readout.textContent = s.text; lastText = s.text; }
  lastGx = s.gx;
}
function tick(now) {
  if (!start) start = now;
  let t = (now - start) / 1000;
  if (touring && t > cur.g + 1.2) { cycle++; cur = plan(PICKS[cycle % PICKS.length], HOME); start = now; t = 0; }
  if (!touring && t > cur.f) { draw(state(cur.f, cur)); frame = 0; return; }
  draw(state(t, cur));
  frame = visible ? requestAnimationFrame(tick) : 0;
}
const run = () => { if (!frame && visible && !still.matches) { start = 0; frame = requestAnimationFrame(tick); } };
function drive(m) {
  touring = false; clearTimeout(idleTimer);
  idleTimer = setTimeout(() => { touring = !still.matches; userPick = -1; cycle++; cur = plan(PICKS[cycle % PICKS.length], lastGx); start = 0; run(); }, 4000);
  if (m === userPick) return;
  userPick = m; cur = plan(m, lastGx); start = 0; cancelAnimationFrame(frame); frame = 0; run();
}
const nearest = (cx) => { let best = 0, gap = 1e9; folders.forEach((f, i) => { const b = f.getBoundingClientRect(), d = Math.abs((b.left + b.right) / 2 - cx); if (d < gap) { gap = d; best = i; } }); return best; };
stage.addEventListener("pointermove", (e) => drive(nearest(e.clientX)));
stage.addEventListener("keydown", (e) => {
  const here = userPick < 0 ? cur.m : userPick;
  let to = null;
  if (e.key === "ArrowRight" || e.key === "ArrowUp") to = Math.min(SKILLS - 1, here + 1);
  if (e.key === "ArrowLeft" || e.key === "ArrowDown") to = Math.max(0, here - 1);
  if (e.key === "Home") to = 0;
  if (e.key === "End") to = SKILLS - 1;
  if (to === null) return;
  e.preventDefault(); drive(to);
});
new IntersectionObserver((es) => { visible = es[es.length - 1].isIntersecting; if (visible) run(); }, { rootMargin: "120px 0px" }).observe(stage);
if (still.matches) touring = false;
draw(state(still.matches ? cur.e + 0.1 : 0, cur));
`;

const body = k.plateHtml({
  fig: "Fig 1",
  title: "How a skill gets used",
  hint: "Hover or ←/→ picks the match · tour runs when idle",
  readout: `${SKILLS} skills · descriptions only`,
  keys: [
    { mark: "lit", label: "Reading head and the one folder it opens: what gets loaded" },
    { mark: "raised", label: `${SKILLS} folder tabs: the short description each skill keeps in memory` },
  ],
  caption: `Startup reads only each skill's name and description (at most ${DESC_MAX} characters). A matching request opens that one SKILL.md body, about ${BODY_LINES} lines for Anatomy. Its ${REFS} reference guides stay shut until the body points to one.`,
  body: `<div class="iso-stage" tabindex="0" role="img" aria-label="Skill loading in three steps">${svg}</div>`,
});
writeFileSync(OUT, k.pageHtml({ title: "How a skill gets used", theme: "dark", body, script: kitScript() + live }));
console.log("wrote", OUT, "frontIsPosY", frontIsPosY);
