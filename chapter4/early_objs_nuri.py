import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine
import plotly.io as pio

engine = create_engine('mysql+pymysql://victoria:amulets123@localhost:3306/phd_v5')

query = """
SELECT 
    s.site_name,
    b.owner,
    a.artifact_type,
    COUNT(artifact_id) as count
FROM burials b
JOIN sites s
ON s.site_id = b.site_id
JOIN artifacts a
ON a.burial_id = b.burial_id
WHERE temp = 'EN' AND b.site_id IN (2)
GROUP BY 1,2,3
"""

df = pd.read_sql(query, engine)

custom_colors = ['#92cad1', '#e9724d','#d6d727', '#79ccb3', '#868686']

fig = px.scatter(
    df,
    x="owner",
    y="artifact_type",
    color="count",
    text="count",
    facet_col="site_name",
    title="Early Napatan royal object types",
    labels={"count": "Total", "site_name": "Site"},
    color_continuous_scale='Sunset',
    template="plotly_white"
)

fig.update_layout( 
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.70,
        xanchor="center",
        x=0.45,
        traceorder='reversed'),
    font=dict(
        family="Verdana, sans-serif",
        color='black',
        size=8),
    legend_title_text='',
    #yaxis=dict(
        #tickmode='linear',
        #dtick=1),
    margin=dict(l=0, r=10, t=40, b=0),
    autosize=True,
    title_font=dict(size=8)
)

fig.update_traces(textposition='middle right', textfont_size=6)
fig.update_xaxes(title_text='')
fig.update_yaxes(title_text='', categoryorder='category descending')
fig.update_xaxes(
    title_text='',
    categoryorder='category ascending',
    range=[-0.5, len(df['owner'].unique())-0.5],  # Tight range
    showgrid=True
)


pio.write_image(fig, 'images/chapter4/early_objs_nuri.png',scale=3, width=350, height=350)