# Vite React Typescript Frontend and Python Backend

* Frontend : Vite React Typescript
 * MUI
 * React Toolkit
* Backend : Python
 * Flask

## What did I do for FE?

1. make fe directory.

```
npm create vite
```

* input project name as `fe`
* choose `react`
* choose `react-ts`

```
cd fe
npm i
```

2. remove `assets` and `public` directories and `*.css` files.
3. configure `vite.config.ts`.

edit `/vite.config.ts`.
add `PWA` plugin etc.

4. introduce `eslint`

```
npm i eslint --save-dev
npm init @eslint/config
 ...
npm install eslint-config-airbnb-typescript --save-dev
```

5. add mui


## Reference.

* Introduce Vite :  https://zenn.dev/sprout2000/articles/98145cf2a807b1
* Introduce Eslint : https://zenn.dev/longbridge/articles/ae3aa36cf17d73
* MUI : https://mui.com/

