from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Инициализация глобальных переменных
categories = {}
dance_list = {}
pair_list = {}
judge_list = {}
scores_data = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        if 'add_category' in request.form:
            category = request.form.get('category')
            dances = [dance.strip() for dance in request.form.get('dances').split(',') if dance.strip()]
            pairs = [pair.strip() for pair in request.form.get('pairs').split(',') if pair.strip()]
            judges = [judge.strip() for judge in request.form.get('judges').split(',') if judge.strip()]

            if category and dances and pairs and judges:
                categories[category] = {
                    'dances': dances,
                    'pairs': pairs,
                    'judges': judges
                }
                scores_data[category] = {judge: {pair: {dance: '' for dance in dances} for pair in pairs} for judge in judges}
                print(f"Added category: {category}, dances: {dances}, pairs: {pairs}, judges: {judges}")

        elif 'delete_category' in request.form:
            category = request.form.get('category')
            if category in categories:
                del categories[category]
                del scores_data[category]
                print(f"Deleted category: {category}")

    return render_template('admin.html', categories=categories)

@app.route('/judging', methods=['GET', 'POST'])
def judging():
    selected_category = None
    selected_letter = None
    if request.method == 'POST':
        if 'selected_category' in request.form:
            selected_category = request.form.get('selected_category')
        if 'selected_letter' in request.form:
            selected_letter = request.form.get('selected_letter')
        if 'save_scores' in request.form:
            selected_category = request.form.get('selected_category')
            selected_letter = request.form.get('selected_letter')
            if selected_category and selected_letter:
                for pair in categories[selected_category]['pairs']:
                    for dance in categories[selected_category]['dances']:
                        score = request.form.get(f'score_{selected_category}_{pair}_{dance}')
                        if score is not None:
                            if selected_category not in scores_data:
                                scores_data[selected_category] = {}
                            if selected_letter not in scores_data[selected_category]:
                                scores_data[selected_category][selected_letter] = {}
                            if pair not in scores_data[selected_category][selected_letter]:
                                scores_data[selected_category][selected_letter][pair] = {}
                            scores_data[selected_category][selected_letter][pair][dance] = score
                            print(f"Score for category {selected_category}, judge {selected_letter}, pair {pair}, dance {dance}: {score}")

    return render_template('judging.html', categories=categories, scores=scores_data, selected_category=selected_category, selected_letter=selected_letter)

@app.route('/results')
def results():
    return render_template('results.html', scores_data=scores_data, categories=categories)
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=55807, debug=True)
  