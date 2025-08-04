import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine
import plotly.io as pio

pio.defaults.chromium_executable = '/usr/bin/chromium'

engine = create_engine('mysql+pymysql://victoria:amulets123@localhost:3306/phd_v5')

query = """
SELECT 
    s.site_name,
    b.owner,
    CASE 
        WHEN a.artifact_material = 'lapis' THEN 'lapis lazuli'
        WHEN a.artifact_material = 'sandalwood' THEN 'wood'
        WHEN a.artifact_material = 'cowrie shell' THEN 'shell'
        WHEN a.artifact_material = 'snail shell' THEN 'shell'
        ELSE a.artifact_material
    END AS material,
    COUNT(artifact_id) as count
FROM burials b
JOIN sites s
ON s.site_id = b.site_id
JOIN artifacts a
ON a.burial_id = b.burial_id
WHERE temp = '25th dyn.' AND b.site_id IN (1) AND a.artifact_material IS NOT NULL
GROUP BY 1,2,3
"""

df = pd.read_sql(query, engine)

custom_colors = ['#e9724d', '#92cad1', '#d6d727', '#79ccb3', '#868686']

fig = px.scatter(
    df,
    y="material",
    x="count",
    color="owner",
    symbol="owner",
    facet_col='site_name',
    title="25th dynasty object materials",
    labels={"owner": "owner", "site_name": "site"},
    color_discrete_sequence=custom_colors,
    template="plotly_white"
)

fig.update_layout(yaxis={'categoryorder': 'total ascending'}, 
    legend=dict(
        orientation="h",
        yanchor="top",
        y=-0.03,
        xanchor="right",
        x=0.90,
        traceorder='reversed'),
    font=dict(
        family="Verdana, sans-serif",
        color='black',
        size=8),
    legend_title_text='',
    margin=dict(l=0, r=5, t=40, b=0),
    autosize=True,
    title_font=dict(size=8)
)

fig.update_xaxes(title_text='')
fig.update_yaxes(title_text='')

pio.write_image(fig, 'phd_final/images/objects_mat_25_kurru.png',scale=3, width=450, height=450)