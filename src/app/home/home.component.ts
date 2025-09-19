import { CommonModule } from '@angular/common';
import { Component, ViewEncapsulation, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { URLHelpers } from '../../_helpers/url-helpers';
import { SeoService } from '../../_shared/services/seo.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  imports: [CommonModule, FormsModule],
  encapsulation: ViewEncapsulation.None,
})
export class HomeComponent implements OnInit {
  SearchText: string = '';
  Companies: string[] = ['VBT Yazılım'];


  filteredCompanies: string[] = [];

  constructor(
    private router: Router,
    private http: HttpClient,
    private seoService: SeoService
  ) {
    this.filteredCompanies = this.Companies;
  }

  ngOnInit() {
    // SEO ayarları
    this.seoService.setHomePage();

    this.filteredCompanies = this.Companies;
    this.http.get<string[]>('/data/companies.json').subscribe((data) => {
      console.log(data);
      this.Companies = data;
    });
  }

  onSearchTextChanged() {
    const search = this.SearchText?.toLowerCase() || '';
    this.filteredCompanies = this.Companies.filter((c) =>
      c.toLowerCase().includes(search)
    );
  }

  selectCompany(company: string) {
    this.SearchText = company;
    this.filteredCompanies = [];
    this.Search();
  }

  Search() {
    //console.log(this.SearchText);
    const company = this.Companies.find(
      (c) => c.toLowerCase() === this.SearchText.toLowerCase()
    );
    if (company) {
      const url = URLHelpers.toFriendlyUrl(company);
      this.router.navigate(['/company/' + url]);
    } else {
      alert('Company not found!');
    }
  }
}
