import pandas as pd
import plotly.express as px
import plotly.io as pio
from sqlalchemy import create_engine

engine = create_engine('mysql+pymysql://victoria:amulets123@localhost:3306/phd_v5')

query = """
SELECT
    b.sub,
    b.super,
    COUNT(b.burial_id) AS total
FROM burials b
WHERE dating = 'napatan' 
AND sub != 'deposit'
AND b.site_id IN (1,2,4,5,6,7,8,9,10)
GROUP BY 1,2
"""

df = pd.read_sql(query, engine)

fig = px.scatter(
    df,
    x='sub',
    y='super',
    color='total',
    size='total',
    #text='total',
    title='<b>Correlation of super- and substructures</b>',
    color_continuous_scale='Sunset',
    template="plotly_white",
)

#fig.update_traces(textposition='outside')
fig.update_xaxes(title_text='')
fig.update_yaxes(title_text='')

fig.update_layout(
    yaxis={'categoryorder': 'total ascending'}, 
    legend=dict(
        orientation="h",
        yanchor="top",
        y=-0.10,
        xanchor="center",
        x=0.50),
        #traceorder='reversed'),
    font=dict(
        family="Verdana, sans-serif",
        color="black",
        size=8),
    legend_title_text='',
    margin=dict(l=0, r=10, t=50, b=0),
    autosize=True,
    title_font=dict(size=8)
    )

pio.write_image(fig, 'diversenile/images/tombs.png',scale=4, width=400, height=280)