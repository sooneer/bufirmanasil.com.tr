
export default {
  bootstrap: () => import('./main.server.mjs').then(m => m.default),
  inlineCriticalCss: true,
  baseHref: '/',
  locale: undefined,
  routes: [
  {
    "renderMode": 2,
    "preload": [
      "chunk-TA7BGAXW.js",
      "chunk-3R5AGSWV.js"
    ],
    "route": "/"
  },
  {
    "renderMode": 2,
    "preload": [
      "chunk-TA7BGAXW.js",
      "chunk-3R5AGSWV.js"
    ],
    "route": "/home"
  },
  {
    "renderMode": 2,
    "preload": [
      "chunk-IOD74HBE.js"
    ],
    "route": "/about"
  },
  {
    "renderMode": 2,
    "preload": [
      "chunk-2QR6SZOW.js"
    ],
    "route": "/contact"
  },
  {
    "renderMode": 2,
    "preload": [
      "chunk-5HIGSBI3.js",
      "chunk-3R5AGSWV.js"
    ],
    "route": "/company-list"
  },
  {
    "renderMode": 0,
    "preload": [
      "chunk-DHUTG2NW.js"
    ],
    "route": "/company/*"
  },
  {
    "renderMode": 2,
    "redirectTo": "/",
    "route": "/**"
  }
],
  entryPointToBrowserMapping: undefined,
  assets: {
    'index.csr.html': {size: 4681, hash: '28ad301c459b10fcab9e4fc1009d52503e05fdfcc04d4f93f9cb1e94e37284f4', text: () => import('./assets-chunks/index_csr_html.mjs').then(m => m.default)},
    'index.server.html': {size: 4535, hash: '16f284c538cf5f6a77e473f7ad93f7aa09c452ed00b99805ff0c4b1da187a978', text: () => import('./assets-chunks/index_server_html.mjs').then(m => m.default)},
    'about/index.html': {size: 11798, hash: 'be3c36d7fa42d8ea4176387205a424d7903151a3a4269c56e9077e47cbb39201', text: () => import('./assets-chunks/about_index_html.mjs').then(m => m.default)},
    'company-list/index.html': {size: 9222, hash: '95659fee24e522b78022f3e02edcf350bde9b8b380c2c2c3daca5a94cf887292', text: () => import('./assets-chunks/company-list_index_html.mjs').then(m => m.default)},
    'index.html': {size: 10740, hash: 'b9f5abb20e69822b9170eea394b6551fe48e5b3f400ed04fcd2f99fa3695c745', text: () => import('./assets-chunks/index_html.mjs').then(m => m.default)},
    'home/index.html': {size: 10740, hash: 'b9f5abb20e69822b9170eea394b6551fe48e5b3f400ed04fcd2f99fa3695c745', text: () => import('./assets-chunks/home_index_html.mjs').then(m => m.default)},
    'contact/index.html': {size: 13602, hash: 'd30b281c349b612a9c3d78b4d5c3f39f95746a8e73b8ee468e0af5d9f9a80f2f', text: () => import('./assets-chunks/contact_index_html.mjs').then(m => m.default)},
    'styles-EIHVT2BJ.css': {size: 6096, hash: 'EOcKcuS8Tpg', text: () => import('./assets-chunks/styles-EIHVT2BJ_css.mjs').then(m => m.default)}
  },
};
