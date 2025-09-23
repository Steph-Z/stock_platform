from dash import html, dcc

#Layout main Page 
explain_text = """This Dashboard is a Work in progress to learn more Software engineering best practices. I test the code, use CI/CD workflows and build a robust 
application. Feel free to pick any Stock you like and explore the tabs. The Github repository can be found under https://github.com/Steph-Z/stock_platform.
\n I hope you enjoy as much as I did building the page."""  

layout = html.Div([ #short learning. a Div is a container for almost anything that flows and can be anything
    html.H1("Stock Dashboard", style={'textAlign': 'center'}),    
    dcc.Markdown(explain_text)
    ])