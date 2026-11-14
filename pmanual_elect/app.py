import io
from flask import Flask, render_template, request, send_file, abort

app = Flask(__name__)

SERVICES = [
    {
        "id": "enrollment-adding",
        "title": "Subject Adding & Changing (ACE)",
        "category": "Registrar",
        "office": "Registrar's Office - Window 2 (confirm location)",
        "processing_time": "1–2 Working Days (unverified estimate)",
        "summary": (
            "A guide for adding or replacing subjects, changing class sections, "
            "and requesting eligible enrollment adjustments after initial registration."
        ),
        "requirements": [
            "Printed current Certificate of Registration (COR)",
            "Accomplished ACE Form (2 copies, if required)",
            "Correct subject codes, titles, and preferred sections",
            "Academic Adviser's approval or signature",
            "Department Chairperson's approval or signature",
            "Additional supporting documents if requested by the Registrar"
        ],
        "steps": [
            "Check the academic calendar and confirm that the adding/changing period is still open.",
            "Review your current COR and list the subjects or sections you want to add or change.",
            "Confirm subject availability, prerequisites, and possible schedule conflicts with your Academic Adviser.",
            "Get the current ACE Form from the Registrar's Office or an authorized campus source.",
            "Fill out the form legibly with your student details and exact subject codes and sections.",
            "Present the form to your Academic Adviser for review and obtain the required signature.",
            "Have the request checked and approved by the Department Chairperson or designated official.",
            "Submit the approved form and required attachments to the Registrar's Office; ask for proof of receipt.",
            "Wait for confirmation that the change has been encoded; do not assume submission means approval.",
            "Recheck and reprint your COR, verify the subjects, units, and schedule, and report any errors promptly."
        ]
    },
    {
        "id": "id-replacement",
        "title": "Lost / Damaged Student ID Replacement",
        "category": "Student Affairs",
        "office": "Office of Student Services (OSS) - confirm the campus issuing desk",
        "processing_time": "3–5 Working Days (unverified estimate)",
        "summary": (
            "Instructions for requesting a replacement student ID when the original "
            "is lost, stolen, unreadable, or physically damaged."
        ),
        "requirements": [
            "Notarized Affidavit of Loss if required for a lost ID, or the damaged ID",
            "Current Certificate of Registration (COR)",
            "Student number and another acceptable proof of identity",
            "Accomplished ID replacement request form if required",
            "Official Receipt of ID replacement fee (₱150.00 in the group's draft; verify)"
        ],
        "steps": [
            "Report the lost or damaged ID to the Office of Student Services and ask whether a temporary pass is available.",
            "Confirm the exact requirements for lost IDs versus damaged IDs before paying for documents.",
            "Prepare your COR, proof of identity, and an affidavit of loss if the campus requires it.",
            "Present the documents at the designated OSS or ID issuing desk for identity verification.",
            "Complete the replacement request form and check the spelling of your personal information.",
            "Obtain an official payment assessment or instructions from authorized staff.",
            "Pay the confirmed fee only through the authorized university payment channel and keep the receipt.",
            "Return to the issuing office, submit the receipt, and complete any required photo capture or verification.",
            "Record the reference number or scheduled release date provided by the office.",
            "Claim the replacement ID, inspect the details, and ask how to deactivate a lost card if applicable."
        ]
    },
    {
        "id": "good-moral",
        "title": "Certificate of Good Moral Character",
        "category": "Student Affairs",
        "office": "Guidance & Counseling Office (confirm issuing office)",
        "processing_time": "Same Day (2 Hours) - unverified estimate",
        "summary": (
            "A request guide for students and alumni who need a character "
            "certification for scholarships, internships, transfers, or employment."
        ),
        "requirements": [
            "Valid Student ID or acceptable alumni identification",
            "Latest Certificate of Registration (COR) or proof of graduation, as applicable",
            "Student number and purpose of request",
            "Request form or logbook entry if required",
            "Cashier Official Receipt (₱50.00 in the group's draft; verify)",
            "Any additional clearance requested by the issuing office"
        ],
        "steps": [
            "Ask the Guidance & Counseling Office whether it issues the certificate for your student or alumni status.",
            "Prepare your ID, COR or graduation record, and the name of the organization requesting the certificate.",
            "Visit the authorized office during service hours and sign the request logbook if required.",
            "Complete the request form accurately, including your program and purpose of request.",
            "Have the requirements checked and obtain an official payment assessment if a fee applies.",
            "Pay at the authorized Cashier's Office and keep the official receipt.",
            "Return the assessed documents and receipt to the issuing office.",
            "Allow the office to verify your records and approve the request in accordance with its policy.",
            "Claim the signed certificate or follow the release instructions given by the office.",
            "Before leaving, check your full name, purpose, issue date, and authorized signatory."
        ]
    },
    {
        "id": "faculty-hiring-COS",
        "title": "Full-Time Faculty Application (Contract of Service)",
        "category": "Faculty Recruitment",
        "office": "Office of the Head of Academic Programs - PUP Santa Maria Campus",
        "processing_time": "Not specified; subject to campus recruitment schedule",
        "summary": (
            "Application guide for the full-time Contract of Service faculty "
            "recruitment listed in the group's draft for the second semester "
            "of AY 2026–2027, covering BSIT, BSA, BS Entrepreneurship, and BSCpE. "
            "Confirm the vacancy announcement and deadline before applying."
        ),
        "requirements": [
            "Letter of Intent addressed to Dr. Arman DC. Santos, Campus Director",
            "Fully accomplished Personal Data Sheet (CS Form No. 212, Revised 2026)",
            "Authenticated Transcript of Records and Diploma, as specified in the announcement",
            "Authenticated Certificate of Eligibility or professional license, if applicable",
            "Certificate of Employment or Service Record",
            "Photocopies of relevant seminar and training certificates",
            "Any additional materials, copies, or format required by the recruitment announcement"
        ],
        "steps": [
            "Locate the latest recruitment notice and confirm the open programs, qualifications, submission location, and deadline.",
            "Review the minimum educational and professional qualifications for the discipline you intend to teach.",
            "Download CS Form No. 212 (Revised 2026) and its completion guide from the Civil Service Commission website.",
            "Complete the Personal Data Sheet accurately and prepare related work-experience information if requested.",
            "Write a formal Letter of Intent addressed to Dr. Arman DC. Santos, identifying your intended teaching field.",
            "Collect your TOR, diploma, eligibility or license documents, employment records, and relevant training certificates.",
            "Arrange authentication or certification of your credentials only as required by the official announcement.",
            "Check the completeness, legibility, and requested number of copies of every document.",
            "Submit your application in person to the Head of Academic Programs, Dr. Katherin Joyce M. Castro, if the current notice directs applicants there.",
            "Use November 30, 2026 only as the deadline stated in the group's draft; verify it from the actual vacancy posting.",
            "Request acknowledgment of receipt and monitor the official channel for screening, interview, or demonstration-teaching instructions.",
            "Attend any scheduled evaluation and wait for a formal hiring decision before assuming an appointment."
        ]
    },
    {
        "id": "cor-request",
        "title": "Certificate of Registration (COR) Request / Reprint",
        "category": "Registrar",
        "office": "Campus Registrar / Authorized Student Portal",
        "processing_time": "Depends on portal availability and certification request",
        "summary": (
            "How to view, download, reprint, or request an official copy "
            "of your current semester's Certificate of Registration."
        ),
        "requirements": [
            "Student number and access to the authorized student portal",
            "Current enrollment details (academic year and semester)",
            "Valid Student ID if requesting an office-issued copy",
            "Document request form and receipt if the office requires certification or payment"
        ],
        "steps": [
            "Confirm that your enrollment is finalized and your subject adjustments are already encoded.",
            "Sign in to the official student portal using your own account.",
            "Open the registration or enrollment records section and select the correct semester.",
            "Review your name, program, section, subjects, and academic units for accuracy.",
            "Use the portal's download or print function if a COR is available.",
            "If the COR is missing, incorrect, or must be officially certified, contact the Campus Registrar.",
            "Present the requested proof of identity and complete any additional request form.",
            "Follow the authorized payment and document release instructions, if applicable.",
            "Keep the correct, updated COR and avoid sharing copies containing private student details publicly."
        ]
    },
    {
        "id": "subject-dropping",
        "title": "Official Subject Dropping / Withdrawal",
        "category": "Registrar",
        "office": "Academic Adviser / Department Office / Campus Registrar",
        "processing_time": "Depends on academic deadline and approval",
        "summary": (
            "A procedure for formally dropping an enrolled subject within "
            "the permitted period rather than simply stopping attendance."
        ),
        "requirements": [
            "Current Certificate of Registration (COR)",
            "Student ID or student number",
            "Official dropping or enrollment adjustment form, if applicable",
            "Academic Adviser and department approval, when required",
            "Supporting explanation or documents, if requested"
        ],
        "steps": [
            "Read the university's current academic calendar and verify the deadline for dropping or withdrawal.",
            "Identify the exact subject code, section, and instructor on your current COR.",
            "Consult your Academic Adviser about minimum units, prerequisites, and possible effects on scholarship eligibility.",
            "Ask the Registrar which dropping or ACE form applies to your situation.",
            "Complete the form and state the required reason for the request.",
            "Obtain all required signatures from your adviser, chairperson, or authorized personnel.",
            "Submit the form before the deadline and retain proof that it was received.",
            "Wait for the decision and check how the subject will appear on your official enrollment record.",
            "Get an updated COR or written confirmation and resolve discrepancies promptly."
        ]
    },
    {
        "id": "grades-request",
        "title": "Certificate of Grades / Academic Grades Request",
        "category": "Registrar",
        "office": "Campus Registrar / PUP Online Document Request System (if available)",
        "processing_time": "Varies by academic record and document type",
        "summary": (
            "Instructions for obtaining academic grades for scholarships, "
            "employment, transfers, or record-keeping."
        ),
        "requirements": [
            "Student number and valid identification",
            "Academic year and semester to be covered",
            "Completed document request, if required",
            "Relevant supporting documents or receipt shown by the office or request system"
        ],
        "steps": [
            "Determine whether you need an online grade view, an official Certificate of Grades, or a certified copy.",
            "Check that all grades for the requested semester have already been submitted and posted.",
            "Ask the Campus Registrar whether your requested document is handled locally or through PUP ODRS.",
            "If directed to ODRS, sign in to https://odrs.pup.edu.ph/ and choose the appropriate available document type.",
            "Enter accurate student and academic-period information and upload required documents when prompted.",
            "Review the request summary and complete any authorized payment instructions if applicable.",
            "Save your reference or request number and monitor the official status notices.",
            "Claim or receive the document according to the office's instructions.",
            "Verify that the name, subject grades, semester, and authentication information are correct."
        ]
    },
    {
        "id": "tor-request",
        "title": "Transcript of Records (TOR) Request",
        "category": "Registrar",
        "office": "Campus Registrar / PUP Online Document Request System (ODRS)",
        "processing_time": "Varies; check the request system or Registrar",
        "summary": (
            "A guide to requesting an official transcript containing "
            "completed subjects, grades, and academic units."
        ),
        "requirements": [
            "Student or graduate identification and student number",
            "Accurate program, attendance, and graduation information",
            "Completed online or campus document request",
            "Clearance or release documents, if required for the requested TOR",
            "Photo, request letter, payment voucher, or proof of payment if instructed"
        ],
        "steps": [
            "Identify why you need the TOR and whether it is a first copy or a subsequent copy.",
            "Check the Campus Registrar's current TOR requirements, especially for graduates and transferring students.",
            "Visit https://odrs.pup.edu.ph/ if the campus instructs you to use PUP's Online Document Request System.",
            "Register or log in and select the correct campus or registrar when applicable.",
            "Choose the available TOR document option and complete the request details.",
            "Upload any required photo, clearance, or supporting document shown for your request.",
            "Review and submit the request, then follow the prescribed payment process if required.",
            "Monitor official updates and comply with requests for missing or corrected requirements.",
            "Follow the approved pickup or delivery arrangement and present the necessary claim documents.",
            "Inspect the released TOR for correct identifying details and complete academic records."
        ]
    },
    {
        "id": "document-certification",
        "title": "Certified True Copy / Document Authentication",
        "category": "Registrar",
        "office": "Campus Registrar / Designated Document Certification Desk",
        "processing_time": "Varies by document and verification requirements",
        "summary": (
            "Request official certification or authentication of eligible "
            "university-issued academic documents."
        ),
        "requirements": [
            "Original university-issued document for inspection, if required",
            "Photocopies of the document in the number requested by the office",
            "Valid student or government-issued ID",
            "Document request or certification form, if required",
            "Official receipt or payment voucher when applicable"
        ],
        "steps": [
            "Ask the receiving organization whether it needs a certified true copy, authentication, or another form of verification.",
            "Confirm with the Campus Registrar that your document is eligible for that service.",
            "Prepare the original document and required photocopies, keeping them clean and readable.",
            "Complete any prescribed request form and specify the number of certified copies.",
            "Submit the documents for checking against university records.",
            "Pay only the officially assessed amount, if applicable, and retain the receipt.",
            "Obtain a claim date or request reference and monitor any additional instructions.",
            "Receive the certified document and check the seal, signature, and information."
        ]
    },
    {
        "id": "library-clearance",
        "title": "Library Clearance Request",
        "category": "Library",
        "office": "PUP Santa Maria Campus Library",
        "processing_time": "Varies by account verification and outstanding obligations",
        "summary": (
            "A guide to securing library clearance for graduation, "
            "transfers, or other official requirements."
        ),
        "requirements": [
            "Valid Student ID and student number",
            "Clearance form or request reference, if required",
            "All outstanding borrowed books or library materials",
            "Proof of settlement of any applicable obligations"
        ],
        "steps": [
            "Check whether your requested academic transaction requires library clearance.",
            "Review your library borrowing account and identify any unreturned materials.",
            "Return all outstanding borrowed books and materials to the designated circulation staff.",
            "Ask library personnel whether a physical form or electronic clearance is used.",
            "Present your student ID and submit the appropriate clearance request.",
            "Allow staff to verify borrowing history and any remaining obligations.",
            "Resolve outstanding issues through the official library procedure.",
            "Request the authorized signature, clearance status update, or proof of clearance.",
            "Save the clearance result for your graduation or document-processing requirements."
        ]
    },
    {
        "id": "student-portal-recovery",
        "title": "Student Portal Login / Account Recovery",
        "category": "IT Services",
        "office": "Campus ICT Support / Official PUP Student Support Channel",
        "processing_time": "Varies by cause and identity verification",
        "summary": (
            "Troubleshooting and account recovery steps for students "
            "unable to access university student systems."
        ),
        "requirements": [
            "Student number and registered email address",
            "Valid Student ID for account ownership verification, if requested",
            "Exact error message or screenshot with sensitive details hidden",
            "A reachable recovery email or communication channel"
        ],
        "steps": [
            "Confirm that you are visiting the official university portal rather than an unfamiliar link.",
            "Check your internet connection, browser, and correctly typed student number or username.",
            "Use the portal's official forgot-password or account recovery feature if available.",
            "Check your registered email for a legitimate verification or password reset message.",
            "If unsuccessful, contact Campus ICT Support or PUP's official student support channel.",
            "Describe the problem and provide non-secret account details needed to locate your record.",
            "Complete the office's identity verification before an account is changed.",
            "Follow authorized recovery steps and sign in with the updated credentials.",
            "Set a strong, unique password and never disclose passwords or one-time codes to support staff."
        ]
    },
    {
        "id": "scholarship-inquiry",
        "title": "Scholarship Application and Renewal Inquiry",
        "category": "Student Affairs",
        "office": "Office of Student Services / Designated Scholarship Coordinator",
        "processing_time": "Depends on scholarship announcement and selection period",
        "summary": (
            "A preparation guide for checking scholarship eligibility, "
            "submitting an application, or renewing an existing award."
        ),
        "requirements": [
            "Current Certificate of Registration or proof of enrollment",
            "Valid Student ID and contact details",
            "Grade record or academic evaluation, if listed in the scholarship notice",
            "Application or renewal form provided by the scholarship program",
            "Income, residency, or other eligibility documents only if officially required"
        ],
        "steps": [
            "Check the official university or scholarship-provider announcement for open applications.",
            "Read the eligibility rules, covered programs, grade requirements, and deadlines carefully.",
            "Ask the designated Scholarship Coordinator whether new applications or renewals are currently accepted.",
            "Prepare your enrollment record and the exact supporting documents listed in the announcement.",
            "Fill out the current application or renewal form using complete and truthful information.",
            "Submit through the authorized portal, email, or office stated in the notice.",
            "Keep a copy of your submission confirmation and monitor your official contact channel.",
            "Provide missing information or attend a required screening only when instructed.",
            "Check the official result and follow the acceptance or renewal requirements."
        ]
    },
    {
        "id": "student-record-correction",
        "title": "Correction of Student Personal Records",
        "category": "Registrar",
        "office": "PUP Santa Maria Campus Registrar",
        "processing_time": "Depends on requested correction and supporting documents",
        "summary": (
            "How to request corrections to your name, birth date, "
            "or other recorded personal details in university systems."
        ),
        "requirements": [
            "Valid PUP Student ID and student number",
            "Current COR or university record showing the incorrect detail",
            "Proof of correct information, such as an accepted civil registry record",
            "Completed correction request form, if required",
            "Other supporting records specified by the Registrar"
        ],
        "steps": [
            "Locate the exact error in your student portal or printed university document.",
            "Prepare a clear description of the incorrect entry and the correct information.",
            "Contact the Campus Registrar to learn the requirements for that specific kind of correction.",
            "Collect official supporting documents proving the correct detail.",
            "Complete the prescribed request form and attach clear copies of the evidence.",
            "Submit the request for validation and obtain a reference or acknowledgement.",
            "Provide any additional evidence requested during verification.",
            "After approval, check that your student portal and future records show the correction.",
            "Request replacement copies of affected documents if necessary."
        ]
    },
    {
        "id": "transfer-credentials",
        "title": "Transfer Credentials / Honorable Dismissal",
        "category": "Registrar",
        "office": "PUP Santa Maria Campus Registrar",
        "processing_time": "Varies by clearance and document processing",
        "summary": (
            "A guide for students requesting official transfer credentials "
            "when applying to continue studies at another institution."
        ),
        "requirements": [
            "Valid student identification and student number",
            "Completed transfer credential request, if required",
            "Current COR or academic record",
            "General or departmental clearance, if required",
            "Receiving school's instructions or request letter, if applicable",
            "Official payment documents, if applicable"
        ],
        "steps": [
            "Confirm the receiving school's required transfer documents before beginning your request.",
            "Consult the Campus Registrar about consequences of issuing transfer credentials for your PUP enrollment status.",
            "Ask whether your campus accepts the request in person, through ODRS, or both.",
            "Complete the prescribed form and identify the receiving institution if requested.",
            "Secure required departmental, library, and financial clearances if applicable.",
            "Submit the requirements and complete any official payment process.",
            "Keep your acknowledgement or reference number and monitor the processing status.",
            "Collect the credentials following the authorized release policy.",
            "Inspect the documents and submit them to your receiving school as instructed."
        ]
    }
]

CATEGORIES = ["All", "Registrar", "Student Affairs", "IT Services", "Library", "Faculty Recruitment"]


@app.route("/")
def index():
    query = request.args.get("q", "").strip().lower()
    selected_category = request.args.get("category", "All")

    filtered = []
    for svc in SERVICES:
        matches_cat = (selected_category == "All") or (svc["category"] == selected_category)
        matches_query = (
            not query
            or query in svc["title"].lower()
            or query in svc["summary"].lower()
            or query in svc["category"].lower()
        )
        if matches_cat and matches_query:
            filtered.append(svc)
        
    return render_template(
        "index.html",
        services=filtered,
        categories=CATEGORIES,
        selected_category=selected_category,
        query=query,
    )


@app.route("/download/<service_id>")
def download_guide(service_id):
    svc = next((s for s in SERVICES if s["id"] == service_id), None)
    if not svc:
        abort(404)

    lines = [
        "PMANUAL - DIGITAL CAMPUS SERVICES MANUAL",
        "========================================",
        f"Service: {svc['title']}",
        f"Category: {svc['category']}",
        f"Office: {svc['office']}",
        f"Processing Time: {svc['processing_time']}",
        "\nREQUIREMENTS:",
        *[f" - {req}" for req in svc["requirements"]],
        "\nSTEP-BY-STEP PROCEDURE:",
        *[f" {i}. {step}" for i, step in enumerate(svc["steps"], 1)],
    ]
    buf = io.BytesIO("\n".join(lines).encode("utf-8"))
    return send_file(
        buf,
        as_attachment=True,
        download_name=f"{svc['id']}-guide.txt",
        mimetype="text/plain",
    )


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=8001)
