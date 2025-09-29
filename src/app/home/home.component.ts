import { CommonModule } from '@angular/common';
import { Component, ViewEncapsulation, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { CompanyListItem } from '../../_shared/models/Company';
import { SeoService } from '../../_shared/services/seo.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  imports: [CommonModule, FormsModule],
  encapsulation: ViewEncapsulation.None,
})
export class HomeComponent implements OnInit {
  SearchText: string = '';
  Companies: CompanyListItem[] = [];
  filteredCompanies: CompanyListItem[] = [];

  constructor(
    private router: Router,
    private http: HttpClient,
    private seoService: SeoService
  ) {}

  ngOnInit() {
    // SEO ayarları
    this.seoService.setHomePage();

    this.http.get<CompanyListItem[]>('/data/companies.json').subscribe((data) => {
      this.Companies = data;
      this.filteredCompanies = [];
    });
  }

  onSearchTextChanged() {
    const search = this.SearchText?.toLowerCase() || '';
    this.filteredCompanies = this.Companies.filter((c) =>
      c.name.toLowerCase().includes(search)
    ).slice(0, 10); // En fazla 10 sonuç göster
  }

  selectCompany(company: CompanyListItem) {
    this.SearchText = company.name;
    this.filteredCompanies = [];
    this.Search();
  }

  Search() {
    const company = this.Companies.find(
      (c) => c.name.toLowerCase() === this.SearchText.toLowerCase()
    );
    if (company) {
      // Artık slug'ı kullanabiliyoruz
      this.router.navigate(['/company/' + company.slug]);
    } else {
      alert('Company not found!');
    }
  }
}
