#################### RiP ######################
## Funtion to perform MCA energy calibration ##
## and Resolution linear regression          ##
###############################################

## ---------------------------- ##
import matplotlib.pyplot as plt
from matplotlib.pylab import *
## ---------------------------- ##

def Calib(E, Ch, dCh):
   
    sx=0.0 #Declaração de variáveis para simplificar os somatórios 
    sy=0.0 #que são precisos para calcular os paremetros da reta
    sxy=0.0
    sxx=0.0
    syy=0.0
    sinv=0.0

    for i in range(0,len(Ch)):  #De acordo com as listas criadas, calcula os somatórios
                                #que usamos de seguida
        sx+=E[i]/((dCh[i])**2)
        sy+=Ch[i]/((dCh[i])**2)
        sxy+=(E[i]*Ch[i])/((dCh[i])**2)
        sxx+=((E[i])**2)/((dCh[i])**2)
        syy+=((Ch[i])**2)/((dCh[i])**2)
        sinv+= 1/((dCh[i])**2)     
    delta = sinv*sxx - (sx*sx)

    m = (sinv*sxy-sx*sy)/(delta)    #Calcula o declive
    b = (sxx*sy-sx*sxy)/(delta)     #Calcula a ordenada na origem
    sigma_m = (sinv/delta)**(0.5)   #Calcula incerteza associada ao declive
    sigma_b = (sxx/delta)**(0.5)    #Calcula incerteza associada à ordenada na origem   

    print('E (keV) = (', "{:.6f}".format(1/m), '+-',"{:.6f}".format(
        sigma_m/m**2),') x Channel + (',"{:.6f}".format(b/m), '+-', "{:.6f}".format(
            ((sigma_b/m)**2+(b*sigma_m/m**2)**2)**0.5), ') \n')
 
    return 1/m, b/m, sigma_m/m**2, ((sigma_b/m)**2+(b*sigma_m/m**2)**2)**0.5


def Resolution(R, sqrtE, dR):
   
    sx=0.0  
    sy=0.0 
    sxy=0.0
    sxx=0.0
    syy=0.0
    sinv=0.0

    for i in range(0,len(sqrtE)):  
                                
        sx+=sqrtE[i]/((dR[i])**2)
        sy+=R[i]/((dR[i])**2)
        sxy+=(sqrtE[i]*R[i])/((dR[i])**2)
        sxx+=((sqrtE[i])**2)/((dR[i])**2)
        syy+=((R[i])**2)/((dR[i])**2)
        sinv+= 1/((dR[i])**2)     
    delta = sinv*sxx - (sx*sx)

    m = (sinv*sxy-sx*sy)/(delta)    #Calcula o declive
    b = (sxx*sy-sx*sxy)/(delta)     #Calcula a ordenada na origem
    sigma_m = (sinv/delta)**(0.5)   #Calcula incerteza associada ao declive
    sigma_b = (sxx/delta)**(0.5)    #Calcula incerteza associada à ordenada na origem   

    print('R (%) = (', "{:.6f}".format(m), '+-',"{:.6f}".format(
        sigma_m),') x 1/sqrt(E) + (',"{:.6f}".format(b), '+-', "{:.6f}".format(
            (sigma_b), ')'))
    
    ## Fake E error for error bars
    dE = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    ## For linear regression plot
    X = np.linspace(min(sqrtE), max(sqrtE))
    Y = m*X+b

    ## Plot experimental and linear regression
    fig, ax = plt.subplots()
    ax.errorbar(sqrtE, R, dR, dE, 'D', color='k', label='Resolution')
    ax.plot(X, Y, color='xkcd:blue', label='Linear Fit')
    legend = ax.legend(loc="best",ncol=1,shadow=False,fancybox=True,framealpha = 0.0,fontsize=20)
    legend.get_frame().set_facecolor('#DAEBF2')
    tick_params(axis='both', which='major', labelsize=22)
    xlabel('$1/\sqrt{E}\ (\mathrm{keV}^{-1/2}$)',fontsize=22)
    xlim(left=0.)
    ylabel('R (%)', fontsize=22)
    show()
 
    return m, b, sigma_m, sigma_b