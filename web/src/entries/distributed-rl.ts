// Distributed RL explainer bootstrap
// - Wires UI placeholders to a Maze engine and renderer
// - Spawns a worker (inlined blob) and displays heartbeat

import { Maze } from '../core/maze/maze';
import { MazeRenderer } from '../ui/maze_renderer';

function getEl<T extends HTMLElement>(id: string): T | null {
  return document.getElementById(id) as T | null;
}

function initMaze(): void {
  const canvas = getEl<HTMLCanvasElement>('maze-canvas');
  const lightsCheckbox = getEl<HTMLInputElement>('maze-lights');
  const lightsLabel = getEl<HTMLSpanElement>('maze-lights-label');
  const toast = getEl<HTMLDivElement>('maze-toast');
  const newBtn = getEl<HTMLButtonElement>('new');
  const resetBtn = getEl<HTMLButtonElement>('reset');

  if (!canvas || !lightsCheckbox) return;

  const DEFAULT_SIZE = 10;
  const DEFAULT_OPENNESS = 0.0; // classic: very dense walls, few/no loops
  const getConfig = () => ({
    size: DEFAULT_SIZE,
    openness: DEFAULT_OPENNESS,
    lightsOn: !!lightsCheckbox.checked,
  });

  const maze = new Maze(getConfig());
  const renderer = new MazeRenderer(canvas);

  function resizeCanvas() {
    if (!canvas) return;
    const wrap = canvas.parentElement as HTMLElement;
    if (!wrap) return;
    const target = Math.min(wrap.clientWidth, 480);
    // Set logical canvas dimensions (no DPR scaling to keep renderer simple)
    canvas.width = target;
    canvas.height = target;
  }

  function redraw() {
    resizeCanvas();
    renderer.draw(maze.getState());
  }

  function updateLabels() {
    if (!lightsCheckbox) return;
    if (lightsLabel) lightsLabel.textContent = lightsCheckbox.checked ? 'On' : 'Off';
  }

  updateLabels();
  redraw();

  window.addEventListener('resize', () => redraw());

  lightsCheckbox.addEventListener('change', () => {
    maze.setLights(getConfig().lightsOn);
    updateLabels();
    redraw();
  });

  if (newBtn) newBtn.addEventListener('click', () => { maze.reset(getConfig()); redraw(); });
  if (resetBtn) resetBtn.addEventListener('click', () => { maze.resetPosition(); redraw(); });

  // Keyboard controls
  window.addEventListener('keydown', (e) => {
    const k = e.key;
    if (['ArrowUp','ArrowDown','ArrowLeft','ArrowRight','w','a','s','d','W','A','S','D'].includes(k)) {
      e.preventDefault();
    }
    if (k === 'l' || k === 'L' || (k === ' ')) {
      if (k === ' ') e.preventDefault();
      lightsCheckbox.checked = !lightsCheckbox.checked;
      maze.setLights(lightsCheckbox.checked);
      updateLabels();
      redraw();
      return;
    }
    if (k === 'ArrowUp' || k === 'w' || k === 'W') maze.move('up');
    if (k === 'ArrowDown' || k === 's' || k === 'S') maze.move('down');
    if (k === 'ArrowLeft' || k === 'a' || k === 'A') maze.move('left');
    if (k === 'ArrowRight' || k === 'd' || k === 'D') maze.move('right');
    redraw();
  });
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => {
    initMaze();
  });
} else {
  initMaze();
}


