import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine
import plotly.io as pio

engine = create_engine('mysql+pymysql://victoria:amulets123@localhost:3306/phd_v5')

query = """
SELECT 
    s.site_name,
    CASE 
        WHEN a.form = 'deity' THEN 'unknown deity'
        WHEN a.form = 'deities' THEN 'group of deities'
        ELSE a.form
    END AS form,
    COUNT(a.amulet_id) AS total
FROM amulets a
JOIN burials b ON b.burial_id = a.burial_id
JOIN sites s ON s.site_id = b.site_id
WHERE 
    dating = 'napatan'
    AND temp = '25th-EN'
    AND s.site_id IN (4,5,6,7,8,9,10)
    AND a.form IS NOT NULL
    AND a.form2 IS NULL
    AND a.form3 IS NULL
    AND super != 'pyramid' 
    AND sub NOT IN ('chambers', 'cave tomb')
    AND form IN ('udjat', 'quadruple udjat')
GROUP BY 1,2
"""

df = pd.read_sql(query, engine)

custom_colors = ['#e9724d', '#b19cd9', '#d6d727', '#79ccb3', '#868686']

fig = px.bar(
    df,
    x="form",
    y="total",
    color="site_name",
    text="total",
    barmode='group',
    title="25th Dynasty-Early Napatan non-elite udjat amulets",
    labels={"super": "superstructure", "sub": "substructure", "site_name": "site"},
    color_discrete_sequence=custom_colors,
    template="plotly_white"
)

fig.update_layout(xaxis=dict(categoryorder='total descending', automargin=True, title_standoff=0), 
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.21,
        xanchor="center",
        x=0.50),
        #traceorder='reversed'),
    font=dict(
        family="Verdana, sans-serif",
        color='black',
        size=8),
    legend_title_text='',
    #yaxis=dict(
        #tickmode='linear',
        #dtick=1),
    margin=dict(l=0, r=0, t=20, b=0),
    autosize=True,
    title_font=dict(size=8)
)

fig.update_traces(textposition='outside', textfont_size=6)
fig.update_xaxes(title_text='')
fig.update_yaxes(title_text='')

pio.write_image(fig, 'images/chapter5/25-EN_amulets_form1_udjat.png',scale=4, width=550, height=250)