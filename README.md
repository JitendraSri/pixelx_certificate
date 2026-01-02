# DEPLOYX Certificate Portal

## How to Run
This application is designed to run entirely locally in your browser.

1.  **Open the Application**:
    - Locate the `index.html` file in this folder.
    - Double-click it or right-click and select **Open with Google Chrome** (or Edge/Firefox).
    - The app will load with the floating background, sponsor logos, and QR scanner ready to use.

## How to Update Data
The student data and certificate template are **embedded** into `script.js` to allow the app to work without a web server. If you change the source data, you must rebuild the script.

1.  **Update Source Files**:
    - Modify `students.json` with new student data.
    - Start or replace `images/Certificate.png` if needed.
2.  **Run Build Script**:
    - Open a terminal/command prompt in this folder.
    - Run the following command:
      ```powershell
      python build_app.py
      ```
    - This will update `script.js`.
3.  **Refresh**: Refresh `index.html` in your browser to see the changes.
