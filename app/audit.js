// The audit: every number is counted from the loaded data at runtime, nothing here is a typed-in total.
import { h } from './dom.js';

export function audit(data) {
  const trophies = data.trophies;
  const steps = trophies.flatMap((t) => t.steps);
  const hosts = new Set(Object.values(data.sources).map((s) => new URL(s.url).hostname));
  return {
    trophies: trophies.length,
    official: trophies.filter((t) => t.name && t.description && t.grade).length,
    claims: trophies.reduce((n, t) => n + t.claims, 0),
    cited: steps.filter((s) => s.refs.length >= 1).length,
    multi: steps.filter((s) => s.refs.length >= 2).length,
    guidesCiting: trophies.filter((t) => t.steps.some((s) => s.refs.length)).length,
    disputes: data.disputes.length,
    atRisk: trophies.filter((t) => t.atRisk || t.missable || t.unconfirmed).length,
    pages: Object.keys(data.sources).length,
    sites: hosts.size,
    missable: trophies.filter((t) => t.missable).length,
  };
}

// Per source: how many claims cite it, in how many guides.
export function sourceStats(data) {
  return Object.fromEntries(
    Object.keys(data.sources).map((key) => {
      const cited = data.trophies.map((t) => t.steps.filter((s) => s.refs.includes(key)).length);
      return [key, { claims: cited.reduce((a, b) => a + b, 0), guides: cited.filter((n) => n > 0).length }];
    }),
  );
}

export function renderKpi(data, root) {
  const a = audit(data);
  const cells = [
    [`${a.official}/${a.trophies}`, 'official name, desc, grade'],
    [`${a.cited}/${a.claims}`, 'claims cited'],
    [`${a.guidesCiting}/${a.trophies}`, 'guides cite sources'],
    [String(a.multi), 'claims backed by 2+ sites'],
    [String(a.disputes), 'disputes, both ways'],
    [String(a.atRisk), 'at risk'],
    [`${a.pages} pages`, `${a.sites} sites read`],
    [String(a.missable), 'possibly missable'],
  ];
  root.replaceChildren(
    ...cells.map(([big, small]) => {
      const cell = h('div', 'kpi');
      cell.append(h('b', '', big), h('span', '', small));
      return cell;
    }),
  );
}
