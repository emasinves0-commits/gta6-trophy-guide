// Saving and loading progress, count trackers and settings in localStorage, plus export/import of progress files.
const PROGRESS_KEY = 'gta6-trophy-guide:earned';
const SETTINGS_KEY = 'gta6-trophy-guide:settings';
const COUNTS_KEY = 'gta6-trophy-guide:counts';

export function loadEarnedIds() {
  try {
    const ids = JSON.parse(localStorage.getItem(PROGRESS_KEY) ?? '[]');
    return new Set(Array.isArray(ids) ? ids.filter(Number.isInteger) : []);
  } catch {
    return new Set();
  }
}

export function saveEarnedIds(earned) {
  localStorage.setItem(PROGRESS_KEY, JSON.stringify([...earned].sort((a, b) => a - b)));
}

// Count trackers: { trophyId: number } for the "YOUR COUNT" widgets.
export function loadCounts() {
  try {
    const raw = JSON.parse(localStorage.getItem(COUNTS_KEY) ?? '{}');
    return cleanCounts(raw);
  } catch {
    return {};
  }
}

export function saveCounts(counts) {
  localStorage.setItem(COUNTS_KEY, JSON.stringify(counts));
}

function cleanCounts(raw, validIds) {
  const out = {};
  for (const [id, n] of Object.entries(raw && typeof raw === 'object' ? raw : {})) {
    if (Number.isInteger(n) && n >= 0 && (!validIds || validIds.has(Number(id)))) out[id] = n;
  }
  return out;
}

export function loadSettings() {
  const defaults = { hideStorySpoilers: true };
  try {
    return { ...defaults, ...JSON.parse(localStorage.getItem(SETTINGS_KEY) ?? '{}') };
  } catch {
    return defaults;
  }
}

export function saveSettings(settings) {
  localStorage.setItem(SETTINGS_KEY, JSON.stringify(settings));
}

export function downloadProgressFile(earned, counts) {
  const body = JSON.stringify({ game: 'Grand Theft Auto VI', earned: [...earned].sort((a, b) => a - b), counts }, null, 2);
  const link = document.createElement('a');
  link.href = URL.createObjectURL(new Blob([body], { type: 'application/json' }));
  link.download = 'gta6-trophy-progress.json';
  link.click();
  URL.revokeObjectURL(link.href);
}

// Returns { earned: Set, counts: object }. Older files (a bare list, or no counts) still import.
export function parseProgressFile(text, validIds) {
  const data = JSON.parse(text);
  const list = Array.isArray(data) ? data : data.earned;
  if (!Array.isArray(list)) throw new Error('No "earned" list in this file.');
  return { earned: new Set(list.filter((id) => validIds.has(id))), counts: cleanCounts(data.counts, validIds) };
}
