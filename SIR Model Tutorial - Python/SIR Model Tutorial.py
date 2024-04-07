# Import necessary packages
import numpy as np
from scipy.integrate import odeint
import plotly.graph_objects as go

# Define the SIR model
def sir_model(variables, time, N, beta, gamma):
    S, I, R = variables
    dSdt = -beta * S * I / N
    dIdt = beta * S * I / N - gamma * I
    dRdt = gamma * I
    return [dSdt, dIdt, dRdt]

# Set initial conditions and parameters
N = 1000  # Total population
initial_conditions = [999, 1, 0]  # S, I, R
beta = 0.3  # Contact rate
gamma = 0.1  # Mean recovery rate
times = np.arange(0, 51, 1)  # Time from 0 to 50 days

# Solve the SIR model
sir_solution = odeint(sir_model, initial_conditions, times, args=(N, beta, gamma))

# Plot the results with Plotly
fig = go.Figure()

# Susceptible
fig.add_trace(go.Scatter(x=times, y=sir_solution[:, 0], mode='lines', name='Susceptible', line=dict(color='blue')))
# Infected
fig.add_trace(go.Scatter(x=times, y=sir_solution[:, 1], mode='lines', name='Infected', line=dict(color='red')))
# Recovered
fig.add_trace(go.Scatter(x=times, y=sir_solution[:, 2], mode='lines', name='Recovered', line=dict(color='green')))

# Update layout
fig.update_layout(title='SIR Model Simulation',
                  xaxis_title='Time',
                  yaxis_title='Population')

fig.show()
