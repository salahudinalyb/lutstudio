# LUT Studio

Apply LUT filters to your photos right in the browser. Add photos, pick a filter, compare before and after, and download at full quality. Everything runs on the user's device, and photos are never uploaded anywhere.

## Features

- **3D LUT filters** from `.cube` files or **HALD CLUT** images (`.png`). Import them with the button or drop them anywhere on the page.
- **Before / after** in three modes: Split (draggable divider), Side by side, and Result. Press and hold the photo, or hold `B`, to see the original.
- **Intensity from 0 to 100%.** Click the active filter again to adjust it.
- **Batch editing.** Each photo keeps its own filter, or you can apply one filter to all of them.
- **Export** as JPG, PNG, or WebP, at quality up to 100, in original size or Instagram's 1080 px. Download all photos at once as a single ZIP.
- **Zoom and pan** with scroll, pinch, or double-tap. The canvas background can be dark, neutral gray, or white.
- **Filter management:** rename, download as `.cube`, or delete (with undo). Imported filters are saved in the user's browser (IndexedDB).
- **Keyboard shortcuts:** press `?` in the app to see them all.

Rendering uses WebGL2 with 16-bit float 3D LUTs and trilinear interpolation. Exports are always rendered at full resolution.

## Structure

```
index.html            ← the deployable app (built, single file, works offline)
src/index.src.html    ← app source
luts/*.cube           ← built-in filters (embedded at build time)
tools/build.py        ← build script (Python 3, no dependencies)
```

## Adding built-in filters

1. Put a `.cube` file (3D LUT) in `luts/`. The file name becomes the filter name, so `WarmFilm.cube` shows up as "Warm Film".
2. Run:
   ```bash
   python3 tools/build.py
   ```
3. Commit the updated `index.html`.

To change the app's UI or behavior, edit `src/index.src.html` and build again.

## Deploy

It's a static site with no server-side build step.

- **Vercel:** import this repo, set Framework Preset to **Other**, leave the build command empty, and keep the output directory at the root.
- **GitHub Pages:** go to Settings → Pages → Deploy from branch → `main` / root.
- Or just open `index.html` in a browser.

## Browser support

Requires a browser with WebGL2: Chrome, Edge, Firefox, or Safari 15+. HEIC photos can only be opened in Safari. Older Safari versions can't export WebP.

## License

MIT
