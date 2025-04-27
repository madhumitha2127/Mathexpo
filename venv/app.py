from flask import Flask, render_template, request
import sympy as sp

app = Flask(__name__)

# Function to parse and evaluate the user-inputted differential equation
def f(x, y, equation):
    y_sym = sp.symbols('y')
    x_sym = sp.symbols('x')
    eq = sp.sympify(equation)
    result = eq.subs({x_sym: x, y_sym: y})
    return result

# Adams-Bashforth method for prediction
def adams_bashforth_2_step(x_values, y_values, h, equation):
    fn = f(x_values[-1], y_values[-1], equation)
    fn_minus_1 = f(x_values[-2], y_values[-2], equation)
    y_next = y_values[-1] + (h / 2) * (3 * fn - fn_minus_1)
    return y_next

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get the user input
        equation = request.form['equation']
        n = int(request.form['num_points'])
        x_values = [float(request.form[f'x{i+1}']) for i in range(n)]
        y_values = [float(request.form[f'y{i+1}']) for i in range(n)]
        h = float(request.form['step_size'])
        target_x = float(request.form['target_x'])
        
        # Calculate the number of steps to reach the target x-value
        steps_needed = int((target_x - x_values[-1]) / h)
        
        # Predict the value of y for the given target_x using Adams-Bashforth method
        predicted_value = y_values[-1]
        for i in range(steps_needed):
            predicted_value = adams_bashforth_2_step(x_values, y_values, h, equation)
            x_values.append(x_values[-1] + h)
            y_values.append(predicted_value)
        
        # Format the predicted value to 3 decimal places
        predicted_value = round(predicted_value, 3)
        
        return render_template('index.html', predicted_value=predicted_value, target_x=target_x)
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
