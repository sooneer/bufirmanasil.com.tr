# bufirmanasil.com.tr

This project is an Angular application built for the bufirmanasil.com.tr website.

## Overview

This project appears to be a website built using Angular, utilizing server-side rendering (SSR). It seems focused on company related pages, potentially providing information about different companies. A key feature is extracting the company name from the URL path.

## Technologies Used

*   **Angular:** The core framework for building the application.
*   **Angular CLI:** Used for project setup, development, and build processes.
*   **TypeScript:** The primary programming language.
*   **Angular Router:** Used for navigation and URL handling.
*   **Angular SSR:** Enables server-side rendering for improved performance and SEO.
*   **Express:** Used as the server for SSR.
*   **rxjs:** For reactive programming

## Project Structure (Based on Available Files)

*   `src/app/company/`: Contains the `CompanyComponent`, responsible for displaying company-specific information.
*   `company.component.ts`: TypeScript file for the component logic.
*   `company.component.html`: HTML template for the component.
*   `package.json`: Lists project dependencies and scripts.

## Key Features (Based on Code)

*   **Dynamic Company Pages:** The `CompanyComponent` appears to dynamically load content based on the company name extracted from the URL.
* The code `this.CompanyUrl = event[1]?.path;` indicates the company URL segment is likely in the second position within the path array.
*   **Server-Side Rendering (SSR):** The `serve:ssr:bufirmanasil` script and `@angular/ssr` dependency indicate the project uses SSR for improved performance and SEO.
* **Angular v19**: The project uses Angular version 19.

## Development

### Prerequisites

*   Node.js (version 18 or higher)
*   npm (comes with Node.js)
*   Angular CLI (`npm install -g @angular/cli`)

### Setup

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd bufirmanasil.com.tr
    ```
2.  **Install dependencies:**
    ```bash
    npm install
    ```

### Development server

1.  Run `ng serve` for a dev server. Navigate to `http://localhost:4200/`. The application will automatically reload if you change any of the source files.
    ```bash
    npm start
    ```

### Build

1. Run `ng build` to build the project. The build artifacts will be stored in the `dist/` directory.

    ```bash
    npm run build
    ```

### Running SSR

1. **Build:**
   ```bash
   npm run build
