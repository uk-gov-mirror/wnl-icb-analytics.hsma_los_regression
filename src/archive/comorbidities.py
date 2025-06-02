#Functions to extract the lower and upper bounds from the HRG Name in the Trim data

#Function to extract the CC Score Range from the HRG Name in the Trim Point data
def get_score_from_name(name):
    split_name = name.split("CC Score ")
    if len(split_name) == 1:
        return None
    else:
        return split_name[1]

#Function to seperate out the upper and lower bounds of the CC Score Ranges
def get_lower_and_upper(ccr, upper=0):

    #Case 1: No CC Score Range
    if ccr is None:
        return None
    #Case 2: CC Score has upper and lower bound
    if "-" in ccr:
        return ccr.split("-")[upper]
    #Case 3: Lower Bound with no upper bound
    if "+" in ccr:
        if not upper:
            return ccr[:-1]
        else:
            return None
    #Case 4: CC Score Range is a single value
    else:
        return ccr