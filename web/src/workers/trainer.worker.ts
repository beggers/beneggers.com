// Minimal trainer worker to prove wiring. Replaces with real RL loop later.
declare const self: DedicatedWorkerGlobalScope;

let counter = 0;
let interval: number | undefined;

self.onmessage = (ev: MessageEvent) => {
  const { type } = ev.data || {};
  if (type === 'init') {
    if (interval !== undefined) return;
    interval = (self.setInterval(() => {
      counter += 1;
      self.postMessage(`heartbeat ${counter}`);
    }, 1000) as unknown) as number;
  }
};
