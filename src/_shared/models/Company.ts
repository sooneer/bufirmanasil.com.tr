export class Company {
  name: string;
  logo: string;
  tagline: string;
  foundationYear?: number;
  about: string;
  BIST?: {
    code: string;
    KAP: string;
  };
  sector?: string[];
  services: { title: string; description: string }[];
  clients: string[];
  map: string;
  address: string;
  contact: {
    web?: string;
    email: string;
    phone: string;
    phone2?: string;
    address: string;
    googleMaps?: string;
    googleMapsIframe?: string;
    formEndpoint?: string;
  };
  tax?: {
    taxOffice: string;
    taxNumber: string;
  };
  social: {
    linkedin: string;
    x: string;
    instagram: string;
    facebook: string;
    youtube: string;
    github: string;
  };

  constructor(data: any) {
    this.name = data.name;
    this.logo = data.logo;
    this.tagline = data.tagline;
    this.foundationYear = data.foundationYear;
    this.about = data.about;
    this.BIST = data.BIST;
    this.sector = data.sector;
    this.services = data.services;
    this.clients = data.clients;
    this.map = data.map;
    this.address = data.address;
    this.contact = data.contact;
    this.tax = data.tax;
    this.social = data.social;
  }
}
