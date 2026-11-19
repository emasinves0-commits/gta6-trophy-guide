// Entry point: loads the data, holds the state, and wires the controls to the renderers.
import { renderChecklist } from './checklist.js';
import { KIND_FILTERS, filterTrophies } from './filters.js';
import { renderProgress } from './progress.js';
import { renderRoadmap } from './roadmap.js';
import { downloadProgressFile, loadEarnedIds, loadSettings, parseProgressFile, saveEarnedIds, saveSettings } from './storage.js';

const data = await (await fetch('data/trophies.json')).json();
const validIds = new Set(data.trophies.map((t) => t.id));
const $ = (selector) => document.querySelector(selector);

const state = {
  earned: new Set([...loadEarnedIds()].filter((id) => validIds.has(id))),
  settings: loadSettings(),
  kind: 'all',
  grade: 'all',
  query: '',
  hideEarned: false,
};

function setEarned(id, isEarned) {
  if (isEarned) state.earned.add(id);
  else state.earned.delete(id);
  saveEarnedIds(state.earned);
  renderAll();
}

function renderAll() {
  const visible = filterTrophies(data.trophies, state);
  renderProgress(data.trophies, state.earned, $('#progress'));
  renderChecklist(visible, { earned: state.earned, settings: state.settings, sourceIndex: data.sources, onToggle: setEarned }, $('#list'));
  renderRoadmap(data, state.earned, state.settings, $('#roadmap-body'), setEarned);
  $('#roadmap-notes').replaceChildren(...data.roadmapNotes.map((n) => Object.assign(document.createElement('li'), { textContent: n })));
  $('#missable-note').textContent = data.missableNote;
  $('#result-count').textContent = `${visible.length} shown`;
  const missing = data.trophies.filter((t) => t.missable && !state.earned.has(t.id)).length;
  $('#missable-count').textContent = missing ? `${missing} possibly missable trophy still open: Positive Mental Attitude (Chapter 1 meditation)` : 'No missable trophies left open';
}

function buildKindButtons() {
  const bar = $('#kinds');
  for (const [value, label] of KIND_FILTERS) {
    const button = document.createElement('button');
    button.type = 'button';
    button.textContent = label;
    button.dataset.kind = value;
    button.setAttribute('aria-pressed', String(value === state.kind));
    button.addEventListener('click', () => {
      state.kind = value;
      bar.querySelectorAll('button').forEach((b) => b.setAttribute('aria-pressed', String(b.dataset.kind === value)));
      renderAll();
    });
    bar.append(button);
  }
}

function wireControls() {
  $('#search').addEventListener('input', (e) => ((state.query = e.target.value), renderAll()));
  $('#grade').addEventListener('change', (e) => ((state.grade = e.target.value), renderAll()));
  $('#hide-earned').addEventListener('change', (e) => ((state.hideEarned = e.target.checked), renderAll()));
  $('#spoilers').checked = state.settings.hideStorySpoilers;
  $('#spoilers').addEventListener('change', (e) => {
    state.settings.hideStorySpoilers = e.target.checked;
    saveSettings(state.settings);
    renderAll();
  });
  $('#export').addEventListener('click', () => downloadProgressFile(state.earned));
  $('#import').addEventListener('change', async (e) => {
    const file = e.target.files[0];
    if (!file) return;
    try {
      state.earned = parseProgressFile(await file.text(), validIds);
      saveEarnedIds(state.earned);
      $('#message').textContent = `Imported ${state.earned.size} earned trophies.`;
      renderAll();
    } catch (error) {
      $('#message').textContent = `Import failed: ${error.message}`;
    }
    e.target.value = '';
  });
  $('#reset').addEventListener('click', () => {
    if (!confirm('Clear all progress on this device?')) return;
    state.earned = new Set();
    saveEarnedIds(state.earned);
    renderAll();
  });
}

buildKindButtons();
wireControls();
renderAll();
