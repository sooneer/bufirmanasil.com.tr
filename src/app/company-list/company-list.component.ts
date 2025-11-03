import { Component, OnInit, ViewEncapsulation } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { CompanyListItem } from '../../_shared/models/Company';
import { SeoService } from '../../_shared/services/seo.service';

@Component({
  selector: 'app-company-list',
  standalone: true,
  imports: [CommonModule, RouterModule, FormsModule],
  templateUrl: './company-list.component.html',
  styleUrls: ['./company-list.component.css'],
  encapsulation: ViewEncapsulation.None,
})
export class CompanyListComponent implements OnInit {
  companies: CompanyListItem[] = [];
  filteredCompanies: CompanyListItem[] = [];
  searchTerm: string = '';

  constructor(
    private http: HttpClient,
    private seoService: SeoService
  ) { }

  ngOnInit() {
    // SEO ayarları
    this.seoService.setCompanyListPage();

    this.http.get<CompanyListItem[]>('/data/companies.json').subscribe((data) => {
      this.companies = data;
      this.filteredCompanies = data;
    });
  }

  filterCompanies() {
    const term = this.searchTerm.toLowerCase().trim();

    if (!term) {
      this.filteredCompanies = this.companies;
      return;
    }

    this.filteredCompanies = this.companies.filter(company =>
      company.name.toLowerCase().includes(term) ||
      company.web?.toLowerCase().includes(term) ||
      company.slug.toLowerCase().includes(term)
    );
  }

  clearSearch() {
    this.searchTerm = '';
    this.filterCompanies();
  }
}
