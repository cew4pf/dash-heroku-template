%%capture

# setup
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import dash
from jupyter_dash import JupyterDash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']



# accessing and cleaning data
gss = pd.read_csv("https://github.com/jkropko/DS-6001/raw/master/localdata/gss2018.csv",
                 encoding='cp1252', na_values=['IAP','IAP,DK,NA,uncodeable', 'NOT SURE',
                                               'DK', 'IAP, DK, NA, uncodeable', '.a', "CAN'T CHOOSE"])

mycols = ['id', 'wtss', 'sex', 'educ', 'region', 'age', 'coninc',
          'prestg10', 'mapres10', 'papres10', 'sei10', 'satjob',
          'fechld', 'fefam', 'fepol', 'fepresch', 'meovrwrk'] 
gss_clean = gss[mycols]
gss_clean = gss_clean.rename({'wtss':'weight', 
                              'educ':'education', 
                              'coninc':'income', 
                              'prestg10':'job_prestige',
                              'mapres10':'mother_job_prestige', 
                              'papres10':'father_job_prestige', 
                              'sei10':'socioeconomic_index', 
                              'fechld':'relationship', 
                              'fefam':'male_breadwinner', 
                              'fehire':'hire_women', 
                              'fejobaff':'preference_hire_women', 
                              'fepol':'men_bettersuited', 
                              'fepresch':'child_suffer',
                              'meovrwrk':'men_overwork'},axis=1)
gss_clean.age = gss_clean.age.replace({'89 or older':'89'})
gss_clean.age = gss_clean.age.astype('float')



# problem 1
markdown_text = '''
According to the [Center for American Progress](https://www.americanprogress.org/issues/women/reports/2020/03/24/482141/quick-facts-gender-wage-gap/), the gender wage gap is, in essence "the difference in earnings between women and men," and in the United States at the very least, it usually refers to the fact that women do not earn as much money as men. These differences become even more pronounced when looking at salaries for women of color. Census Bureau data on median annual income indicates that women earn only about 80% much as men, which translates to approximately 82 cents earned for women for every dollar earned by a man.

Many factors contribute to the observed differences in wages earned between men and women, as well as the influence a woman's race can have on her earning compared to men (and, in fact, other women). The [Center for American Progress](https://www.americanprogress.org/issues/women/reports/2020/03/24/482141/quick-facts-gender-wage-gap/) highlights several. These include differences in:
* Occupations: Positions in female-dominated industries, such as nursing and teaching, disproportionately generally receive lower salaries than those with greater representation of male workers, such as construction.
* Experience: The responsibility of caring for the home, children, and other relatives often still falls to women. This arrangment results in experience gaps between women obligated to leave the workforce and men who maintained their jobs.
* Hours worked: In addition, shouldering the domestic responsibilities outlined above lead to fewer hours worked for women compared to men.
* Discrimination: Paying men and women different amounts on the basis of sex remains illegal in the United States, as it has been for nearly 60 years now. However, though overt discrimination is forbidden, there are often subtler tactics employers still use to engage in this illicit practice.

**Please note that this information is taken from the [Center for American Progress](https://www.americanprogress.org/issues/women/reports/2020/03/24/482141/quick-facts-gender-wage-gap/) and is based on the work they have done. I do not claim any of information as my own.**

The data for this dashboard comes from the [General Social Survey (GSS)](http://www.gss.norc.org/About-The-GSS), a survey conducted annually by the National Opinion Research Center (NORC) at the University of Chicago that aims to, in a sense, "take the pulse" of the American public on a board range of relevant social, political, economic, and psychological issues. 

Since 1972, the National Opinion Research Center (NORC) at the  GSS has collected demographic information and opinions from thousands of Americans of all different races, ethnicities, and lifestyles. Certain topics are particularly relevant to an analysis on the gender wage gap, such as gender, annual income, employment specifics (e.g. hours worked, occupational prestige of both the indivual him or herself and his or her parent(s)), and perceptions of gender roles in the workforce and families (e.g. whether men work too much, whether women should work at all, and how this affects family life).
'''


# problem 2
gss_clean_display = gss_clean.groupby('sex').agg({'income': 'mean',
                                                 'job_prestige': 'mean',
                                                 'socioeconomic_index': 'mean',
                                                 'education': 'mean'}).reset_index()

gss_clean_display = round(gss_clean_display, 2)

gss_clean_display = gss_clean_display.rename({'sex': 'Sex',
                                             'income': 'Annual Income',
                                             'job_prestige': 'Occupational Prestige',
                                             'socioeconomic_index': 'Socioeconomc Status',
                                             'education': 'Education'}, axis = 1)

table = ff.create_table(gss_clean_display)
table.show()



# problem 3
gss_clean['male_breadwinner'] = gss_clean['male_breadwinner'].astype('category') 

gss_clean['male_breadwinner'] = gss_clean['male_breadwinner'].cat.reorder_categories(['strongly disagree', 'disagree', 'agree','strongly agree'])

gss_clean.male_breadwinner.value_counts().sort_index()

breadwinner_bar = gss_clean.groupby(['sex', 'male_breadwinner']).size().reset_index()
breadwinner_bar = breadwinner_bar.rename({0:'count'}, axis = 1)

bread_bar = px.bar(breadwinner_bar, x = 'male_breadwinner', y = 'count', color = 'sex', barmode = 'group',
      labels = {'male_breadwinner': 'Men should be the primary breadwinners in a family', 'count': 'Number of responses'})

bread_bar.show()



# problem 4
prestige_scatter = px.scatter(gss_clean, x = 'job_prestige', y = 'income',
          color = 'sex', trendline = 'ols',
          hover_data = ['education', 'socioeconomic_index'],
          labels = {'job_prestige': 'Occupational Prestige Score', 'income': 'Annual Income'})

prestige_scatter.show()



# problem 5
income_box = px.box(gss_clean, x = 'sex', y = 'income', color = 'sex',
                    labels = {'sex': '', 'income': 'Annual Income'})

# using the framework from Surfuing the Data Pipeline with Python (Ch. 12: Interactive Data Visualizations and Dashboards)
# add help from stack overflow: https://stackoverflow.com/questions/61693014/how-to-hide-plotly-yaxis-title-in-python
income_box.update_layout(showlegend = False, xaxis = {'visible': False})

income_box.show()

prestige_box = px.box(gss_clean, x = 'sex', y = 'job_prestige', color = 'sex',
                    labels = {'job_prestige': 'Occupational Prestige Score'})

# using the framework from Surfuing the Data Pipeline with Python (Ch. 12: Interactive Data Visualizations and Dashboards)
# add help from stack overflow: https://stackoverflow.com/questions/61693014/how-to-hide-plotly-yaxis-title-in-python
prestige_box.update_layout(showlegend = False, xaxis = {'visible': False})

prestige_box.show()



# problem 6
# create new dataframe with only income, sex, job_prestige
new_df = gss_clean[['income', 'sex', 'job_prestige']]

# break job_prestige into six categories with equally sized ranges
new_df['prestige_cat'] = pd.cut(new_df['job_prestige'], bins = 6)

# remove rows with missing values
new_df = new_df.dropna()

new_df['prestige_cat'] = new_df['prestige_cat'].astype('str')

pres_income_box = px.box(new_df, y = 'income', color = 'sex',
                        facet_col = 'prestige_cat', facet_col_wrap = 2,
                        color_discrete_map = {'male':'blue', 'female':'red'})
pres_income_box.show()

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

new_app = JupyterDash(__name__, external_stylesheets=external_stylesheets)

new_app.layout = html.Div([
    html.H1("Exploring the Gender Wage Gap Using Data from the 2019 General Social Survey (GSS)"),
    
    html.H2('Overview'),
    dcc.Markdown(children = markdown_text),
    
    html.H2('Average Annual Income, Occupational Prestige Score, Socioeconomic Status, and Years of Education by Gender'), 
    dcc.Graph(figure = table),
    
    html.H2('Responses to the Statement on the GSS:'),
    html.H3('It is much better for everyone involved if the man is the achiever outside the home and the woman takes care of the home and family.'),
    dcc.Graph(id = "bread_bar", figure = bread_bar),
    
    html.H2('Annual Income Compared to Occupational Prestige Score by Gender'),
    dcc.Graph(figure = prestige_scatter),
    
    html.Div([
        html.H2('Distribution of Annual Income by Gender'),
        dcc.Graph(figure = income_box)], style = {'width': '48%', 'float': 'left'}),
    
    html.Div([
        html.H2('Distribution of Occupational Prestige Score by Gender'),
        dcc.Graph(figure = prestige_box)], style = {'width': '48%', 'float': 'right'}),
    
    html.H2('Income Distribution by Occupational Prestige Score Category and Gender'),
    dcc.Graph(figure = pres_income_box)
    
]
)

if __name__ == '__main__':
    new_app.run_server(mode = 'inline', debug = True, port = 8051)

