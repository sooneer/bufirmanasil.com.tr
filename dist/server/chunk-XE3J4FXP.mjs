import './polyfills.server.mjs';
var e=class{static toFriendlyUrl(r){return r.toLowerCase().replace(/ç/g,"c").replace(/ğ/g,"g").replace(/ı/g,"i").replace(/ö/g,"o").replace(/ş/g,"s").replace(/ü/g,"u").replace(/[^a-z0-9]+/g,"-").replace(/^-+|-+$/g,"")}};export{e as a};
