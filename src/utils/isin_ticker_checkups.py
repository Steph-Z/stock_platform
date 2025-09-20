def input_case_insensitive(isin_input):
    '''returns a case insensitive version of the user input'''
    return isin_input.upper().replace(' ','')

def remove_dashes(isin_input: str):
    '''removes the dashes from a seemingly valid isin in case there are any '''
    
    newstr = isin_input.replace('-', '')
    return newstr

def isValid_ISIN_Code(isin_input: str):
    
    ##https://www.geeksforgeeks.org/dsa/how-to-validate-isin-using-regular-expressions/

    # Regex to check valid ISIN Code
    regex = "^[A-Z]{0,1}[0-9A-Z]{9}[0-9]{1}$" #original function contained an option to check for dashes, removed in prev. step now

    # Compile the ReGex
    p = re.compile(regex)

    # If the string is empty
    # return false
    if (isin_input == None):
        return False

    # Return if the string
    # matched the ReGex
    if(re.search(p, isin_input)):
        return True
    else:
        return False
    
#Luhns algo
#for conversion of letters need to look at wiki artivle of isin
#I really did not expect this much depths for such a "simple" task
#convert letters to ascii -55 

def check_luhns(isin_input):
    '''the str will have passed the is isin valid function. 
    checks if the isin is correct by employing luhn algorithm
    #https://en.wikipedia.org/wiki/Luhn_algorithm, even with pseudocode '''
    
    #Takes care of the possible characters in the isin
    transformed_isin = ""
    for ch in isin_input:
        if ch.isdigit():
            transformed_isin+= ch
        else:
            transformed_isin += str(ord(ch)-55)
            
    #Now we can apply the actual algorithm
    checksum = 0
    parity = len(transformed_isin) % 2
    
    for idx, digit in enumerate(transformed_isin[:-1]): #iterate through the isin but omit checksum number 
        number = int(digit)
        if (idx+1) % 2 == parity: #not digit, look pseudocode....
            checksum += number
        elif number > 4:
            checksum += 2* number -9
        else:
            checksum += 2* number

    return int(transformed_isin[-1]) == ((10 - (checksum % 10)) % 10)


def check_ticker(user_input: str, check_function = None):
    '''takes a users input that resembles a ticker and checks if it is valid,
    has an input for the check function to avoid online lookup during testing,
    to check, see if it has a price during market hours'''
    
    try:
        if check_function(user_input).info['regularMarketPrice'] is not None:
            return True
        else: 
            return False
    except Exception:
        return False
    
check_ticker('asdPL', check_function= yf.Ticker)