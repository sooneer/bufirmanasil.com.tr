import { Component, OnInit } from '@angular/core';

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

  ngOnInit() {
    this.emailAddress = `${this.emailUser}@${this.emailDomain}`;
    this.mailtoLink = `mailto:${this.emailAddress}`;
  }
}
