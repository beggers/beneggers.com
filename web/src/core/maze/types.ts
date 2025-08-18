// Bitmask cell openings (N/E/S/W)
export const N = 1;
export const E = 2;
export const S = 4;
export const W = 8;

export interface GridPosition {
  r: number;
  c: number;
}

export interface StartExitCell extends GridPosition {
  bit: number; // opening direction on perimeter
}

export interface MazeConfig {
  size: number;      // rows = cols
  openness: number;  // 0..1 (0 classic; higher = more loops)
  lightsOn: boolean;
}

export interface MazeState {
  rows: number;
  cols: number;
  grid: number[][];         // bitmask of openings per cell
  start: StartExitCell;
  exit: StartExitCell;
  key: GridPosition;
  player: GridPosition;
  hasKey: boolean;
  won: boolean;
  explored: Set<string>;    // "r,c"
  lightsOn: boolean;
}

export type Direction = 'up' | 'down' | 'left' | 'right';
