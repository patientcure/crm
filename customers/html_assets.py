
def get_onboarding_html(context):
    """
    Returns the HTML string with dynamic data injected.
    Expects 'context' to be a dict with:
    - product_name
    - bank_name
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
        <title>Application for {context['product_name']}</title>
        <style>
            body {{ font-family: sans-serif; background: #f3f4f6; padding: 20px; display: flex; justify-content: center; }}
            .card {{ background: white; padding: 30px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); width: 100%; max-width: 450px; }}
            .header {{ text-align: center; margin-bottom: 20px; }}
            .logos {{ display: flex; justify-content: space-around; margin-bottom: 20px; }}
            .logos img {{ height: 40px; }}
            .info-box {{ background: #eff6ff; padding: 10px; border-radius: 6px; font-size: 0.9em; margin-bottom: 20px; }}
            label {{ display: block; margin-top: 10px; font-weight: bold; font-size: 0.9rem; }}
            input {{ width: 100%; padding: 10px; margin-top: 5px; border: 1px solid #ccc; border-radius: 6px; box-sizing: border-box; }}
            button {{ width: 100%; background: #2563eb; color: white; padding: 12px; border: none; border-radius: 6px; margin-top: 20px; cursor: pointer; font-size: 1rem; }}
            button:hover {{ background: #1d4ed8; }}
            .error {{ color: red; font-size: 0.8rem; display: none; margin-top: 5px; }}
        </style>
    </head>
    <body>
        <div class="card">
            <div class="header">
                <div class="logos">
                    <img src="https://cdn-icons-png.flaticon.com/512/2702/2702702.png" alt="App">
                    <img src="https://cdn-icons-png.flaticon.com/512/2830/2830284.png" alt="Bank">
                </div>
                <h2>{context['product_name']}</h2>
            </div>

            <div class="info-box">
                <strong>Connector:</strong> {context['connector_name']}<br>
                <strong>Bank:</strong> {context['bank_name']}
            </div>

            <form id="appForm">
                <label>Full Name</label>
                <input type="text" id="name" required>

                <label>Phone</label>
                <input type="tel" id="phone" pattern="[0-9]{{10}}" required>

                <label>Email</label>
                <input type="email" id="email" required>

                <label>PAN Number</label>
                <input type="text" id="pan" style="text-transform: uppercase" maxlength="10" required>
                <div id="error-msg" class="error"></div>

                <button type="submit" id="btn">Submit Application</button>
            </form>
        </div>

        <script>
            document.getElementById('appForm').addEventListener('submit', async function(e) {{
                e.preventDefault();
                const btn = document.getElementById('btn');
                const err = document.getElementById('error-msg');
                
                btn.disabled = true;
                btn.innerText = "Processing...";
                err.style.display = 'none';

                const payload = {{
                    name: document.getElementById('name').value,
                    phone: document.getElementById('phone').value,
                    email: document.getElementById('email').value,
                    pan: document.getElementById('pan').value.toUpperCase()
                }};

                try {{
                    const response = await fetch("{context['post_url']}", {{
                        method: 'POST',
                        headers: {{ 'Content-Type': 'application/json' }},
                        body: JSON.stringify(payload)
                    }});
                    
                    const data = await response.json();

                    if (response.ok) {{
                        btn.style.backgroundColor = "green";
                        btn.innerText = "Success! Redirecting...";
                        setTimeout(() => {{
                            window.location.href = data.redirect_url; 
                        }}, 1500);
                    }} else {{
                        throw new Error(JSON.stringify(data));
                    }}
                }} catch (error) {{
                    btn.disabled = false;
                    btn.innerText = "Submit Application";
                    err.innerText = "Error: " + error.message;
                    err.style.display = 'block';
                }}
            }});
        </script>
    </body>
    </html>
    """