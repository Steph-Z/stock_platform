import pytest
import re
import yfinance as yf

from utils.isin_ticker_checkups import input_case_insensitive, remove_dashes, isValid_ISIN_Code, check_luhn, check_ticker, check_isin_ticker_input


#I write this for learning purposes and (ofc) use LLM help for it. 
#I do not copy paste LLM code in a learning project, but learn the concepts here as well as asking a lot of questions. 
#i.e. I would have left the faketicke class as is (just the fake ticker), with the LLM help I learned how to use a decorator for the mck class to make it
#widely available. For me personally it helps to learn a lot. Not everything that works is already good enough 
# BTW I first learned about decorators, when implementing a transformer in pytorch to avoid the calculation and tracking of gradients for certain functions

###Mock class to avoid calling yfinance for the test of ticker, We now always need to use AAPL to test ticker symbols
@pytest.fixture
def FakeTicker():
    class _FakeTicker: #cconvention to remember: a leading _ indicates this is for internal use 
        def __init__(self, ticker):
            self.info = {'regularMarketPrice': 1} if ticker == 'AAPL' else {}
    return _FakeTicker
        
#test individual functions, so called unit test
#The test of the overall input function is technically an integration test since its a function of functions 

#Test for the helper functions , unit tests
#write the ranw inputs vs the expected outcome for the function
@pytest.mark.parametrize('raw,expected', [
    ('        aApL 121212', 'AAPL121212'),
     ("\t us-0378331005 \n", "US-0378331005"),
    ("Mixed CASE   Tabsand Spaces", "MIXEDCASETABSANDSPACES")
])

def test_input_case_insensitive(raw, expected):
    '''tests the function, should strip and delete all spaces or tabs'''
    assert input_case_insensitive(raw) == expected
    
    

@pytest.mark.parametrize('raw, expected', [ #test if dashes are handles properly 
        ("US-0378331005", "US0378331005"),
    ("ABC-123-XYZ", "ABC123XYZ"),
    ("----DASHES----", "DASHES"),
])

def test_remove_dashes(raw, expected):
    '''tests the function, should strip and delete all spaces or tabs'''
    assert remove_dashes(raw) == expected
    


@pytest.mark.parametrize("isin, valid", [
    ("US0378331005", True),    # real Apple ISIN and different ways to write it 
    ("US0378331004", True),     #wrong checksum but should be true as luhn is not checked 
    ("us0378331005", False),    #spelling is not capitalized
    ("zzzzzz", False),          #cause not right len, empty str are handled in another function
    ("  US0378331005", False)   #spaces initially are not handled
])

def test_isValid_ISIN_Code(isin, valid):
    '''tests the re ex test for isin check'''
    assert isValid_ISIN_Code(isin) == valid
    
    
@pytest.mark.parametrize("isin, valid", [
    ("US0378331005", True),#apple isin
    ("US0378331002", False), #wrong check number
    ("US0738331005", False), #permutation in isin 

])

def test_check_luhn_computes_checksum_correctly(isin, valid):
    '''
    check_luhn assumes the ISIN passed re ex validation,
    '''
    assert check_luhn(isin) is valid
    
##Test for the ticker cheker using the mock class 

@pytest.mark.parametrize("symbol, expected", [
    ('AAPL', True),   
    ('GOOG', False),  # not in dict
    ('', False),      
    ('1234', False),  
])

def test_check_ticker_with_injected_fake(FakeTicker, symbol, expected):
    '''
    check_ticker should call the injected class for checking not yfinance 
    '''
    assert check_ticker(symbol, check_function=FakeTicker) is expected
    
    
#Integration test of the full thing; now I use more LLM code as it is quite the hastle to build the str by hand;
#I make sure that i have the cases '', a valid ticker ( apple) , a valid isin, isin with wrong check number, a permutation, and werid spacings 

#the llm output actually provides all of these 
@pytest.mark.parametrize("user_input, expected", [
    # Valid ISIN without dashes, mixed casing, extra whitespace
    (" us-0378331005 ", True),
    # Valid ISIN, no preprocessing needed
    ("GB0002634946", True),
    # Invalid ISIN (bad checksum)
    ("US0378331004", False),
    # Valid ticker
    ("  aapl  ", True),
    # Invalid ticker
    ("NOSUCH", False),
    # Non-string input
    (12345, False),
    # Empty or whitespace-only
    ("     ", False),
    # Short string that is alphanumeric but not a real ticker
    ("XYZ", False),
])

def test_check_isin_ticker_input_end_to_end(FakeTicker, user_input, expected):
    """
    This integration-style test drives the full pipeline:
    """
    result = check_isin_ticker_input(user_input, check_function=FakeTicker)
    assert result is expected
    
    
    #Tests are passed for now. 
 #   tests\test_user_input.py ...                                                                                                              [100%]
#27 passed in 1.22s ====