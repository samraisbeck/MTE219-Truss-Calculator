"""
File to store helper functions in.
Most used is ifThen, described by the two helpers to that, ifthen and ifthenelif.
Then, some basic unit conversions.
"""

def ifthen(statement, resT, resF):
    """
    This would be used for the case of, if the statement is true, a variable
    equals one thing (resT). Else, that variable equals another (resF).
    You can see examples throughout this project.
    """
    if statement:
        return resT
    return resF

def ifthenelif(statements, returns, resF=None):
    """
    For a series of if, elif, elif,..., else.
    Usually used for one variable with multiple situations.
    See loadAndSave.py for a good example
    statements -> [list of boolean statements]
    returns -> [value]
    resF -> [value]"""
    for i in range(len(statements)):
        if statements[i]:
            return returns[i]
    return resF

def ifThen(statements, returns, resF=None):
    """
    USE THIS ONE!
    works for both of the above cases.
    """
    if type(statements) == bool:
        return ifthen(statements, returns, resF)
    elif type(statements) == list:
        return ifthenelif(statements, returns, resF)

def m2mm(meters):
    """ Meters to millimeters """
    return round(meters*1000, 3)

def mm2m(millimeters):
    """ Millimeters to meters """
    return millimeters/1000.0

def mc2cmc(metersCubed):
    """ Meters cubed to centimeters cubed """
    return round(metersCubed*(1000**2), 3)

def cmc2mc(cmCubed):
    """ Centimeters cubed to meters cubed """
    return cmCubed/(1000.0**2)

def mq2mmq(metersQuartic):
    """ Meters quartic to millimeters quartic """
    return round(metersQuartic*(1000**4), 3)

def mmq2mq(mmQuartic):
    """ Millimeters quartic to meters quartic """
    return mmQuartic/(1000.0**4)
