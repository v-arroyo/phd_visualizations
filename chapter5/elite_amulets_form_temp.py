import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine
import plotly.io as pio
import plotly.graph_objects as go
import numpy as np

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
        AND s.site_id IN (4,5,8)
        AND a.form IS NOT NULL
        AND (super = 'pyramid' OR sub IN ('chambers', 'cave tomb'))

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
        AND s.site_id IN (4,5,8)
        AND a.form2 IS NOT NULL
        AND (super = 'pyramid' OR sub IN ('chambers', 'cave tomb'))

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
        AND s.site_id IN (4,5,8)
        AND a.form3 IS NOT NULL
        AND (super = 'pyramid' OR sub IN ('chambers', 'cave tomb'))
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
GROUP BY 1,2
"""

df = pd.read_sql(query, engine)

custom_colors = ['#e9724d', '#92cad1', '#d6d727', '#79ccb3', '#868686', '#2c3e50', '#a85d3a', '#9b8fd4', '#8a9a5b', '#d4a5a5', '#4a4a4a']

phase_order = [
    "pre-25th", "25th", "25th-EN", "25th-MN", "EN",
    "EN-MN", "EN-LN", "MN", "MN-LN", "LN"
]

pivot_df = df.pivot(index='form', columns='temp', values='total').fillna(0)
df_stacked = pivot_df.reset_index().melt(id_vars='form', var_name='temp', value_name='total')

fig = px.scatter(
    df,
    x="form",
    y="temp",
    color="total",
    text='total',                 
    color_continuous_scale='Sunset',
    title="Elite amulet types by chronological phase",
    size_max=20,
    template='plotly_white'                     
)

fig.update_layout(
    xaxis={'categoryorder': 'total descending'},
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.15,
        xanchor="center",
        x=0.50,
        traceorder='reversed'
    ),
    font=dict(
        family="Verdana, sans-serif",
        color='black',
        size=7
    ),
    legend_title_text='',
    margin=dict(l=0, r=10, t=20, b=0),
    autosize=True,
    title_font=dict(size=7)
)

fig.update_traces(textposition='top center', textfont_size=6)
fig.update_xaxes(title_text='')
fig.update_yaxes(title_text='', categoryorder='array', categoryarray=phase_order[::-1])

pio.write_image(fig, 'images/chapter5/elite_amulets_form_temp.png',scale=4, width=550, height=300)