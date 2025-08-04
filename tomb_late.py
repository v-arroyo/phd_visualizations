import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine
import plotly.io as pio

engine = create_engine('mysql+pymysql://victoria:amulets123@localhost:3306/phd_v5')

query = """
SELECT 
    s.site_name,
    owner,
    super,
    sub,
    COUNT(burial_id) as total_burials
FROM burials b
JOIN sites s
ON s.site_id = b.site_id
WHERE temp = 'late napatan' AND b.site_id IN (1,2)
GROUP BY 1,2,3,4
"""

df = pd.read_sql(query, engine)

custom_colors = ['#e9724d', '#92cad1', '#d6d727', '#79ccb3', '#868686']

fig = px.bar(
    df,
    x="super",
    y="total_burials",
    color="owner",
    facet_col="site_name",
    facet_row="sub",
    text="total_burials",
    title="Late Napatan tomb structure",
    labels={"super": "superstructure", "sub": "substructure", "site_name": "site"},
    color_discrete_sequence=custom_colors,
    template="plotly_white"
)

fig.update_layout(xaxis={'categoryorder': 'total descending'}, 
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.20,
        xanchor="center",
        x=0.40,
        traceorder='reversed'),
    font=dict(
        family="Verdana, sans-serif",
        color='black',
        size=10),
    legend_title_text='',
    #yaxis=dict(
        #tickmode='linear',
        #dtick=1),
    margin=dict(l=0, r=10, t=50, b=0),
    autosize=True,
    title_font=dict(size=10)
)

fig.update_traces(textposition='auto')
fig.update_xaxes(title_text='')
fig.update_yaxes(title_text='')

pio.write_image(fig, 'images/tomb_late.png',scale=3, width=450, height=350)