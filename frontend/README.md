# SolidJS app

Everything you need to build a Solid project, powered by [`solid-start`](https://start.solidjs.com);

## Install

```bash
pnpm install
```

## Developing

Once you've created a project and installed dependencies, start a development server:

```bash
pnpm dev
```

## Building

Solid apps are built with _adapters_, which optimise your project for deployment to different environments.

By default, `npm run build` will generate a Node app that you can run with `npm start`. To use a different adapter, add it to the `devDependencies` in `package.json` and specify in your `vite.config.js`.

```bash
pnpm build
```

Built HTML is in `.output/public`
