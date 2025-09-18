import { Component, OnInit } from '@angular/core';
import { FormsModule, NgForm } from '@angular/forms';
import { SeoService } from '../services/seo.service';

@Component({
  selector: 'app-contact',
  standalone: true,
  imports: [FormsModule],
  templateUrl: './contact.component.html',
})
export class ContactComponent implements OnInit {
  emailUser = 'ben';
  emailDomain = 'soneracar.net';
  emailAddress = '';
  mailtoLink = '';

  formData = {
    name: '',
    email: '',
    subject: '',
    message: ''
  };

  constructor(private seoService: SeoService) {}

  ngOnInit() {
    // SEO ayarları
    this.seoService.setContactPage();

    this.emailAddress = `${this.emailUser}@${this.emailDomain}`;
    this.mailtoLink = `mailto:${this.emailAddress}`;
  }

  onSubmit(form: NgForm) {
    if (form.valid) {
      // E-posta içeriğini hazırla
      const subject = encodeURIComponent(this.formData.subject || 'İletişim Formu');
      const body = encodeURIComponent(
        `Ad Soyad: ${this.formData.name}\n` +
        `E-posta: ${this.formData.email}\n` +
        `Konu: ${this.formData.subject}\n\n` +
        `Mesaj:\n${this.formData.message}`
      );

      // Mailto bağlantısını oluştur ve aç
      const mailtoUrl = `mailto:${this.emailAddress}?subject=${subject}&body=${body}`;
      window.location.href = mailtoUrl;

      // Form verilerini temizle
      this.formData = {
        name: '',
        email: '',
        subject: '',
        message: ''
      };
      form.resetForm();
    }
  }
}
