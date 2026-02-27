# AmericanGarageCleaning

This repository hosts a static marketing site for American Garage Cleaning. The page content is stored in `src/index.html` and the build process minifies assets and copies them into the `dist` folder.

## Prerequisites

- Node.js 16+ (the `engines` field in package.json) is required.

## Building

Install dependencies and run the build script:

```bash
npm install
npm run build
```

The optimized output will be available in `dist/`. You can preview it locally with:

```bash
npm run start
```

or by opening `dist/index.html` in a browser.

### Quality checks

A simple HTML validator is included. Run:

```bash
npm run lint:html
```

(or `npm run check`) to verify your markup before building.

## Development notes

- Add static assets (images, favicon, etc.) under `src/` alongside `index.html`; they will be copied automatically during build.
- The form endpoint in the HTML is currently blank; replace `endpoint` in the inline script with your webhook URL.
