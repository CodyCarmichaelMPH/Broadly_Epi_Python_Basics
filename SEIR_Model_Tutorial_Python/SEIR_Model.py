# Import necessary packages
import numpy as np
from scipy.integrate import odeint
import plotly.graph_objects as go

# Define the SEIR model
def seir_model(variables, time, N, beta, gamma, sigma):
    S, E, I, R = variables
    dSdt = -beta * S * I / N
    dEdt = beta * S * I / N - sigma * E
    dIdt = sigma * E - gamma * I
    dRdt = gamma * I
    return [dSdt, dEdt, dIdt, dRdt]

# Set initial conditions and parameters
N = 1000  # Total population
initial_conditions = [999, 0, 1, 0]  # S, E, I, R
beta = 0.5  # Contact rate
gamma = 0.1  # Mean recovery rate
sigma = 1/5  # Rate of incubation (assuming a 5 day incubation period)
times = np.arange(0, 51, 1)  # Time from 0 to 50 days

# Solve the SEIR model
seir_solution = odeint(seir_model, initial_conditions, times, args=(N, beta, gamma, sigma))

# Plot the results with Plotly
fig = go.Figure()

# Susceptible
fig.add_trace(go.Scatter(x=times, y=seir_solution[:, 0], mode='lines', name='Susceptible', line=dict(color='blue')))
# Exposed
fig.add_trace(go.Scatter(x=times, y=seir_solution[:, 1], mode='lines', name='Exposed', line=dict(color='orange')))
# Infected
fig.add_trace(go.Scatter(x=times, y=seir_solution[:, 2], mode='lines', name='Infected', line=dict(color='red')))
# Recovered
fig.add_trace(go.Scatter(x=times, y=seir_solution[:, 3], mode='lines', name='Recovered', line=dict(color='green')))

# Update layout
fig.update_layout(title='SEIR Model Simulation',
                  xaxis_title='Time',
                  yaxis_title='Population')

fig.show()
