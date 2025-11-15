from dash import Dash, dash_table, html, dcc,  Input, Output
import pandas as pd
import plotly.express as px
from datetime import date
from django_plotly_dash import DjangoDash
import numpy as np

app = DjangoDash('conversion_ratio',add_bootstrap_links=True)  
app.css.append_css({ "external_url" : "/static/css/conversion_ratio.css" })


# df = pd.read_csv('/Users/varadmore/workspace/sharp_data/whisselrealtygroup_opp_data.csv')
df = pd.read_csv('/Users/saikiran/Desktop/interface/conversion_ration/whisselrealtygroup_opp_data.csv')

# df = pd.read_csv('/Users/varadmore/Downloads/whisselrealtygroup_opp_data.csv')


def get_agent_data(df):
    # get unique agents and their opps
    df_agents = df.groupby('opp_assigned_osa', dropna=True).count().reset_index()

    # Filter only the columns of interest
    df_agents = df_agents[['opp_assigned_osa', 'opp_appt_date', 'opp_appt_met_date', 'opp_agreement_signed_date', 'opp_under_contract_date', 'opp_settlement_date']]

    # Calculate the ratios
    df_agents['show_up_rate'] = df_agents['opp_appt_met_date'].div(df_agents['opp_appt_date']) * 100
    df_agents['signed_ratio'] = df_agents.get('opp_agreement_signed_date', 0).div(df_agents['opp_appt_met_date']) * 100
    df_agents['closed_ratio'] = df_agents['opp_settlement_date'].div(df_agents['opp_appt_met_date']) * 100

    # Rounding Off
    df_agents.show_up_rate = df_agents.show_up_rate.round(1)
    df_agents.signed_ratio = df_agents.signed_ratio.round(1)
    df_agents.closed_ratio = df_agents.closed_ratio.round(1)

    df_agents.fillna(0, inplace = True)
    df_agents = df_agents.replace([np.inf, -np.inf], "NaN")

    # Rename columns
    df_agents = df_agents.rename(columns={"opp_assigned_osa": "Agent Names"})
    # df_agents = df_agents.rename(columns={"opp_stage": "total_opportunities"})
    df_agents = df_agents.rename(columns={"opp_appt_date": "Appointment Assigned"})
    df_agents = df_agents.rename(columns={"opp_appt_met_date": "Appointment Showed"})
    df_agents = df_agents.rename(columns={"opp_agreement_signed_date": "Signed"})
    df_agents = df_agents.rename(columns={"opp_under_contract_date": "Contracted"})
    df_agents = df_agents.rename(columns={"opp_settlement_date": "Closed"})
    df_agents = df_agents.rename(columns={"show_up_rate": "Show Up Rate"})
    df_agents = df_agents.rename(columns={"signed_ratio": "Signed Ratio"})
    df_agents = df_agents.rename(columns={"closed_ratio": "Closed Ratio"})

    return df_agents


df_agents = get_agent_data(df)


# Callback for transaction Type
# @app.callback(
#     # Output('agents-dropdown', 'options'),
#     Input('transaction-type-dropdown', 'value')
# )
# def update_output(value):
#     transaction_type = value
#     print("transaction_type", transaction_type)

#     if transaction_type == 'Buyer':
#         df_filtered = df[df['opp_transaction_type'] == 'Buyer']
#     elif transaction_type == 'Seller':
#         df_filtered = df[df['opp_transaction_type'] == 'Seller']
#     else:
#         df_filtered = df

#     df_filtered

@app.callback(
    Output('output-container', 'children'),
    Input('agents-dropdown', 'value'),
    Input('date-picker-range', 'start_date'),
    Input('date-picker-range', 'end_date')
)
def update_output(value, start_date, end_date):
    selected_agents = value

    if not selected_agents:
        selected_agents = df_agents['Agent Names']

    df_filtered = df[(df['opp_created_ts'] >= start_date) & (df['opp_created_ts'] <= end_date)]

    df_filtered = get_agent_data(df_filtered)
    df_filtered = df_filtered[df_filtered['Agent Names'].isin(selected_agents)]

    # Stages = ['closed', 'contracted', 'signed', 'Appointment Showed', 'Appointment Assigned',]
    # bar_graph_agent_opp_stages = px.histogram(df_filtered, x=Stages, y='Agent Names', barmode='group', title='Opportunities by Stages')
    # bar_graph_agent_opp_stages.update_layout(legend_title="Stages", xaxis_title="Count", yaxis_title="Stages")

    # date_range_agent_opp_stages = px.line(df_filtered, x='Agent Names', y=['Appointment Assigned', 'Appointment Showed', 'signed', 'contracted', 'closed'], title='Opportunities by Stages')
    # date_range_agent_opp_stages.update_layout(legend_title="Stages")
    # date_range_agent_conv_ratio = px.line(df_filtered, x='Agent Names', y=['show_up_rate', 'signed_ratio', 'closed_ratio'], title='Conversion Ratios')
    # date_range_agent_conv_ratio.update_layout(legend_title="Conversion Ratio")

    return [dash_table.DataTable(
            id='table',
            sort_action='native',
            
            data=df_filtered.to_dict('records'), 
            style_header={'fontweight': 'bold', 'textAlign': 'center'},
            style_cell={'textAlign': 'left'},
            style_data_conditional=[
                {
                    'if': {'row_index': 'odd'},
                    'backgroundColor': 'rgb(248, 248, 248)'
                },
                {
                    'if': {
                        'filter_query': '{Show Up Rate} >= 50',
                        'column_id': 'Show Up Rate'
                            },
                            'backgroundColor': '#28a745',
                            'color': 'white'
                },
                {
                    'if': {
                        'filter_query': '{Show Up Rate} < 50 and {Show Up Rate} > 40',
                        'column_id': 'Show Up Rate'
                            },
                            'backgroundColor': '#F3B007',
                            'color': 'black'
                },
                {
                    'if': {
                        'filter_query': '{Show Up Rate} <= 40',
                        'column_id': 'Show Up Rate'
                            },
                            'backgroundColor': '#dc3545',
                            'color': 'white'
                },
                {
                    'if': {
                        'filter_query': '{Closed Ratio} >= 20',
                        'column_id': 'Closed Ratio'
                            },
                            'backgroundColor': '#28a745',
                            'color': 'white'
                },
                {
                    'if': {
                        'filter_query': '{Closed Ratio} > 10 && {Closed Ratio} < 20',
                        'column_id': 'Closed Ratio'
                            },
                            'backgroundColor': '#F3B007',
                            'color': 'black'
                },
                {
                    'if': {
                        'filter_query': '{Closed Ratio} <= 10',
                        'column_id': 'Closed Ratio'
                            },
                            'backgroundColor': '#dc3545',
                            'color': 'white'
                }

            ],

            columns=[{"name": i, "id": i} for i in df_filtered.iloc[:, [0, 1, 2, 6, 3, 7, 5, 8]].columns]),

            # dcc.Graph(figure=bar_graph_agent_opp_stages),
            # dcc.Graph(figure=date_range_agent_opp_stages),
            # dcc.Graph(figure=date_range_agent_conv_ratio),
            ]


# Dash App Layout
app.layout = html.Div(
    children=[

        html.Label('Filter Agents: '),
        
        dcc.Dropdown(id='agents-dropdown', options=df_agents['Agent Names'], searchable=True, clearable=True, multi=True, placeholder="Search",),
        html.Br(),
        # dcc.Dropdown(id='transaction-type-dropdown', options=[{'label': 'Buyer', 'value': 'Buyer'}, {'label': 'Seller', 'value': 'Seller'}], searchable=True, clearable=True, multi=True, placeholder="Search",),
        html.Label('Select Date Range: '),
        html.Br(),
        dcc.DatePickerRange(
        id='date-picker-range',
        min_date_allowed=date(2018, 1, 1),
        max_date_allowed=date.today(),
        initial_visible_month=date.today(),
        start_date=date(2018, 1, 1),
        end_date=date.today()
        ),
        
        html.Div(id='output-container'),
]
)
