// The progress bar and the counts by grade.
const GRADES = ['platinum', 'gold', 'silver', 'bronze'];

export function countByGrade(trophies, earned) {
  const counts = Object.fromEntries(GRADES.map((g) => [g, { earned: 0, total: 0 }]));
  for (const t of trophies) {
    counts[t.grade].total += 1;
    if (earned.has(t.id)) counts[t.grade].earned += 1;
  }
  return counts;
}

export function renderProgress(trophies, earned, root) {
  const counts = countByGrade(trophies, earned);
  const percent = Math.round((earned.size / trophies.length) * 100);
  const bar = root.querySelector('.bar-fill');
  bar.style.width = `${percent}%`;
  root.querySelector('[role=progressbar]').setAttribute('aria-valuenow', String(percent));
  root.querySelector('.progress-text').textContent = `${earned.size} of ${trophies.length} earned · ${percent}%`;
  root.querySelector('.grade-counts').replaceChildren(
    ...GRADES.map((g) => {
      const chip = document.createElement('span');
      chip.className = `chip grade-${g}`;
      chip.textContent = `${g} ${counts[g].earned}/${counts[g].total}`;
      return chip;
    }),
  );
}
