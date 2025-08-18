import { Direction, GridPosition, MazeConfig, MazeState, N, E, S, W, StartExitCell } from './types';

function clamp(value: number, min: number, max: number): number {
  return Math.max(min, Math.min(max, value));
}

function keyOf(r: number, c: number): string { return `${r},${c}`; }

export class Maze {
  private state: MazeState;

  constructor(config: MazeConfig) {
    this.state = this.generate(config);
  }

  public getState(): MazeState {
    // Expose references that are safe for read-only consumers
    return this.state;
  }

  public reset(config: MazeConfig): void {
    this.state = this.generate(config);
  }

  public setLights(on: boolean): void {
    this.state.lightsOn = on;
  }

  public move(direction: Direction): void {
    if (this.state.won) return;
    const dir = this.dirFrom(direction);
    const { player, grid, rows, cols, exit } = this.state;
    const cell = grid[player.r][player.c];
    // Wall check
    if (!(cell & dir.bit)) {
      // Special case: attempting to step outward through the exit opening
      const nr = player.r + dir.dr, nc = player.c + dir.dc;
      const goingOut = nr < 0 || nr >= rows || nc < 0 || nc >= cols;
      if (goingOut && player.r === exit.r && player.c === exit.c) {
        if (this.state.hasKey) this.win();
      }
      return;
    }
    // Move
    const nr = player.r + dir.dr, nc = player.c + dir.dc;
    if (nr < 0 || nr >= rows || nc < 0 || nc >= cols) {
      // Moving out of bounds; if exiting and hasKey then win
      if (player.r === exit.r && player.c === exit.c && this.state.hasKey) this.win();
      return;
    }
    player.r = nr; player.c = nc;
    // Pick up key
    if (!this.state.hasKey && nr === this.state.key.r && nc === this.state.key.c) {
      this.state.hasKey = true;
    }
    // Mark explored (lights off mode uses this)
    this.state.explored.add(keyOf(player.r, player.c));
    if (!this.state.lightsOn) this.revealVisibleFromPlayer();
  }

  private win(): void {
    this.state.won = true;
  }

  public resetPosition(): void {
    this.state.player = { r: this.state.start.r, c: this.state.start.c };
    this.state.hasKey = false;
    this.state.won = false;
    this.state.explored = new Set<string>([keyOf(this.state.player.r, this.state.player.c)]);
    if (!this.state.lightsOn) this.revealVisibleFromPlayer();
  }

  private dirFrom(direction: Direction): { bit: number; dr: number; dc: number } {
    if (direction === 'up') return { bit: N, dr: -1, dc: 0 };
    if (direction === 'down') return { bit: S, dr: 1, dc: 0 };
    if (direction === 'left') return { bit: W, dr: 0, dc: -1 };
    return { bit: E, dr: 0, dc: 1 };
  }

  private generate(config: MazeConfig): MazeState {
    const size = clamp(Math.round(config.size), 5, 15);
    const rows = size, cols = size;
    const openness = clamp(config.openness, 0, 1);

    const grid: number[][] = Array.from({ length: rows }, () => Array<number>(cols).fill(0));
    const visited: boolean[][] = Array.from({ length: rows }, () => Array<boolean>(cols).fill(false));

    // Randomized DFS to carve a perfect maze
    const stack: Array<[number, number]> = [];
    let sr = Math.floor(Math.random() * rows);
    let sc = Math.floor(Math.random() * cols);
    visited[sr][sc] = true; stack.push([sr, sc]);
    while (stack.length) {
      const [cr, cc] = stack[stack.length - 1];
      const neighbors: Array<{ bit: number; dr: number; dc: number; opp: number; nr: number; nc: number }>=[];
      for (const d of [ {bit:N,dr:-1,dc:0,opp:S}, {bit:E,dr:0,dc:1,opp:W}, {bit:S,dr:1,dc:0,opp:N}, {bit:W,dr:0,dc:-1,opp:E} ]) {
        const nr = cr + d.dr, nc = cc + d.dc;
        if (nr >= 0 && nr < rows && nc >= 0 && nc < cols && !visited[nr][nc]) neighbors.push({ ...d, nr, nc });
      }
      if (neighbors.length) {
        const { bit, opp, nr, nc } = neighbors[Math.floor(Math.random()*neighbors.length)];
        grid[cr][cc] |= bit;
        grid[nr][nc] |= opp;
        visited[nr][nc] = true;
        stack.push([nr, nc]);
      } else {
        stack.pop();
      }
    }

    // Add extra openings to create loops according to openness
    if (openness > 0) {
      for (let r = 0; r < rows; r++) {
        for (let c = 0; c < cols; c++) {
          if (c < cols - 1 && r > 0 && r < rows - 1) {
            if (Math.random() < openness * 0.6) {
              if (!((grid[r][c] & E) || (grid[r][c+1] & W))) { grid[r][c] |= E; grid[r][c+1] |= W; }
            }
          }
          if (r < rows - 1 && c > 0 && c < cols - 1) {
            if (Math.random() < openness * 0.6) {
              if (!((grid[r][c] & S) || (grid[r+1][c] & N))) { grid[r][c] |= S; grid[r+1][c] |= N; }
            }
          }
        }
      }
    }

    // Choose distinct start and exit on the perimeter
    const choosePerimeter = (): StartExitCell => {
      const side = Math.floor(Math.random()*4);
      if (side === 0) return { r: 0, c: Math.floor(Math.random()*cols), bit: N };
      if (side === 1) return { r: Math.floor(Math.random()*rows), c: cols-1, bit: E };
      if (side === 2) return { r: rows-1, c: Math.floor(Math.random()*cols), bit: S };
      return { r: Math.floor(Math.random()*rows), c: 0, bit: W };
    };
    let start = choosePerimeter();
    let exit = choosePerimeter();
    while (start.r === exit.r && start.c === exit.c) exit = choosePerimeter();
    // Open perimeter at start/exit
    grid[start.r][start.c] |= start.bit;
    grid[exit.r][exit.c] |= exit.bit;

    // Place key in the interior away from start/exit
    let key: GridPosition = { r: 1 + Math.floor(Math.random()*Math.max(1, rows-2)), c: 1 + Math.floor(Math.random()*Math.max(1, cols-2)) };
    while ((key.r === start.r && key.c === start.c) || (key.r === exit.r && key.c === exit.c)) {
      key = { r: 1 + Math.floor(Math.random()*Math.max(1, rows-2)), c: 1 + Math.floor(Math.random()*Math.max(1, cols-2)) };
    }

    const explored = new Set<string>([keyOf(start.r, start.c)]);

    const state: MazeState = {
      rows, cols,
      grid,
      start, exit,
      key,
      player: { r: start.r, c: start.c },
      hasKey: false,
      won: false,
      explored,
      lightsOn: !!config.lightsOn,
    };
    // Initial reveal if lights are off (so corridors become explored)
    if (!state.lightsOn) this.revealVisibleFromPlayer(state);
    return state;
  }

  private revealVisibleFromPlayer(stateArg?: MazeState): void {
    const s = stateArg ?? this.state;
    if (s.lightsOn) return;
    const add = (r:number,c:number) => s.explored.add(keyOf(r,c));
    add(s.player.r, s.player.c);
    for (const d of [ {bit:N,dr:-1,dc:0}, {bit:E,dr:0,dc:1}, {bit:S,dr:1,dc:0}, {bit:W,dr:0,dc:-1} ]) {
      let cr = s.player.r, cc = s.player.c;
      while (s.grid[cr][cc] & d.bit) {
        const nr = cr + d.dr, nc = cc + d.dc;
        if (nr < 0 || nr >= s.rows || nc < 0 || nc >= s.cols) break;
        add(nr, nc);
        cr = nr; cc = nc;
      }
    }
  }
}

