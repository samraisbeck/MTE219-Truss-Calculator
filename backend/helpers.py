# File to store helper functions in

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

def m2mm(meters):
    return round(meters*1000, 3)

def mm2m(millimeters):
    return millimeters/1000.0

def mc2cmc(metersCubed):
    return round(metersCubed*(1000**2), 3)

def cmc2mc(cmCubed):
    return cmCubed/(1000.0**2)

def mq2mmq(metersQuartic):
    return round(metersQuartic*(1000**4), 3)

def mmq2mq(mmQuartic):
    return mmQuartic/(1000.0**4)
