import os
from flask import Flask, render_template_string, request, redirect, url_for, session

# Initialize the Flask application
app = Flask(__name__)
# A secret key is required for sessions (to store answers between pages)
# In a real app, set this as an environment variable
app.secret_key = os.urandom(24)

# --- MOCK DATA ---
# This is a simplified, mock representation of ISO/IEC 42001 requirements
# In a real project, this would be loaded from a database.
ISO_42001_SECTIONS = [
    {
        "title": "Section 1: Context & Leadership (Clauses 4 & 5)",
        "description": "Understanding the organization's context and the role of top management in the AI Management System (AIMS).",
        "questions": [
            {
                "id": "C4_1",
                "text": "Has the organization determined external and internal issues relevant to its purpose and that affect its ability to achieve the intended outcomes of its AIMS?",
                "recommendation": "Conduct a formal 'Context of the Organization' analysis (e.g., PESTLE, SWOT) specifically for your AI systems. Identify all internal/external stakeholders (regulators, customers, data subjects) and their expectations."
            },
            {
                "id": "C5_1",
                "text": "Does top management demonstrate leadership and commitment with respect to the AIMS (e.g., establishing an AI policy, ensuring integration of AIMS into business processes)?",
                "recommendation": "Develop and formally approve a high-level AI Policy. Assign clear roles and responsibilities for AI governance, and ensure leadership regularly reviews the AIMS performance."
            },
            {
                "id": "C5_2",
                "text": "Has an AI policy been established, documented, and communicated within the organization and to relevant stakeholders?",
                "recommendation": "Ensure the AI policy is easily accessible (e.g., on the intranet) and that all relevant personnel (developers, procurement, legal) have received training on it."
            }
        ]
    },
    {
        "title": "Section 2: Planning & Risk Management (Clause 6)",
        "description": "Addressing actions to manage risks and opportunities related to the AIMS.",
        "questions": [
            {
                "id": "C6_1",
                "text": "Has the organization established a formal AI risk assessment process, including criteria for risk acceptance?",
                "recommendation": "Adopt a risk management framework (like ISO 31000 or NIST AI RMF). Define clear criteria for assessing AI-specific risks (e.g., bias, privacy, security, fairness) and establish a risk register."
            },
            {
                "id": "C6_2",
                "text": "Are AI risk treatment plans developed and implemented to address unacceptable risks?",
                "recommendation": "For each high-risk item, document a treatment plan (Avoid, Mitigate, Transfer, Accept). This plan should link to specific controls from Annex A or other sources."
            },
            {
                "id": "C6_3",
                "text": "Are AI system impact assessments (AIIA) conducted for AI systems, considering their potential consequences?",
                "recommendation": "Develop a standardized AIIA template. This should be a mandatory step in the AI system lifecycle, especially before deploying new systems or making major updates to existing ones."
            }
        ]
    },
    {
        "title": "Section 3: Support & Resources (Clause 7)",
        "description": "Ensuring the AIMS is supported with adequate resources, competence, awareness, and documentation.",
        "questions": [
            {
                "id": "C7_1",
                "text": "Does the organization provide necessary resources (human, technical, financial) for the AIMS?",
                "recommendation": "Budget for AIMS-specific roles (e.g., AI Governance Officer, AI auditors), necessary tools (e.g., model monitoring, data validation), and training programs."
            },
            {
                "id": "C7_2",
                "text": "Are personnel involved in the AIMS competent on the basis of appropriate education, training, or experience?",
                "recommendation": "Create a training matrix for AI-related roles. Training should cover responsible AI principles, cybersecurity best practices for AI, data privacy, and the organization's specific AI policies."
            },
            {
                "id": "C7_3",
                "text": "Is documented information required by the AIMS and this standard controlled (e.g., created, updated, available, and protected)?",
                "recommendation": "Establish a document control procedure. Use a central repository (e.g., SharePoint, Confluence) for all AIMS documentation (policies, risk assessments, audit reports) with version control and access restrictions."
            }
        ]
    },
    {
        "title": "Section 4: AI System Lifecycle (Clause 8)",
        "description": "Managing the planning, design, development, verification, validation, and operation of AI systems.",
        "questions": [
            {
                "id": "C8_1",
                "text": "Are processes in place to manage the entire AI system lifecycle, from conception to decommissioning?",
                "recommendation": "Define and document a formal AI System Development Lifecycle (SDLC). This should integrate AIMS requirements (e.g., AIIAs, V&V, data governance) at each stage."
            },
            {
                "id": "C8_2",
                "text": "Is data for AI system development and operation managed according to quality, security, and privacy requirements?",
                "recommendation": "Implement robust data governance practices. This includes data lineage documentation, quality checks, data minimization, and applying security controls (e.g., encryption, access control) to training and operational data."
            },
            {
                "id": "C8_3",
                "text": "Are verification and validation (V&V) activities performed to ensure the AI system meets its intended requirements?",
                "recommendation": "Develop V&V plans that test for more than just accuracy. Include tests for robustness, fairness/bias, and security vulnerabilities (e.g., model evasion, data poisoning)."
            },
            {
                "id": "C8_4",
                "text": "Are processes established for the responsible deployment, operation, and monitoring of AI systems in production?",
                "recommendation": "Implement continuous monitoring for AI systems. This should track model performance, data drift, and potential emergence of bias. Establish a clear human-in-the-loop (HITL) process for critical decisions."
            }
        ]
    },
    {
        "title": "Section 5: Evaluation & Improvement (Clauses 9 & 10)",
        "description": "Monitoring, measuring, analyzing, and improving the AI Management System.",
        "questions": [
            {
                "id": "C9_1",
                "text": "Is the performance and effectiveness of the AIMS monitored, measured, analyzed, and evaluated?",
                "recommendation": "Define key performance indicators (KPIs) for your AIMS. Examples: % of AI systems that completed an AIIA, # of AI-related incidents, % of staff trained on AI policy."
            },
            {
                "id": "C9_2",
                "text": "Are internal audits of the AIMS conducted at planned intervals?",
                "recommendation": "Schedule and conduct internal AIMS audits. These should be performed by competent auditors (internal or external) who are independent of the AI system's development."
            },
            {
                "id": "C9_3",
                "text": "Does top management review the AIMS at planned intervals (Management Review)?",
                "recommendation": "Establish a formal Management Review meeting (e.g., annually). This meeting must review AIMS performance, audit results, and opportunities for improvement, with documented minutes and actions."
            },
            {
                "id": "C9_4",
                "text": "Does the organization continually improve the suitability, adequacy, and effectiveness of the AIMS, including addressing non-conformities?",
                "recommendation": "Implement a formal corrective action process (CAPA). When non-conformities are found (from audits or incidents), they must be logged, a root cause analysis performed, and corrective actions tracked to completion."
            }
        ]
    }
]

# --- HTML TEMPLATES (using Jinja2 syntax) ---

# Base layout template
layout_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ISO/IEC 42001 Gap Assessment Tool</title>
    <!-- Load Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- Use Inter font family -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Inter', sans-serif; }
        /* Print styles */
        @media print {
            body { font-family: 'Inter', sans-serif; }
            #header, #report-buttons { display: none !important; }
            .assessment-container {
                display: block !important;
                box-shadow: none !important;
                border: none !important;
                width: 100% !important;
                max-width: 100% !important;
                margin: 0 !important;
                padding: 0 !important;
            }
            .report-card {
                box-shadow: none !important;
                border: 1px solid #e5e7eb;
                break-inside: avoid;
            }
            h1, h2, h3 { color: #000 !important; }
            a { text-decoration: none; color: #000; }
        }
    </style>
</head>
<body class="bg-gray-100 min-h-screen flex items-center justify-center p-4">
    <div class="container mx-auto max-w-4xl">
        <!-- Header -->
        <header id="header" class="text-center mb-6">
            <h1 class="text-3xl font-bold text-gray-800">AI Compliance Assessment Tool</h1>
            <p class="text-lg text-gray-600">Organizational Readiness for ISO/IEC 42001</p>
        </header>

        <!-- Dynamic Content -->
        <div class="assessment-container bg-white p-8 rounded-lg shadow-lg">
            {{ content|safe }}
        </div>
    </div>
</body>
</html>
"""

# Welcome page template
welcome_template = """
<div class="text-center">
    <h2 class="text-2xl font-semibold text-gray-700 mb-4">Welcome to the Assessment</h2>
    <p class="text-gray-600 mb-6">
        This tool will guide you through a gap assessment to evaluate your organization's readiness for compliance with the ISO/IEC 42001 standard for AI management systems. You will be asked a series of questions based on the standard's key requirements.
    </p>
    <p class="text-gray-600 mb-8">
        Upon completion, you will receive a structured report identifying compliance gaps and providing improvement suggestions.
    </p>
    <a href="{{ url_for('start') }}" class="bg-blue-600 text-white font-semibold py-3 px-6 rounded-lg shadow-md hover:bg-blue-700 transition duration-300">
        Start Assessment
    </a>
</div>
"""

# Assessment page template
assessment_template = """
<form method="POST">
    <h2 class="text-2xl font-semibold text-gray-700 mb-2">{{ section.title }}</h2>
    <p class="text-gray-600 mb-6">{{ section.description }}</p>
    
    <!-- Progress Bar -->
    <div class="w-full bg-gray-200 rounded-full h-2.5 mb-6">
        <div class="bg-blue-600 h-2.5 rounded-full transition-all duration-500" style="width: {{ progress }}%"></div>
    </div>

    <!-- Questions Container -->
    <div class="space-y-6">
        {% for q in section.questions %}
        <div class="py-4 border-b border-gray-200">
            <label for="{{ q.id }}" class="block text-md font-medium text-gray-700">{{ q.text }}</label>
            {% set saved_val = saved_answers.get(q.id, 'not_implemented') %}
            <select id="{{ q.id }}" name="{{ q.id }}" class="mt-2 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm rounded-md">
                <option value="not_implemented" {% if saved_val == 'not_implemented' %}selected{% endif %}>Not Implemented</option>
                <option value="partially_implemented" {% if saved_val == 'partially_implemented' %}selected{% endif %}>Partially Implemented</option>
                <option value="fully_implemented" {% if saved_val == 'fully_implemented' %}selected{% endif %}>Fully Implemented</option>
            </select>
        </div>
        {% endfor %}
    </div>

    <!-- Navigation Buttons -->
    <div class="flex justify-between mt-8">
        {% if current_index > 0 %}
            <button type="submit" name="action" value="prev" class="bg-gray-300 text-gray-700 font-semibold py-2 px-6 rounded-lg hover:bg-gray-400 transition duration-300">
                Previous
            </button>
        {% else %}
            <div></div> <!-- Placeholder for alignment -->
        {% endif %}
        
        {% if current_index < total_sections - 1 %}
            <button type="submit" name="action" value="next" class="bg-blue-600 text-white font-semibold py-2 px-6 rounded-lg shadow-md hover:bg-blue-700 transition duration-300">
                Next
            </button>
        {% else %}
            <button type="submit" name="action" value="report" class="bg-green-600 text-white font-semibold py-2 px-6 rounded-lg shadow-md hover:bg-green-700 transition duration-300">
                Generate Report
            </button>
        {% endif %}
    </div>
</form>
"""

# Report page template
report_template = """
<div class="flex justify-between items-center mb-6" id="report-buttons">
    <h2 class="text-3xl font-bold text-gray-800">Assessment Report</h2>
    <div class="space-x-2">
        <a href="{{ url_for('reset') }}" class="bg-gray-300 text-gray-700 font-semibold py-2 px-4 rounded-lg hover:bg-gray-400 transition duration-300">
            Back to Start
        </a>
        <button onclick="window.print()" class="bg-blue-600 text-white font-semibold py-2 px-4 rounded-lg hover:bg-blue-700 transition duration-300">
            Print Report
        </button>
    </div>
</div>

<!-- Summary Card -->
<div class="bg-gray-50 p-6 rounded-lg border border-gray-200 mb-8">
    <h3 class="text-xl font-semibold text-gray-700 mb-4">Overall Compliance</h3>
    <div class="flex items-center space-x-4">
        <div class="relative w-24 h-24">
            <svg class="w-full h-full" viewBox="0 0 36 36">
                <path class="text-gray-200"
                    d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                    fill="none" stroke-width="3" />
                <path class="text-blue-600"
                    stroke-width="3"
                    stroke-dasharray="{{ score }}, 100"
                    fill="none"
                    d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                />
            </svg>
            <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 text-2xl font-bold text-gray-700">
                {{ score }}%
            </div>
        </div>
        <div>
            <p class="text-gray-600">
                Your organization has implemented <strong>{{ implemented_count }}</strong> out of 
                <strong>{{ total_questions }}</strong> total requirements.
            </p>
            <p class="mt-1 text-gray-600">{{ summary_text }}</p>
        </div>
    </div>
</div>

<!-- Gap Analysis Section -->
<h3 class="text-2xl font-semibold text-gray-700 mb-4">Gap Analysis & Recommendations</h3>
<div class="space-y-4">
    {% if not gaps %}
        <div class="text-center text-gray-500 py-6 bg-gray-50 rounded-lg">
            <h4 class="text-lg font-semibold">Congratulations!</h4>
            <p>No major compliance gaps were identified based on your responses.</p>
        </div>
    {% else %}
        {% for gap in gaps %}
            <div class="report-card bg-white p-6 rounded-lg border border-gray-200 shadow-sm">
                <div class="flex justify-between items-start mb-2">
                    <h4 classs="text-lg font-semibold text-gray-800">{{ gap.text }}</h4>
                    {% if gap.status == 'not_implemented' %}
                        <span class="text-sm font-medium py-1 px-3 rounded-full text-red-600 bg-red-100">Not Implemented</span>
                    {% else %}
                        <span class="text-sm font-medium py-1 px-3 rounded-full text-yellow-600 bg-yellow-100">Partially Implemented</span>
                    {% endif %}
                </div>
                <p class="text-sm text-gray-500 mb-3">Associated Requirement: {{ gap.id }}</p>
                <h5 class="font-semibold text-gray-700 mb-1">Recommendation:</h5>
                <p class="text-gray-600">{{ gap.recommendation }}</p>
            </div>
        {% endfor %}
    {% endif %}
</div>
"""

# --- HELPER FUNCTION ---

def generate_report_data(answers):
    """Processes session answers into a report."""
    implemented_count = 0
    total_questions = 0
    gaps = []

    for section in ISO_42001_SECTIONS:
        for q in section["questions"]:
            total_questions += 1
            answer = answers.get(q["id"], "not_implemented")
            
            if answer == 'fully_implemented':
                implemented_count += 1
            else:
                gaps.append({
                    "id": q["id"],
                    "text": q["text"],
                    "recommendation": q["recommendation"],
                    "status": answer
                })

    score = 0
    if total_questions > 0:
        score = round((implemented_count / total_questions) * 100)

    # Determine summary text based on score
    if score == 100:
        summary_text = "Excellent! You are fully aligned with all assessed requirements."
    elif score >= 75:
        summary_text = "Great start! You have a solid foundation. Focus on the gaps below."
    elif score >= 50:
        summary_text = "Good progress, but there are several key areas to address."
    else:
        summary_text = "You have significant gaps. Use the report below to prioritize actions."

    return {
        "score": score,
        "implemented_count": implemented_count,
        "total_questions": total_questions,
        "gaps": gaps,
        "summary_text": summary_text
    }

# --- FLASK ROUTES ---

@app.route("/")
def index():
    """Display the welcome page."""
    session.clear() # Start fresh
    content = render_template_string(welcome_template)
    return render_template_string(layout_template, content=content)

@app.route("/start")
def start():
    """Clear session and redirect to the first section."""
    session.clear()
    session['answers'] = {}
    return redirect(url_for('section', section_index=0))

@app.route("/section/<int:section_index>", methods=["GET", "POST"])
def section(section_index):
    """Display a section of the assessment."""
    
    # Ensure 'answers' is in session
    if 'answers' not in session:
        session['answers'] = {}

    total_sections = len(ISO_42001_SECTIONS)

    # Handle form submission
    if request.method == "POST":
        # Save answers from the form to the session
        # Use request.form.to_dict() to get all form data
        session['answers'].update(request.form.to_dict())
        session.modified = True # Mark session as modified
        
        action = request.form.get('action')
        
        if action == "next":
            next_index = section_index + 1
            if next_index < total_sections:
                return redirect(url_for('section', section_index=next_index))
        elif action == "prev":
            prev_index = section_index - 1
            if prev_index >= 0:
                return redirect(url_for('section', section_index=prev_index))
        elif action == "report":
            return redirect(url_for('report'))

    # Handle GET request
    if 0 <= section_index < total_sections:
        current_section = ISO_42001_SECTIONS[section_index]
        progress = ((section_index + 1) / total_sections) * 100
        saved_answers = session.get('answers', {})
        
        content = render_template_string(
            assessment_template,
            section=current_section,
            current_index=section_index,
            total_sections=total_sections,
            progress=progress,
            saved_answers=saved_answers
        )
        return render_template_string(layout_template, content=content)
    else:
        # Invalid index, redirect to start
        return redirect(url_for('index'))

@app.route("/report")
def report():
    """Generate and display the final report."""
    answers = session.get('answers', {})
    report_data = generate_report_data(answers)
    
    content = render_template_string(
        report_template,
        score=report_data['score'],
        implemented_count=report_data['implemented_count'],
        total_questions=report_data['total_questions'],
        summary_text=report_data['summary_text'],
        gaps=report_data['gaps']
    )
    return render_template_string(layout_template, content=content)

@app.route("/reset")
def reset():
    """Clear session and redirect to the welcome page."""
    session.clear()
    return redirect(url_for('index'))

# --- RUN THE APP ---
if __name__ == "__main__":
    app.run(debug=True)
