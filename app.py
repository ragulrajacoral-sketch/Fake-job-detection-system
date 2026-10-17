from flask import Flask, render_template, request
import re

app = Flask(__name__)

RED_FLAGS = [
    (r"\b(pay|paying)\s+(a\s+)?(registration|training|security|verification|processing)\s+fee\b", 25,
     "Requests a registration, training, security, verification, or processing fee."),
    (r"\b(guaranteed job|guaranteed placement|100% placement)\b", 12,
     "Promises a guaranteed job or placement."),
    (r"\b(urgent hiring|hire immediately|no interview|without interview)\b", 10,
     "Uses pressure tactics or claims hiring without a normal interview."),
    (r"\b(whatsapp|telegram)\b", 5,
     "Moves recruitment communication to a messaging app; verify the contact independently."),
    (r"\b(crypto|cryptocurrency|bitcoin|investment scheme)\b", 12,
     "Mentions cryptocurrency or an investment scheme in a job context."),
    (r"\b(earn\s+\$?\d[\d,]*\s*(per|a)\s*(day|week|hour)|easy money|get rich quick)\b", 10,
     "Makes an unusually easy or high-earnings claim."),
    (r"\b(bank password|otp|one.time password|cvv|gift card)\b", 30,
     "Requests highly sensitive credentials or payment instruments."),
    (r"\b(no experience required|work from home)\b", 3,
     "Broad work-from-home or no-experience wording; this alone is not proof of fraud."),
    (r"\b(gmail\.com|yahoo\.com|outlook\.com)\b", 5,
     "Uses a generic email provider rather than a clearly verified company domain."),
    (r"\b(send money|transfer money|buy equipment from us|purchase equipment)\b", 20,
     "Asks the applicant to send money or buy equipment through the recruiter."),
]

def assess_job(text):
    score = 0
    reasons = []
    lower = text.lower()
    for pattern, points, explanation in RED_FLAGS:
        if re.search(pattern, lower):
            score += points
            reasons.append({"text": explanation, "points": points})

    # A few weak context checks. Missing details are a reason to verify, not proof of fraud.
    if not re.search(r"\b(company|inc\.|ltd\.|limited|llc|corporation|pvt\.?)\b", lower):
        score += 5
        reasons.append({"text": "No clear company legal name was detected; verify who is hiring.", "points": 5})
    if not re.search(r"\b(interview|qualification|experience|responsibilit|requirement)\b", lower):
        score += 5
        reasons.append({"text": "The description may lack normal role or hiring details.", "points": 5})

    score = min(score, 100)
    if score >= 50:
        level, label = "high", "High risk indicators"
    elif score >= 25:
        level, label = "medium", "Some risk indicators"
    else:
        level, label = "low", "Few risk indicators detected"

    if not reasons:
        reasons.append({"text": "No listed warning patterns were detected. This does not verify the job is genuine.", "points": 0})

    return {"score": score, "level": level, "label": label, "reasons": reasons}


@app.route("/", methods=["GET", "POST"])
def index():
    text = ""
    result = None
    if request.method == "POST":
        text = request.form.get("job_text", "").strip()
        if text:
            result = assess_job(text)
        else:
            result = {"error": "Paste a job description or recruiter message to analyze."}
    return render_template("index.html", job_text=text, result=result)


if __name__ == "__main__":
    app.run(debug=True)
