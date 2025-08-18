import { MazeState, N, E, S, W } from '../core/maze/types';

export interface RenderOptions {
  wallColor?: string;
  bgColor?: string;
  exploredColor?: string;
  playerColor?: string;
  exitColor?: string;
}

export class MazeRenderer {
  private ctx: CanvasRenderingContext2D;
  private canvas: HTMLCanvasElement;
  private opts: Required<RenderOptions>;

  constructor(canvas: HTMLCanvasElement, opts?: RenderOptions) {
    const ctx = canvas.getContext('2d');
    if (!ctx) throw new Error('Canvas 2D context not available');
    this.canvas = canvas;
    this.ctx = ctx;
    this.opts = {
      wallColor: opts?.wallColor ?? '#111',
      bgColor: opts?.bgColor ?? '#ffffff',
      exploredColor: opts?.exploredColor ?? '#e5e7eb',
      playerColor: opts?.playerColor ?? '#111',
      exitColor: opts?.exitColor ?? '#111',
    };
  }

  public draw(state: MazeState): void {
    const { width, height } = this.canvas;
    const rows = state.rows, cols = state.cols;
    const cellSize = Math.floor(Math.min(width, height) / Math.max(rows, cols));
    let pad = Math.floor((Math.min(width, height) - cellSize * Math.max(rows, cols)) / 2);
    const wall = 2;

    // Background
    this.ctx.clearRect(0, 0, width, height);
    this.ctx.fillStyle = this.opts.bgColor;
    this.ctx.fillRect(0, 0, width, height);

    // Helper draw walls of a single cell
    const drawCellWalls = (r: number, c: number) => {
      const x = pad + c * cellSize;
      const y = pad + r * cellSize;
      const cell = state.grid[r][c];
      this.ctx.beginPath();
      this.ctx.strokeStyle = this.opts.wallColor;
      this.ctx.lineWidth = wall;
      this.ctx.lineCap = 'square';
      this.ctx.lineJoin = 'miter';
      if (!(cell & N)) { this.ctx.moveTo(x, y); this.ctx.lineTo(x + cellSize, y); }
      if (!(cell & E)) { this.ctx.moveTo(x + cellSize, y); this.ctx.lineTo(x + cellSize, y + cellSize); }
      if (!(cell & S)) { this.ctx.moveTo(x, y + cellSize); this.ctx.lineTo(x + cellSize, y + cellSize); }
      if (!(cell & W)) { this.ctx.moveTo(x, y); this.ctx.lineTo(x, y + cellSize); }
      this.ctx.stroke();
    };

    const drawNotch = (cellPos: { r:number; c:number }, bit: number) => {
      const { r, c } = cellPos;
      const x = pad + c * cellSize;
      const y = pad + r * cellSize;
      this.ctx.beginPath();
      this.ctx.fillStyle = this.opts.wallColor;
      const m = Math.max(2, Math.floor(cellSize * 0.15));
      if (bit === N) this.ctx.fillRect(x + cellSize/2 - m, y - wall, 2*m, wall);
      if (bit === S) this.ctx.fillRect(x + cellSize/2 - m, y + cellSize, 2*m, wall);
      if (bit === W) this.ctx.fillRect(x - wall, y + cellSize/2 - m, wall, 2*m);
      if (bit === E) this.ctx.fillRect(x + cellSize, y + cellSize/2 - m, wall, 2*m);
    };

    const keyOf = (r:number, c:number) => `${r},${c}`;

    // Compute visible set if lights off
    let visible: Set<string> | null = null;
    if (!state.lightsOn) {
      visible = new Set<string>();
      const add = (r:number,c:number) => visible!.add(keyOf(r,c));
      add(state.player.r, state.player.c);
      for (const d of [ {bit:N,dr:-1,dc:0}, {bit:E,dr:0,dc:1}, {bit:S,dr:1,dc:0}, {bit:W,dr:0,dc:-1} ]) {
        let cr = state.player.r, cc = state.player.c;
        while (state.grid[cr][cc] & d.bit) {
          const nr = cr + d.dr, nc = cc + d.dc;
          if (nr < 0 || nr >= rows || nc < 0 || nc >= cols) break;
          add(nr,nc);
          cr = nr; cc = nc;
        }
      }
      // Mark explored (renderer does not mutate state; assume core already marks on move)
    }

    // Draw grid
    if (state.lightsOn) {
      for (let r = 0; r < rows; r++) for (let c = 0; c < cols; c++) drawCellWalls(r,c);
      drawNotch(state.start, state.start.bit);
      drawNotch(state.exit, state.exit.bit);
    } else {
      // Fill explored cells
      for (const k of state.explored) {
        const [rs, cs] = k.split(',');
        const r = +rs, c = +cs;
        const x = pad + c * cellSize, y = pad + r * cellSize;
        const isVis = visible?.has(k);
        this.ctx.fillStyle = isVis ? '#ffffff' : this.opts.exploredColor;
        this.ctx.fillRect(x + wall/2, y + wall/2, cellSize - wall, cellSize - wall);
      }
      // Draw walls for explored cells
      for (const k of state.explored) {
        const [rs, cs] = k.split(',');
        drawCellWalls(+rs, +cs);
      }
      // Perimeter notches only if their cell is explored
      if (state.explored.has(keyOf(state.start.r, state.start.c))) drawNotch(state.start, state.start.bit);
      if (state.explored.has(keyOf(state.exit.r, state.exit.c))) drawNotch(state.exit, state.exit.bit);
    }

    // Key (diamond)
    const drawKey = (alpha = 1) => {
      const x = pad + state.key.c * cellSize + cellSize/2;
      const y = pad + state.key.r * cellSize + cellSize/2;
      const s = Math.max(3, Math.floor(cellSize * 0.22));
      this.ctx.save();
      this.ctx.globalAlpha = alpha;
      this.ctx.translate(x,y);
      this.ctx.rotate(Math.PI/4);
      this.ctx.beginPath();
      this.ctx.rect(-s,-s,2*s,2*s);
      this.ctx.strokeStyle = this.opts.wallColor;
      this.ctx.lineWidth = Math.max(2, wall);
      this.ctx.stroke();
      this.ctx.restore();
    };

    if (!state.hasKey) {
      const keyK = keyOf(state.key.r, state.key.c);
      const explored = state.explored.has(keyK);
      if (state.lightsOn) {
        drawKey(1);
      } else if (explored) {
        const vis = visible?.has(keyK) ?? false;
        drawKey(vis ? 1 : 0.45);
      }
    }

    // Exit marker (solid square)
    const ex = pad + state.exit.c * cellSize + cellSize/2;
    const ey = pad + state.exit.r * cellSize + cellSize/2;
    const es = Math.max(3, Math.floor(cellSize * 0.18));
    const exitShouldDraw = state.lightsOn || state.explored.has(keyOf(state.exit.r, state.exit.c));
    if (exitShouldDraw) {
      this.ctx.fillStyle = this.opts.exitColor;
      this.ctx.fillRect(ex - es, ey - es, es*2, es*2);
    }

    // Player
    const px = pad + state.player.c * cellSize + cellSize/2;
    const py = pad + state.player.r * cellSize + cellSize/2;
    const pr = Math.max(4, Math.floor(cellSize * 0.22));
    this.ctx.beginPath();
    this.ctx.arc(px, py, pr, 0, Math.PI * 2);
    this.ctx.fillStyle = this.opts.playerColor;
    this.ctx.fill();
  }
}


