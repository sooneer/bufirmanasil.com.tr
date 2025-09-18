import { Component, OnInit } from '@angular/core';
import { SeoService } from '../services/seo.service';

@Component({
  selector: 'app-contact',
  standalone: true,
  imports: [],
  templateUrl: './contact.component.html',
})
export class ContactComponent implements OnInit {
  emailUser = 'ben';
  emailDomain = 'soneracar.net';
  emailAddress = '';
  mailtoLink = '';

  constructor(private seoService: SeoService) {}

  ngOnInit() {
    // SEO ayarları
    this.seoService.setContactPage();

    this.emailAddress = `${this.emailUser}@${this.emailDomain}`;
    this.mailtoLink = `mailto:${this.emailAddress}`;
  }
}
