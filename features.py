# all other features

import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from tkinter import ttk
import math
import decimal

# from 15112
def roundHalfUp(d):
    # Round to nearest with ties going away from zero.
    rounding = decimal.ROUND_HALF_UP
    # See other rounding options here:
    # https://docs.python.org/3/library/decimal.html#rounding-modes
    return int(decimal.Decimal(d).to_integral_value(rounding=rounding))

# returns dictionary of data that map year to month to category to amount
def getDataDictionary(file = "data.csv") :
    file = open(file, "r")
    data = file.read()
    file.close()
    result = {}
    for line in data.splitlines() :
        elements = line.split(",")
        # line format is name, amount, category, month, day, year, fixed
        name, amount, category = elements[0], float(elements[1]), elements[2]
        month, day, year =  int(elements[3]), int(elements[4]), int(elements[5])
        if year not in result :
            result[year] = dict()
        if month not in result[year] :
            result[year][month] = dict()
        if category not in result[year][month] :
            result[year][month][category] = 0
        result[year][month][category] += amount
    return result

#####################################################
# INPUT TRANSACTION
#####################################################

class Input(object) :
    # inputs new spending/saving entry into csv file containing all data
    # if there is a savings plan and inputted category is Savings, then it will
    # automatically put savings into separate savings plan account
    def inputEntry(name, amount, category, month, day, year, fixed, file="data.csv"):
        savingsPlans = Plan.getPlans()
        data = getDataDictionary()
        if category == "Savings" and savingsPlans != [] :
            for plan in savingsPlans :
                # name, goalAmount, months, goalPerMonth, startMonth, startYear
                planName = plan[0]
                goalPerMonth = float(plan[3])
                planMonths = int(plan[2])
                planStartMonth = int(plan[4])
                planStartYear = int(plan[5])
                year = int(year)
                month = int(month)
                amount = float(amount)
                if (year == planStartYear and month >= planStartMonth) :
                    if month not in data[year] :
                        data[year][month] = dict()
                    if planName not in data[year][month] :
                        data[year][month][planName] = 0
                    savedSoFar = float(data[year][month][planName])
                    if savedSoFar != goalPerMonth :
                        remaining = goalPerMonth - savedSoFar
                        if amount > remaining :
                            savingsAmount = remaining
                        else :
                            savingsAmount = amount
                        f = open(file, "a")
                        f.write(f'\n{planName},{savingsAmount},{planName},{month},{day},{year},Yes')
                        f.close()
                        amount -= savingsAmount
        if amount != 0 :
            f = open(file, "a")
            f.write(f'\n{name},{amount},{category},{month},{day},{year},{fixed}')
            f.close()
        Plan.checkGoalReached()

#####################################################
# SHOW ALL TRANSACTIONS
#####################################################

class Transactions(object) :
    # returns net amount of money
    def getTotalSavings() :
        dataDictionary = getDataDictionary()
        result = 0
        for year in dataDictionary :
            for month in dataDictionary[year] :
                for category in dataDictionary[year][month] :
                    if category == "Savings" :
                        result += dataDictionary[year][month][category]
                    else :
                        result -= dataDictionary[year][month][category]
        return result

    # returns string of all entries and string of amount for each category
    def getAllData(file = "data.csv") :
        file = open(file, "r")
        data = file.read()
        file.close()
        entries = ""
        categoryAmounts = dict()
        for line in data.splitlines() :
            elements = line.split(",")
            # line format is name, amount, category, month, day, year
            name, amount, category = elements[0], float(elements[1]), elements[2]
            month, day, year =  int(elements[3]), int(elements[4]), int(elements[5])
            if category not in categoryAmounts :
                categoryAmounts[category] = 0
            categoryAmounts[category] += amount
            date = f'{month}/{day}/{year}'
            # entries start from most recent
            entries = f'{date}, {name}, {category}, ${amount}\n' + entries
        if entries == "" :
            entries = "No data"
        return entries

#####################################################
# GRAPHS
#####################################################

class Graphs(object) :

    # partly from https://stackoverflow.com/questions/22720843/how-to-center-
    # a-widget-vertically-in-tkinter
    def drawNoDataWindow() :
        window = tk.Tk()
        window.title("Money Tracker: Graph")
        window.geometry("400x400")
        text = tk.Label(window, text = "No Data", font = 'Arial 18')
        text.place(relx = .5, rely = 0.5, anchor = "c")
        window.mainloop()

    def getPieChartData(month, year) :
        data = getDataDictionary()
        if year not in data :
            Graphs.drawNoDataWindow()
            return
        yearData = data[year]
        if month not in yearData :
            Graphs.drawNoDataWindow()
            return
        monthData = yearData[month]
        categories = []
        money = []
        for category in monthData :
            if category != "Savings" :
                categories.append(category)
                money.append(monthData[category])
        return categories, money

    # pie chart that shows current month's spending for each category using tkinter
    # tkinter code from https://www.python-course.eu/tkinter_canvas.php
    # based on 15112 hw4
    def monthlySpendingPieChart(month, year) :
        categories, money = Graphs.getPieChartData(month, year)
        total = sum(money)
        months = ["January", "February", "March", "April", "May", "June", "July", 
            "August", "September", "October", "November", "December"]
        monthName = months[month-1]
        width = 500
        height = 500
        window = tk.Tk()
        window.title("Money Tracker: Monthly Spending Graph")
        canvas = tk.Canvas(window, width = width, height = height)
        canvas.pack()
        canvas.create_text(width/2, 20, text = f"Spending Data for {monthName} {year}",
            font = "Optima 25")
        cx = width / 2
        cy = height / 2
        r = min(width/2, height/2) * 0.8
        amountSoFar = 0
        colors = ["pink", "light blue", "aquamarine", "tomato", "medium purple", 
            "light salmon", "turquoise"]
        for i in range(len(categories)) :
            category = categories[i]
            amount = money[i]
            color = colors[i]
            percent = str(roundHalfUp((amount/total) * 1000)/10) + "%"
            angle = (amount / total) * 360
            startAngle = (amountSoFar/total) * 360
            canvas.create_arc(cx-r, cy-r, cx+r, cy+r, start = startAngle, 
                extent = angle, fill = color)
            endAngle = startAngle + angle 
            mid = math.radians((startAngle + endAngle) / 2)
            labelX = cx + (r/2) * math.cos(mid)
            labelY = cy - (r/2) * math.sin(mid)
            canvas.create_text(labelX, labelY, text = f'{category}, {percent}',
                font = "Arial 12 bold")
            amountSoFar += amount
        tk.mainloop()

    # returns list of categories to graph in yearly spending line graph given input 
    # from list of values from checkboxes
    def getCategories(L) :
        categories = ["Housing/Utilities", "Food", "Entertainment", "Insurance", 
        "Clothes", "Personal Spending"]
        result = []
        for i in range(len(L)) :
            if L[i] == 1 : # checkbox is checked
                result.append(categories[i])
        return result

    # line graph that shows total spending per month during given year for 
    # given list of categories
    def yearlySpendingLineGraph(year, categories) :
        data = getDataDictionary()
        if year not in data :
            Graphs.drawNoDataWindow()
            return
        yearData = data[year]
        monthNames = ["January", "February", "March", "April", "May", "June", "July",
            "August", "September", "October", "November", "December"]
        months = []
        fig, ax = plt.subplots()
        ax.set_title(f'Spending for Each Month in {year}')
        ax.set_xlabel("Month")
        ax.set_ylabel("Amount Spent")
        for month in yearData :
            monthNameIndex = month - 1
            months.append(monthNames[monthNameIndex])
            monthSpending = 0
        for category in categories :
            spendingPerMonth = []
            for month in yearData :
                if category in yearData[month] :
                    spendingPerMonth.append(yearData[month][category])
                else :
                    spendingPerMonth.append(0)
            ax.plot(months, spendingPerMonth, label = category)
        ax.set_ylim(bottom = 0)
        plt.autoscale(enable = True, axis = 'both')
        plt.legend()
        plt.show()

#####################################################
# SAVINGS/DEBT CALCULATORS
#####################################################

class Calculators(object) :
    # returns amount to save per period to reach savings goal
    def savingsGoal(goal, years, interestRate, periodsPerYear) :
        interestRate /= 100 # to convert from percentage to decimal
        # using compound interest formula
        principalPayment = goal/((1+(interestRate/periodsPerYear))**(periodsPerYear*years))
        totalPeriods = periodsPerYear * years
        paymentPerPeriod = principalPayment / totalPeriods
        # to round to two decimal places
        return roundHalfUp(paymentPerPeriod * 100)/100

    def getStringSavingsGoal(goal, years, interestRate, periodsPerYear, paymentPerPeriod) :
        months = 12 / periodsPerYear
        result = f'''\
    Savings Goal: ${goal}
    Years: {years}
    Interest Rate: {interestRate}%
    Number of Deposits Per Year: {periodsPerYear}
    Deposit every: {months} Months
    How much to save each deposit: ${paymentPerPeriod}'''
        return result

    def drawSavingsCalculatorWindow(goal, years, interestRate, periodsPerYear) :
        paymentPerPeriod = Calculators.savingsGoal(goal, years, interestRate, periodsPerYear)
        text = Calculators.getStringSavingsGoal(goal, years, interestRate, periodsPerYear, 
            paymentPerPeriod)
        window = tk.Tk()
        window.title("Money Tracker: Savings Calculator")
        window.geometry("400x300")
        title = tk.Label(window, justify = 'center', font = 'Optima 18', text = "Result")
        title.pack()
        showResult = tk.Text(window, width = 400, font = 'Arial 14')
        showResult.pack()
        showResult.insert(tk.END, text)
        tk.mainloop()

    def debtPayoff(debt, goalTime, interestRate, periodsPerYear) :
        interestRate /= 100 # to convert from percentage to decimal
        # using compound interest formula
        amountAfterInterest = debt * ((1 + interestRate/periodsPerYear) ** (periodsPerYear * goalTime))
        totalPeriods = periodsPerYear * goalTime
        paymentPerPeriod = amountAfterInterest / totalPeriods
        # to round to two decimal places
        return roundHalfUp(paymentPerPeriod * 100) / 100

    def getStringDebtPayoff(debt, goalTime, interestRate, periodsPerYear, paymentPerPeriod) :
        months = 12 / periodsPerYear
        result = f'''\
    Amount of Debt: ${debt}
    Years to Pay Off Debt: {goalTime}
    Interest Rate: {interestRate}%
    Number of Payments Per Year: {periodsPerYear}
    Pay every: {months} months
    How much to pay each payment: {paymentPerPeriod}'''
        return result

    def drawDebtCalculatorWindow(debt, goalTime, interestRate, periodsPerYear) :
        paymentPerPeriod = Calculators.debtPayoff(debt, goalTime, interestRate, periodsPerYear)
        text = Calculators.getStringDebtPayoff(debt, goalTime, interestRate, periodsPerYear, 
            paymentPerPeriod)
        window = tk.Tk()
        window.title("Money Tracker: Debt Calculator")
        window.geometry("400x300")
        title = tk.Label(window, justify = 'center', font = 'Optima 18', text = "Result")
        title.pack()
        showResult = tk.Text(window, width = 400, font = 'Arial 14')
        showResult.pack()
        showResult.insert(tk.END, text)
        tk.mainloop()

#####################################################
# CREATE SAVINGS PLAN
#####################################################

class Plan(object) :
    # adds inputted plan to csv file that will keep track of all savings plans
    def createPlan(name, amount, months, startMonth, startYear, file = "plans.csv") :
        amountPerMonth = roundHalfUp((float(amount)/float(months))*100)/100
        file = open(file, "a")
        file.write(f'\n{name},{amount},{months},{amountPerMonth},{startMonth},{startYear}')
        file.close()
    
    # returns list of any current savings plans
    def getPlans(file = "plans.csv") :
        file = open(file, "r")
        plans = file.read()
        file.close()
        result = []
        for line in plans.splitlines() :
            if len(line) != 0 :
                plan = []
                for elem in line.split(",") :
                    plan.append(elem)
                result.append(plan)
        return result
    
    # removes plan from csv once goal is reached
    def removePlan(finishedPlan, file = "plans.csv") :
        f = open(file, "r")
        plans = f.read()
        f.close()
        result = ""
        for plan in plans.splitlines() :
            planName = plan.split(",")[0]
            if planName != finishedPlan :
                result += plan + "\n"
        newPlans = open(file, "w")
        newPlans.write(result)
        newPlans.close()

    # checks if any savings goals are reached and removes them from plans if 
    # it has been reached
    def checkGoalReached() :
        plans = Plan.getPlans()
        data = getDataDictionary()
        for plan in plans :
            # name, amount, months, amountPerMonth, startMonth, startYear
            planName = plan[0]
            goalAmount = float(plan[1])
            months = int(plan[2])
            startMonth = int(plan[4])
            startYear = int(plan[5])
            savedSoFar = 0
            yearData = data[startYear]
            endMonth = startMonth + months
            for month in range(startMonth, endMonth) :
                if month in yearData and planName in yearData[month] :
                    savedSoFar += yearData[month][planName]
            if savedSoFar == goalAmount :
                Plan.removePlan(planName)

    def drawNoPlansWindow() :
        window = tk.Tk()
        window.title("Money Tracker: Savings Plans")
        window.geometry("400x400")
        text = tk.Label(window, text = "No Current Savings Plans", font = 'Arial 18')
        text.place(relx = .5, rely = 0.5, anchor = "c")
        window.mainloop()

    def getPlansString() :
        plans = Plan.getPlans()
        result = ""
        for plan in plans :
            # name, amount, months, amountPerMonth, startMonth, startYear
            name, amount, months = plan[0], plan[1], plan[2]
            amountPerMonth, startMonth, startYear = plan[3], plan[4], plan[5]
            result += f'''Savings Plan: {name}
Goal Amount: {amount}
Number of Months: {months}
Amount Saved Per Month: {amountPerMonth}
Starting Month: {startMonth}/{startYear}
Ending Month: {int(startMonth) + int(months) - 1}/{startYear}\n\n'''
        return result

    def drawPlansWindow() :
        plans = Plan.getPlans()
        if plans == [] :
            Plan.drawNoPlansWindow()
            return
        text = Plan.getPlansString()
        window = tk.Tk()
        window.title("Money Tracker: Savings Plans")
        window.geometry("400x400")
        title = tk.Label(window, justify = 'center', font = 'Optima 18', 
            text = "Current Savings Plans")
        title.pack()
        showPlans = tk.Text(window, width = 400, font = 'Arial 14')
        showPlans.pack()
        showPlans.insert(tk.END, text)
        tk.mainloop()