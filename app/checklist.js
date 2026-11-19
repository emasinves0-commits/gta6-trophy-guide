// The trophy checklist: one card per trophy with badge, official text, guide, flags and cited sources.
import { isSpoilerHidden } from './filters.js';

// Guides the user has opened; survives re-renders (ticking a checkbox rebuilds the list).
const openGuides = new Set();

function element(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined) node.textContent = text;
  return node;
}

function buildSources(trophy, sourceIndex) {
  const line = element('p', 'sources');
  line.append('Sources: ');
  trophy.sources.forEach((key, i) => {
    const source = sourceIndex[key];
    const link = element('a', '', source.name);
    link.href = source.url;
    link.target = '_blank';
    link.rel = 'noopener noreferrer';
    line.append(link);
    if (i < trophy.sources.length - 1) line.append(' · ');
  });
  return line;
}

function buildCard(trophy, ctx) {
  const hidden = isSpoilerHidden(trophy, ctx.earned, ctx.settings);
  const done = ctx.earned.has(trophy.id);
  const card = element('li', `card grade-${trophy.grade}${done ? ' done' : ''}`);

  const box = document.createElement('input');
  box.type = 'checkbox';
  box.checked = done;
  box.setAttribute('aria-label', hidden ? 'Mark hidden trophy as earned' : `Mark ${trophy.name} as earned`);
  box.addEventListener('change', () => ctx.onToggle(trophy.id, box.checked));

  const head = element('div', 'card-head');
  head.append(
    element('span', `badge grade-${trophy.grade}`, trophy.grade),
    element('h3', '', hidden ? 'Hidden trophy' : trophy.name),
  );
  if (trophy.missable) head.append(element('span', 'flag', 'MISSABLE'));
  if (trophy.unconfirmed) head.append(element('span', 'flag unconfirmed', 'UNCONFIRMED'));
  head.append(element('span', 'kind', trophy.kind));

  const body = element('div', 'card-body');
  body.append(element('p', 'desc', hidden ? 'Earn it, or turn off spoiler hiding, to reveal this.' : trophy.description));
  if (!hidden) {
    const details = element('details');
    details.open = openGuides.has(trophy.id);
    details.addEventListener('toggle', () => (details.open ? openGuides.add(trophy.id) : openGuides.delete(trophy.id)));
    details.append(element('summary', '', 'Guide'), element('p', 'guide', trophy.guide), buildSources(trophy, ctx.sourceIndex));
    body.append(details);
  }
  card.append(box, element('div', 'card-main'));
  card.lastChild.append(head, body);
  return card;
}

export function renderChecklist(trophies, ctx, root) {
  if (!trophies.length) {
    root.replaceChildren(element('li', 'empty', 'No trophies match these filters.'));
    return;
  }
  root.replaceChildren(...trophies.map((t) => buildCard(t, ctx)));
}
