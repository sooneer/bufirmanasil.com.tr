import { Component, OnInit, Inject, PLATFORM_ID } from '@angular/core';
import { isPlatformBrowser, CommonModule } from '@angular/common';

@Component({
  selector: 'app-giscus',
  standalone: true,
  imports: [CommonModule],
  template: `<div id="giscus_container"></div>`
})
export class GiscusComponent implements OnInit {
  constructor(@Inject(PLATFORM_ID) private pid: Object) {}
  ngOnInit() {
    if (!isPlatformBrowser(this.pid)) return;
    const s = document.createElement('script');
    s.src = 'https://giscus.app/client.js';

    s.setAttribute('data-repo', 'sooneer/bufirmanasil.com.tr');
    s.setAttribute('data-repo-id', 'R_kgDOM5y9Zg');
    s.setAttribute('data-category', 'General');
    s.setAttribute('data-category-id', 'DIC_kwDOM5y9Zs4CjcAh');
    s.setAttribute('data-mapping', 'pathname');
    s.setAttribute('data-strict', '0');
    s.setAttribute('data-reactions-enabled', '1');
    s.setAttribute('data-emit-metadata', '0');
    s.setAttribute('data-input-position', 'top');
    s.setAttribute('data-theme', 'light');
    s.setAttribute('data-lang', 'tr');
    s.setAttribute('crossorigin', 'anonymous');
    s.async = true;
    s.crossOrigin = 'anonymous';
    
    document.getElementById('giscus_container')?.appendChild(s);
  }
}