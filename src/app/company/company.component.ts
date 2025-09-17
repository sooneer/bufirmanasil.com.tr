import { HttpClient } from '@angular/common/http';
import { Component, Inject, OnInit, ViewEncapsulation, Renderer2, ElementRef, AfterViewInit } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { Company } from '../../models/Company';
import { CommonModule } from '@angular/common';
import { DomSanitizer } from '@angular/platform-browser';
import { trigger, state, style, transition, animate } from '@angular/animations';
import { GiscusComponent } from '../../_shared/giscus.component';

@Component({
  selector: 'app-company',
  standalone: true,
  imports: [CommonModule, GiscusComponent],
  templateUrl: './company.component.html',
  styleUrl: './company.component.scss',
  animations: [
    trigger('fadeInOut', [
      state('void', style({ opacity: 0, transform: 'translateY(20px)' })),
      transition('void <=> *', animate('1000ms ease-in-out')),
    ]),
  ],
  encapsulation: ViewEncapsulation.None,
})
export class CompanyComponent implements OnInit {
  CompanyUrl?: string;
  Company: Company | null = null;

  constructor(
    private router: Router,
    private route: ActivatedRoute,
    private http: HttpClient
  ) {}

  ngOnInit() {
    this.route.url.subscribe((event) => {
      //console.log(event); // It's an array remember [0]
      this.CompanyUrl = event[1]?.path;
      this.LoadCompany();
    });
  }

  LoadCompany() {
    if (this.CompanyUrl && this.CompanyUrl !== 'company') {
      this.http
        .get<Company>('/data/company/' + this.CompanyUrl + '.json')
        .subscribe((data) => {
          this.Company = data;
        });
    }
  }
}
