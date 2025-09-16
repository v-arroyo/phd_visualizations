import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine
import plotly.io as pio

engine = create_engine('mysql+pymysql://victoria:amulets123@localhost:3306/phd_v5')

query = """
WITH expanded_forms AS (
    SELECT 
        s.site_name,
        a.form AS form,
        a.amulet_id
    FROM amulets a
    JOIN burials b ON b.burial_id = a.burial_id
    JOIN sites s ON s.site_id = b.site_id
    WHERE 
        dating = 'napatan'
        AND temp = '25th'
        AND s.site_id IN (4,5,6,7,8,9,10)
        AND a.form IS NOT NULL
        and super != 'pyramid' 
        and sub not in ('chambers', 'cave tomb')
        and type != 'deity'

    UNION ALL

    SELECT 
        s.site_name,
        a.form2 AS form,
        a.amulet_id
    FROM amulets a
    JOIN burials b ON b.burial_id = a.burial_id
    JOIN sites s ON s.site_id = b.site_id
    WHERE 
        dating = 'napatan'
        AND temp = '25th'
        AND s.site_id IN (4,5,6,7,8,9,10)
        AND a.form2 IS NOT NULL
        and super != 'pyramid' 
        and sub not in ('chambers', 'cave tomb')
        and type != 'deity'

    UNION ALL

    SELECT 
        s.site_name,
        a.form3 AS form,
        a.amulet_id
    FROM amulets a
    JOIN burials b ON b.burial_id = a.burial_id
    JOIN sites s ON s.site_id = b.site_id
    WHERE 
        dating = 'napatan'
        AND temp = '25th'
        AND s.site_id IN (4,5,6,7,8,9,10)
        AND a.form3 IS NOT NULL
        and super != 'pyramid' 
        and sub not in ('chambers', 'cave tomb')
        and type != 'deity'
)
SELECT 
    site_name,
    CASE 
        WHEN form = 'deity' THEN 'unknown deity'
        WHEN form = 'deities' THEN 'group of deities'
        ELSE form
    END AS form,
    COUNT(amulet_id) AS total
FROM expanded_forms
WHERE form NOT IN ('udjat')
GROUP BY 1,2
"""

df = pd.read_sql(query, engine)

custom_colors = ['#e9724d', '#92cad1', '#d6d727', '#79ccb3', '#868686']

fig = px.bar(
    df,
    x="form",
    y="total",
    color="site_name",
    text="total",
    barmode='stack',
    title="25th Dynasty non-elite amulet motifs (excluding deities and udjat)",
    labels={"super": "superstructure", "sub": "substructure", "site_name": "site"},
    color_discrete_sequence=custom_colors,
    template="plotly_white"
)

fig.update_layout(xaxis=dict(categoryorder='total descending', automargin=True, title_standoff=0), 
    legend=dict(
        #orientation="h",
        yanchor="bottom",
        y=0.40,
        xanchor="center",
        x=0.80,
        traceorder='reversed'),
    font=dict(
        family="Verdana, sans-serif",
        color='black',
        size=6),
    legend_title_text='',
    #yaxis=dict(
        #tickmode='linear',
        #dtick=1),
    margin=dict(l=0, r=0, t=15, b=0),
    autosize=True,
    title_font=dict(size=6)
)

fig.update_traces(textposition='outside', textfont_size=5, width=0.4)
fig.update_xaxes(title_text='')
fig.update_yaxes(title_text='')

pio.write_image(fig, 'images/chapter5/25_amulets_form_rest.png',scale=4, width=500, height=250)