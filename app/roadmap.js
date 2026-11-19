// The roadmap to the platinum: ordered stages, each listing its trophies and how many are done.
import { isSpoilerHidden } from './filters.js';

export function renderRoadmap(data, earned, settings, root, onToggle) {
  root.replaceChildren(
    ...data.roadmap.map((stage) => {
      const items = data.trophies.filter((t) => t.stage === stage.stage);
      const done = items.filter((t) => earned.has(t.id)).length;
      const section = document.createElement('section');
      section.className = 'stage';
      const head = document.createElement('h3');
      head.textContent = `Stage ${stage.stage}: ${stage.title} (${stage.hours})`;
      const count = document.createElement('span');
      count.className = 'stage-count';
      count.textContent = `${done}/${items.length}`;
      head.append(count);
      const detail = document.createElement('p');
      detail.textContent = stage.detail;
      const list = document.createElement('ul');
      for (const t of items) list.append(buildStageItem(t, earned, settings, onToggle));
      section.append(head, detail, list);
      return section;
    }),
  );
}

function buildStageItem(trophy, earned, settings, onToggle) {
  const li = document.createElement('li');
  const box = document.createElement('input');
  box.type = 'checkbox';
  box.checked = earned.has(trophy.id);
  box.setAttribute('aria-label', `Earned: ${trophy.name}`);
  box.addEventListener('change', () => onToggle(trophy.id, box.checked));
  const label = document.createElement('span');
  label.textContent = isSpoilerHidden(trophy, earned, settings) ? `Hidden trophy (${trophy.grade})` : trophy.name;
  li.append(box, label);
  if (trophy.missable) {
    const flag = document.createElement('span');
    flag.className = 'flag';
    flag.textContent = 'MISSABLE';
    li.append(flag);
  }
  return li;
}
