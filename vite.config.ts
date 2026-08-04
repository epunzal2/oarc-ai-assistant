import { resolve } from "node:path";

import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";

export default defineConfig({
  base: "/ui-static/",
  plugins: [react()],
  root: "src/rag/ui_app",
  publicDir: "public",
  build: {
    outDir: "../ui_static",
    emptyOutDir: true,
    sourcemap: false,
    assetsDir: ".",
    chunkSizeWarningLimit: 700,
    rollupOptions: {
      input: resolve(import.meta.dirname, "src/rag/ui_app/index.html"),
      output: {
        entryFileNames: "app.js",
        chunkFileNames: "[name].js",
        assetFileNames: (assetInfo) => {
          if (assetInfo.name?.endsWith(".css")) {
            return "styles.css";
          }
          return "[name][extname]";
        },
      },
    },
  },
  server: {
    proxy: {
      "/health": "http://127.0.0.1:8088",
      "/v1": "http://127.0.0.1:8088",
      "/ui": "http://127.0.0.1:8088",
    },
  },
});
