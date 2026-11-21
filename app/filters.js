// Which trophies are visible: the filter list (with live counts), grade, search text, hide-earned and the spoiler shield.
export const KIND_FILTERS = [
  ['all', 'All', () => true],
  ['story', 'Story', (t) => t.kind === 'story'],
  ['missable', 'Missable', (t) => t.missable],
  ['collectibles', 'Collectibles', (t) => t.kind === 'collectibles'],
  ['activities', 'Activities', (t) => t.kind === 'activities'],
  ['disputed', 'Disputed', (t, ctx) => ctx.disputed.has(t.id)],
  ['atrisk', 'At risk', (t) => Boolean(t.atRisk || t.missable || t.unconfirmed)],
  ['psnhidden', 'PSN-hidden', (t) => t.hidden],
  ['unconfirmed', 'Unconfirmed', (t) => t.unconfirmed],
  ['notearned', 'Not earned', (t, ctx) => !ctx.earned.has(t.id)],
];

export function disputedIds(data) {
  return new Set(data.disputes.flatMap((d) => d.trophies));
}

export function filterCounts(trophies, ctx) {
  return Object.fromEntries(KIND_FILTERS.map(([key, , test]) => [key, trophies.filter((t) => test(t, ctx)).length]));
}

export function isSpoilerHidden(trophy, earned, settings) {
  return settings.hideStorySpoilers && trophy.hidden === true && !earned.has(trophy.id);
}

export function maskedCount(trophies, earned, settings) {
  return trophies.filter((t) => isSpoilerHidden(t, earned, settings)).length;
}

export function matchesSearch(trophy, query, spoilerHidden) {
  const q = query.trim().toLowerCase();
  if (!q) return true;
  // A masked trophy is not searchable by name, description or steps, so search cannot leak it.
  const text = spoilerHidden ? trophy.grade : `${trophy.name} ${trophy.description} ${trophy.grade} ${trophy.steps.map((s) => s.text).join(' ')}`;
  return text.toLowerCase().includes(q);
}

export function filterTrophies(trophies, state, ctx) {
  const test = KIND_FILTERS.find(([key]) => key === state.kind)[2];
  return trophies.filter(
    (t) =>
      test(t, ctx) &&
      (state.grade === 'all' || t.grade === state.grade) &&
      (!state.hideEarned || !state.earned.has(t.id)) &&
      matchesSearch(t, state.query, isSpoilerHidden(t, state.earned, state.settings)),
  );
}
