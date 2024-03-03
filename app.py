from flask import Flask, request, render_template_string
import random

app = Flask(__name__)

HTML_TEMPLATE = """
<!doctype html>
<html lang="en">
<head>
  <title>족보위원 선출 프로그램</title>
</head>
<body>
  <h1>족보위원 선출 프로그램</h1>
  <form method="post">
    <div>
      <label for="subject">과목 이름:</label>
      <input type="text" id="subject" name="subject" required>
    </div>
    <div>
      <label for="elements0">족보위원 횟수 0회 후보들 (공백으로 구분):</label>
      <input type="text" id="elements0" name="elements0" required>
    </div>
    <div>
      <label for="weight0">이 그룹의 가중치:</label>
      <input type="text" id="weight0" name="weight0" required>
    </div>
    <div>
      <label for="elements1">족보위원 횟수 1회 후보들 (공백으로 구분):</label>
      <input type="text" id="elements1" name="elements1" required>
    </div>
    <div>
      <label for="weight1">이 그룹의 가중치:</label>
      <input type="text" id="weight1" name="weight1" required>
    </div>
    <div>
      <label for="k">선출할 족보위원 수:</label>
      <input type="number" id="k" name="k" min="1" required>
    </div>
    <button type="submit">선출하기</button>
  </form>
  {% if selected_elements %}
  <h2>선출된 {{ subject }} 과목의 족보 위원</h2>
  <p>{{ selected_elements|join(', ') }}</p>
  {% endif %}
</body>
</html>
"""

def weighted_random_sample(elements, weights, k):
    weighted_elements = []
    for element_group, weight in zip(elements, weights):
        for element in element_group:
            weighted_elements += [element] * int(weight * 10)
    
    unique_elements = list(set(weighted_elements))
    
    if k <= len(unique_elements):
        return random.sample(unique_elements, k)
    else:
        return []

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        subject = request.form['subject']
        elements0 = request.form['elements0'].split()
        weight0 = float(request.form['weight0'])
        elements1 = request.form['elements1'].split()
        weight1 = float(request.form['weight1'])
        k = int(request.form['k'])
        
        elements = [elements0, elements1]
        weights = [weight0, weight1]
        
        selected_elements = weighted_random_sample(elements, weights, k)
        
        return render_template_string(HTML_TEMPLATE, selected_elements=selected_elements, subject=subject)
    return render_template_string(HTML_TEMPLATE, selected_elements=None)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
