import { defineConfig } from 'vite';

const outDir = process.env.OUT_DIR || '../public';

export default defineConfig({
  build: {
    outDir,
    emptyOutDir: false,
    sourcemap: false,
    target: 'es2017',
    cssCodeSplit: false,
    assetsDir: '',
    rollupOptions: {
      input: {
        'distributed-rl': './src/entries/distributed-rl.ts',
      },
      output: {
        format: 'iife',
        entryFileNames: `scripts/[name].js`,
        chunkFileNames: `[name].js`,
        manualChunks: undefined,
      },
      treeshake: true,
    },
  },
});


