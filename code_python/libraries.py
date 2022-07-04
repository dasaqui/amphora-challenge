#!/usr/bin/env python

# this code is designed to test all the needed libraries and tell the user if one
# required library is not installed

# error flag
error_flag = False

try:
    import sklearn
    print( "sklearn is correctly installed\n")
except:
    print( "python 'sklearn' module is not installed, please install it to continue")
    print( "If you habe pip installed you can run:\npip install sklearn\n")
    error_flag = True

try:
    import pandas
    print( "pandas is correctly installed\n")
except:
    print( "python 'pandas' module is not installed, please install it to continue")
    print( "If you habe pip installed you can run:\npip install pandas\n")
    error_flag = True

try:
    import matplotlib
    print( "matplotlib is correctly installed\n")
except:
    print( "python 'matplotlib' module is not installed, please install it to continue")
    print( "If you habe pip installed you can run:\npip install matplotlib\n")
    error_flag = True

# Be explicit to indicate the results
if error_flag:
    print( "Some required libraries are not installed, please read previous messages to install them\n")
else:
    print( "All the required libraries are installed and ready to be used\n")