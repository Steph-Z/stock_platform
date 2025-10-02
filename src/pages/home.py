from dash import html, dcc
import dash_bootstrap_components as dbc
from utils.config import flatly_colors

#Layout main Page 
explain_text_german = """
### Hallo liebe Besucher:innen! 

Mein Name ist Stephan und ich habe vor kurzem meinen Master in Data Science abgeschlossen.
Diese Seite/ Dasboard ist ein "passion project" um noch mehr über saubere Software und AI Engineering praktiken zu lernen.
Nutzt gern die Menüs unter diesem Text um zu sehen welche Techniken ich dabei umsetze und was man auf dieser Seite machen kann. Der gesamte Code des Projekts kann öffentlich auf meinem GitHub eingesehen werden (inkl. Tests):

https://github.com/Steph-Z/stock_platform 

---

**Bitte meldet euch bei mir falls ihr Anregungen oder Fragen jeglicher Art habt**

---

Da es in diesem Bereich Englisch die Sprache ist, die am meisten genutzt wird, ob fürs Coding an sich,
Kommentare im Code aber auch die Zusammenarbeit mit internationalen Kolleg:innen, habe ich entschieden dieses Projekt auf Englisch zu verfassen.

---

**Ich hoffe ihr habt bei eurem Besuch auf dieser Seite genauso viel Spaß wie ich dabei hatte, diese Seite zu entwickeln** (außer das Zentrieren der html-Blöcke, das war kein Spaß)!

"""  

explain_text_engl = """ 
### Hello dear visitor!

My name is Stephan and I am a recent graduate with a Masters Degree in Data Science.
This side/dashboard is a learning project to strengthen my ability with Software engineering best practices for Data Science and AI Engineerig.  
Use the menus below to find out more about the project. The code of the project (incl. tests) is publicly available on my GitHub under:

https://github.com/Steph-Z/stock_platform 

---

**Please feel free to reach out in case you have any suggestions!**

---

Although I am German, English is the language used to write and document code most of the time. Additionally collaboration across international teams requires English as well. As a result, I decided to use English for this project.

---

**I hope you enjoy your visit on the page as much as I had building it** (except for centering the different blocks of the layout, that was pain)!
"""

software_text = """
#### Git/GitHub:  
  I work on two branches: The main branch is always deployed (see CI/CD).  
  On the working branch I update the app and once I like the new state, I push to main.  
  Since this project is done by myself, I don’t worry too much about committing every small local change immediately.

---

#### Testing:  
  At the moment, I’m using a small set of unit tests and a basic integration test for the Ticker/ISIN input.  
  I set them up to minimize calls to yfinance using a custom checker during testing.  
  Even in production I try to reduce calls to yfinance by validating ISIN inputs using a regular expression and Luhn's algorithm.  
  In the coming days, I plan to add a test for the dashboard itself by emulating user inputs, so a more thorough integration test of the overall app.

---

#### CI/CD:  
  This website is the CD part of a CI/CD pipeline.  
  I use GitHub Actions to automatically run tests (including flake8) whenever I push to the main branch.  
  Once tests pass successfully, Render deploys the updated version of the site.

---

#### Code Structure:  
  I encourage you to look at the structure of the project.  
  It's set up to be scalable and reusable for others as well.  
  I maintain a requirements.txt using pipreqs and the project is documented in a README, including a guide for local setup.

---

#### Caching Strategy:  
  A users Inputs/ Stock downloads are cached for up to 10 minutes for up to 10 Stocks. 
"""

what_you_can_do = """
#### Dashboard Section:  
You can explore different stocks by entering their Ticker or ISIN.  
The dashboard displays a chart of the last 5 years and a table showing recent trading data.  

**LLM Analysis**
The LLM Tab is connected to the HuggingFace API. Throuh a prompt injection, RAG-inspired, pipeline an LLM is queried qith a standardizes prompt to explain 
the stocks price movement for the selected period. For that the llm has acess to the relevant data. 
To control the cost of this feature only a three month period can be used, also the additional questions input has a limited input size. 
In addition, the number of output tokens is capped.

**Feel free to test everything in the Dashboard tab**

---

#### Upcoming Features:  
I’m actively working on expanding the dashboard’s functionality.  
Here are the next major improvements I plan to implement:

**Enhanced testing**  
Add full integration tests that emulate user inputs across the dashboard.

**Metrics**
Add a comprehensive table with metrics like volatility etc. in the tab. 
Add custom timeframes for the metrics next to the standard

**Plot**
Add moving average dropdown menu to add a moving average line to the plot; 200 days
"""
  
#The Container for the pages content. A Row vor each Contents row and a column so I can have a multi column layout as well as center everything on the page 
#Problem is: the NAVBAR; Since it uses a combination of different object with different paddings 
#The standard centering does not work here. So I need a Div in the col to account for that behavior. 
#The dummy LAyout for all future single col content that should e centered on the page is: 
#Since this might change if I introduce new sides we set it as a variable:

layout = dbc.Container([
    dbc.Row(
        dbc.Col(
            dbc.Accordion([
                dbc.AccordionItem(
                    [
                        dcc.Markdown(explain_text_engl, className='text-center', style= {"color": flatly_colors["light"]})
                    ],
                    title=html.Div([
                        html.H3("Introduction", className='text-center')
                    ]),
                    item_id="intro"
                )
            ], start_collapsed=False,
                class_name="bg-light text-dark"),
            width=10,
            #style={'paddingRight': pad_for_centering}
        ),
        justify='center',
        className='mt-4'
    ),

    dbc.Row(
        dbc.Col(
            dbc.Accordion([
                dbc.AccordionItem(
                    [
                        dcc.Markdown(explain_text_german, className='text-center', style= {"color": flatly_colors["light"]})
                    ],
                    title=html.H3("Einleitung", className='text-center'),
                    item_id="einleitung"
                )
            ], start_collapsed=True),
            width=10,
            #style={'paddingRight': pad_for_centering} #not needed for accordion anymore 
        ),
        justify='center',
        className='mt-4'
    ),
    dbc.Row(
        dbc.Col(
            dbc.Accordion([
                dbc.AccordionItem(
                    [
                        dcc.Markdown(what_you_can_do, className='text-center', style= {"color": flatly_colors["light"]})
                    ],
                    title=html.H3('What you can do on this Side/Dashboard', className='text-center'),
                    item_id='contentgeneral'
                )
            ], start_collapsed=True),
            width=10,
            #style={'paddingRight': pad_for_centering} #not needed for accordion anymore 
        ),
        justify='center',
        className='mt-4'
    ),
    dbc.Row(
        dbc.Col(
            dbc.Accordion([
                dbc.AccordionItem(
                    [
                        dcc.Markdown(software_text, className='text-center')
                    ],
                    title=html.H3('Software/AI engineering practises', className='text-center'),
                    item_id='parctices'
                )
            ], start_collapsed=True),
            width=10,
            #style={'paddingRight': pad_for_centering} #not needed for accordion anymore 
        ),
        justify='center',
        className='mt-4'
    )
], fluid=True)

