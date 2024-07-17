import { externalDepsPlugin } from "@heraclius/external-deps-plugin"
import { resolve } from "path"
import swc from "unplugin-swc"
import { defineConfig } from "vite"
import dtsPlugin from "vite-plugin-dts"

export default defineConfig({
  plugins: [dtsPlugin({ rollupTypes: true }), swc.vite(), externalDepsPlugin()],
  build: {
    lib: {
      entry: resolve(__dirname, "src/index.ts"),
      fileName: "www",
      formats: ["es"]
    }
  }
})
