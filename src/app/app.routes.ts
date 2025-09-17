import { Routes } from '@angular/router';

export const routes: Routes = [
  {
    path: '',
    loadComponent: () => import('./home/home.component').then((m) => m.HomeComponent),
  },
  {
    path: 'home',
    loadComponent: () => import('./home/home.component').then((m) => m.HomeComponent),
  },
  {
    path: 'about',
    loadComponent: () => import('./about/about.component').then((m) => m.AboutComponent),
  },
  {
    path: 'contact',
    loadComponent: () => import('./contact/contact.component').then((m) => m.ContactComponent),
  },
  {
    path: 'company-list',
    loadComponent: () => import('./company-list/company-list.component').then((m) => m.CompanyListComponent),
  },
  {
    path: 'company/:name',
    loadComponent: () => import('./company/company.component').then((m) => m.CompanyComponent),
  },
  {
    path: '**',
    redirectTo: '',
  },
];
