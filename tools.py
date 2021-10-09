import os


def get_file(file):
    # Returns the full path, if the file is in the same folder as the main .py program.
    return os.path.join(os.path.dirname(file), file)


def get_folder_file(folder, file):
    # Returns the full path, if the file is not in the same folder as the main .py program.
    # If this does not work, use: return get_file(os.path.join(folder, file))
    return os.path.join(folder, file)


def eta_comp_func(T1, T2, p1, p2, kappa):
    return ((p2/p1)**((kappa-1)/kappa)-1)/(T2/T1-1)
