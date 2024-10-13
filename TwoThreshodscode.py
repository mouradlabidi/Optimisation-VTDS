# %%
#A: matrice numpy
def diagQ( A,n):
    import numpy as np
    for i in range(0,n):
        A[i,i]=-np.sum(A[i])
        #print(A[i,i])
    return A
# %%
def createMatQ(K,N1,N2,Lambda, mu1, mu2):
    import numpy as np
    Q=np.zeros((N1 + N2 + K - 1,N1 + N2 + K - 1),dtype=float)
    
    #1
    for i in range(0,N2):
        Q[i][i+1] = Lambda
    
    #2
    for i in range(N2,N1):
        Q[i][i + 1] = Lambda
        if (i > N2):
            Q[i][i - 1] = mu2
    
    #3
    for i in range(N1,K):
         Q[i][i+1] = Lambda
         if (i > N1):
             Q[i][i - 1] = mu1
    Q[K][K - 1] = mu1
    #4
    if (N2==1):
        Q[N2][0] = mu2
    else:
        Q[N2][K+1] = mu2
        Q[K+1][N2] = Lambda
    #5
    
    for i in range(K+1,K + N2 - 1):
        Q[i][i+1] = mu2
        if (i > K + 1):
            Q[i][i-1] = Lambda
    
    #6
    if (K + N2 - 1 > K + 1):
        Q[K+N2-1][K+N2-2] = Lambda
    if (K + N2 - 1 >= K + 1):
        Q[K + N2 - 1][0] = mu2
    
    #7
    
    Q[N1][K + N2] = mu1
    Q[K + N2][N1] = Lambda
    #8
    for i in range(K + N2,K + N1 + N2 - 2):
        Q[i][i + 1] = mu1
        if (i > K+N2):
            Q[i][i - 1] = Lambda
    
    #9
    if(N1>2):
        Q[K+N1+N2-2][K+N1+N2-3] = Lambda
    Q[K+N1+N2-2][0] = mu1
    Q = diagQ(Q, N1 + N2 + K - 1)
    return Q

# %%
def matrixToFile(A, filematq):
    with open(filematq, "w") as fich:
        for row in A:
            for value in row:
                s = "{:.8f}".format(value)
                if ',' in s:
                    s = s.replace(',', '.')
                fich.write(s + ' ')
            fich.write('\n')
            

# %%
import subprocess

def call_matlab_script(matlab_script):
    command = f"matlab -nodplash -nodesktop -minimize -wait -r \"run('{matlab_script}'); exit;\""
    subprocess.run(command, shell=True)



# %%
def FileOfProbaToArray(probaFile):
    import numpy as np
    try:
        with open(probaFile, "r") as file:
            line = file.readline().strip().split()
    except FileNotFoundError:
        print("Erreur lors de l'ouverture du fichier.")
        return None

    TPI = np.array([float(value) for value in line])
    #print(TPI)
    return TPI


# %%
#Calcule le débit moyen d'arrivé Lambda_bar
def THarrival(TPI,K,Lambda):
    import numpy as np
    #Lambda_bar = 0
    #for i in range(len(TPI)):
    #   Lambda_bar += TPI[i]
    
    Lambda_bar=np.sum(TPI)
    Lambda_bar -= TPI[K]# car l'etat K,2 ne contient pas une fleche lamda sortante 
    Lambda_bar *= Lambda
    return Lambda_bar


# %%
# Calcule la probabilité d'etre en idle
def ProbaIdle(TPI, N2):
    PIdle = 0
    for i in range(N2):
        PIdle += TPI[i]
    return PIdle

# %%
#Calcule la probabilité d'etre en Semi Busy = la sum des proba des états SB
def ProbaSemiBusy(TPI, K, N1, N2):
    PSB = 0
    for i in range(N2,N1):
        PSB += TPI[i]
    for i in range(K + 1,K + N2):
        PSB += TPI[i]
        
    return PSB

# %%
#Calcule la probabilité d'etre en Busy = la sum des proba des états Busy
def ProbaBusy(TPI, K, N1, N2):
    PB=0
    for i in range(N1,K+1):
        PB += TPI[i]
        
    for i in range(K + N2,len(TPI)):
        PB += TPI[i]
    return PB

# %%
#Calcule la probabilité de blocage
def probaBlocking(TPI , K):
    return TPI[K]


# %%
#Calcule le débit moyen de transition mu2
def throuTranMu2(TPI,K, N1, N2, mu2):
    PSB= ProbaSemiBusy(TPI, K, N1, N2)
    thru_mu2 = PSB * mu2

    return thru_mu2

# %%
#Calcule le débit moyen de transition mu1
def throuTranMu1(TPI,K, N1, N2, mu1):
    thru_mu1 = ProbaBusy(TPI, K, N1, N2) * mu1

    return thru_mu1

# %%
# Qbar= Nombre moyen de paquets dans la file d'attente Qbar
def meanNumbQ(TPI, K, N1, N2):
    Qbar = 0
    for i in range(K + 1):
        Qbar += TPI[i] * i
    for i in range(1, N2):
        Qbar += TPI[K + i] * (N2 - i)
    for i in range(N1 - 1):
        Qbar += TPI[K + N2 + i] * (N1 - i - 1)
    return Qbar

# %%
# Nombre moyen de paquets dans la file d'attente pendant l'état Semi Busy
#pas verifiée
#verifiée et j'ai trouvé une erreur 
def meanNumbQSB(TPI, K, N2,N1):
    QSBbar = 0
    for i in range(N2,N1):
        QSBbar += TPI[i] * i
    for i in range(N2-1):
        QSBbar += TPI[K + i + 1] * (N2 - i - 1)
    return QSBbar

# %%
# Nombre moyen de paquets dans la file d'attente pendant l'état Busy
def meanNumbQBusy(TPI, K, N1, N2):
    QBbar = 0
    for i in range(N1,K + 1):
        QBbar += TPI[i] * i
    for i in range(N1 - 1):
        QBbar += TPI[K + N2 + i] * (N1 - i - 1)
    return QBbar


# %%
#calculer la longueur moyenne d'une période d'attente (idle)
def averageIdlePeriod( N2, Lamda):
    #Two thresholds working vacation policy
    Ibar = N2 / Lamda
    return Ibar

# %%
#calculer la longueur moyenne d'une période Semi Busy
def averageSemiBusyPeriod(N1, N2, Lamda, QSBbar, mu2):
    SBbar = min((N1 - N2) / Lamda, QSBbar / mu2)
    return SBbar

# %%
#calculer la longueur moyenne d'une période Busy
def averageBusyPeriod(QBbar, mu1):
    Bbar = QBbar / mu1
    return Bbar


# %%
#calculer la durée moyenne d'un cycle
def averageCycleDuration(Bbar,Ibar, SBbar) :
    # Two thresholds working vacation policy
    Cbar = (Bbar + SBbar + Ibar)
    return Cbar


# %%
#calculer le délai moyen en utilisant la formule de Little's Law 
def meanSojourTime(Qbar,Lambda_bar): 
    return Qbar / Lambda_bar


# %%
# Based on Jiang et al 
def energyConsumption(PI, PSB, Qbar, Cbar) :
    #Two thresholds working vacation policy
    ECI = 10.0 # consommation énergétique du mode idle
    ECSB = 25 # consommation énergétique du mode semi busy
    ECb = 500.0 # consommation énergétique du mode busy
    ECTx  =5.0 # consommation énergétique pour le maintien de chaque paquet présent dans le nœud capteur
    ECs = 300.0 # consommation énergétique de Switching entre les modes

    EC = (PSB * ECSB) + (PI * ECI) + (ECb * (1 - PSB - PI)) + (ECs / Cbar) + (Qbar * ECTx)
    return EC

# %%
def twoThreshodsPolicy(K, N1, N2, mu1, mu2, Lambda):
    #Creation de la matrice
    Q=createMatQ(K,N1,N2,Lambda, mu1, mu2)

    #print(Q)

    #Sauvegarder la matrice dans un Fichier
    matrixToFile(Q,"MatriceQ.txt")

    #Executer la fonction matlab
    call_matlab_script("MatlabFunction.m")

    #Récuperer le tableau des proba stationaire
    TPI=FileOfProbaToArray("MatlabFunctionResult.txt")
    #print(TPI)
    
    PI=ProbaIdle(TPI, N2)
    PSB=ProbaSemiBusy(TPI, K, N1, N2)
        
    Lambda_bar=THarrival(TPI,K,Lambda)
    Qbar=meanNumbQ(TPI, K, N1, N2)
    QSBbar =meanNumbQSB(TPI, K, N2,N1)
    QBbar=meanNumbQBusy(TPI, K, N1, N2)
    Ibar=averageIdlePeriod( N2, Lambda)
    SBbar=averageSemiBusyPeriod(N1, N2, Lambda, QSBbar, mu2)
    Bbar=averageBusyPeriod(QBbar, mu1)
    Cbar=averageCycleDuration(Bbar,Ibar, SBbar) 
    Wbar=meanSojourTime(Qbar,Lambda_bar)
    EC=energyConsumption(PI, PSB, Qbar, Cbar)
    return EC,Wbar
    

'''
EC, Wbar = twoThreshodsPolicy(5, 3, 1, 0.5, 0.25, 0.25)
print(EC)
print(Wbar)
'''