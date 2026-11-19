// Deciding which trophies are visible: kind filter, grade filter, search text, and the spoiler rule.
export const KIND_FILTERS = [
  ['all', 'All'],
  ['story', 'Story'],
  ['missable', 'Missable'],
  ['collectibles', 'Collectibles'],
  ['activities', 'Activities'],
];

export function isSpoilerHidden(trophy, earned, settings) {
  return settings.hideStorySpoilers && trophy.hidden === true && !earned.has(trophy.id);
}

export function matchesKind(trophy, kind) {
  if (kind === 'all') return true;
  if (kind === 'missable') return trophy.missable;
  return trophy.kind === kind;
}

export function matchesSearch(trophy, query, spoilerHidden) {
  const q = query.trim().toLowerCase();
  if (!q) return true;
  // A hidden spoiler is not searchable by name or description, so search cannot leak it.
  const text = spoilerHidden ? trophy.grade : `${trophy.name} ${trophy.description} ${trophy.grade} ${trophy.guide}`;
  return text.toLowerCase().includes(q);
}

export function filterTrophies(trophies, state) {
  return trophies.filter(
    (t) =>
      matchesKind(t, state.kind) &&
      (state.grade === 'all' || t.grade === state.grade) &&
      (!state.hideEarned || !state.earned.has(t.id)) &&
      matchesSearch(t, state.query, isSpoilerHidden(t, state.earned, state.settings)),
  );
}
