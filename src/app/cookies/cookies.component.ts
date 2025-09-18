import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { SeoService } from '../services/seo.service';

@Component({
  selector: 'app-cookies',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './cookies.component.html',
  styleUrls: ['./cookies.component.scss']
})
export class CookiesComponent implements OnInit {

  constructor(private seoService: SeoService) {}

  ngOnInit(): void {
    this.setSeoData();
  }

  private setSeoData(): void {
    this.seoService.updateMetaTags({
      title: 'Çerez Politikası - Bu Firma Nasıl?',
      description: 'Bu Firma Nasıl platformunun çerez kullanım politikası, çerez türleri ve yönetim seçenekleri.',
      keywords: 'çerez politikası, cookie policy, çerez yönetimi, web çerezleri',
      url: 'https://bufirmanasil.com.tr/cookies'
    });
  }
}