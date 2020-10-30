# File: project.py
# Authors: Sapir Lastimoza-Dooley, Grant Tober, Tanner Hansard
# Date: 05/05/2020
# E-mails: sapirdooley@tamu.edu, gtober@tamu.edu, tanner_h@tamu.edu
# Project Name: The Dealership Manager
# Description: Program reads a data set in csv format, and analyzes it.
# Then it generates the details of the data, a bar chart, two line charts,
# and a pie chart.

import csv
import random
import matplotlib.pyplot as plt; plt.rcdefaults()
import matplotlib.patches as patches
import numpy as np
import pandas as pd  
import datetime

def seperateFile(path):
    """Takes path as input and seperates columns into seperate"""
    with open(path, 'r') as csvfile:
        data_file = csv.reader(csvfile)
        
        data_set = []
        car_model = []
        contract_date = []
        car_brand = []
        state = []
        car_safety_rating = []
        sales_amount = []
        color = []
        
        for line in data_file:
            data_set.append(line)
            car_model.append(line[0])
            contract_date.append(line[1])
            car_brand.append(line[2])
            state.append(line[3])
            car_safety_rating.append(line[4])
            sales_amount.append(line[5])
            color.append(line[6])

    return (data_set, car_model, contract_date, car_brand, state, car_safety_rating, sales_amount, color)

def getUniqueModels(car_model):
    """Finds all unique models within csv and returns as list"""
    unique_models = []
    for model in car_model:
        if model in unique_models:
            pass
        else:
            unique_models.append(model)
    num_models = len(unique_models) - 1
    return(unique_models, num_models)

def getUniqueBrands(car_brand):
    """Finds all unique car brands within csv and returns as list"""
    unique_brands = []
    for brand in car_brand:
        if brand in unique_brands:
            pass
        else:
            unique_brands.append(brand)
    num_brands = len(unique_brands) - 1
    return(unique_brands, num_brands)

def getUniqueRatings(car_safety_rating):
    """Finds all unique ratings within csv and returns as list"""
    unique_ratings = []    
    for rating in car_safety_rating:
        if rating in unique_ratings:
            pass
        else:
            unique_ratings.append(rating)
    num_ratings = len(unique_ratings) - 1
    return(unique_ratings, num_ratings)

def getUniqueColors(color):
    """Finds all unique colors within csv and returns as list"""
    unique_colors = []
    for shade in color:
        if shade in unique_colors:
            pass
        else:
            unique_colors.append(shade)
    num_colors = len(unique_colors) - 1
    return(unique_colors, num_colors)

def findSalesTotal(sales_amount):
    """Finds total sales from csv and returns total sales as int and unique values as list"""
    x = 1
    values = []
    sales_total = 0
    while x < len(sales_amount):
        sale = sales_amount[x]
        if ',' in sale:
            first = sale[::-1]
            first = first[0:3]
            first = first[::-1]
            sale = sale[0:-4] + first
            values.append(int(sale))
        sales_total += int(sale)
        x += 1
    return(sales_total, values)

def brandPercentages(unique_brands, car_brand, values, sales_total):
    """Finds percentage of total sales for each car brang """
    c = 1
    percentages = []
    large_brands = []
    other = 0
    while c < len(unique_brands):
        m = unique_brands[c]
        c += 1
        d = 1
        percent_value = 0
        while d < len(car_brand):
            if m in car_brand[d]:
                percent_value += values[d - 1]
            d += 1
        percent = percent_value / sales_total * 100
        if percent < 4:
            other += percent
        else:
            percentages.append([round(percent, 2), m])
    percentages.append([round(other, 2),'Others'])
    percentages.sort()
    percentages = percentages[::-1]
    return(percentages)

def salesByState(csv):
    """Creates bar chart showing sales per state given user inputted dataframe"""

    # Remove Commas
    csv["sales amount ($)"] = csv["sales amount ($)"].replace(',','', regex=True)

    # Convert to int
    csv["sales amount ($)"] = csv["sales amount ($)"].astype(str).astype(int)

    # Group by State, sum sales amounts
    sales = csv.groupby('State')['sales amount ($)'].sum()

    # Create barchart
    bar = sales.plot.bar(x='State', y='sales amount ($)', rot=0)
    bar.set_ylabel('Sales ($1000)')
    bar.set_title('Sales per State')

    # Find Max
    maxState = sales.idxmax()
    max = sales.max()
    return(maxState, max)

def salesByMonth(csv):
       """ Creates a lineplot showing sales by month given user inputted dataframe, returns month with highest sales and amount"""

       # Remove Commas
       csv["sales amount ($)"] = csv["sales amount ($)"].replace(',','', regex=True)

       # Convert to int
       csv["sales amount ($)"] = csv["sales amount ($)"].astype(str).astype(int)

       # Convert to datetime format
       csv_sorted = csv.sort_values(by = 'contract_date')
       csv_sorted['contract_date'] = pd.to_datetime(csv_sorted['contract_date'])

       # Create Month and Total Columns
       csv_sorted['Mon'] = csv_sorted['contract_date'].dt.strftime('%b')
       csv_sorted['total'] = csv_sorted['sales amount ($)'].groupby(csv_sorted['Mon']).transform('sum')

       #Create series for finding max month
       months = csv_sorted.groupby('Mon')['sales amount ($)'].sum()

       # Create new dataframe
       new = csv_sorted[['Mon','contract_date', 'sales amount ($)', 'total']]
       # Sort by date
       new_sorted = new.sort_values(by = 'contract_date')

       #create line plot
       fig, ax = plt.subplots()
       ax.plot(new_sorted['Mon'], new_sorted['total'])

       ax.set(xlabel='Month', ylabel='Total Sales ($10,000,000)',
              title='Total Sales by Month')
       ax.grid()

       # Find Max
       maxMonth = months.idxmax()
       max = months.max()
       return(maxMonth, max)

def createPieChart(unique_brands, brands, values, sales_total):
    """ Creates pie chart from list of unique brands and their related total sales """
    c = 1
    percentages = []
    large_brands = []
    other = 0
    while c < len(unique_brands):
        m = unique_brands[c]
        c += 1
        d = 1
        percent_value = 0
        while d < len(brands):
            if m in brands[d]:
                percent_value += values[d - 1]
            d += 1
        percent = percent_value / sales_total * 100
        if percent < 4:
            other += percent
        else:
            percentages.append([round(percent, 2), m])
    percentages.append([round(other, 2),'Others'])
    percentages.sort()
    percentages = percentages[::-1]

    c = 0
    sizes = []
    labels = []
    while c < len(percentages):
        sizes.append(percentages[c][0])
        labels.append(percentages[c][1])
        c += 1
        
    colors = []
    x = 0
    while x < len(sizes):
        rgb = [random.random(), random.random(), random.random()]
        d = 0
        y = 0
        while d < len(colors):
            if rgb[0] in colors[d]:
                y += 1
            if rgb[1] in colors[d]:
                y += 1
            if rgb[2] in colors[d]:
                y += 1
            if rgb[1] < 0.4:
                y += 1
            d += 1
        if y == 0:
            colors.append(rgb)
            x += 1
        else:
            pass
    plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', shadow=False, startangle=0)
    plt.title('Percentage of Sale Based on Different Car Brands')

def stateSalesPerMonth(csv):
    """ Creates a lineplot showing sales/month by state given user inputted dataframe"""
    # Create the Dataframe from the excel data
    DataFrame = csv    
    # Remove the commas
    DataFrame["sales amount ($)"] = DataFrame["sales amount ($)"].replace(',','', regex=True)
    
    # Convert to int
    DataFrame["sales amount ($)"] = DataFrame["sales amount ($)"].astype(str).astype(int)
    
    #convert to datetime format
    DataFrame_time = DataFrame.sort_values(by='contract_date')
    DataFrame_time['contract_date']=pd.to_datetime(DataFrame_time['contract_date'])
    
    #create a column for months
    DataFrame_time['Mon'] = DataFrame_time['contract_date'].dt.strftime('%b')
    monthlist = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    DataFrame_time['Mon'] = pd.Categorical(DataFrame_time['Mon'], categories= monthlist, ordered=True)
    
    #create a column for state sales per month
    StateSalesMonth = DataFrame_time.groupby(['State','Mon'])['sales amount ($)'].sum()
    TexasLine = StateSalesMonth['Texas']
    FloridaLine = StateSalesMonth['Florida']
    CaliforniaLine = StateSalesMonth['California']
    NevadaLine = StateSalesMonth['Nevada']
    OhioLine = StateSalesMonth['Ohio']
    
    # Group by months, sales
    month = DataFrame_time.groupby('Mon')['sales amount ($)'].sum()
    StateSales = DataFrame_time.groupby('State')['sales amount ($)'].sum()
    
    # Create the linechart
    Line1 = FloridaLine.plot()
    Line2 = OhioLine.plot()
    Line3 = TexasLine.plot()
    line4 = CaliforniaLine.plot()
    Line5 = NevadaLine.plot()
    
    # Create the legend
    green_patch = patches.Patch(color='green', label ='Texas')
    red_patch = patches.Patch(color='red', label ='California')
    blue_patch = patches.Patch(color='blue', label ='Florida')
    orange_patch = patches.Patch(color='orange', label ='Ohio')
    purple_patch = patches.Patch(color='purple', label ='Nevada')
    plt.legend(handles=[green_patch,red_patch,blue_patch,orange_patch,purple_patch])
    
    '''Create the axis labels'''
    x_labels= ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    plt.xticks(np.arange(len(x_labels)), x_labels, rotation = 90)
    plt.ylim([0,15000000])
    plt.xlabel("Month")
    plt.ylabel("Amount of Sales")
    plt.title("Amount of sales in different months in each state")

def main():
    path = 'C:/MyFiles/Repo/Programming1/2019_car_sale.csv'

    # Get Lists for data analysus
    data_set, car_model, contract_date, car_brand, state, car_safety_rating, sales_amount, color = seperateFile(path)

    # Find Unique values
    unique_models, num_models = getUniqueModels(car_model)
    unique_brands, num_brands = getUniqueBrands(car_brand)
    unique_ratings, num_ratings = getUniqueRatings(car_safety_rating)
    unique_colors, num_colors = getUniqueColors(color)

    deals = len(data_set) - 1
    sales_total, values = findSalesTotal(sales_amount)
    percentages = brandPercentages(unique_brands,car_brand, values, sales_total)

    # Bar Chart
    df = pd.read_csv(path, delimiter= ',')
    maxState,max1 = salesByState(df)
    bar = salesByState(df)
    plt.show(bar)

    # Line plot 1
    maxMonth, max2 = salesByMonth(df)
    line1 = (salesByMonth(df))
    plt.show(line1)

    # Pie Chart
    pie = createPieChart(unique_brands, car_brand, values, sales_total)
    plt.show(pie)

    # Line plot 2
    line2 = stateSalesPerMonth(df)
    plt.show(line2)

    print('========Dataset Details========')
    print()
    print(f'Total number of deals: {deals}')
    print(f'Number of different car models: {num_models}')
    print(f'Number of different car brands: {num_brands}')
    print(f'Number of different car safety ratings: {num_ratings}')
    print(f'Number of different car colors: {num_colors}')
    print(f'Total amount of sale: {sales_total}')
    print()
    print('===============================')
    print()
    print(f"The state with the highest sales is {maxState} at ${max1}")
    print(f"The month with the highest sales is {maxMonth} at ${max2}")
    print()
    print('========Amount of Sale Based on Car Brands========')
    print()
    c = 0
    while c < len(percentages):
        print(f'{percentages[c][1]} : {percentages[c][0]}')
        c += 1
    print()
    print('===============================')

main()