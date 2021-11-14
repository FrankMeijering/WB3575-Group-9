import os
import numpy as np


def get_file(file):
    # Returns the full path, if the file is in the same folder as the main .py program.
    return os.path.join(os.path.dirname(file), file)


def get_folder_file(folder, file):
    # Returns the full path, if the file is not in the same folder as the main .py program.
    # If this does not work, use: return get_file(os.path.join(folder, file))
    return os.path.join(folder, file)


def eta_comp_func(T1, T2, p1, p2, kappa):
    return ((p2/p1)**((kappa-1)/kappa)-1)/(T2/T1-1)


def cp_lemmon(T, R):
    # Specific heat cp according to Lemmon
    return R*(3.491+2.396e-6*T+7.172e-9*T**2-3.115e-13*T**3+0.224*T**-1.5+0.791*((3364/T)**2)*np.exp(3364/T)/
              ((np.exp(3364/T)-1)**2)+0.212*((2242/T)**2)*np.exp(2242/T)/((np.exp(2242/T)-1)**2)+
              (2/3)*0.198*((11580/T)**2)*np.exp(-11580/T)/(((2/3)*np.exp(-11580/T)+1)**2))


def kappa_calc(cp, R):
    return 1/(1-R/cp)
