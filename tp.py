import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from tkinter import ttk
from cmu_112_graphics import *
from suggestions import *
from features import *

# from http://www.cs.cmu.edu/~112/notes/notes-graphics.html#customColors
def rgbString(red, green, blue):
    # Don't worry about how this code works yet.
    return "#%02x%02x%02x" % (red, green, blue)

# from https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html#subclassing
# ModalApp
class IntroScreenMode(Mode) :
    def redrawAll(mode, canvas) :
        margin = 25
        width = 245
        height = 160
        padding = 5
        font = 'Optima 20'
        fill = rgbString(81, 123, 118)

        # background
        canvas.create_rectangle(0, 0, mode.width, mode.height, width = 0, 
            fill = rgbString(234, 244, 252))

        # decoration
        canvas.create_text(mode.width/2, 10, text = "$$$$$$$$$$$$$$$$$$$$$$$$$$\
$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$",
            font = 'Optima 14', fill = fill)
        canvas.create_text(mode.width/2, mode.height - 10, text = "$$$$$$$$$$$$$\
$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$\
$$$$$$$", font = 'Optima 14', fill = fill)

        # title
        canvas.create_text(mode.width/2, mode.height/6, text = "MONEY TRACKER", 
            font = 'Optima 50', fill = rgbString(112, 112, 112))

        # features
        canvas.create_rectangle(margin, mode.height/3, margin + width, 
            mode.height/3 + height, fill = "white")
        canvas.create_text(margin + width/2, mode.height/3 + height/2, 
            text = "INPUT TRANSACTIONS", font = font, fill = fill)
        canvas.create_rectangle(margin + width + padding, mode.height/3,
            margin + 2 * width + padding, mode.height/3 + height, fill = "white")
        canvas.create_text(margin + 3 * width/2 + padding, mode.height/3 + height/2,
            text = "TRANSACTION HISTORY", font = font, fill = fill)
        canvas.create_rectangle(margin + 2 * (width + padding), mode.height/3,
            margin + 3 * width + 2 * padding, mode.height/3 + height, fill = "white")
        canvas.create_text(margin + 5 * width/2 + padding * 2, mode.height/3 + height/2,
            text = "GRAPH EXPENSES", font = font, fill = fill)
        canvas.create_rectangle(margin, mode.height/3 + height + padding, 
            margin + width, mode.height/3 + 2 * height + padding, fill = "white")
        canvas.create_text(margin + width/2, mode.height/3 + height * 1.5 + padding, 
            text = "SAVING SUGGESTIONS", font = font, fill = fill)
        canvas.create_rectangle(margin + width + padding, 
            mode.height/3 + height + padding, margin + 2 * width + padding, 
            mode.height/3  + 2 * height + padding, fill = "white")
        canvas.create_text(margin + 3 * width/2 + padding, (mode.height/3 + 
            height * 1.5 + padding), text = "SAVINGS AND DEBT\n    CALCULATORS", 
            font = font, fill = fill)
        canvas.create_rectangle(margin + 2 * (width + padding), 
            mode.height/3 + height + padding, margin + 3 * width + 2 * padding, 
            mode.height/3 + 2 * height + padding, fill = "white")
        canvas.create_text(margin + 5 * width/2 + padding * 2, (mode.height/3 + 
            height * 1.5 + padding), text = "CREATE SAVINGS\n          PLAN", 
            font = font, fill = fill)
        canvas.create_rectangle(mode.width/2 - 90, mode.height * 0.85 - 25,
            mode.width/2 + 90, mode.height * 0.85 + 25, fill = "white")
        canvas.create_text(mode.width/2, mode.height * 0.85, text = "GUIDE",
            font = "Optima 16", fill = fill)

    def mousePressed(mode, event) :
        margin = 25
        width = 245
        height = 160
        padding = 5
        if (event.x >= margin and event.x <= margin + width and
            event.y >= mode.height/3 and event.y <= mode.height/3 + height) :
            drawInputWindow()
        elif (event.x >= margin + width + padding and 
            event.x <= margin + 2 * width + padding and event.y >= mode.height/3 and 
            event.y <= mode.height/3 + height) :
            drawTransactionHistoryWindow()
        elif (event.x >= margin + 2 * (width + padding) and 
            event.x <= margin + 3 * width + 2 * padding and 
            event.y >= mode.height/3 and event.y <= mode.height/3 + height) :
            drawGraphWindow()
        elif (event.x >= margin and event.x <= margin + width and
            event.y >= mode.height/3 + height + padding and 
            event.y <= mode.height/3 + 2 * height + padding) :
            drawSavingSuggestionsWindow()
        elif (event.x >= margin + width + padding and 
            event.x <= margin + 2 * width + padding and 
            event.y >= mode.height/3 + height + padding and 
            event.y <= mode.height/3 + 2 * height + padding) :
            drawCalculatorsWindow()
        elif (event.x >= margin + 2 * (width + padding) and 
            event.x <= margin + 3 * width + 2 * padding and 
            event.y >= mode.height/3 + height + padding and 
            event.y <= mode.height/3 + 2 * height + padding) :
            drawCreatePlanWindow()
        elif (event.x >= mode.width/2 - 90 and event.x <= mode.width/2 + 90 and
            event.y >= mode.height * 0.85 - 25 and 
            event.y <= mode.height * 0.85 + 25) :
            mode.app.setActiveMode(mode.app.helpMode)

# describes all features
class HelpMode(Mode) :
    def redrawAll(mode, canvas) :
        headingFont = "Optima 22"
        bodyFont = "Arial 13"
        headingFill = rgbString(81, 123, 118)

        # background
        canvas.create_rectangle(0, 0, mode.width, mode.height, width = 0, 
            fill = rgbString(234, 244, 252))
        
        # title
        canvas.create_text(mode.width/2, 55, text = "GUIDE TO MONEY TRACKER", 
            font = "Optima 40", fill = rgbString(112, 112, 112))
        
        # descriptions
        canvas.create_text(mode.width/2, 105, text = "Input Transactions", 
            font = headingFont, fill = headingFill)
        canvas.create_text(mode.width/2, 145, 
            text = '''Keep track of all your transactions by inputting the name, \
amount, category, date, and whether it is a fixed expense or \nnot. \
Money Tracker will keep track of all your transactions in a CSV file.''', 
            font = bodyFont)
        canvas.create_text(mode.width/2, 185, text = "See Transaction History",
            font = headingFont, fill = headingFill)
        canvas.create_text(mode.width/2, 225, 
            text = '''See all of your transaction history by clicking the 'See \
Transactions' button. This will show you your total savings, total \nspending in \
each category, and all your past transactions listed from most to least recent.''',
            font = bodyFont)
        canvas.create_text(mode.width/2, 265, text = "Monthly and Yearly Spending Graphs",
            font = headingFont, fill = headingFill)
        canvas.create_text(mode.width/2, 310, 
            text = '''Visualize your spending data by selecting a month and year to \
generate a pie chart of your spending in that month. \nYou can also see your \
spending data from a given year by selecting the year and categories to get a line \
graph of \nspending in the selected categories for each month of the year.''',
            font = bodyFont)
        canvas.create_text(mode.width/2, 355, text = "Saving Suggestions",
            font = headingFont, fill = headingFill)
        canvas.create_text(mode.width/2, 430, 
            text = '''To get suggestions on how to save money, click the 'See \
Suggestions' button. This will give you an analysis of your \nspending and will show \
you your average spending per month, the percentage of your savings you're \
spending \neach month on average, and what percentage of your total spending you're \
spending in each category on average \neach month. It will also give you a list \
of categories to cut back on spending, listed from most to least important, 
which is determined by the amount of spending and amount of flexible expenses in \
each category. Each category \nwill have three suggestions for a percentage to \
cut back spending, which type of spending, and amount of money \nthat will be \
saved each month.''', font = bodyFont)
        canvas.create_text(mode.width/2, 500, text = "Savings and Debt Calculators",
            font = headingFont, fill = headingFill)
        canvas.create_text(mode.width/2, 550, 
            text = '''To determine how much money to save each deposit to reach \
your savings goal, enter the goal amount, goal \nnumber of years, interest rate, \
and number of deposits per year into the savings calculator. To determine how \
much \nmoney to pay each payment to pay off debt in a certain amount of time, \
enter the amount of debt, goal number \nof years, interest rate, and number of \
payments per year into the debt calculator.''', font = bodyFont)
        canvas.create_text(mode.width/2, 605, text = "Create Savings Plan",
            font = headingFont, fill = headingFill)
        canvas.create_text(mode.width/2, 650, 
            text = '''To set aside a fixed amount of money each month for a \
savings plan, enter in the name of the savings plan, goal \namount that you want \
to save, how many months you want to save for, the start month, and start year \
of the savings \nplan. It will automatically set aside money whenever \
savings are inputted each month for that savings plan.''', font = bodyFont)

        # button to go back to home page
        canvas.create_rectangle(mode.width/2 - 100, mode.height * 0.935 - 15, 
            mode.width/2 + 100, mode.height * 0.935 + 15, fill = "white")
        canvas.create_text(mode.width/2, mode.height * 0.935, text = "Home Page", 
            font = "Optima 15", fill = headingFill)

        # decoration
        canvas.create_text(mode.width/2, 10, text = "$$$$$$$$$$$$$$$$$$$$$$$$$$\
$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$",
            font = 'Optima 14', fill = headingFill)
        canvas.create_text(mode.width/2, mode.height - 10, text = "$$$$$$$$$$$$$\
$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$\
$$$$$$$", font = 'Optima 14', fill = headingFill)

    def mousePressed(mode, event) :
        if (event.x >= mode.width/2 - 100 and event.x <= mode.width/2 + 100 and 
            event.y >= mode.height * 0.935 - 15 and 
            event.y <= mode.height * 0.935 + 15) :
            mode.app.setActiveMode(mode.app.introScreenMode)

class MyModalApp(ModalApp) :
    def appStarted(app) :
        app.introScreenMode = IntroScreenMode()
        app.helpMode = HelpMode()
        app.setActiveMode(app.introScreenMode)
        app.timerDelay = 50

# from https://www.python-course.eu/tkinter_entry_widgets.php
# and https://www.delftstack.com/tutorial/tkinter-tutorial/tkinter-combobox/
# and https://www.delftstack.com/howto/python-tkinter/how-to-bind-multiple-
# commands-to-tkinter-button/
# and https://stackoverflow.com/questions/2260235/how-to-clear-the-entry-widget
# -after-a-button-is-pressed-in-tkinter
# and https://stackoverflow.com/questions/35233043/how-to-clear-text-field-part-
# of-ttk-combobox
def drawInputWindow() :
    window = tk.Tk()
    window.title("Money Tracker")
    window.geometry("600x300")
    tk.Label(window, text = "Input spending or savings:").grid(row = 1, sticky = "w")
    tk.Label(window, text = "Name:").grid(row = 2, sticky = "e")
    nameEntry = tk.Entry(window)
    nameEntry.grid(row = 2, column = 1)
    tk.Label(window, text = "Amount:").grid(row = 3, sticky = "e")
    amountEntry = tk.Entry(window)
    amountEntry.grid(row = 3, column = 1)
    tk.Label(window, text = "Category:").grid(row = 4, sticky = "e")
    categoryEntry = ttk.Combobox(window, values = ["Housing/Utilities", "Food", 
        "Entertainment", "Insurance", "Personal Spending", "Clothes", "Savings"])
    categoryEntry.grid(row = 4, column = 1)
    tk.Label(window, text = "Is this fixed?").grid(row = 5, sticky = "e")
    fixedEntry = ttk.Combobox(window, values = ["Yes", "No"])
    fixedEntry.grid(row = 5, column = 1)
    tk.Label(window, text = "Date:").grid(row = 6, sticky = "e")
    monthEntry = ttk.Combobox(window, values = [1,2,3,4,5,6,7,8,9,10,11,12], width = 8)
    monthEntry.grid(row = 6, column = 1, sticky = "w")
    dayEntry = ttk.Combobox(window, values = [i for i in range(1, 32)], width = 9)
    dayEntry.grid(row = 6, column = 1, sticky = "e")
    yearEntry = ttk.Combobox(window, values = [i for i in range(2020, 2000, -1)], width = 10)
    yearEntry.grid(row = 6, column = 2, sticky = "w")
    submitButton = tk.Button(window, text = "Input", width = 20, 
        command = lambda: [Input.inputEntry(nameEntry.get(), amountEntry.get(), 
        categoryEntry.get(), monthEntry.get(), dayEntry.get(), yearEntry.get(),
        fixedEntry.get()), nameEntry.delete(0, tk.END), amountEntry.delete(0, tk.END),
        categoryEntry.set(''), fixedEntry.set(''), monthEntry.set(''), 
        dayEntry.set(''), yearEntry.set('')])
    submitButton.grid(row = 7, column = 1)
    tk.mainloop()

def drawTransactionHistoryWindow() :
    entries = Transactions.getAllData()
    totalSavings = "Total Savings: $" + str(Transactions.getTotalSavings())
    window = tk.Tk()
    window.title("Money Tracker: Transaction History")
    window.geometry("500x600")
    showTotalSavings = tk.Label(window, width = 600, font = 'Optima 20', 
        justify = 'center', text = totalSavings)
    showTotalSavings.pack()
    showEntries = tk.Text(window, width = 600, font = 'Arial 14')
    showEntries.pack()
    showEntries.insert(tk.END, entries, "\n")
    tk.mainloop()

def drawGraphWindow() :
    window = tk.Toplevel()
    window.title("Money Tracker")
    window.geometry("600x400")

    #monthly spending pie chart
    tk.Label(window, text = "To see graph of a month's spending:").grid(row = 0, 
        sticky = "w")
    tk.Label(window, text = "Month:").grid(row = 1, sticky = "e")
    monthPieEntry = ttk.Combobox(window, values = [1,2,3,4,5,6,7,8,9,10,11,12])
    monthPieEntry.grid(row = 1, column = 1)
    tk.Label(window, text = "Year:").grid(row = 2, sticky = "e")
    yearPieEntry = ttk.Combobox(window, values = [i for i in range(2020, 2000, -1)])
    yearPieEntry.grid(row = 2, column = 1)
    showMonthPieButton = tk.Button(window, text = "See Graph", width = 20,
        command = lambda: Graphs.monthlySpendingPieChart(int(monthPieEntry.get()), 
        int(yearPieEntry.get())))
    showMonthPieButton.grid(row = 3, column = 1)
    tk.Label(window, text = "").grid(row = 4)

    # yearly spending line graph
    tk.Label(window, text = "To see graph of a year's spending:").grid(row = 5, 
        sticky = "w")
    tk.Label(window, text = "Year:").grid(row = 6, sticky = "e")
    yearLineEntry = ttk.Combobox(window, values = [i for i in range(2020, 2000, -1)])
    yearLineEntry.grid(row = 6, column = 1)
    tk.Label(window, text = "Choose categories to graph:").grid(row = 7, stick = "e")
    var1 = tk.IntVar()
    c1 = tk.Checkbutton(window, text = "Housing/Utilities", variable = var1, 
        onvalue = 1, offvalue = 0).grid(row = 7, column = 1, stick = "w")
    var2 = tk.IntVar()
    c2 = tk.Checkbutton(window, text = "Food", variable = var2, 
        onvalue = 1, offvalue = 0).grid(row = 7, column = 1, stick = "e")
    var3 = tk.IntVar()
    c3 = tk.Checkbutton(window, text = "Entertainment", variable = var3, 
        onvalue = 1, offvalue = 0).grid(row = 8, column = 1, stick = "w")
    var4 = tk.IntVar()
    c4 = tk.Checkbutton(window, text = "Insurance", variable = var4, 
        onvalue = 1, offvalue = 0).grid(row = 9, column = 1, stick = "w")
    var5 = tk.IntVar()
    c5 = tk.Checkbutton(window, text = "Clothes", variable = var5, 
        onvalue = 1, offvalue = 0).grid(row = 9, column = 1, stick = "e")
    var6 = tk.IntVar()
    c6 = tk.Checkbutton(window, text = "Personal Spending", variable = var6, 
        onvalue = 1, offvalue = 0).grid(row = 10, column = 1, stick = "w")
    showYearLineButton = tk.Button(window, text = "See Graph", width = 20,
        command = lambda: Graphs.yearlySpendingLineGraph(int(yearLineEntry.get()), 
        Graphs.getCategories([var1.get(), var2.get(), var3.get(), var4.get(), 
        var5.get(), var6.get()])))
    showYearLineButton.grid(row = 11, column = 1)

    window.mainloop()

def drawSavingSuggestionsWindow() :
    analysis = Suggestions.getStringAnalysis()
    suggestions = Suggestions.getStringSavingSuggestions()
    window = tk.Tk()
    window.title("Money Tracker: Saving Suggestions")
    window.geometry("500x750")
    analysisTitle = tk.Label(window, text = "Analysis of Spending", font = 'Optima 20', 
        justify = 'center')
    analysisTitle.pack()
    showAnalysis = tk.Text(window, width = 800, font = 'Arial 14', height = 10)
    showAnalysis.pack()
    showAnalysis.insert(tk.END, analysis)
    suggestionsTitle = tk.Label(window, text = "Suggestions for Saving", 
        font = 'Optima 20', justify = 'center')
    suggestionsTitle.pack()
    showSuggestions = tk.Text(window, width = 800, height = 100, font = 'Arial 14')
    showSuggestions.pack()
    showSuggestions.insert(tk.END, suggestions)
    tk.mainloop()

def drawCalculatorsWindow() :
    window = tk.Tk()
    window.title("Money Tracker")
    window.geometry("700x400")

    # savings calculator
    tk.Label(window, text = "Savings Calculator:").grid(row = 1, stick = "w")
    tk.Label(window, text = "Goal Amount:").grid(row = 2, stick = "e")
    savingsGoalEntry = tk.Entry(window)
    savingsGoalEntry.grid(row = 2, column = 1)
    tk.Label(window, text = "Number of Years:").grid(row = 2, column = 2, stick = "w")
    savingsYearsEntry = tk.Entry(window)
    savingsYearsEntry.grid(row = 2, column = 3)
    tk.Label(window, text = "Interest Rate (%):").grid(row = 3, stick = "e")
    savingsInterestEntry = tk.Entry(window)
    savingsInterestEntry.grid(row = 3, column = 1)
    tk.Label(window, text = "Payments Per Year:").grid(row = 3, column = 2, stick = "w")
    savingsPeriodsEntry = tk.Entry(window)
    savingsPeriodsEntry.grid(row = 3, column = 3)
    savingsCalculatorButton = tk.Button(window, text = "Calculate", width = 20,
        command = lambda: Calculators.drawSavingsCalculatorWindow(float(savingsGoalEntry.get()),
        int(savingsYearsEntry.get()), float(savingsInterestEntry.get()), 
        int(savingsPeriodsEntry.get())))
    savingsCalculatorButton.grid(row = 4, column = 1)
    tk.Label(window, text = "").grid(row = 5)

    # debt calculator
    tk.Label(window, text = "Debt Calculator:").grid(row = 6, stick = "w")
    tk.Label(window, text = "Debt Amount:").grid(row = 7, stick = "e")
    debtAmountEntry = tk.Entry(window)
    debtAmountEntry.grid(row = 7, column = 1)
    tk.Label(window, text = "Number of Years:").grid(row = 7, column = 2, stick = "w")
    debtYearsEntry = tk.Entry(window)
    debtYearsEntry.grid(row = 7, column = 3)
    tk.Label(window, text = "Interest Rate (%):").grid(row = 8, stick = "e")
    debtInterestEntry = tk.Entry(window)
    debtInterestEntry.grid(row = 8, column = 1)
    tk.Label(window, text = "Payments Per Year:").grid(row = 8, column = 2, stick = "w")
    debtPeriodsEntry = tk.Entry(window)
    debtPeriodsEntry.grid(row = 8, column = 3)
    debtCalculatorButton = tk.Button(window, text = "Calculate", width = 20,
        command = lambda: Calculators.drawDebtCalculatorWindow(float(debtAmountEntry.get()),
        int(debtYearsEntry.get()), float(debtInterestEntry.get()), 
        int(debtPeriodsEntry.get())))
    debtCalculatorButton.grid(row = 9, column = 1)
    tk.mainloop()

def drawCreatePlanWindow() :
    window = tk.Tk()
    window.title("Money Tracker")
    window.geometry("500x500")
    tk.Label(window, text = "Create a saving plan: ").grid(row = 1, stick = "w")
    tk.Label(window, text = "Name of Savings Plan: ").grid(row = 2, stick = "e")
    nameEntry = tk.Entry(window)
    nameEntry.grid(row = 2, column = 1)
    tk.Label(window, text = "Total Amount to Save: ").grid(row = 3, stick = "e")
    amountEntry = tk.Entry(window)
    amountEntry.grid(row = 3, column = 1)
    tk.Label(window, text = "Months to Reach Goal: ").grid(row = 4, stick = "e")
    monthsEntry = tk.Entry(window)
    monthsEntry.grid(row = 4, column = 1)
    tk.Label(window, text = "Starting Month: ").grid(row = 5, stick = "e")
    startMonthEntry = ttk.Combobox(window, values = [1,2,3,4,5,6,7,8,9,10,11,12])
    startMonthEntry.grid(row = 5, column = 1)
    tk.Label(window, text = "Starting Year: ").grid(row = 6, stick = "e")
    startYearEntry = ttk.Combobox(window, values = [i for i in range(2020, 2000, -1)])
    startYearEntry.grid(row = 6, column = 1)
    submitButton = tk.Button(window, text = "Create", width = 20, 
        command = lambda: [Plan.createPlan(nameEntry.get(), amountEntry.get(), 
        monthsEntry.get(), startMonthEntry.get(), startYearEntry.get()), 
        nameEntry.delete(0, tk.END), amountEntry.delete(0, tk.END), 
        monthsEntry.delete(0, tk.END), startMonthEntry.set(''), 
        startYearEntry.set('')])
    submitButton.grid(row = 7, column = 1)
    tk.Label(window, text = "").grid(row = 8)
    showPlansButton = tk.Button(window, text = "See All Plans", width = 20,
        command = lambda: Plan.drawPlansWindow())
    showPlansButton.grid(row = 9, column = 1)

app = MyModalApp(width=800, height=750)