from flask import Flask, request, render_template

app = Flask(__name__)

# Cutoff values
initial_treatment_cutoff = 4
sodium_cutoff = 133
bilirubin_cutoff = 0.5
n_lr_cutoff = 2.6

def calculate_shizuoka_score(patient):
    score = 0
    if patient["initial_treatment_days"] < initial_treatment_cutoff:
        score += 1
    if patient["sodium_level"] < sodium_cutoff:
        score += 1
    if patient["total_bilirubin"] >= bilirubin_cutoff:
        score += 1
    if patient["neutrophil_to_lymphocyte_ratio"] >= n_lr_cutoff:
        score += 1
    return score

def is_high_risk_ivig_non_responder(score):
    return score >= 2

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        initial_treatment_days = int(request.form['initial_treatment_days'])
        sodium_level = float(request.form['sodium_level'])
        total_bilirubin = float(request.form['total_bilirubin'])
        n_lr = float(request.form['n_lr'])

        patient = {
            "name": name,
            "initial_treatment_days": initial_treatment_days,
            "sodium_level": sodium_level,
            "total_bilirubin": total_bilirubin,
            "neutrophil_to_lymphocyte_ratio": n_lr
        }

        score = calculate_shizuoka_score(patient)
        high_risk = is_high_risk_ivig_non_responder(score)
        
        return render_template('index.html', score=score, high_risk=high_risk, patient=patient)
    
    return render_template('index.html', score=None)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)
