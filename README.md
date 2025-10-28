````markdown
# ISO/IEC 42001 Gap Assessment Tool

This is a web application prototype, built with Python and Flask, to conduct a gap assessment for organizational readiness for the ISO/IEC 42001 AI Management Systems (AIMS) standard.

This prototype was built as a proactive demonstration for the graduation internship project at Bureau Veritas Cybersecurity.

## Features

* **Interactive Questionnaire:** A multi-page assessment that walks the user through key clauses of the ISO 42001 standard.
* **Dynamic Scoring:** A simple, three-tiered response system (`Not Implemented`, `Partially Implemented`, `Fully Implemented`) for each question.
* **Session Management:** User's answers are saved in a server-side session as they navigate between pages.
* **Automated Report Generation:** A final report page that calculates an overall compliance score (in percentage) and provides a detailed gap analysis.
* **Gap Analysis:** The report lists all non-compliant items ("gaps") and provides mock recommendations for remediation.
* **Printable Report:** A clean, print-friendly version of the report is available.

## Tech Stack

* **Backend:** Python 3
* **Framework:** Flask
* **Frontend:** HTML / Jinja2 Templating
* **Styling:** Tailwind CSS (loaded via CDN)
* **Session:** Server-side sessions (Flask default)

## How to Run Locally

1.  Clone this repository (or download the files).
2.  Ensure you have Python 3 installed.
3.  From your project's root folder, create and activate a virtual environment:
    ```bash
    # Create the venv
    python -m venv venv
    
    # Activate the venv
    # On Windows (CMD): venv\Scripts\activate
    # On Windows (PowerShell): Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process; venv\Scripts\activate
    # On Mac/Linux: source venv/bin/activate
    ```
4.  Install the required dependencies:
    ```bash
    pip install Flask
    ```
5.  Run the application:
    ```bash
    python app.py
    ```
6.  Open your browser and navigate to `http://127.0.0.1:5000`.

## Future Plans

This prototype serves as a foundation. Given the opportunity, future development would include:

* **Database Integration:** Replacing the hard-coded mock data with a proper database (e.g., PostgreSQL or SQLite) to store questions, recommendations, and user results.
* **User Authentication:** Adding user accounts so multiple users or organizations can securely save and manage their assessments.
* **Expanded Content:** Ingesting the full set of ISO 42001 controls (including Annex A) to create a comprehensive assessment.
* **Visual Dashboard:** Using a library like Chart.js to provide a more visual dashboard of compliance scores by clause.
