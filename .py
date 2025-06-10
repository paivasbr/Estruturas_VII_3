import numpy as np
import matplotlib.pyplot as plt

# === PARÂMETROS DO PROBLEMA ===
E0 = 100        # Módulo de Elasticidade
S = 1           # Área da seção transversal
L = 1.0         # Comprimento total da barra
rho = 1.0       # Densidade
n_elems = 2     # Número de elementos
n_nodes = 3     # 2 elementos → 3 nós
L_elem = L / n_elems  # Comprimento de cada elemento
Pmax = 10.0
dt = 0.01
t_total = 0.2
gamma = 0.5
beta = 0.25

# === MATRIZES DE MASSA E RIGIDEZ ===
def element_stiffness(E, A, L):
    return (E * A / L) * np.array([[1, -1], [-1, 1]])

def element_mass(rho, A, L):
    return (rho * A * L / 6.0) * np.array([[2, 1], [1, 2]])

K_global = np.zeros((n_nodes, n_nodes))
M_global = np.zeros((n_nodes, n_nodes))

# Montagem das matrizes globais
for e in range(n_elems):
    k_e = element_stiffness(E0, S, L_elem)
    m_e = element_mass(rho, S, L_elem)
    dof = [e, e + 1]
    for i in range(2):
        for j in range(2):
            K_global[dof[i], dof[j]] += k_e[i, j]
            M_global[dof[i], dof[j]] += m_e[i, j]

# === CONDIÇÕES DE CONTORNO E INICIAIS ===
free_dofs = [1, 2]  # Nó 0 fixo
K = K_global[np.ix_(free_dofs, free_dofs)]
M = M_global[np.ix_(free_dofs, free_dofs)]

u = np.zeros((2, int(t_total / dt) + 1))  # Deslocamento
v = np.zeros_like(u)                      # Velocidade
a = np.zeros_like(u)                      # Aceleração
a[:, 0] = np.linalg.solve(M, -K @ u[:, 0])

# === NEWMARK IMPLÍCITO (LINEAR) ===
K_eff = M + beta * dt**2 * K
K_eff_inv = np.linalg.inv(K_eff)

# Carregamento de impacto (como em sala)
force = np.zeros_like(u)
for i in range(force.shape[1]):
    t = i * dt
    if t <= 0.02:
        force[-1, i] = Pmax * (t / 0.02)
    else:
        force[-1, i] = 0.0

# Iteração no tempo
for i in range(u.shape[1] - 1):
    f_eff = (force[:, i + 1] +
             M @ (u[:, i] / (beta * dt**2) +
                  v[:, i] / (beta * dt) +
                  a[:, i] * (1 / (2 * beta) - 1)) +
             K @ (u[:, i] + dt * v[:, i] + dt**2 * (0.5 - beta) * a[:, i]))

    u[:, i + 1] = K_eff_inv @ f_eff
    a[:, i + 1] = (u[:, i + 1] - u[:, i]) / (beta * dt**2) - v[:, i] / (beta * dt) - a[:, i] * (1 / (2 * beta) - 1)
    v[:, i + 1] = v[:, i] + dt * ((1 - gamma) * a[:, i] + gamma * a[:, i + 1])

# === PLOTAGEM DOS RESULTADOS ===
time = np.linspace(0, t_total, u.shape[1])
plt.figure(figsize=(10, 5))
plt.plot(time, u[1, :], label="Deslocamento no nó 2 (extremidade)")
plt.xlabel("Tempo [s]")
plt.ylabel("Deslocamento [u]")
plt.title("Resposta Dinâmica Linear com 2 Elementos Finitos")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
