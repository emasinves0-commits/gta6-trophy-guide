// The checklist pane: one compact row per trophy (grade, name, flags, checkbox). Clicking a row opens its guide.
import { h } from './dom.js';
import { isSpoilerHidden } from './filters.js';

export function flagsFor(trophy, ctx) {
  const flags = [];
  if (trophy.missable) flags.push(['flag', 'MISSABLE']);
  else if (trophy.atRisk && !trophy.unconfirmed) flags.push(['flag risk', 'AT RISK']);
  if (trophy.unconfirmed) flags.push(['flag unconfirmed', 'UNCONFIRMED']);
  if (ctx && ctx.disputed.has(trophy.id)) flags.push(['flag disputed', 'DISPUTED']);
  return flags;
}

function buildRow(trophy, ctx) {
  const hidden = isSpoilerHidden(trophy, ctx.earned, ctx.settings);
  const done = ctx.earned.has(trophy.id);
  const row = h('li', `row grade-${trophy.grade}${done ? ' done' : ''}${ctx.openId === trophy.id ? ' open' : ''}`);
  row.dataset.id = String(trophy.id);

  const box = document.createElement('input');
  box.type = 'checkbox';
  box.checked = done;
  box.setAttribute('aria-label', hidden ? 'Mark hidden trophy as earned' : `Mark ${trophy.name} as earned`);
  box.addEventListener('click', (e) => e.stopPropagation());
  box.addEventListener('change', () => ctx.onToggle(trophy.id, box.checked));

  const open = h('button', 'row-open');
  open.type = 'button';
  open.setAttribute('aria-pressed', String(ctx.openId === trophy.id));
  open.append(h('span', `badge grade-${trophy.grade}`, trophy.grade[0].toUpperCase()), h('span', 'row-name', hidden ? 'Hidden trophy' : trophy.name));
  if (!hidden) for (const [cls, text] of flagsFor(trophy, ctx)) open.append(h('span', cls, text));
  open.addEventListener('click', () => ctx.onOpen(trophy.id));
  row.append(box, open);
  return row;
}

export function renderChecklist(trophies, ctx, root) {
  if (!trophies.length) {
    root.replaceChildren(h('li', 'empty', 'No trophies match these filters.'));
    return;
  }
  root.replaceChildren(...trophies.map((t) => buildRow(t, ctx)));
}
