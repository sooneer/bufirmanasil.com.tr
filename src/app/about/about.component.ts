import { Component, OnInit } from '@angular/core';
import { SeoService } from '../services/seo.service';

@Component({
  selector: 'app-about',
  standalone: true,
  imports: [],
  templateUrl: './about.component.html',
})
export class AboutComponent implements OnInit {

  constructor(private seoService: SeoService) {}

  ngOnInit() {
    this.seoService.setAboutPage();
  }
}
