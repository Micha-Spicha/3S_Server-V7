from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

categories = {}
judges = []
all_results = {}  # Хранилище для всех введенных результатов

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scoring')
def goto_ms_calc():
    return redirect('http://192.168.1.44:55807')  # URL MS Calc Server

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    global categories, judges
    if request.method == 'POST':
        if 'add_category' in request.form:
            category = request.form['category']
            dances = [dance.strip() for dance in request.form['dances'].split(',')]
            pairs = [pair.strip() for pair in request.form['pairs'].split(',')]
            judges = [judge.strip() for judge in request.form['judges'].split(',')]
            categories[category] = {'dances': dances, 'pairs': pairs, 'judges': judges}
        elif 'delete_category' in request.form:
            category_to_delete = request.form['category']
            if category_to_delete in categories:
                del categories[category_to_delete]
    return render_template('admin.html', categories=categories.keys())

@app.route('/calc', methods=['GET', 'POST'])
def calc():
    selected_category = request.args.get('category')
    results = {}

    if request.method == 'POST' and selected_category:
        details = categories[selected_category]
        for dance in details['dances']:
            results[dance] = {}
            for pair in details['pairs']:
                scores = []
                for judge in details['judges']:
                    score = int(request.form[f'{selected_category}_{dance}_{pair}_{judge}'])
                    scores.append(score)
                average_score = sum(scores) / len(scores)
                results[dance][pair] = {'score': round(average_score, 2)}

        overall_results = {}
        for pair in details['pairs']:
            total_scores = []
            for dance in details['dances']:
                total_scores.append(results[dance][pair]['score'])
            overall_score = sum(total_scores) / len(total_scores)
            overall_results[pair] = {'score': round(overall_score, 2)}

        sorted_pairs = sorted(overall_results.items(), key=lambda item: item[1]['score'], reverse=True)
        for i, (pair, data) in enumerate(sorted_pairs):
            if data['score'] >= 3:
                data['place'] = 1
            elif 2 <= data['score'] < 3:
                data['place'] = 2
            else:
                data['place'] = 3
        results['overall'] = overall_results

        # Сохраняем результаты в хранилище
        all_results[selected_category] = results

    return render_template('calc.html', categories=categories.keys(), selected_category=selected_category, details=categories.get(selected_category), results=results)

@app.route('/all_results')
def all_results_view():
    return render_template('all_results.html', all_results=all_results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
