from flask import Flask, request, jsonify, render_template
import pandas as pd

app = Flask(__name__)

# Load Excel once
df = pd.read_excel("Sample Work File.xlsx")
df['Month'] = pd.to_datetime(df['Date']).dt.strftime('%B')  # Extract month name

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/ask', methods=['POST'])
def ask():
    prompt = request.json.get("prompt", "").lower()

    months = ['january', 'february', 'march', 'april', 'may', 'june', 'july',
              'august', 'september', 'october', 'november', 'december']
    matched_months = [m.capitalize() for m in months if m in prompt]

    if matched_months:
        result = df[df['Month'].isin(matched_months)]['Sale Amount'].sum()
        return jsonify({"answer": f"Total sales in {', '.join(matched_months)}: {result}"})

    for name in df['Sold by'].unique():
        if name.lower() in prompt:
            result = df[df['Sold by'].str.lower() == name.lower()]['Sale Amount'].sum()
            return jsonify({"answer": f"Total sales by {name}: {result}"})

    return jsonify({"answer": "Couldn't understand your prompt. Try asking about month or name."})

if __name__ == '__main__':
    app.run(debug=True)
