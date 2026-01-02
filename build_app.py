
import json
import base64
import os

# Define paths
base_dir = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(base_dir, "students.json")
img_path = os.path.join(base_dir, "images", "Certificate.png")
js_path = os.path.join(base_dir, "script.js")

print("Reading student data...")
try:
    with open(json_path, "r") as f:
        students_data = json.load(f)
except Exception as e:
    print(f"Error reading students.json: {e}")
    exit(1)

print("Reading certificate image and converting to Base64...")
try:
    with open(img_path, "rb") as f:
        img_b64 = base64.b64encode(f.read()).decode("utf-8")
except Exception as e:
    print(f"Error reading Certificate.png: {e}")
    exit(1)

print("Generating script.js content...")
js_content = f"""document.addEventListener('DOMContentLoaded', () => {{
    const form = document.getElementById('certificateForm');
    const rollNoInput = document.getElementById('rollNo');
    const canvas = document.getElementById('certificateCanvas');
    const downloadLink = document.getElementById('downloadLink');
    const certificateResult = document.getElementById('certificateResult');
    const notRegisteredMessage = document.getElementById('notRegisteredMessage');
    const ctx = canvas.getContext('2d');

    // AUTO-GENERATED DATA FROM students.json
    // To update this, re-run the build_app.py script
    const studentsData = {json.dumps(students_data, indent=4)};

    console.log(`✓ Loaded ${{Object.keys(studentsData).length}} students from embedded data`);

    // Embedded Certificate Image (Base64) to avoid Tainted Canvas issues on local file execution
    const certificateTemplate = new Image();
    certificateTemplate.src = "data:image/png;base64,{img_b64}";

    certificateTemplate.onload = () => {{
        canvas.width = certificateTemplate.width;
        canvas.height = certificateTemplate.height;
        console.log("Certificate template loaded successfully");

        // QR Code Scanner Logic
        const btnScanQr = document.getElementById('btnScanQr');
        const readerDiv = document.getElementById('reader');
        let html5QrcodeScanner = null;

        btnScanQr.addEventListener('click', () => {{

            if (readerDiv.style.display === 'none') {{
                readerDiv.style.display = 'block';
                btnScanQr.textContent = 'Stop Scanning';

                html5QrcodeScanner = new Html5QrcodeScanner(
                    "reader",
                    {{
                        fps: 10,
                        qrbox: {{ width: 250, height: 250 }}
                    }},
                    false
                );

                html5QrcodeScanner.render(
                    (decodedText, decodedResult) => {{
                        console.log("QR Scanned:", decodedText);

                        // Stop scanner after success
                        html5QrcodeScanner.clear().then(() => {{
                            readerDiv.style.display = 'none';
                            btnScanQr.textContent = 'Scan QR Code';
                            html5QrcodeScanner = null;
                        }});

                        // Put QR data into input field
                        rollNoInput.value = decodedText.toUpperCase().trim();

                        // Auto-submit form
                        form.dispatchEvent(new Event('submit'));
                    }},
                    (errorMessage) => {{
                        // Ignore scan errors (continuous scanning)
                    }}
                );

            }} else {{
                // Manual stop
                if (html5QrcodeScanner) {{
                    html5QrcodeScanner.clear().then(() => {{
                        readerDiv.style.display = 'none';
                        btnScanQr.textContent = 'Scan QR Code';
                        html5QrcodeScanner = null;
                    }});
                }}
            }}
        }});

        form.addEventListener('submit', (e) => {{
            e.preventDefault();

            const rollNo = rollNoInput.value.toUpperCase().trim();
            console.log(`Searching for roll number: ${{rollNo}}`);
            const name = studentsData[rollNo];

            certificateResult.style.display = 'none';
            notRegisteredMessage.style.display = 'none';

            if (name) {{
                console.log(`Found student: ${{name}}`);
                ctx.clearRect(0, 0, canvas.width, canvas.height);
                ctx.drawImage(certificateTemplate, 0, 0);

                // Set up the font with Google Sans
                ctx.font = 'bold 130px "Google Sans", Roboto, Arial, sans-serif';
                ctx.fillStyle = '#000';  // Assuming black color
                ctx.textAlign = 'center';
                ctx.textBaseline = 'middle';

                const textX = canvas.width / 2;
                // DROPPING THE NAME BY 55 PIXELS (Relative to previous logic)
                // Original logic: canvas.height * 0.45 + 135
                const textY = canvas.height * 0.45 + 135;

                ctx.fillText(name, textX, textY);

                // Convert canvas to blob for download
                try {{
                    canvas.toBlob((blob) => {{
                        if (!blob) {{
                            console.error("Canvas toBlob failed");
                            alert("Error generating certificate image.");
                            return;
                        }}
                        const url = URL.createObjectURL(blob);
                        downloadLink.href = url;
                        downloadLink.download = `PIXELX_Certificate_${{name.replace(/\\s+/g, '_')}}.png`;
                        
                        // Clean up object URL after click
                        downloadLink.onclick = () => {{
                            setTimeout(() => URL.revokeObjectURL(url), 100);
                        }};
                        
                        downloadLink.style.display = 'inline-block';
                        certificateResult.style.display = 'block';
                        console.log("Certificate generated and ready for download");
                    }}, 'image/png');
                }} catch (err) {{
                    console.error("Error in toBlob:", err);
                    alert("Security Error: Unable to export certificate. If running locally, please use a local server or the provided build script.");
                }}

            }} else {{
                console.log("Roll number not found");
                notRegisteredMessage.style.display = 'block';
            }}
        }});
    }};
    
    certificateTemplate.onerror = (e) => {{
        console.error("Error loading certificate template image", e);
        alert("Failed to load certificate template.");
    }};
}});
"""

try:
    with open(js_path, "w", encoding="utf-8") as f:
        f.write(js_content)
    print(f"Successfully wrote updated script.js to {js_path}")
except Exception as e:
    print(f"Error writing script.js: {e}")
