from flask import Flask, request, render_template, redirect, url_for
import pandas as pd
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return '''
        <h2>Upload Excel File</h2>
        <form method="POST" action="/analyze" enctype="multipart/form-data">
            <input type="file" name="excel_file" required>
            <br><br>
            <input type="submit" value="Upload & Analyze">
        </form>
    '''

@app.route('/analyze', methods=['POST'])
def analyze():
    file = request.files.get('excel_file')

    if not file:
        return "No file uploaded."

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)

    try:
        df = pd.read_excel(filepath)

        # Example Analysis: Show top 5 rows and total sale amount
        preview = df.head().to_html(index=False)
        total_sales = df['Sale Amount'].sum()

        return f"""
            <h2>Analysis Results</h2>
            <p><strong>Total Sale Amount:</strong> {total_sales}</p>
            <h3>File Preview:</h3>
            {preview}
            <br><a href="/">Upload another file</a>
        """

    except Exception as e:
        return f"Error reading Excel file: {e}"

if __name__ == '__main__':
    app.run(debug=True)
