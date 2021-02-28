import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
t = np.arange(0,2*np.pi,0.001)
y=2*t+9*np.exp(-t/5)-9

sns.reset_defaults()
sns.set(
    rc={'figure.figsize':(7,5)},
    style="dark"
)
sns.color_palette('tab10')

sns.lineplot(x=t,y=y)

plt.grid()
plt.xlabel('t')
plt.ylabel('$y(t)$')
plt.title("Punto 7")
plt.show()