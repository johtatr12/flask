from flask import Flask, request, render_template_string, redirect, url_for
import random

app = Flask(__name__)

# 선출된 족보위원을 저장할 전역 변수
selected_members = []

HTML_TEMPLATE = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>족보위원 선출 프로그램</title>
  <style>
    body {
      font-family: 'Arial', sans-serif;
      margin: 0;
      padding: 0;
      display: flex;
      justify-content: center;
      align-items: center;
      flex-direction: column;
      min-height: 100vh;
      background-color: #f0f0f0;
    }
    .container {
      width: 80%;
      max-width: 600px;
      background-color: #fff;
      padding: 20px;
      box-shadow: 0 0 10px rgba(0,0,0,0.1);
      border-radius: 8px;
    }
    h1, h2 {
      text-align: center;
    }
    form > div {
      margin-bottom: 15px;
    }
    label {
      display: block;
      margin-bottom: 5px;
      font-size: 1.2rem;
    }
    input, button {
      width: 100%;
      padding: 10px;
      margin-top: 5px;
      box-sizing: border-box;
      font-size: 1.1rem;
    }
    table {
      width: 100%;
      border-collapse: collapse;
      margin-top: 20px;
    }
    th, td {
      text-align: left;
      padding: 8px;
      border: 1px solid #ddd;
      font-size: 1.1rem;
    }
    th {
      background-color: #f2f2f2;
    }
    button {
      background-color: #4CAF50;
      color: white;
      border: none;
      cursor: pointer;
    }
    button:hover {
      opacity: 0.8;
    }
  </style>
</head>
<body>
  <div class="container">
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
      <button type="submit" name="action" value="select">선출하기</button>
      <button type="submit" name="action" value="reset">초기화</button>
    </form>
    {% if selected_elements %}
    <h2>선출된 {{ subject }} 과목의 족보 위원</h2>
    <p>{{ selected_elements|join(', ') }}</p>
    {% endif %}
    {% if selected_members %}
    <h2>누적 선출된 족보위원 목록</h2>
    <table>
      <tr>
        <th>과목</th>
        <th>족보위원</th>
      </tr>
      {% for member in selected_members %}
      <tr>
        <td>{{ member[0] }}</td>
        <td>{{ member[1]|join(', ') }}</td>
      </tr>
      {% endfor %}
    </table>
    {% endif %}
  </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def home():
    global selected_members
    if request.method == 'POST':
        action = request.form['action']
        if action == 'select':
            subject = request.form['subject']
            elements0 = request.form['elements0'].split()
            weight0 = float(request.form['weight0'])
            elements1 = request.form['elements1'].split()
            weight1 = float(request.form['weight1'])
            k = int(request.form['k'])
            
            elements = [elements0, elements1]
            weights = [weight0, weight1]
            
            selected_elements = weighted_random_sample(elements, weights, k)
            selected_members.append((subject, selected_elements))
            
            return render_template_string(HTML_TEMPLATE, selected_elements=selected_elements, subject=subject, selected_members=selected_members)
        elif action == 'reset':
            selected_members = []  # 누적된 목록을 초기화
            return redirect(url_for('home'))
    return render_template_string(HTML_TEMPLATE, selected_elements=None, selected_members=selected_members)

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
      

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
