let currentDocId = null;
let currentDraftId = null;

// DOM Elements
const fileInput = document.getElementById('file-input');
const uploadStatus = document.getElementById('upload-status');
const processBtn = document.getElementById('process-btn');
const processLoader = document.getElementById('process-loader');
const processResult = document.getElementById('process-result');
const jsonResult = document.getElementById('json-result');
const generateBtn = document.getElementById('generate-btn');
const generateLoader = document.getElementById('generate-loader');
const draftResult = document.getElementById('draft-result');
const draftContent = document.getElementById('draft-content');
const evidenceList = document.getElementById('evidence-list');
const feedbackBtn = document.getElementById('feedback-btn');
const feedbackStatus = document.getElementById('feedback-status');

// Step 1: Upload
fileInput.addEventListener('change', async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    uploadStatus.textContent = `Uploading ${file.name}...`;
    const formData = new FormData();
    formData.append('file', file);

    try {
        const res = await fetch('/api/v1/upload', {
            method: 'POST',
            body: formData
        });
        const data = await res.json();
        currentDocId = data.document_id;
        uploadStatus.textContent = `Uploaded successfully! Document ID: ${currentDocId}`;
        
        // Enable Step 2
        document.getElementById('step2').classList.remove('disabled');
    } catch (error) {
        uploadStatus.textContent = `Upload failed: ${error.message}`;
        uploadStatus.style.color = '#ef4444';
    }
});

// Step 2: Process
processBtn.addEventListener('click', async () => {
    if (!currentDocId) return;
    
    processBtn.classList.add('hidden');
    processLoader.classList.remove('hidden');

    try {
        const res = await fetch('/api/v1/process', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ document_id: currentDocId })
        });
        const data = await res.json();
        
        jsonResult.textContent = JSON.stringify(data.structured_data, null, 2);
        processLoader.classList.add('hidden');
        processResult.classList.remove('hidden');
        
        // Enable Step 3
        document.getElementById('step3').classList.remove('disabled');
    } catch (error) {
        alert(`Processing failed: ${error.message}`);
        processBtn.classList.remove('hidden');
        processLoader.classList.add('hidden');
    }
});

// Step 3: Generate Draft
generateBtn.addEventListener('click', async () => {
    if (!currentDocId) return;
    
    generateBtn.classList.add('hidden');
    generateLoader.classList.remove('hidden');

    try {
        const res = await fetch('/api/v1/generate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ document_ids: [currentDocId], draft_type: "case_summary" })
        });
        const data = await res.json();
        
        currentDraftId = data.draft_id;
        draftContent.innerHTML = marked.parse(data.content);
        
        evidenceList.innerHTML = '';
        data.evidence_links.forEach(link => {
            const li = document.createElement('li');
            li.innerHTML = `<strong>[Chunk ${link.chunk_id.substring(0,8)}]</strong>: ${link.text}`;
            evidenceList.appendChild(li);
        });

        generateLoader.classList.add('hidden');
        draftResult.classList.remove('hidden');
        
        // Enable Step 4
        document.getElementById('step4').classList.remove('disabled');
    } catch (error) {
        alert(`Generation failed: ${error.message}`);
        generateBtn.classList.remove('hidden');
        generateLoader.classList.add('hidden');
    }
});

// Step 4: Feedback
feedbackBtn.addEventListener('click', async () => {
    const oldText = document.getElementById('fb-old').value;
    const newText = document.getElementById('fb-new').value;

    if (!oldText || !newText || !currentDraftId) return;

    feedbackBtn.textContent = "Submitting...";

    try {
        const replaceDict = {};
        replaceDict[oldText] = newText;

        const res = await fetch('/api/v1/feedback', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                draft_id: currentDraftId,
                context: "case_summary",
                replace: replaceDict
            })
        });
        const data = await res.json();
        
        feedbackStatus.textContent = `Successfully learned! Future drafts will replace '${oldText}' with '${newText}'.`;
        feedbackBtn.textContent = "Submit Another";
        
        document.getElementById('fb-old').value = '';
        document.getElementById('fb-new').value = '';
    } catch (error) {
        feedbackStatus.textContent = `Feedback failed: ${error.message}`;
        feedbackStatus.style.color = '#ef4444';
        feedbackBtn.textContent = "Submit Edit";
    }
});
