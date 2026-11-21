// Roadmap order: the NEXT UP list in the tracker's left pane, and the Roadmap tab with its stages.
import { h } from './dom.js';
import { flagsFor } from './checklist.js';
import { isSpoilerHidden } from './filters.js';

// Roadmap order: possibly missable first, then by stage, then by list position. Earned trophies drop out.
export function nextUp(data, earned) {
  return data.trophies
    .map((t, i) => ({ t, i }))
    .filter(({ t }) => !earned.has(t.id))
    .sort((a, b) => Number(b.t.missable) - Number(a.t.missable) || a.t.stage - b.t.stage || a.i - b.i)
    .map(({ t }) => t);
}

export function renderNextUp(data, ctx, root, limit = 8) {
  root.replaceChildren(
    ...nextUp(data, ctx.earned)
      .slice(0, limit)
      .map((t, i) => {
        const hidden = isSpoilerHidden(t, ctx.earned, ctx.settings);
        const li = h('li');
        const btn = h('button', 'nu');
        btn.type = 'button';
        btn.append(h('b', 'nu-n', String(i + 1)), h('span', 'nu-name', hidden ? `Hidden trophy (${t.grade})` : t.name));
        if (!hidden) for (const [cls, text] of flagsFor(t)) btn.append(h('span', cls, text));
        btn.addEventListener('click', () => ctx.onOpen(t.id));
        li.append(btn);
        return li;
      }),
  );
}

export function renderRoadmap(data, ctx, root) {
  const stages = data.roadmap.map((stage) => {
    const items = data.trophies.filter((t) => t.stage === stage.stage);
    const done = items.filter((t) => ctx.earned.has(t.id)).length;
    const section = h('section', 'stage');
    const head = h('h3', '');
    head.append(`Stage ${stage.stage}: ${stage.title}`, h('span', 'stage-count', `${done}/${items.length} done`));
    section.append(head, h('p', 'stage-meta', `${items.length} trophies · ${stage.hours}`), h('p', 'stage-detail', stage.detail));
    const list = h('ul', 'stage-list');
    for (const t of items) {
      const hidden = isSpoilerHidden(t, ctx.earned, ctx.settings);
      const li = h('li', ctx.earned.has(t.id) ? 'done' : '');
      const box = document.createElement('input');
      box.type = 'checkbox';
      box.checked = ctx.earned.has(t.id);
      box.setAttribute('aria-label', `Earned: ${hidden ? 'hidden trophy' : t.name}`);
      box.addEventListener('change', () => ctx.onToggle(t.id, box.checked));
      li.append(box, h('span', 'stage-name', hidden ? `Hidden trophy (${t.grade})` : t.name));
      if (t.missable) li.append(h('span', 'flag', 'MISSABLE'));
      list.append(li);
    }
    section.append(list);
    return section;
  });
  const notes = h('div', 'road-notes');
  notes.append(h('p', 'callout', data.missableNote), h('h4', '', 'TOTAL TIME & SAVING'));
  const ul = h('ul', 'notes');
  for (const n of data.roadmapNotes) ul.append(h('li', '', n));
  notes.append(ul);
  root.replaceChildren(h('div', 'stages', ''), notes);
  root.firstChild.append(...stages);
}
