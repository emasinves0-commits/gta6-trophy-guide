// Sources tab: the numbered source index with read dates and claim counts, then every dispute (both versions + our call).
import { chips, h, kindTag } from './dom.js';
import { sourceStats } from './audit.js';

export function renderSources(data, root) {
  const stats = sourceStats(data);
  const table = h('table', 'src-table');
  const head = h('tr');
  for (const c of ['#', 'Source', 'Address', 'Read', 'Claims cited', 'In guides']) head.append(h('th', '', c));
  table.append(head);
  Object.entries(data.sources).forEach(([key, src], i) => {
    const row = h('tr');
    const link = h('a', '', src.url);
    link.href = src.url;
    link.target = '_blank';
    link.rel = 'noopener noreferrer';
    const addr = h('td');
    addr.append(link);
    row.append(h('td', 'num', String(i + 1)), h('td', '', src.name), addr, h('td', '', src.read), h('td', 'num', String(stats[key].claims)), h('td', 'num', `${stats[key].guides}/${data.trophies.length}`));
    table.append(row);
  });
  const disputes = h('div', 'disputes-grid');
  data.disputes.forEach((d, i) => {
    const box = h('div', 'dispute');
    const ids = d.trophies.length ? ` · ${d.trophies.map((id) => `#${id}`).join(' ')}` : ' · whole list';
    box.append(kindTag(d), h('p', 'dq', `${i + 1}. ${d.q}`), h('p', 'muted', ids.slice(3)));
    for (const [label, v] of [['A', d.a], ['B', d.b]]) {
      const row = h('p', 'ver');
      row.append(h('b', '', `${label} `), `${v.say} `, chips(v.by, data));
      box.append(row);
    }
    const call = h('p', 'call');
    call.append(h('b', '', 'OUR CALL '), d.call);
    box.append(call);
    disputes.append(box);
  });
  root.replaceChildren(h('h3', '', 'SOURCE INDEX'), table, h('h3', '', `DISPUTES AND OPEN QUESTIONS: ${data.disputes.length}, BOTH WAYS (${data.disputes.filter((x) => x.kind === 'disagree').length} are true source disagreements)`), disputes);
}
