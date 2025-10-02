// companies.json için lightweight liste modeli
export interface CompanyListItem {
  slug: string;        // Dosya adı (ado-bilisim)
  name: string;        // Şirket adı (Ado Bilişim)
  web: string;         // Web sitesi
  logo: string;        // Logo path
}

export class Company {
  name: string;
  logo: string;
  web?: string;
  description?: string;
  tagline?: string;
  foundationYear?: number;
  founded?: string;
  about?: string;
  employees?: string;
  headquarters?: string;
  companySize?: string;
  BIST?: {
    code: string;
    KAP: string;
  };
  sector?: string[];
  tags?: string[];
  clients?: string[];
  careers?: string;
  internship?: string;
  remote?: string;
  contact?: {
    web?: string;
    email?: string;
    phone?: string;
    phone2?: string;
    address?: string;
    googleMaps?: string;
    googleMapsIframe?: string;
    formEndpoint?: string;
  };
  tax?: {
    taxOffice: string;
    taxNumber: string;
  };
  social?: {
    linkedin?: string;
    x?: string;
    twitter?: string;
    instagram?: string;
    facebook?: string;
    youtube?: string;
    github?: string;
  };

  constructor(data: any) {
    this.name = data.name;
    this.logo = data.logo;
    this.web = data.web;
    this.description = data.description;
    this.tagline = data.tagline;
    this.foundationYear = data.foundationYear;
    this.founded = data.founded;
    this.about = data.about;
    this.employees = data.employees;
    this.headquarters = data.headquarters;
    this.companySize = data.companySize;
    this.BIST = data.BIST;
    this.sector = data.sector;
    this.tags = data.tags;
    this.clients = data.clients;
    this.careers = data.careers;
    this.internship = data.internship;
    this.remote = data.remote;
    this.contact = data.contact;
    this.tax = data.tax;
    this.social = data.social;
  }
}
