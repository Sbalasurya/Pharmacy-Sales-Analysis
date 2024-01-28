# -*- coding: utf-8 -*-
"""Untitled1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1mR8sTH_AhP3PRF4B9n256-_op3P2UbPb
"""

# This script defines a Gradio interface for a billing software and sales analysis system. It includes functions to predict sales, generate various charts, and visualize sales data.
# The billing software interface allows users to input customer details, product information, and calculates the total bill.
# The overall sales analysis tab provides visualizations of total monthly consumption and total yearly consumption for different drug categories.
# The product analysis tab allows users to input start date, end date, and select a product to analyze its sales trends.

import gradio as gr
from datetime import date
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import gradio as gr
import pickle
import xgboost
from sklearn.preprocessing import LabelEncoder

# save the model to disk
filename = "C:/Users/yuges/OneDrive/Documents/pharma_model (1).sav"

# load the model from disk
loaded_model = pickle.load(open(filename, 'rb'))

# Load sales data from an Excel file
df = pd.read_excel("salesdaily.xlsx")
df['datum'] = pd.to_datetime(df['datum'])

# Extract relevant columns for M01AB category
df_m01ab = df[['M01AB','Year','Month']]
df_m01ab = df_m01ab.groupby(['Year', 'Month']).sum().reset_index()
t=True

# Function to predict sales for a given date range and drug category
def predict_sales(start_date,end_date,drug):
    # dates selected from celander and category(int) from options
    # Generate a range of dates
    dates = pd.date_range(start=start_date, end=end_date, freq='D')
    # Create the DataFrame with dates as the index
    df_test = pd.DataFrame(index=dates)
    df_test['Year'] = df_test.index.year
    df_test['Month'] = df_test.index.month
    df_test['Weekday Name'] = df_test.index.weekday
    df_test['day'] = df_test.index.day
    df_test['Drug'] = drug
    le = LabelEncoder()
    df_test['Weekday Name'] = le.fit_transform(df_test['Weekday Name'])
    df_test['predicted_quantity'] = loaded_model.predict(df_test)
    return df_test

# Sample prediction for the date range '2023-10-01' to '2023-10-31' for M01AB category
x=predict_sales('2023-10-01','2023-10-31',drug = 3)

# Functions to create different charts for sales analysis

# ... (Total Monthly Consumption of Each Category)
def chart1():
    melted_df = pd.melt(df, id_vars=['Year', 'Month'], value_vars=['M01AB', 'M01AE', 'N02BA', 'N02BE', 'N05B', 'N05C', 'R03', 'R06'],var_name='Category',value_name='Consumption')
    # Group the data by Category and Month and calculate the total consumption
    grouped_df = melted_df.groupby(['Category', 'Month']).sum().reset_index()
    # Create the bar chart
    fig = px.bar(grouped_df, x='Month', y='Consumption', color='Category', barmode='group')
    # Customize the layout
    fig.update_layout(
      title='Total Monthly Consumption of Each Category',
      xaxis_title='Month',
      yaxis_title='Consumption',
      legend_title='Category',
    )
    return fig

# ... (Pie chart for total consumption of each category)
def chart2():
    x=df[['M01AB', 'M01AE', 'N02BA', 'N02BE', 'N05B', 'N05C', 'R03', 'R06']].sum()
    fig=plt.figure()
    plt.pie(x,labels=['M01AB', 'M01AE', 'N02BA', 'N02BE', 'N05B', 'N05C', 'R03', 'R06'])
    return fig

# ... (Histogram for total monthly consumption of each category)
def chart3():
    data = {'M01AB':df['M01AB'].sum(),'M01AE':df['M01AE'].sum(),'N02BE':df['N02BE'].sum(),'N05B':df['N05B'].sum(),'N05C':df['N05C'].sum(),'R03':df['R03'].sum(),'R06':df['R06'].sum()}
    y1 = list(data.keys())
    x1 = list(data.values())
    fig=px.histogram(x1,y1)
    fig.update_layout(
      title='Total Monthly Consumption of Each Category',
      xaxis_title='Month',
      yaxis_title='Consumption',
    )
    return fig

# Function to create all charts
def create_charts():
    fig1 = chart1()
    fig2 = chart2()
    fig3 = chart3()
    return fig1, fig2, fig3

# ... (Line chart for predicted consumption of M01AB)
def chart4():
    #dates = pd.date_range(start='2023-10-01', end='2023-10-01', freq='D')
    dat=x.index
    blankIndex=[''] * len(x)
    x.index=blankIndex
    plt.plot(x["day"], x['predicted_quantity'])
    plt.xlabel("DAY")
    plt.ylabel("Predicted Consumption")
    plt.title("Graph for the given date & M01AB")
    # Customize the layout
    return plt

# ... (Bar chart for total yearly consumption of M01AB)
def chart5():
    dfs = df_m01ab.groupby('Year')['M01AB'].sum().reset_index()
    # Create the bar chart
    fig = px.bar(dfs, x='Year', y='M01AB', color='Year')
    # Customize the layout
    fig.update_layout(
        title='Total Yearly Consumption of M01AB',
        xaxis_title='Year',
        yaxis_title='Consumption',
        showlegend=False
    )
    return fig

# Function to create charts for product analysis
def create_charts1():
    fig1 = chart4()
    fig2 = chart5()
    return fig1, fig2

# Get the current date
today = date.today()

# Global variables for the billing software interface
numv=False
z=7
y=0

# Function to update the total in the billing software interface
def func(x):
    global y
    y+=x

# Format the current date
d1 = today.strftime("%d/%m/%Y")

# List of medicine categories
medicine=['M01AB', 'M01AE', 'N02BA', 'N02BE', 'N05B', 'N05C', 'R03', 'R06']

# Dictionary mapping medicine categories to product IDs and prices
md={"M01AB":[101,10],"M01AE":[102,202],"N02BA":[103,3],"N02BE":[104,4],"N05B":[105,20],"N05C":[106,30],"R03":[107,40],"R06":[108,5]}

# Gradio interface for the billing software and sales analysis
with gr.Blocks(css="""
 .title {
  color:#5A67BA;
  font-family:Poppins;
  font-size:20px;
  font-style:normal;
  font-weight:700;
  line-height:11px;
  letter-spacing:0.5px;}
 .center1 {
  margin: auto;
  width: 60%;
  border: white;
  padding: 10px;
} .center2 {
  margin: auto;
  width: 60%;
  border: 3px solid #73AD21;
   text-align: center;
  padding: 10px;
}
""") as demo:
        # ... (Billing software interface components)
        with gr.Tab("BILLING SOFTWARE") as bs:
            with gr.Row():
                gr.Markdown("NEXUS MEDICAL PRIVATE LTD.",elem_classes="center2",)
            with gr.Row(elem_classes="center1"):
                name=gr.Textbox(label="NAME:")
                billno=gr.Textbox(label="Bill No:")
                date=gr.Textbox(label="Date",value=d1)
            while(z>0):
                    with gr.Row():
                            med = gr.Dropdown(medicine, label="Product Name",type="value")
                            prodid = gr.Textbox(label="Product ID")
                            price = gr.Number(label="Price")
                            med.change(lambda x:md[x][0],med,prodid)
                            med.change(lambda x:md[x][1],med,price)
                            quan=gr.Number(label="Quantiy")
                            prodtot=gr.Number(label='Total')
                            quan.change(lambda x,y:x*y,[price,quan],prodtot)
                            prodtot.change(func,prodtot)
                            z-=1
            with gr.Row():
                    tot2=gr.Button("Total",elem_classes="center1")
                    total=gr.Number(label="Total")
                    tot2.click(lambda x:y,total,total)

        # ... (Sales analysis visualization interface)
        with gr.Tab("OVERALL SALES ANALYSIS") as sv:
            iface = gr.Interface(
            fn=create_charts,
            inputs=[],
            outputs=["plot","plot","plot"],
            title="Sales Data Visualization",
            live="true")

        # ... (Product analysis interface)
        with gr.Tab("PRODUCT ANALYSIS") as pda:
            with gr.Row(elem_classes="center1"):
                a=gr.Textbox(label="STARTD ATE")
                b=gr.Textbox(label="END DATE")
                c=gr.Dropdown(medicine,label="Product")
            ifac = gr.Interface(
            fn=create_charts1,
            inputs=[],
            outputs=["plot","plot"],
            title="Sales Data Visualization",
            live="true")
demo.launch(auth=("nexus", "123"),auth_message="WELCOME BACK BOSS!")