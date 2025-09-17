import { RenderMode, ServerRoute } from '@angular/ssr';
import { promises as fs } from 'fs';
import { join } from 'path';
import { URLHelpers } from '../_helpers/url-helpers';

export const serverRoutes: ServerRoute[] = [
  {
    path: 'company/:name',
    renderMode: RenderMode.Prerender,
    getPrerenderParams: async () => {
      const filePath = join(process.cwd(), 'docs/browser/data/companies.json');
      try {
        const content = await fs.readFile(filePath, 'utf-8');
        const companies: string[] = JSON.parse(content);
        return companies.map(name => ({ name: URLHelpers.toFriendlyUrl(name) }));
      } catch (error) {
        console.error('Error reading companies.json for prerendering:', error);
        return [];
      }
    },
  },
  // 2. Diğer tüm statik rotalar için genel "catch-all" kuralı
  {
    path: '**',
    renderMode: RenderMode.Prerender
  }
];
