// Test case data
const testCases = {
    case1: {
        title: "Suspected Acute Coronary Syndrome",
        age: 62,
        gender: "male",
        medicalHistory: [
            "Type 2 diabetes (diagnosed 10 years ago)",
            "Hypertension (diagnosed 15 years ago)",
            "Hyperlipidemia",
            "Former smoker (quit 5 years ago, 30 pack-year history)"
        ],
        medications: [
            "Metformin 1000mg twice daily",
            "Lisinopril 20mg once daily",
            "Atorvastatin 40mg once daily",
            "Aspirin 81mg once daily"
        ],
        symptoms: [
            "Substernal chest pressure (8/10 intensity) for 45 minutes",
            "Radiation to left arm and jaw",
            "Diaphoresis",
            "Nausea",
            "Shortness of breath"
        ],
        vitals: {
            "BP": "165/95 mmHg",
            "HR": "92 bpm",
            "RR": "22/min",
            "O2 Sat": "94% on room air",
            "Temp": "37.0°C"
        },
        questions: [
            {
                text: "What is the most likely diagnosis based on this presentation?",
                additionalContext: "Physical Exam: Anxious appearing, diaphoretic, no murmurs or gallops, no rales or rhonchi. Lab Results: Initial Troponin I: 0.04 ng/mL (slightly elevated), EKG: 1mm ST depression in leads V3-V5, BNP: 190 pg/mL"
            },
            {
                text: "What immediate interventions should be considered?",
                additionalContext: "Patient is currently experiencing ongoing chest pain rated 8/10. EKG shows 1mm ST depression in leads V3-V5. Initial Troponin I: 0.04 ng/mL (slightly elevated)."
            },
            {
                text: "What additional diagnostic tests would you recommend?",
                additionalContext: "Initial EKG shows 1mm ST depression in leads V3-V5. Initial Troponin I: 0.04 ng/mL (slightly elevated). Patient has risk factors including diabetes, hypertension, and hyperlipidemia."
            },
            {
                text: "What changes to his medication regimen would be appropriate at this time?",
                additionalContext: "Current medications: Metformin 1000mg twice daily, Lisinopril 20mg once daily, Atorvastatin 40mg once daily, Aspirin 81mg once daily. Suspected ACS with 1mm ST depression in leads V3-V5."
            },
            {
                text: "What is the TIMI risk score for this patient and what does it indicate?",
                additionalContext: "Additional information: Age 62, diagnosed risk factors include diabetes, hypertension, hyperlipidemia. EKG shows ST-segment changes. Initial Troponin I: 0.04 ng/mL (slightly elevated)."
            }
        ]
    },
    case2: {
        title: "Pediatric Respiratory Distress",
        age: 4,
        gender: "female",
        medicalHistory: [
            "Asthma diagnosed at age 3",
            "Eczema since infancy",
            "Two previous hospitalizations for asthma exacerbations"
        ],
        medications: [
            "Albuterol inhaler PRN",
            "Fluticasone inhaler BID (often missed doses per parent)"
        ],
        symptoms: [
            "Progressive cough and wheezing for 2 days",
            "Increased work of breathing",
            "Decreased appetite",
            "Mild fever",
            "Limited speech to 2-3 words per breath"
        ],
        vitals: {
            "Temp": "38.1°C",
            "HR": "135 bpm",
            "RR": "38/min",
            "O2 Sat": "91% on room air",
            "BP": "95/60 mmHg"
        },
        questions: [
            {
                text: "What is the severity of this asthma exacerbation based on the information provided?",
                additionalContext: "Physical Exam: Moderate respiratory distress, bilateral wheezing with prolonged expiratory phase, subcostal and intercostal retractions, no cyanosis, no foreign body suspected. Recent URI symptoms in daycare classmates."
            },
            {
                text: "What immediate treatment should be initiated in the ED?",
                additionalContext: "Physical Exam shows moderate respiratory distress, bilateral wheezing with prolonged expiratory phase, subcostal and intercostal retractions. O2 Sat: 91% on room air."
            },
            {
                text: "What further evaluation should be performed?",
                additionalContext: "Child has moderate respiratory distress with bilateral wheezing. History of two previous hospitalizations for asthma. Current O2 Sat: 91% on room air, Temperature: 38.1°C."
            },
            {
                text: "What factors may have triggered this exacerbation?",
                additionalContext: "Recent URI symptoms in daycare classmates. Parent reports often missed doses of Fluticasone inhaler. Child has history of eczema and known allergies to peanuts and dust mites."
            }
        ]
    },
    case3: {
        title: "Complex Geriatric Fall Evaluation",
        age: 84,
        gender: "female",
        medicalHistory: [
            "Parkinson's disease (diagnosed 8 years ago)",
            "Osteoporosis (diagnosed 12 years ago)",
            "Atrial fibrillation (diagnosed 5 years ago)",
            "Stage 3 CKD (eGFR 45)",
            "Mild cognitive impairment"
        ],
        medications: [
            "Carbidopa/Levodopa 25/100mg TID",
            "Apixaban 2.5mg BID",
            "Alendronate 70mg weekly",
            "Vitamin D3 1000 IU daily",
            "Calcium carbonate 500mg BID",
            "Metoprolol 25mg BID"
        ],
        symptoms: [
            "Fall yesterday evening in bathroom",
            "Left hip pain (7/10)",
            "Unable to bear weight",
            "No loss of consciousness reported",
            "No preceding dizziness noted",
            "Spent approximately 1 hour on floor before using medical alert"
        ],
        vitals: {
            "BP": "128/72 mmHg",
            "HR": "78 bpm, irregular",
            "RR": "18/min",
            "O2 Sat": "96% on room air",
            "Temp": "36.8°C"
        },
        questions: [
            {
                text: "What are the most urgent management considerations for this patient?",
                additionalContext: "Physical Exam: Alert, oriented to person and place, unclear on time. Left hip with external rotation and shortening. Pain with passive movement of left hip. X-ray shows left intertrochanteric femur fracture. INR: 2.1 (on apixaban)."
            },
            {
                text: "How should her anticoagulation be managed in the perioperative period?",
                additionalContext: "Patient on Apixaban 2.5mg BID for atrial fibrillation. Current INR: 2.1. X-ray shows left intertrochanteric femur fracture requiring surgical intervention. eGFR: 38 mL/min."
            },
            {
                text: "What is the optimal timing for surgical intervention?",
                additionalContext: "84-year-old female with left intertrochanteric femur fracture. On Apixaban with INR: 2.1. Comorbidities include Parkinson's disease, atrial fibrillation, Stage 3 CKD (current eGFR: 38 mL/min), and mild cognitive impairment."
            }
        ]
    },
    case4: {
        title: "Diabetic Ketoacidosis with Comorbidities",
        age: 28,
        gender: "male",
        medicalHistory: [
            "Type 1 diabetes (diagnosed at age 12)",
            "Depression",
            "History of recurrent DKA (3 episodes in past 2 years)"
        ],
        medications: [
            "Insulin glargine 28 units at bedtime",
            "Insulin lispro sliding scale",
            "Sertraline 100mg daily"
        ],
        symptoms: [
            "Nausea and vomiting for 2 days",
            "Abdominal pain (diffuse)",
            "Extreme thirst",
            "Frequent urination",
            "Progressive confusion per roommate",
            "Last insulin dose: unknown (roommate reports patient may have run out)"
        ],
        vitals: {
            "BP": "102/68 mmHg",
            "HR": "118 bpm",
            "RR": "28/min (deep respirations)",
            "O2 Sat": "97% on room air",
            "Temp": "37.2°C"
        },
        questions: [
            {
                text: "What are the diagnostic criteria for DKA, and does this patient meet them?",
                additionalContext: "Lab Results: Glucose: 485 mg/dL, Arterial pH: 7.12, Bicarbonate: 8 mEq/L, Anion gap: 28, Serum ketones: Large, Potassium: 5.8 mEq/L, Sodium: 132 mEq/L (corrected Na: 139)"
            },
            {
                text: "What is the appropriate initial fluid management strategy?",
                additionalContext: "Lab Results: Glucose: 485 mg/dL, Arterial pH: 7.12, Bicarbonate: 8 mEq/L, BUN: 38 mg/dL, Creatinine: 1.6 mg/dL, Potassium: 5.8 mEq/L, Sodium: 132 mEq/L (corrected Na: 139)"
            }
        ]
    },
    case5: {
        title: "Suspected Pulmonary Embolism in Pregnancy",
        age: 31,
        gender: "female",
        medicalHistory: [
            "Current pregnancy (28 weeks gestation)",
            "Prior pregnancy with postpartum DVT 2 years ago",
            "Hypothyroidism",
            "Mild asthma"
        ],
        medications: [
            "Prenatal vitamins",
            "Levothyroxine 125 mcg daily",
            "Albuterol inhaler PRN"
        ],
        symptoms: [
            "Sudden onset shortness of breath for 3 hours",
            "Pleuritic right-sided chest pain",
            "Mild hemoptysis (noticed once)",
            "Palpitations",
            "No syncope or dizziness",
            "No calf pain or swelling"
        ],
        vitals: {
            "BP": "138/88 mmHg",
            "HR": "114 bpm",
            "RR": "24/min",
            "O2 Sat": "93% on room air",
            "Temp": "37.0°C"
        },
        questions: [
            {
                text: "How does the modified Wells score assess this patient's risk of PE?",
                additionalContext: "31-year-old female at 28 weeks gestation with sudden onset shortness of breath, pleuritic chest pain, mild hemoptysis, and history of postpartum DVT 2 years ago. HR: 114 bpm, RR: 24/min, O2 Sat: 93%."
            },
            {
                text: "What is the appropriate diagnostic approach given her pregnancy?",
                additionalContext: "28 weeks pregnant with suspected PE. D-dimer: 1850 ng/mL (elevated, but note physiologic elevation in pregnancy). CXR: No infiltrates, effusions, or pneumothorax. Vitals: HR: 114 bpm, RR: 24/min, O2 Sat: 93%."
            }
        ]
    },
    case6: {
        title: "Altered Mental Status with Metabolic Derangements",
        age: 73,
        gender: "male",
        medicalHistory: [
            "Cirrhosis due to alcohol use (Child-Pugh Class B)",
            "Chronic hepatic encephalopathy",
            "Type 2 diabetes",
            "Hypertension",
            "GERD"
        ],
        medications: [
            "Lactulose 20g TID",
            "Rifaximin 550mg BID",
            "Propranolol 20mg BID",
            "Furosemide 40mg daily",
            "Spironolactone 100mg daily",
            "Insulin glargine 15 units daily",
            "Pantoprazole 40mg daily"
        ],
        symptoms: [
            "Progressive confusion over 3 days",
            "Lethargy",
            "Poor oral intake",
            "No fever or chills",
            "Mild abdominal distension",
            "One episode of melena 2 days ago"
        ],
        vitals: {
            "BP": "108/64 mmHg",
            "HR": "92 bpm",
            "RR": "18/min",
            "O2 Sat": "94% on room air",
            "Temp": "37.3°C"
        },
        questions: [
            {
                text: "What are the potential causes of this patient's altered mental status?",
                additionalContext: "Lab Results: Ammonia: 95 μmol/L (elevated), Sodium: 129 mEq/L, Potassium: 3.2 mEq/L, Glucose: 68 mg/dL, Hgb: 8.5 g/dL (baseline 10.5), Creatinine: 1.7 mg/dL (baseline 1.2)"
            },
            {
                text: "What is the most appropriate initial diagnostic approach?",
                additionalContext: "73-year-old male with cirrhosis, chronic hepatic encephalopathy, and episode of melena 2 days ago. Current labs: Ammonia: 95 μmol/L, Sodium: 129 mEq/L, Hgb: 8.5 g/dL (baseline 10.5), INR: 1.8"
            }
        ]
    }
};

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('medical-query-form');
    const responseContainer = document.getElementById('response-container');
    const loadingIndicator = document.getElementById('loading-indicator');
    const responseContent = document.getElementById('response-content');
    const disclaimer = document.getElementById('disclaimer');
    const modelUsed = document.getElementById('model-used');
    const tokensUsed = document.getElementById('tokens-used');
    
    // Configure marked.js for safe rendering
    marked.setOptions({
        breaks: true,        // Add line breaks
        gfm: true,          // GitHub flavored markdown
        headerIds: true,    // Add IDs to headers
        sanitize: false     // Don't sanitize (marked.js will handle this)
    });
    
    // Add test case selector to the page
    const formSection = document.querySelector('.medical-interface');
    const testCaseDiv = document.createElement('div');
    testCaseDiv.className = 'test-case-selector';
    testCaseDiv.innerHTML = `
        <h3>Test Cases</h3>
        <div class="form-row">
            <div class="form-field">
                <label for="test-case-select">Select a clinical test case:</label>
                <select id="test-case-select">
                    <option value="">-- Select a test case --</option>
                    ${Object.keys(testCases).map(key => 
                        `<option value="${key}">${testCases[key].title}</option>`
                    ).join('')}
                </select>
            </div>
            <div class="form-field">
                <label for="question-select">Select a clinical question:</label>
                <select id="question-select" disabled>
                    <option value="">-- First select a test case --</option>
                </select>
            </div>
        </div>
        <button type="button" id="load-case-btn" class="button">Load Selected Case</button>
    `;
    
    // Insert test case selector before the form
    formSection.insertBefore(testCaseDiv, formSection.querySelector('.form-container'));
    
    // Get test case elements
    const testCaseSelect = document.getElementById('test-case-select');
    const questionSelect = document.getElementById('question-select');
    const loadCaseBtn = document.getElementById('load-case-btn');
    
    // Update question dropdown when test case changes
    testCaseSelect.addEventListener('change', function() {
        const selectedCase = testCaseSelect.value;
        questionSelect.innerHTML = '';
        questionSelect.disabled = true;
        
        if (selectedCase && testCases[selectedCase]) {
            questionSelect.disabled = false;
            // Add default option
            const defaultOption = document.createElement('option');
            defaultOption.value = '';
            defaultOption.textContent = '-- Select a question --';
            questionSelect.appendChild(defaultOption);
            
            // Add questions for the selected case
            testCases[selectedCase].questions.forEach((question, index) => {
                const option = document.createElement('option');
                option.value = index;
                option.textContent = question.text;
                questionSelect.appendChild(option);
            });
        } else {
            const option = document.createElement('option');
            option.value = '';
            option.textContent = '-- First select a test case --';
            questionSelect.appendChild(option);
        }
    });
    
    // Load the selected case
    loadCaseBtn.addEventListener('click', function() {
        const selectedCase = testCaseSelect.value;
        const selectedQuestionIndex = questionSelect.value;
        
        if (!selectedCase || !testCases[selectedCase]) {
            alert('Please select a test case');
            return;
        }
        
        const caseData = testCases[selectedCase];
        
        // Fill the form with case data
        document.getElementById('age').value = caseData.age;
        document.getElementById('gender').value = caseData.gender;
        
        // Format medical history as comma-separated list
        document.getElementById('medical-history').value = caseData.medicalHistory.join(', ');
        
        // Format medications as comma-separated list
        document.getElementById('current-medications').value = caseData.medications.join(', ');
        
        // Format symptoms as comma-separated list
        document.getElementById('symptoms').value = caseData.symptoms.join(', ');
        
        // If a specific question is selected, use it
        if (selectedQuestionIndex !== '' && caseData.questions[selectedQuestionIndex]) {
            const question = caseData.questions[selectedQuestionIndex];
            document.getElementById('query').value = question.text;
            document.getElementById('additional-context').value = question.additionalContext || '';
        } else {
            // Default to first question if none selected
            document.getElementById('query').value = '';
            document.getElementById('additional-context').value = '';
        }
    });
    
    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        // Show loading state
        responseContainer.style.display = 'block';
        loadingIndicator.style.display = 'block';
        responseContent.innerHTML = '';
        disclaimer.innerHTML = '';
        modelUsed.innerHTML = '';
        tokensUsed.innerHTML = '';
        
        // Scroll to the response container
        responseContainer.scrollIntoView({ behavior: 'smooth' });
        
        // Get form data
        const age = document.getElementById('age').value;
        const gender = document.getElementById('gender').value;
        const medicalHistory = document.getElementById('medical-history').value.split(',').map(item => item.trim()).filter(Boolean);
        const currentMedications = document.getElementById('current-medications').value.split(',').map(item => item.trim()).filter(Boolean);
        const symptoms = document.getElementById('symptoms').value.split(',').map(item => item.trim()).filter(Boolean);
        const query = document.getElementById('query').value;
        const additionalContext = document.getElementById('additional-context').value;
        
        // Prepare request payload
        const payload = {
            patient_info: {
                age: age ? parseInt(age) : null,
                gender: gender || null,
                medical_history: medicalHistory,
                current_medications: currentMedications,
                symptoms: symptoms
            },
            query: query,
            additional_context: additionalContext || null
        };
        
        try {
            console.log('Sending request to /test/llm endpoint');
            // Make API request to the test endpoint without authentication
            const response = await fetch('/test/llm', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(payload)
            });
            
            if (!response.ok) {
                throw new Error(`Error: ${response.status}`);
            }
            
            const data = await response.json();
            console.log('Response received:', data);
            
            // Update UI with response - convert markdown to HTML
            responseContent.innerHTML = marked.parse(data.response);
            
            // Apply syntax highlighting to code blocks if needed
            document.querySelectorAll('pre code').forEach((block) => {
                if (window.hljs) {
                    hljs.highlightBlock(block);
                }
            });
            
            // Format tables with Bootstrap styling
            const tables = responseContent.querySelectorAll('table');
            tables.forEach(table => {
                table.classList.add('table', 'table-bordered', 'table-hover', 'table-sm');
            });
            
            disclaimer.innerHTML = data.disclaimer;
            modelUsed.innerHTML = `Model: ${data.model_used}`;
            tokensUsed.innerHTML = data.tokens_used ? `Tokens: ${data.tokens_used}` : '';
            
        } catch (error) {
            console.error('Error:', error);
            responseContent.innerHTML = `<p class="text-danger">An error occurred: ${error.message}</p>`;
        } finally {
            // Hide loading indicator
            loadingIndicator.style.display = 'none';
        }
    });
});