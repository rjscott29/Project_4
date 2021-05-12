# imports of external packages to use in our code
import sys
import math
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats
import statistics

# gets table of dielectric materials and constants as tuple [dielectric,kappa]
def Dielectrics(InputFile):
    table = []
    with open(InputFile, "r") as datatable:
        for line in datatable:
            table.append(line.rstrip('\n').split(','))
    return table

def Measure(kappa, sigma):
    return round(np.random.normal(kappa,sigma),1)

# Function to sort the list by second item of tuple
def Sort_Tuple(tup): 
    # reverse = None (Sorts in Ascending order) 
    # key is set to sort using second element of 
    # sublist lambda has been used 
    tup.sort(key = lambda x: x[1]) 
    return tup 

# gets rules from the text file associated with input files
def GetRules(InputFile):
    RulesFile = "rules_" + InputFile
    rules = []
    with open(RulesFile, "r") as rulesfile:
        for rule in rulesfile:
            rules.append(rule.rstrip('\n'))
        rules = [float(i) for i in rules]
        # print("kappa: " + str(rules[0]))
        # print("sigma: " + str(rules[1]))
        # print("Nmeas: " + str(rules[2]))
        # print("Nexp: " + str(rules[3]))
    return rules

# get theoretical probability distribution based on gimme and Ncards
def NormalProbability(kappa,sigma,data):
    prob = []
    for i in data:
        prob.append(scipy.stats.norm(loc=kappa, scale=sigma).pdf(i))
    return prob

# Reorganizes inputfile data for our use, outputs as tuple
def DataResults(InputFile):
    with open(InputFile,'r') as exps:
        # organizes data into tuple where each item is a set
        # removes information that is not a digit
        data = [[x.strip() for x in line.split(',')] for line in exps]
        data = [list(filter(None,x)) for x in data]
        data = [[float(x) for x in y] for y in data]
        return data
    
# just gets all of the values from the tuple and compiles it
def TotalResults(DataResults):
    results = []
    for data in DataResults:
        for x in data:
            results.append(x)
    return results

# Gets likelihood from one set (input as list), returns single float value
def Likelihood(data,probability):
    L = []
    for value in data:
        # take each value from data and multiply by the probability of getting
        # that value from prob
        # data value corresponds to index of probability distribution
        l = probability[value]
        L.append(l)
    likelihood = np.product(L)
    return likelihood

# Input unnormalized data as list, output list of data normalized [0,1]
def NormalizeData(data):
    return (data - np.min(data)) / (np.max(data) - np.min(data))    

TableFile = "dielectric_table.txt"    

# main function for our coin toss Python code
if __name__ == "__main__":
    # not making any assumptions about what is provided by user
    haveH = False
            
    # available options for user input
    if '-input' in sys.argv:
        p = sys.argv.index('-input')
        InputFile = sys.argv[p+1]
        haveH = True
    # if the user includes the flag -h or --help print the options
    if '-h' in sys.argv or '--help' in sys.argv or not haveH:
        print ("Usage: %s [options]" % sys.argv[0])
        print ("  options:")
        print ("   --help(-h)          print options")
        print ("   -input [filename]  name of file for data")
        sys.exit(1)
    
    # get data from the input file rules so we know what we are working with
    rules = GetRules(InputFile)
    kappa_true = rules[0]
    sigma = rules[1]
    Nmeas = rules[2]
    Nexp = rules[3]
    
    # reads data from text file table
    data_raw = Dielectrics(TableFile)
    data = []
    for d in data_raw:
        data.append([d[0],float(d[1])])
    data = Sort_Tuple(data)
    kappa_list = [item[1] for item in data]
    kappa_list = [float(i) for i in kappa_list]
            
    # use our definitions to get data, tuple [[set1],[set2],[set3],...]
    data_sets = DataResults(InputFile)
    
    # compiles all sets of data into one list (tuple --> list)
    data_list = TotalResults(data_sets)
                       
    # define some lists for collecting data
    kappa_exp = []
    pull = []
    sigma_exp = []
    # we take each set of data and find associated likelihood from each possible
    # kappa value and then place those in a list
    for data_set_i in data_sets:
        likelihood_dist = []
        for kappa in kappa_list:
            prob = []
            for item in data_set_i:
                prob.append(scipy.stats.norm(loc=kappa, scale=sigma).pdf(item))
            likelihood_dist.append(np.product(prob))
        kappa_maxes_L_index = likelihood_dist.index(max(likelihood_dist))
        kappa_maxes_L = kappa_list[kappa_maxes_L_index]
        kappa_exp.append(kappa_maxes_L)
        
        L = likelihood_dist
        # find stdev of data
        LLR = []
        for l_value in L:
            # record very large negative number to avoid log(0) = -inf
            if l_value == 0:
                LLR.append(-1e32)
            else:
                LLR_i = np.log(l_value) - np.log(L[kappa_maxes_L_index])
                LLR.append(LLR_i)
        # add .5 to all values to find where LLR exceeds .5
        LLR_math = [x+.5 for x in LLR]
        # look for the sign change in the data and get the index location
        where = (np.diff(np.sign(LLR_math)) != 0)*1
        if sum(where) < 2:
            L_sigma = 0 - [i for i, n in enumerate(where) if n == 1][0]
        else:
            L_sigma = ([i for i, n in enumerate(where) if n == 1][1] - [i for i, n in enumerate(where) if n == 1][0])
        sigma_exp.append(L_sigma)
        # error when L_sigma = 0, use 0 as pull value
        if L_sigma != 0:
            pull.append((kappa_maxes_L-kappa_true)/L_sigma)
        else:
            pull.append(0)
        
    # determine parameters for plotting
    # ticks associated with bin width
    # select associated with naming the plot with the predicted dielectric constant    
    ticks = kappa_list.index(max(kappa_exp))-kappa_list.index(min(kappa_exp))
    if ticks == 0:
        ticks = 1
    select = [item[0] for item in data if item[1] == statistics.mode(kappa_exp)]
    selection = ""
    for i in select:
        selection += " " + str(i)
    
        
##########################            
    # Set binwidth for plots
    binwidth = 1
    
    # plt.figure()
    # plt.hist2d(x_g_true,y_g_best,bins=[n,n*2],range=[[0,n],[0,n]],
    #            cmap=plt.cm.Reds)
    # plt.colorbar()
    # plt.show()
    
##########################                    
# # PLOT 1: Frequency plot
#     title1 = "Frequency Table for Number of Games Won"
                
#     # make figure
#     plt.figure()
#     plt.hist(data_list, binwidth, facecolor='deepskyblue',
#               alpha=0.5, align = 'left', label="$\\mathbb{H}$")
      
#     plt.xlabel('$N_{wins}$ per game')
#     plt.ylabel('Frequency')
#     plt.legend(loc = 2)
#     plt.xlim(-.5 , n+.5)
#     plt.tick_params(axis='both')
#     plt.title(title1)
#     plt.grid(True)

#     plt.show()

##########################     
# # PLOT 2: Density plot
#     title2 = "Density Table for Number of Games Won"
                
#     # make figure
#     plt.figure()
#     plt.bar(prob[0], prob[1], width=binwidth, facecolor='deepskyblue',
#               alpha=0.5, label="$\\mathbb{H}$")
      
#     plt.xlabel('$N_{wins}$ per game')
#     plt.ylabel('Probability')
#     plt.legend(loc = 2)
#     plt.xlim(-.5 , n+.5)
#     plt.tick_params(axis='both')
#     plt.title(title2)
#     plt.grid(True)

#     plt.show()
    
# ########################## 
# PLOT 3: Combined G and Pull plots
    title3 = str(Nexp) + " experiments; " + str(Nmeas) + " measurements / experiment; " + str(kappa_true) + " $\kappa$ ; $\sigma$ = " + str(sigma) 
                 
      # make figure
    fig, (ax1, ax2) = plt.subplots(1,2,figsize = [12.8, 4.8])
    fig.suptitle(title3)
    ax1.hist(kappa_exp, bins=ticks, align = 'left',
              facecolor='deepskyblue', edgecolor = 'black', density = True, alpha=0.5)
    ax2.hist(pull, bins=8, range=[-2,2],
              facecolor='deepskyblue', density = True, edgecolor = 'black', alpha=0.5, align = 'left')
        
    ax1.set_title("Predicted $\kappa$ Plot; Predicted material:" + str(selection) + ", $\kappa$ = " + str(statistics.mode(kappa_exp)))
    ax2.set_title("Pull Plot")
    ax1.set(xlabel='$\kappa$', ylabel="Probability")
    ax2.set(xlabel='Pull', ylabel="Probability")
    ax1.tick_params(axis='both')
    ax1.set_xticks(range(math.floor(min(kappa_exp)-1),math.ceil(max(kappa_exp))+1))
    ax2.tick_params(axis='both')
    ax1.grid(True)
    ax2.grid(True)
    
    plt.show()
    
# ########################## 
# # PLOT 4: Predicted g plot
#     title4 = "Predicted G Plot (actual value: G = " + str(g_true) + ")"
                
#     # make figure data, bins=np.arange(min(data), max(data) + binwidth, binwidth)
#     plt.figure(figsize=[10,8])
#     plt.hist(g_exp, bins=max(g_exp)-min(g_exp), align = 'left',
#               facecolor='deepskyblue', edgecolor = 'black', density = True, alpha=0.5)
      
#     plt.xlabel('G')
#     plt.ylabel('Probability')
#     plt.xlim()
#     plt.tick_params(axis='both')
#     plt.xticks(range(min(g_exp),max(g_exp)))
#     plt.title(title4)
#     plt.grid(True)

#     plt.show()
    
# ########################## 
# # PLOT 5: Pull plot
#     title4 = "Pull Plot"
                
#     # make figure data, bins=np.arange(min(data), max(data) + binwidth, binwidth)
#     plt.figure()
#     plt.hist(pull, bins=8, range=[-2,2],
#               facecolor='deepskyblue', density = True, alpha=0.5, align = 'left')
      
#     plt.xlabel('Pull')
#     plt.ylabel('Probability')
#     plt.xlim()
#     plt.tick_params(axis='both')
#     plt.title(title5)
#     plt.grid(True)

#     plt.show()