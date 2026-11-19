// Saving and loading progress and settings in localStorage, plus export/import of progress files.
const PROGRESS_KEY = 'gta6-trophy-guide:earned';
const SETTINGS_KEY = 'gta6-trophy-guide:settings';

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

export function downloadProgressFile(earned) {
  const body = JSON.stringify({ game: 'Grand Theft Auto VI', earned: [...earned].sort((a, b) => a - b) }, null, 2);
  const link = document.createElement('a');
  link.href = URL.createObjectURL(new Blob([body], { type: 'application/json' }));
  link.download = 'gta6-trophy-progress.json';
  link.click();
  URL.revokeObjectURL(link.href);
}

export function parseProgressFile(text, validIds) {
  const data = JSON.parse(text);
  const list = Array.isArray(data) ? data : data.earned;
  if (!Array.isArray(list)) throw new Error('No "earned" list in this file.');
  return new Set(list.filter((id) => validIds.has(id)));
}
