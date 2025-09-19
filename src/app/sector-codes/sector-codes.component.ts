import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { SeoService } from '../../_shared/services/seo.service';

interface Sector {
  code: string;
  name: string;
}

interface SectorData {
  sectors: Sector[];
}

@Component({
  selector: 'app-sector-codes',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './sector-codes.component.html',
  styleUrls: ['./sector-codes.component.scss']
})
export class SectorCodesComponent implements OnInit {
  sectors: Sector[] = [];
  filteredSectors: Sector[] = [];
  searchText: string = '';
  loading: boolean = true;
  error: string = '';
  totalSectors: number = 0;

  constructor(
    private http: HttpClient,
    private seoService: SeoService
  ) {}

  ngOnInit(): void {
    this.setSeoData();
    this.loadSectors();
  }

  private setSeoData(): void {
    this.seoService.setSektorKodlariPage();
  }

  private loadSectors(): void {
    this.loading = true;
    this.error = '';

    this.http.get<SectorData>('/data/SektorKodlari.json').subscribe({
      next: (data) => {
        this.sectors = data.sectors || [];
        this.filteredSectors = [...this.sectors];
        this.totalSectors = this.sectors.length;
        this.loading = false;
      },
      error: (err) => {
        console.error('Sektör kodları yüklenemedi:', err);
        this.error = 'Sektör kodları yüklenirken bir hata oluştu. Lütfen sayfayı yenileyin.';
        this.loading = false;
      }
    });
  }

  onSearchChange(): void {
    if (!this.searchText || this.searchText.trim() === '') {
      this.filteredSectors = [...this.sectors];
      return;
    }

    const searchLower = this.searchText.toLowerCase().trim();
    this.filteredSectors = this.sectors.filter(sector =>
      sector.code.toLowerCase().includes(searchLower) ||
      sector.name.toLowerCase().includes(searchLower)
    );
  }

  downloadJson(): void {
    try {
      const dataToDownload = {
        title: "NACE Sektör Kodları - Tüm Veriler",
        description: "Avrupa Topluluğunda Ekonomik Faaliyetlerin İstatistiki Sınıflaması - Tam Liste",
        totalCount: this.sectors.length,
        downloadDate: new Date().toISOString(),
        sectors: this.sectors
      };

      const dataStr = JSON.stringify(dataToDownload, null, 2);
      const dataBlob = new Blob([dataStr], { type: 'application/json' });

      const url = window.URL.createObjectURL(dataBlob);
      const link = document.createElement('a');
      link.href = url;
      link.download = 'nace-sektor-kodlari-tum-veriler.json';

      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
    } catch (error) {
      console.error('JSON indirme hatası:', error);
      alert('Dosya indirilirken bir hata oluştu. Lütfen tekrar deneyin.');
    }
  }
}
