def get_onboarding_html(context):
    """
    Returns a professional, production-ready HTML onboarding form.
    Expects 'context' to be a dict with:
    - product_name
    - bank_name
    - bank_logo_url (optional)
    - connector_name
    - post_url
    - redirect_url
    """
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Apply for {context['product_name']} | {context['bank_name']}</title>
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            
            body {{
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 20px;
                display: flex;
                align-items: center;
                justify-content: center;
            }}
            
            .container {{
                background: white;
                border-radius: 20px;
                box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
                width: 100%;
                max-width: 520px;
                overflow: hidden;
                animation: slideUp 0.5s ease-out;
            }}
            
            @keyframes slideUp {{
                from {{
                    opacity: 0;
                    transform: translateY(30px);
                }}
                to {{
                    opacity: 1;
                    transform: translateY(0);
                }}
            }}
            
            .header {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 40px 30px;
                text-align: center;
            }}
            
            .logo-container {{
                display: flex;
                justify-content: center;
                align-items: center;
                gap: 20px;
                margin-bottom: 20px;
            }}
            
            .logo {{
                background: white;
                width: 60px;
                height: 60px;
                border-radius: 12px;
                display: flex;
                align-items: center;
                justify-content: center;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
            }}
            
            .logo img {{
                max-width: 40px;
                max-height: 40px;
                object-fit: contain;
            }}
            
            .connector-icon {{
                width: 36px;
                height: 36px;
                background: rgba(255, 255, 255, 0.2);
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 18px;
            }}
            
            .header h1 {{
                font-size: 24px;
                font-weight: 700;
                margin-bottom: 8px;
                letter-spacing: -0.5px;
            }}
            
            .header p {{
                font-size: 14px;
                opacity: 0.9;
                font-weight: 400;
            }}
            
            .info-banner {{
                background: linear-gradient(135deg, #e0e7ff 0%, #ede9fe 100%);
                padding: 16px 30px;
                display: flex;
                align-items: center;
                gap: 12px;
                border-bottom: 1px solid #e5e7eb;
            }}
            
            .info-icon {{
                width: 40px;
                height: 40px;
                background: white;
                border-radius: 10px;
                display: flex;
                align-items: center;
                justify-content: center;
                flex-shrink: 0;
                box-shadow: 0 2px 8px rgba(102, 126, 234, 0.2);
            }}
            
            .info-text {{
                font-size: 13px;
                line-height: 1.5;
                color: #4c1d95;
            }}
            
            .info-text strong {{
                display: block;
                color: #5b21b6;
                margin-bottom: 2px;
            }}
            
            .form-content {{
                padding: 40px 30px;
            }}
            
            .form-group {{
                margin-bottom: 24px;
            }}
            
            label {{
                display: block;
                font-size: 14px;
                font-weight: 600;
                color: #374151;
                margin-bottom: 8px;
            }}
            
            .required {{
                color: #ef4444;
                margin-left: 2px;
            }}
            
            .input-wrapper {{
                position: relative;
            }}
            
            input {{
                width: 100%;
                padding: 14px 16px;
                border: 2px solid #e5e7eb;
                border-radius: 10px;
                font-size: 15px;
                font-family: inherit;
                transition: all 0.2s ease;
                background: #f9fafb;
            }}
            
            input:focus {{
                outline: none;
                border-color: #667eea;
                background: white;
                box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.1);
            }}
            
            input:valid {{
                border-color: #10b981;
                background: white;
            }}
            
            input.error {{
                border-color: #ef4444;
                background: #fef2f2;
            }}
            
            .error-message {{
                display: none;
                color: #ef4444;
                font-size: 13px;
                margin-top: 6px;
                font-weight: 500;
            }}
            
            .error-message.show {{
                display: block;
            }}
            
            .input-hint {{
                font-size: 12px;
                color: #6b7280;
                margin-top: 6px;
            }}
            
            .submit-btn {{
                width: 100%;
                padding: 16px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border: none;
                border-radius: 12px;
                font-size: 16px;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.3s ease;
                box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
                margin-top: 10px;
            }}
            
            .submit-btn:hover:not(:disabled) {{
                transform: translateY(-2px);
                box-shadow: 0 6px 20px rgba(102, 126, 234, 0.5);
            }}
            
            .submit-btn:active:not(:disabled) {{
                transform: translateY(0);
            }}
            
            .submit-btn:disabled {{
                opacity: 0.7;
                cursor: not-allowed;
            }}
            
            .submit-btn.success {{
                background: linear-gradient(135deg, #10b981 0%, #059669 100%);
            }}
            
            .submit-btn.error {{
                background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
            }}
            
            .loader {{
                display: inline-block;
                width: 16px;
                height: 16px;
                border: 2px solid rgba(255, 255, 255, 0.3);
                border-top-color: white;
                border-radius: 50%;
                animation: spin 0.8s linear infinite;
                margin-right: 8px;
                vertical-align: middle;
            }}
            
            @keyframes spin {{
                to {{ transform: rotate(360deg); }}
            }}
            
            .footer {{
                text-align: center;
                padding: 20px 30px;
                background: #f9fafb;
                border-top: 1px solid #e5e7eb;
                font-size: 12px;
                color: #6b7280;
            }}
            
            .footer-icon {{
                display: inline-block;
                margin: 0 4px;
                font-size: 14px;
            }}
            
            @media (max-width: 600px) {{
                body {{
                    padding: 10px;
                }}
                
                .header {{
                    padding: 30px 20px;
                }}
                
                .form-content {{
                    padding: 30px 20px;
                }}
                
                .header h1 {{
                    font-size: 20px;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <div class="logo-container">
                    <div class="logo">
                        <img src="{context.get('bank_logo_url') or 'https://cdn-icons-png.flaticon.com/512/2830/2830284.png'}" alt="{context['bank_name']}">
                    </div>
                    <div class="connector-icon">🔗</div>
                    <div class="logo">
                        <img src="https://cdn-icons-png.flaticon.com/512/2702/2702702.png" alt="Product">
                    </div>
                </div>
                <h1>{context['product_name']}</h1>
                <p>Complete your application in minutes</p>
            </div>
            
            <div class="info-banner">
                <div class="info-icon">ℹ️</div>
                <div class="info-text">
                    <strong>Your Application Partner</strong>
                    {context['connector_name']} • {context['bank_name']}
                </div>
            </div>
            
            <div class="form-content">
                <form id="appForm" novalidate>
                    <div class="form-group">
                        <label for="name">Full Name <span class="required">*</span></label>
                        <div class="input-wrapper">
                            <input type="text" id="name" placeholder="Enter your full name" required autocomplete="name">
                            <div class="error-message" id="name-error">Please enter your full name</div>
                        </div>
                    </div>
                    
                    <div class="form-group">
                        <label for="phone">Phone Number <span class="required">*</span></label>
                        <div class="input-wrapper">
                            <input type="tel" id="phone" placeholder="10-digit mobile number" pattern="[0-9]{{10}}" required autocomplete="tel">
                            <div class="input-hint">We'll send OTP for verification</div>
                            <div class="error-message" id="phone-error">Please enter a valid 10-digit phone number</div>
                        </div>
                    </div>
                    
                    <div class="form-group">
                        <label for="email">Email Address <span class="required">*</span></label>
                        <div class="input-wrapper">
                            <input type="email" id="email" placeholder="your.email@example.com" required autocomplete="email">
                            <div class="error-message" id="email-error">Please enter a valid email address</div>
                        </div>
                    </div>
                    
                    <div class="form-group">
                        <label for="pan">PAN Number <span class="required">*</span></label>
                        <div class="input-wrapper">
                            <input type="text" id="pan" placeholder="ABCDE1234F" style="text-transform: uppercase" maxlength="10" pattern="[A-Z]{{5}}[0-9]{{4}}[A-Z]{{1}}" required autocomplete="off">
                            <div class="input-hint">Format: 5 letters, 4 digits, 1 letter (e.g., ABCDE1234F)</div>
                            <div class="error-message" id="pan-error">Please enter a valid PAN number</div>
                        </div>
                    </div>
                    
                    <button type="submit" class="submit-btn" id="submitBtn">
                        Submit Application
                    </button>
                </form>
            </div>
            
            <div class="footer">
                <span class="footer-icon">🔒</span> Secure & Encrypted <span class="footer-icon">•</span> Your data is safe with us
            </div>
        </div>

        <script>
            const form = document.getElementById('appForm');
            const submitBtn = document.getElementById('submitBtn');
            const inputs = {{
                name: document.getElementById('name'),
                phone: document.getElementById('phone'),
                email: document.getElementById('email'),
                pan: document.getElementById('pan')
            }};
            
            // PAN validation pattern
            const panPattern = /^[A-Z]{{5}}[0-9]{{4}}[A-Z]{{1}}$/;
            const phonePattern = /^[0-9]{{10}}$/;
            
            // Real-time validation
            Object.entries(inputs).forEach(([field, input]) => {{
                input.addEventListener('blur', () => validateField(field, input));
                input.addEventListener('input', () => {{
                    if (input.classList.contains('error')) {{
                        validateField(field, input);
                    }}
                }});
            }});
            
            function validateField(field, input) {{
                const errorMsg = document.getElementById(`${{field}}-error`);
                let isValid = true;
                
                if (!input.value.trim()) {{
                    isValid = false;
                    errorMsg.textContent = `Please enter your ${{field}}`;
                }} else if (field === 'pan' && !panPattern.test(input.value)) {{
                    isValid = false;
                    errorMsg.textContent = 'Invalid PAN format (e.g., ABCDE1234F)';
                }} else if (field === 'phone' && !phonePattern.test(input.value)) {{
                    isValid = false;
                    errorMsg.textContent = 'Please enter a valid 10-digit phone number';
                }} else if (field === 'email' && !input.validity.valid) {{
                    isValid = false;
                    errorMsg.textContent = 'Please enter a valid email address';
                }}
                
                if (isValid) {{
                    input.classList.remove('error');
                    errorMsg.classList.remove('show');
                }} else {{
                    input.classList.add('error');
                    errorMsg.classList.add('show');
                }}
                
                return isValid;
            }}
            
            function validateForm() {{
                let isValid = true;
                Object.entries(inputs).forEach(([field, input]) => {{
                    if (!validateField(field, input)) {{
                        isValid = false;
                    }}
                }});
                return isValid;
            }}
            
            form.addEventListener('submit', async function(e) {{
                e.preventDefault();
                
                if (!validateForm()) {{
                    return;
                }}
                
                submitBtn.disabled = true;
                submitBtn.innerHTML = '<span class="loader"></span>Processing...';
                
                const payload = {{
                    name: inputs.name.value.trim(),
                    phone: inputs.phone.value.trim(),
                    email: inputs.email.value.trim(),
                    pan: inputs.pan.value.toUpperCase().trim()
                }};
                
                try {{
                    const response = await fetch("{context['post_url']}", {{
                        method: 'POST',
                        headers: {{ 
                            'Content-Type': 'application/json',
                            'X-Requested-With': 'XMLHttpRequest'
                        }},
                        body: JSON.stringify(payload)
                    }});
                    
                    const data = await response.json();
                    
                    if (response.ok) {{
                        submitBtn.classList.add('success');
                        submitBtn.innerHTML = '✓ Success! Redirecting...';
                        
                        setTimeout(() => {{
                            window.location.href = data.redirect_url || "{context['redirect_url']}";
                        }}, 1500);
                    }} else {{
                        throw new Error(data.message || data.error || 'Submission failed');
                    }}
                }} catch (error) {{
                    submitBtn.disabled = false;
                    submitBtn.classList.add('error');
                    submitBtn.innerHTML = '✗ ' + error.message;
                    
                    setTimeout(() => {{
                        submitBtn.classList.remove('error');
                        submitBtn.innerHTML = 'Submit Application';
                    }}, 3000);
                }}
            }});
            
            // Prevent spaces in PAN and phone
            inputs.pan.addEventListener('keypress', (e) => {{
                if (e.key === ' ') e.preventDefault();
            }});
            inputs.phone.addEventListener('keypress', (e) => {{
                if (e.key === ' ' || isNaN(e.key)) e.preventDefault();
            }});
        </script>
    </body>
    </html>
    """