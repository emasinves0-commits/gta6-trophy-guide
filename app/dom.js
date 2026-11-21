// Tiny DOM helpers shared by every view: element builder and source-chip builder.
export function h(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined) node.textContent = text;
  return node;
}

// Honest label for each dispute: a real source disagreement, or one of the weaker kinds of open point.
export const KIND_LABELS = { disagree: 'SOURCES DISAGREE', targets: 'TWO TARGETS, NOT A CONFLICT', wording: 'WORDING ONLY', unconfirmed: 'UNCONFIRMED TRIGGER', uncertain: 'UNCERTAIN' };
export function kindTag(d) { return h('span', `kind kind-${d.kind}`, KIND_LABELS[d.kind] ?? 'OPEN POINT'); }

// A numbered source chip: the number is the source's place in the sources index (the Sources tab lists the same numbers).
export function chips(refs, data) {
  const keys = Object.keys(data.sources);
  const wrap = h('span', 'chips');
  for (const key of refs) {
    const chip = h('span', 'chip-src', String(keys.indexOf(key) + 1));
    chip.title = data.sources[key].name;
    wrap.append(chip);
  }
  return wrap;
}
