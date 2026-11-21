// The open trophy's guide (center), its sources panel and dispute summary (right).
import { chips, h, kindTag } from './dom.js';
import { flagsFor } from './checklist.js';
import { isSpoilerHidden } from './filters.js';
import { sourceStats } from './audit.js';

function disputesFor(data, trophy) {
  return data.disputes.filter((d) => d.trophies.includes(trophy.id));
}

function countTracker(trophy, ctx) {
  const n = ctx.counts[trophy.id] ?? 0;
  const box = h('div', 'count');
  const label = h('span', 'count-label', `YOUR COUNT — ${n}/${trophy.count} ${trophy.countLabel}`);
  const minus = h('button', 'step-btn', '−');
  const plus = h('button', 'step-btn', '+');
  minus.type = plus.type = 'button';
  minus.setAttribute('aria-label', `One less ${trophy.countLabel}`);
  plus.setAttribute('aria-label', `One more ${trophy.countLabel}`);
  minus.disabled = n <= 0;
  plus.disabled = n >= trophy.count;
  minus.addEventListener('click', () => ctx.onCount(trophy.id, n - 1));
  plus.addEventListener('click', () => ctx.onCount(trophy.id, n + 1));
  const bar = h('div', 'count-bar');
  const fill = h('div', 'count-fill');
  fill.style.width = `${Math.round((n / trophy.count) * 100)}%`;
  bar.append(fill);
  box.append(label, minus, plus, bar);
  return box;
}

function claimsSection(trophy, data) {
  const cited = trophy.steps.filter((s) => s.refs.length >= 1).length;
  const multi = trophy.steps.filter((s) => s.refs.length >= 2).length;
  const box = h('section', 'claims');
  box.append(h('h4', '', 'CLAIMS — EVERY FACT CITED'), h('p', 'claims-sum', `${cited}/${trophy.claims} claims cited · ${multi} backed by 2+ sites`));
  const grid = h('ol', 'claims-grid');
  trophy.steps.forEach((s, i) => {
    const li = h('li');
    li.append(h('b', '', `C${i + 1}`), chips(s.refs, data), h('span', 'sites', `${s.refs.length} site${s.refs.length === 1 ? '' : 's'}`));
    grid.append(li);
  });
  box.append(grid);
  return box;
}

export function renderGuide(data, trophy, ctx, root) {
  if (!trophy) {
    root.replaceChildren(h('p', 'empty', 'Pick a trophy to read its guide.'));
    return;
  }
  const idx = data.trophies.indexOf(trophy) + 1;
  if (isSpoilerHidden(trophy, ctx.earned, ctx.settings)) {
    const box = h('div', 'guide-masked');
    box.append(
      h('h3', '', 'Hidden trophy'),
      h('p', '', `#${idx} of ${data.trophies.length} · ${trophy.grade}. The spoiler shield is on, so the name, description and guide stay hidden until you earn it or turn the shield off.`),
    );
    root.replaceChildren(box);
    return;
  }
  const head = h('header', 'guide-head');
  const title = h('h3', '', trophy.name);
  const meta = h('div', 'guide-meta');
  meta.append(h('span', `badge grade-${trophy.grade}`, trophy.grade), h('span', 'idx', `#${idx} of ${data.trophies.length}`), h('span', 'kind', trophy.kind));
  if (trophy.hidden) meta.append(h('span', 'flag hiddenflag', 'PSN-HIDDEN'));
  for (const [cls, text] of flagsFor(trophy, ctx)) meta.append(h('span', cls, text));
  head.append(title, meta, h('blockquote', 'official', trophy.description));

  const steps = h('ol', 'steps');
  for (const s of trophy.steps) {
    const li = h('li');
    li.append(h('span', 'step-text', s.text), chips(s.refs, data));
    steps.append(li);
  }
  const parts = [head];
  if (trophy.count) parts.push(countTracker(trophy, ctx));
  parts.push(steps);
  if (trophy.window) {
    const w = h('p', 'window');
    w.append(h('b', '', 'WINDOW '), trophy.window, ' ', h('b', '', 'LAST CHANCE '), trophy.lastChance);
    parts.push(w);
  }
  const disputes = disputesFor(data, trophy);
  if (disputes.length) parts.push(h('p', 'differ-note', `⚠ ${disputes.length} open point${disputes.length === 1 ? '' : 's'} here (sources differ, or a target or trigger is unconfirmed): see the box on the right for both versions and our call.`));
  parts.push(claimsSection(trophy, data));
  root.replaceChildren(...parts);
}

// Right pane: sources for this guide with per-source claim counts, then the dispute boxes (both versions + our call).
export function renderSourcesPanel(data, trophy, ctx, root) {
  const keys = Object.keys(data.sources);
  const stats = sourceStats(data);
  root.replaceChildren();
  if (!trophy || isSpoilerHidden(trophy, ctx.earned, ctx.settings)) {
    root.append(h('h4', '', 'SOURCES FOR THIS GUIDE'), h('p', 'muted', 'Hidden while the spoiler shield masks this trophy.'));
    return;
  }
  root.append(h('h4', '', 'SOURCES FOR THIS GUIDE'));
  const list = h('ol', 'src-list');
  for (const key of keys) {
    const n = trophy.steps.filter((s) => s.refs.includes(key)).length;
    if (!n) continue;
    const src = data.sources[key];
    const li = h('li');
    li.value = keys.indexOf(key) + 1;
    const link = h('a', '', src.name);
    link.href = src.url;
    link.target = '_blank';
    link.rel = 'noopener noreferrer';
    li.append(link, h('span', 'src-meta', `${n} of ${trophy.claims} claims here · ${stats[key].claims} overall · read ${src.read}`));
    list.append(li);
  }
  root.append(list);
  const disputes = disputesFor(data, trophy);
  if (!disputes.length) return;
  root.append(h('h4', 'differ-h', 'SOURCES DIFFER? OPEN POINTS'));
  for (const d of disputes) {
    const box = h('div', 'dispute');
    box.append(kindTag(d), h('p', 'dq', d.q));
    for (const [label, v] of [['A', d.a], ['B', d.b]]) {
      const row = h('p', 'ver');
      row.append(h('b', '', `${label} `), `${v.say} `, chips(v.by, data));
      box.append(row);
    }
    const call = h('p', 'call');
    call.append(h('b', '', 'OUR CALL '), d.call);
    box.append(call);
    root.append(box);
  }
}
