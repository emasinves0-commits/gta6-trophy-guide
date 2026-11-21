// Entry point: loads the data, holds the state, routes the four tabs by URL hash and wires the controls.
import { renderKpi } from './audit.js';
import { renderChecklist } from './checklist.js';
import { KIND_FILTERS, disputedIds, filterCounts, filterTrophies, maskedCount } from './filters.js';
import { renderGuide, renderSourcesPanel } from './guide.js';
import { renderMissables } from './missables.js';
import { renderProgress } from './progress.js';
import { nextUp, renderNextUp, renderRoadmap } from './roadmap.js';
import { renderSources } from './sources.js';
import { downloadProgressFile, loadCounts, loadEarnedIds, loadSettings, parseProgressFile, saveCounts, saveEarnedIds, saveSettings } from './storage.js';

const data = await (await fetch('data/trophies.json')).json();
const validIds = new Set(data.trophies.map((t) => t.id));
const disputed = disputedIds(data);
const TABS = ['tracker', 'roadmap', 'missables', 'sources'];
const $ = (selector) => document.querySelector(selector);

const state = {
  earned: new Set([...loadEarnedIds()].filter((id) => validIds.has(id))),
  counts: loadCounts(),
  settings: loadSettings(),
  kind: 'all',
  grade: 'all',
  query: '',
  hideEarned: false,
  tab: 'tracker',
  openId: null,
};

function setEarned(id, isEarned) {
  if (isEarned) state.earned.add(id);
  else state.earned.delete(id);
  saveEarnedIds(state.earned);
  renderAll();
}

function setCount(id, n) {
  const max = data.trophies.find((t) => t.id === id).count;
  state.counts[id] = Math.max(0, Math.min(max, n));
  saveCounts(state.counts);
  renderAll();
}

function openTrophy(id, goTracker = false) {
  state.openId = id;
  if (goTracker) location.hash = `#tracker/${id}`;
  renderAll();
}

// "#tracker", "#roadmap/…", "#tracker/28": the first part picks the tab, a number picks the open trophy.
function readHash() {
  const [tab, id] = location.hash.slice(1).split('/');
  state.tab = TABS.includes(tab) ? tab : 'tracker';
  if (Number(id) && validIds.has(Number(id))) state.openId = Number(id);
}

function ctxNow() {
  return { earned: state.earned, settings: state.settings, counts: state.counts, disputed, openId: state.openId, onToggle: setEarned, onOpen: openTrophy, onCount: setCount };
}

function renderAll() {
  const ctx = ctxNow();
  const keep = [...document.querySelectorAll('.list, .guide, .pane')].map((n) => [n, n.scrollTop]);
  const visible = filterTrophies(data.trophies, state, ctx);
  if (state.openId === null) state.openId = nextUp(data, state.earned)[0]?.id ?? 1;
  ctx.openId = state.openId;
  const open = data.trophies.find((t) => t.id === state.openId);

  renderProgress(data.trophies, state.earned, $('#progress'));
  $('#masked-count').textContent = state.settings.hideStorySpoilers ? `· ${maskedCount(data.trophies, state.earned, state.settings)} masked` : '· off';
  for (const link of document.querySelectorAll('.tabs a')) link.setAttribute('aria-current', String(link.dataset.tab === state.tab));
  for (const tab of TABS) $(`#view-${tab}`).hidden = tab !== state.tab;

  const counts = filterCounts(data.trophies, ctx);
  document.querySelectorAll('#kinds button').forEach((b) => {
    b.setAttribute('aria-pressed', String(b.dataset.kind === state.kind));
    b.querySelector('.n').textContent = String(counts[b.dataset.kind]);
  });
  renderChecklist(visible, ctx, $('#list'));
  renderNextUp(data, ctx, $('#nextup'));
  renderGuide(data, open, ctx, $('#guide'));
  renderSourcesPanel(data, open, ctx, $('#sources-panel'));
  $('#result-count').textContent = `${visible.length} shown`;
  renderRoadmap(data, ctx, $('#view-roadmap'));
  renderMissables(data, ctx, $('#view-missables'));
  renderSources(data, $('#view-sources'));
  for (const [node, top] of keep) node.scrollTop = top;
}

function buildKindButtons() {
  const bar = $('#kinds');
  for (const [value, label] of KIND_FILTERS) {
    const button = document.createElement('button');
    button.type = 'button';
    button.dataset.kind = value;
    button.append(label, Object.assign(document.createElement('span'), { className: 'n' }));
    button.addEventListener('click', () => {
      state.kind = value;
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
  $('#export').addEventListener('click', () => downloadProgressFile(state.earned, state.counts));
  $('#import').addEventListener('change', async (e) => {
    const file = e.target.files[0];
    if (!file) return;
    try {
      const parsed = parseProgressFile(await file.text(), validIds);
      state.earned = parsed.earned;
      state.counts = parsed.counts;
      saveEarnedIds(state.earned);
      saveCounts(state.counts);
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
    state.counts = {};
    saveEarnedIds(state.earned);
    saveCounts(state.counts);
    renderAll();
  });
  addEventListener('hashchange', () => (readHash(), renderAll()));
}

buildKindButtons();
wireControls();
readHash();
renderKpi(data, $('#kpi'));
renderAll();
