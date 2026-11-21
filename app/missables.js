// Missables tab: every missable, at-risk or unconfirmed trophy with its window and last-chance note.
import { h } from './dom.js';
import { flagsFor } from './checklist.js';
import { isSpoilerHidden } from './filters.js';

export function renderMissables(data, ctx, root) {
  const rows = data.trophies.filter((t) => t.missable || t.atRisk || t.unconfirmed);
  const open = rows.filter((t) => !ctx.earned.has(t.id)).length;
  const intro = h('p', 'callout', `${rows.length} trophies carry a risk flag; ${open} still open. ${data.missableNote}`);
  const grid = h('div', 'miss-grid');
  for (const t of rows) {
    const hidden = isSpoilerHidden(t, ctx.earned, ctx.settings);
    const card = h('article', `miss${ctx.earned.has(t.id) ? ' done' : ''}`);
    const box = document.createElement('input');
    box.type = 'checkbox';
    box.checked = ctx.earned.has(t.id);
    box.setAttribute('aria-label', `Earned: ${hidden ? 'hidden trophy' : t.name}`);
    box.addEventListener('change', () => ctx.onToggle(t.id, box.checked));
    const head = h('div', 'miss-head');
    head.append(box, h('b', '', hidden ? `Hidden trophy (${t.grade})` : t.name));
    for (const [cls, text] of flagsFor(t, ctx)) head.append(h('span', cls, text));
    card.append(head);
    if (!hidden) {
      const w = h('p');
      w.append(h('b', '', 'WINDOW '), t.window ?? 'Chapter 1 only');
      const l = h('p');
      l.append(h('b', '', 'LAST CHANCE '), t.lastChance ?? 'See guide');
      card.append(w, l);
      const link = h('button', 'link', 'Open guide');
      link.type = 'button';
      link.addEventListener('click', () => ctx.onOpen(t.id, true));
      card.append(link);
    } else card.append(h('p', 'muted', 'Window hidden by the spoiler shield.'));
    grid.append(card);
  }
  root.replaceChildren(intro, grid);
}
