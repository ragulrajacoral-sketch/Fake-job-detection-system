# Fake Job Detection System

A beginner-friendly Flask web app that screens job descriptions and recruiter messages for common scam warning signs.

## Features
- Paste a job advertisement or recruiter message
- Checks for common red flags such as upfront fees, requests for OTPs/passwords, pressure tactics, and money transfers
- Displays a risk-indicator score and explains each matched warning sign
- Responsive interface for desktop and mobile

## Important limitations
This starter uses transparent keyword and pattern rules. It is **not an AI model**, does not confirm whether a job is real or fake, and may produce false positives or miss scams. A low score does not mean a job is safe. Always verify the company through its independently located official website and never share OTPs, passwords, banking credentials, or money with an unverified recruiter.

## Requirements
- Python 3.10 or newer

## Run on Windows
```powershell
py -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python app.py
```

## Run on macOS/Linux
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000 in your browser. Paste a job description and select **Analyze job**.

## Project structure
```text
fake-job-detection-system/
├── app.py
├── requirements.txt
├── README.md
├── LICENSE
├── .gitignore
├── templates/
│   └── index.html
└── static/
    └── style.css
```

## How the score works
Each matching pattern adds a weighted number of points. The final score is capped at 100 and grouped into low, medium, or high risk indicators. These categories indicate warning patterns only, not a verified fraud probability. See `RED_FLAGS` and `assess_job()` in `app.py`.

## Future improvements
- Train and evaluate an ML model on a properly sourced, labeled dataset
- Add model evaluation metrics and explainability
- Detect suspicious email domains and check verified company sources
- Support CSV batch analysis
- Add tests and multilingual support

## Privacy
Text is analyzed locally by this app and is not sent to an external AI service. Avoid pasting personal information into demos you do not control.

## License
MIT. See `LICENSE`.
