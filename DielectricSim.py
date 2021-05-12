# imports of external packages to use in our code
import sys
import numpy as np

# takes a gaussian measurement centered around kappa with standard deviation sigma
def Measure(kappa, sigma):
    return round(np.random.normal(kappa,sigma),1)

# gets table of dielectric materials and constants as tuple [dielectric,kappa]
def Dielectrics(InputFile):
    table = []
    with open(InputFile, "r") as datatable:
        for line in datatable:
            table.append(line.rstrip('\n').split(','))
    return table

# main function for our card game Python code
if __name__ == "__main__":
    # if the user includes the flag -h or --help print the options
    if '-h' in sys.argv or '--help' in sys.argv:
        print ("Usage: %s [-options]" % sys.argv[0])
        print ("  options:")
        print ("   --help(-h)          print options")
        print ("   -dielectric [text]  choose dielectric material to simulate")
        print ("   -sigma [number]     choose width of gaussian")
        print ("   -Nmeas [number]     choose number of measurements")
        print ("   -Nexp [number]      choose number of experiments")
        print ("   -output [text]      name of file for output data")
        sys.exit(1)
  
    # default dielectric
    dielectric = 'InAs'
    
    # default sigma
    sigma = 2
    
    # default number of measurements
    Nmeas = 10
    
    # default number of experiments
    Nexp = 10
    
    InputFile = "dielectric_table.txt"
    
    # output file defaults
    doOutputFile = False
    material = False

    # read the user-provided seed from the command line (if there)
    if '-dielectric' in sys.argv:
        p = sys.argv.index('-dielectric')
        dielectric = sys.argv[p+1]
        material = True
    if '-sigma' in sys.argv:
        p = sys.argv.index('-sigma')
        sig = int(sys.argv[p+1])
        if sig > 0:
            sigma = sig
    if '-Nmeas' in sys.argv:
        p = sys.argv.index('-Nmeas')
        Nm = int(sys.argv[p+1])
        if Nm > 0:
            Nmeas = Nm
    if '-Nexp' in sys.argv:
        p = sys.argv.index('-Nexp')
        Ne = int(sys.argv[p+1])
        if Ne > 0:
            Nexp = Ne
    if '-input' in sys.argv:
        p = sys.argv.index('-input')
        InputFile = sys.argv[p+1]
    if '-output' in sys.argv:
        p = sys.argv.index('-output')
        OutputFileName = sys.argv[p+1]
        Rulesname = "rules_" + str(OutputFileName)
        doOutputFile = True
        
# get data from dielectric table
data = Dielectrics(InputFile)
kappa = [item[1] for item in data if item[0] == dielectric]
kappa = float(kappa[0])
    
    # writes to txt file from user input
    # txt file shows games in rows and sets in columns
if doOutputFile:
    outfile = open(OutputFileName, 'w')
    outfilerules = open(Rulesname, 'w')
    # records rules in separate text file for use in analysis
    outfilerules.write(str(kappa) + "\n" + str(sigma) + "\n" + str(Nmeas) + "\n" + str(Nexp))
    for e in range(0,Nexp):
        for m in range(0,Nmeas):
            outfile.write(str(Measure(kappa, sigma)))
            outfile.write(",")
        outfile.write("\n")
else:
    for e in range(0,Nexp):
        for m in range(0,Nmeas):
            print(str(Measure(kappa, sigma)))
