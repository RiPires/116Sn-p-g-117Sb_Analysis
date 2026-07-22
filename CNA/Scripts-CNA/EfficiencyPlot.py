import uproot
import matplotlib.pyplot as plt

# 1. Carregar os ficheiros
f8 = uproot.open("HPGe_8mm.root")
f50 = uproot.open("HPGe_50mm.root")
f100 = uproot.open("HPGe_100mm.root")

# Função auxiliar ajustada para converter MeV -> keV
def get_xy(obj):
    # Caso seja TGraph
    if hasattr(obj, "values") and callable(obj.values):
        try:
            x = obj.values("x") * 1000.0  # Converte MeV para keV
            y = obj.values("y")
            return x, y
        except TypeError:
            pass
    
    # Caso seja TH1 (Histograma)
    y = obj.values()
    edges = obj.axis().edges()
    x = ((edges[:-1] + edges[1:]) / 2.0) * 1000.0  # Converte MeV para keV
    return x, y

x8, y8 = get_xy(f8["curva_eficiencia"])
x50, y50 = get_xy(f50["curva_eficiencia"])
x100, y100 = get_xy(f100["curva_eficiencia"])

# 2. Dados Experimentais (já em keV e %)
exp_8mm = {80.5: 4.796, 276.0: 3.714e-01, 1110.5: 2.338e-01}
exp_50mm = {121.0: 1.011, 243.5: 1.708, 276.0: 1.318e-01, 1172.0: 5.0e-02}
exp_100mm = {121.0: 3.483e-01, 243.5: 6.419e-01, 276.0: 4.870e-02}

# 3. Criar a Figura
plt.figure(figsize=(10, 6))

# --- Curvas de Simulação (Linhas) ---
plt.plot(x8, y8, color='blue', linestyle='-', linewidth=1.5, label='Sim. 8 mm')
plt.plot(x50, y50, color='red', linestyle='-', linewidth=1.5, label='Sim. 50 mm')
plt.plot(x100, y100, color='green', linestyle='-', linewidth=1.5, label='Sim. 100 mm')

# --- Pontos Experimentais (Marcadores) ---
plt.scatter(exp_8mm.keys(), exp_8mm.values(), color='blue', label='Exp. 8 mm', marker='o', s=60, zorder=5)
plt.scatter(exp_50mm.keys(), exp_50mm.values(), color='red', label='Exp. 50 mm', marker='s', s=60, zorder=5)
plt.scatter(exp_100mm.keys(), exp_100mm.values(), color='green', label='Exp. 100 mm', marker='^', s=60, zorder=5)

# --- Configurações do Gráfico ---
plt.xlabel('Energia (keV)', fontsize=12)
plt.ylabel('Eficiência Absoluta (%)', fontsize=12)
plt.title('Eficiência Absoluta HPGe (Simulação vs. Experimental)', fontsize=14)
plt.grid(True, which="both", ls="--", alpha=0.5)
plt.legend(fontsize=10, loc='best')

plt.tight_layout()
plt.show()