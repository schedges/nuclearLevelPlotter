import matplotlib.pyplot as plt
import sys
import numpy as np

inpFilename=sys.argv[1]

#Get base name
basename=inpFilename[inpFilename.rfind("/")+1:inpFilename.find(".")]
print(basename)

conversion=0.308

energies=[]
bgts=[]
cum_bgt=0
cum_bgts=[]
for i,line in enumerate(open(inpFilename,"r")):
    if not line=="":
        line=line.strip("\n")
        lineParts=line.split()
        if float(lineParts[0])>0:
            energies.append(float(lineParts[0]))
            bgts.append(conversion*float(lineParts[1]))

indices=np.argsort(energies)
energies=np.array(energies)[indices]
bgts=np.array(bgts)[indices]
for bgt in bgts:
    cum_bgt+=bgt
    cum_bgts.append(cum_bgt)

fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(10,6))
for i,energy in enumerate(energies):
    axes[0].plot([energy,energy],[0,bgts[i]],color="black")

axes[1].plot(energies,cum_bgts)

axes[0].set_xlim(0,3.5)
axes[0].set_ylim(0,0.015)

axes[0].set_xlabel("Energy (MeV)",fontsize=16)
axes[0].set_ylabel("B(GT$_0$)",fontsize=16)

axes[1].set_xlabel("Energy (MeV)",fontsize=16)
axes[1].set_ylabel("$\Sigma$B(GT$_0$)",fontsize=16)

plt.savefig("Fig5.2.png",dpi=500,bbox_inches="tight")
plt.show()