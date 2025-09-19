import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SeoService } from '../../_shared/services/seo.service';

@Component({
  selector: 'app-privacy',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './privacy.component.html',
  styleUrls: ['./privacy.component.scss']
})
export class PrivacyComponent implements OnInit {

  constructor(private seoService: SeoService) {}

  ngOnInit(): void {
    this.setSeoData();
  }

  private setSeoData(): void {
    this.seoService.updateMetaTags({
      title: 'Gizlilik Politikası - Bu Firma Nasıl?',
      description: 'Bu Firma Nasıl platformunun gizlilik politikası, kişisel veri işleme, KVKK ve GDPR uyumluluk bilgileri.',
      keywords: 'gizlilik politikası, KVKK, GDPR, kişisel veri, veri işleme, privacy policy',
      url: 'https://bufirmanasil.com.tr/privacy'
    });
  }
}