from dash import html, dcc
import dash_bootstrap_components as dbc
from utils.config import pad_for_centering

#Layout main Page 
explain_text_german = """Hallo liebe Besucher:innen! 

Mein Name ist Stephan und ich habe vor kurzem meinen Master in Data Science abgeschlossen.
Diese Seite/ Dasboard ist ein "passion project" um noch mehr über saubere Software und AI Engineering praktiken zu lernen.
Nutzt gern die Menüs unter diesem Text um zu sehen welche Techniken ich dabei umsetze und was man auf dieser Seite machen kann. Der gesamte Code des Projekts kann öffentlich auf meinem GitHub eingesehen werden (inkl. Tests):

https://github.com/Steph-Z/stock_platform 

**Bitte meldet euch bei mir falls ihr Anregungen oder Fragen jeglicher Art habt**

Da es in diesem Bereich Englisch die Sprache ist, die am meisten genutzt wird, ob fürs Coding an sich,
Kommentare im Code aber auch die Zusammenarbeit mit internationalen Kolleg:innen, habe ich entschieden dieses Projekt auf Englisch zu verfassen.
**Ich hoffe ihr habt bei eurem Besuch auf dieser Seite genauso viel Spaß wie ich dabei hatte, diese Seite zu entwickeln** (außer das Zentrieren der html-Blöcke, das war kein Spaß)!

"""  

explain_text_engl = """ Hello dear visitor!

My name is Stephan and I am a recent graduate with a Masters Degree in Data Science.
This side/dashboard is a learning project to strengthen my ability with Software engineering best practices for Data Science and AI Engineerig.  
Use the menus below to find out more about the project. The code of the project (incl. tests) is publicly available on my GitHub under:

https://github.com/Steph-Z/stock_platform 

**Please feel free to reach out in case you have any suggestions!**

Although I am german, english is the language used write and document code most of the time. Additionally collaboration across international teams requires english as well. As a consequence, I decided to use english for this project.

**I hope you enjoy your visit on the page as much as I had building it** (except for centering the different blocks of the layout, that was pain)!
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
                        dcc.Markdown(explain_text_engl, className='text-center')
                    ],
                    title=html.Div([
                        html.H3("Introduction", className='text-center')
                    ]),
                    item_id="intro"
                )
            ], start_collapsed=False),
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
                        dcc.Markdown(explain_text_german, className='text-center')
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
                        dcc.Markdown("""Currently (24.09.2025) I worked on an overhaul of the Layout (which you can see right now). But for that I removed most of the functionallity for now.
                                     Please come back tomorrow. Or have a look at the Repo to see the inner workings of the Side as well as the CI/CD Pipeline used to automatically deploy new versions. 
                                     Thank you for understanding!""", className='text-center')
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
                        dcc.Markdown('Software/AI engineering practises', className='text-center')
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

