import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SeoService } from '../services/seo.service';

@Component({
  selector: 'app-terms',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './terms.component.html',
  styleUrls: ['./terms.component.scss']
})
export class TermsComponent implements OnInit {

  constructor(private seoService: SeoService) {}

  ngOnInit(): void {
    this.setSeoData();
  }

  private setSeoData(): void {
    this.seoService.updateMetaTags({
      title: 'Kullanım Şartları - Bu Firma Nasıl?',
      description: 'Bu Firma Nasıl platformunun kullanım şartları, kullanıcı sorumlulukları ve hizmet kuralları.',
      keywords: 'kullanım şartları, terms of service, kullanıcı sözleşmesi, hizmet şartları',
      url: 'https://bufirmanasil.com.tr/terms'
    });
  }
}