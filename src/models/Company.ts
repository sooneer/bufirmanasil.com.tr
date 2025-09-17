export class Company {
  name: string;
  logo: string;
  tagline: string;
  about: string;
  services: { title: string; description: string }[];
  clients: string[];
  map:string;
  address:string;
  contact: {
    email: string;
    phone: string;
    address: string;
    formEndpoint: string;
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
    this.about = data.about;
    this.services = data.services;
    this.clients = data.clients;
    this.map = data.map;
    this.address = data.address;
    this.contact = data.contact;
    this.social = data.social;
  }
}
