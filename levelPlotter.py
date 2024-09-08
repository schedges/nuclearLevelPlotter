#Makes a nice plot of the levels of a .lev files from NuShellX
# Usage: python3 levelPlotter.py <path to Name.lev>
import matplotlib.pyplot as plt
import sys
from fractions import Fraction

textGap_fraction=0.025 #Percent of the total plot range
verticalGap_fraction=0.0025 #Percent of the total plot range
firstLine=5
inpFilename=sys.argv[1]

#Get base name
basename=inpFilename[inpFilename.rfind("/")+1:inpFilename.find(".")]
print(basename)

#Plot settings
plt.rcParams['figure.figsize'] = [6, 8]

#Get data
levels=[]
spins=[]
parities=[]
for iline,line in enumerate(open(inpFilename,"r")):
    if iline>=firstLine:
        if not line=="":
            line=line.strip("\n")
            lineParts=line.split()
            levels.append(float(lineParts[0]))
            if not lineParts[1]=="?":
                spins.append(float(lineParts[1])/2.)
                parities.append("+" if lineParts[2]==1 else "-")
            else:
                spins.append("?")
                parities.append("?")


fig,ax=plt.subplots()
#Plot
#Horizontal line settings
startX=1
endX=3
#label settings
startX_left=0.0
endX_left=0.75
startX_right=3.25
endX_right=4.0

#Plot settings
maxEnergy=1.5
textGap=maxEnergy*textGap_fraction
verticalGap=maxEnergy*verticalGap_fraction
plt.ylim(-0.005,maxEnergy*1.1)
plt.xlim(0,4)
width=1

textLocation=0
lineLocation=0
for i,energy in enumerate(levels):
    if energy < maxEnergy:
        #Plot horizontal line

        ax.hlines(energy,xmin=startX,xmax=endX,color="black",lw=width)
        #plt.axline((startX,energy),(endX,energy))
        #Plot level line--either at the same height of line if there's room, or at the first open location
        print(textLocation,energy)
        if textLocation<=energy:
            plt.text(startX_left,energy+verticalGap,"{0:.3f} MeV".format(energy))
            ax.hlines(energy,xmin=startX_left,xmax=startX,color="black",lw=width)
            if not spins[i]=="?":
                plt.text(startX_right,energy+verticalGap,"{0}{1}".format(Fraction(spins[i]),parities[i]))
            else:
                plt.text(startX_right,energy+verticalGap,"?")
            ax.hlines(energy,xmin=endX,xmax=endX_right,color="black",lw=width)
            textLocation=energy
        else:
            plt.text(startX_left,textLocation+verticalGap,"{0:.3f} MeV".format(energy))
            ax.hlines(textLocation,xmin=startX_left,xmax=endX_left,color="black",lw=width)
            plt.plot([endX_left,startX],[textLocation,energy],color="black",lw=width)

            if not spins[i]=="?":
                plt.text(startX_right,textLocation+verticalGap,"{0}{1}".format(Fraction(spins[i]),parities[i]))
            else:
                plt.text(startX_right,textLocation+verticalGap,"?")

            ax.hlines(textLocation,xmin=startX_right,xmax=endX_right,color="black",lw=width)
            plt.plot([endX,startX_right],[energy,textLocation],color="black",lw=width)
            
        #If necessary, plot diagonal lines  
        textLocation+=textGap

'''
plt.xlim(0, 8), plt.ylim(-2, 8)
plt.plot(x1, y1, x2, y2, marker = 'o')
'''
plt.text(1.7,-0.05,basename)
plt.axis('off')
plt.savefig(basename+".png",dpi=500,bbox_inches="tight")
plt.show()
