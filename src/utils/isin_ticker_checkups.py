import yfinance as yf
import re
import logging




def input_case_insensitive(isin_input):
    '''returns a case insensitive version of the user input'''
    return isin_input.upper().replace(' ','').strip() #strip helps agaist unwanted tabs or spaces that are not defined as ' '

def remove_dashes(isin_input: str):
    '''removes the dashes from a seemingly valid isin in case there are any '''
    
    newstr = isin_input.replace('-', '')
    return newstr

def isValid_ISIN_Code(isin_input: str):
    
    ##https://www.geeksforgeeks.org/dsa/how-to-validate-isin-using-regular-expressions/

    # Regex to check valid ISIN Code
    regex = "^[A-Z]{2}[0-9A-Z]{9}[0-9]{1}$" #original function contained an option to check for dashes, removed in prev. step now

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

def check_luhn(isin_input):
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
    
    if check_function is None:
        check_function = yf.Ticker
    try:
        if check_function(user_input).info['regularMarketPrice'] is not None:
            return True
        else: 
            return False
    except Exception:
        return False

############
def check_isin_ticker_input(user_input:str, check_function = None):
    '''checks the users input of stock data and returns true or false depending on its validity'''
    
    #At this point I will stop optimizing the code/isin/ticker checkup.
    #IT could still be improved i.e. i could save sucessfull checks in a lookup to avoid multiple checks of the same thing 
    
    if not isinstance(user_input, str):
        return False
    
    preprocess_input = input_case_insensitive(remove_dashes(user_input))

    if preprocess_input == '':
        return False
    
    if len(preprocess_input) < 12:
        #must be a ticker/ or invald isin, enter ticker checkup
        validity = check_ticker(preprocess_input, check_function= check_function)
        
        return validity
    else:
        if (isValid_ISIN_Code(preprocess_input) and check_luhn(preprocess_input)):
            return True
        else:
            return False