# saving suggestions

import decimal
import copy

class Suggestions(object) :

    # from 15112
    def roundHalfUp(d):
        # Round to nearest with ties going away from zero.
        rounding = decimal.ROUND_HALF_UP
        # See other rounding options here:
        # https://docs.python.org/3/library/decimal.html#rounding-modes
        return int(decimal.Decimal(d).to_integral_value(rounding=rounding))

    # returns dictionary mapping category to month to list where first element 
    # is total spending and second element is fixed spending
    def getDataForSuggestion(file = "data.csv") :
        file = open(file, "r")
        data = file.read()
        file.close()
        result = {}
        for line in data.splitlines() :
            elements = line.split(",")
            amount, category = int(float(elements[1])), elements[2]
            month, fixed = elements[3], elements[6]
            if category not in result :
                result[category] = dict()
            if month not in result[category] :
                result[category][month] = [0,0]
            result[category][month][0] += amount
            if fixed == "Yes" :
                result[category][month][1] += amount
        return result

    # returns tuple of average monthly spending of given category and average 
    # monthly fixed spending of given category
    def avgMonthlyCategoryTotals(category) :
        data = Suggestions.getDataForSuggestion()
        totalMonths = 0
        totalAmount = 0
        totalFixedAmount = 0
        for month in data[category] :
            totalMonths += 1
            totalAmount += data[category][month][0]
            totalFixedAmount += data[category][month][1]
        avgMonthlyTotal = totalAmount / totalMonths
        avgFixedTotal = totalFixedAmount / totalMonths
        return avgMonthlyTotal, avgFixedTotal

    # returns tuple of average monthly total spending and average monthly total 
    # fixed spending
    def avgMonthlyTotalSpending() :
        data = Suggestions.getDataForSuggestion()
        totalMonths = 0
        months = []
        totalSpending = 0
        totalFixedSpending = 0
        expenseCategories = ["Housing/Utilities", "Food", "Entertainment", 
            "Insurance", "Personal Spending", "Clothes"]
        for category in data :
            if category in expenseCategories :
                for month in data[category] :
                    if month not in months :
                        months.append(month)
                        totalMonths += 1
                    totalSpending += data[category][month][0]
                    totalFixedSpending += data[category][month][1]
        avgTotalSpending = Suggestions.roundHalfUp((totalSpending / totalMonths) * 100) / 100
        avgTotalFixed = Suggestions.roundHalfUp((totalFixedSpending / totalMonths) * 100) / 100
        return avgTotalSpending, avgTotalFixed

    # returns average monthly savings
    def avgMonthlySavings() :
        data = Suggestions.getDataForSuggestion()
        months = 0
        totalSavings = 0
        expenseCategories = ["Housing/Utilities", "Food", "Entertainment", 
            "Insurance", "Personal Spending", "Clothes"]
        for category in data :
            if category not in expenseCategories :
                for month in data[category] :
                    months += 1
                    totalSavings += data[category][month][0]
        avgTotalSavings = totalSavings / months
        return avgTotalSavings

    # returns dictionary mapping category to its percentage of total spending
    def getCategoryPercentages() :
        data = Suggestions.getDataForSuggestion()
        categories = []
        expenseCategories = ["Housing/Utilities", "Food", "Entertainment", 
            "Insurance", "Personal Spending", "Clothes"]
        for category in data :
            if category in expenseCategories :
                categories.append(category)
        result = dict()
        totalSpending, totalFixedSpending = Suggestions.avgMonthlyTotalSpending()
        for category in categories :
            categoryTotal, categoryFixedTotal = Suggestions.avgMonthlyCategoryTotals(category)
            result[category] = Suggestions.roundHalfUp((categoryTotal/totalSpending)*100)
        return result

    # returns percentage of savings spent
    def getSpendingPercentage() :
        totalSpending, totalFixedSpending = Suggestions.avgMonthlyTotalSpending()
        totalSavings = Suggestions.avgMonthlySavings()
        percentage = Suggestions.roundHalfUp((totalSpending / totalSavings) * 100)
        return percentage

    # returns percentage of spending that is fixed for each category of spending
    def getFixedPercentages() :
        data = Suggestions.getDataForSuggestion()
        categories = []
        expenseCategories = ["Housing/Utilities", "Food", "Entertainment", 
            "Insurance", "Personal Spending", "Clothes"]
        for category in data :
            if category in expenseCategories :
                categories.append(category)
        result = dict()
        for category in categories :
            avgMonthlyTotal, avgFixedTotal = Suggestions.avgMonthlyCategoryTotals(category)
            result[category] = Suggestions.roundHalfUp((avgFixedTotal/avgMonthlyTotal) * 100)
        return result

    # returns category with the highest percentage of spending
    def getHighestCategory(L, percentagesDict) :
        highestAmount = 0
        highestCategory = None
        for category in L :
            if category not in percentagesDict :
                L.remove(category)
            elif (percentagesDict[category] > highestAmount or 
                highestCategory == None) :
                highestAmount = percentagesDict[category]
                highestCategory = category
            elif percentagesDict[category] == highestAmount :
                if type(highestCategory) != list :
                    highestCategory = [highestCategory]
                highestCategory.append(category)
        return highestCategory

    # returns list of categories in order from most to least important to cut 
    # back on spending
    import copy
    def getOrder(L) :
        result = []
        categoryPercentagesDict = Suggestions.getCategoryPercentages()
        fixedPercentagesDict = Suggestions.getFixedPercentages()
        highestSpending = Suggestions.getHighestCategory(L, categoryPercentagesDict)
        highestFlexible = Suggestions.getHighestCategory(L, fixedPercentagesDict)
        if type(highestSpending) == list :
            highestSpendingList = copy.copy(highestSpending)
            while len(highestSpendingList) > 0 :
                highestFixed = Suggestions.getHighestCategory(highestSpendingList, fixedPercentagesDict)
                result = [highestFixed] + result
                highestSpendingList.remove(highestFixed)
            for category in L :
                if category not in result :
                    result.append(category)
            for category in result :
                if fixedPercentagesDict[category] == 100 : # move to end
                    result.remove(category)
                    result.append(category)
        if type(highestFlexible) == list :
            highestFlexibleList = copy.copy(highestFlexible)
            while len(highestFlexibleList) > 0 :
                highestAmount = Suggestions.getHighestCategory(highestFlexibleList, categoryPercentagesDict)
                result.append(highestAmount)
                highestFlexibleList.remove(highestAmount)
            for category in L :
                if category not in result :
                    result.append(category)
            for category in result :
                if fixedPercentagesDict[category] == 100 : # move to end
                    result.remove(category)
                    result.append(category)
        if type(highestSpending) != list and type(highestFlexible) != list :
            if highestSpending == highestFlexible :
                result = [highestSpending]
                newL = copy.copy(L)
                highestRemoved = newL.remove(highestSpending)
                secondHighestSpending = Suggestions.getHighestCategory(newL, categoryPercentagesDict)
                result.append(secondHighestSpending)
            elif fixedPercentagesDict[highestFlexible] > 2*fixedPercentagesDict[highestSpending]:
                result = [highestFlexible, highestSpending]
            else :
                result = [highestSpending, highestFlexible]
            for category in L :
                if category not in result :
                    result.append(category)
            for category in result :
                if fixedPercentagesDict[category] == 100 : # move to end
                    result.remove(category)
                    result.append(category)
        return result

    # returns list of lists, where first element is percentage of spendings to cut, 
    # and second element is amount of money saved if cut back by that percentage
    def getAmountSaved(category) :
        totalSpent, fixedAmount = Suggestions.avgMonthlyCategoryTotals(category)
        result = []
        flexibleAmount = totalSpent - fixedAmount
        flexiblePercentage = Suggestions.roundHalfUp((flexibleAmount/totalSpent)*100)
        if fixedAmount == totalSpent : # all fixed expenses
            percentages = [10, 25, 40]
            result.append("fixed")
            for percentage in percentages :
                amountSaved = (percentage/100) * totalSpent
                result.append([percentage, amountSaved])
        else :
            percentages = [int(flexiblePercentage/4), int(flexiblePercentage/2), 
                int(flexiblePercentage*0.75)]
            result.append("total")
            for percentage in percentages :
                amountSaved = (percentage/100) * totalSpent
                result.append([percentage, amountSaved])
        return result

    # returns list of lists, where first element is category and the second element 
    # is a list of lists, where the first element is a percentage and the second 
    # element is the amount of money saved if spending is cut by that percentage
    def savingSuggestions() :
        nonessentials = ["Entertainment", "Personal Spending", "Clothes"]
        essentials = ["Housing/Utilities", "Food", "Insurance"]
        categoryPercentagesDict = Suggestions.getCategoryPercentages()
        fixedPercentagesDict = Suggestions.getFixedPercentages()
        savingsSpentPercentage = Suggestions.getSpendingPercentage()
        categoryOrder = Suggestions.getOrder(nonessentials)+Suggestions.getOrder(essentials)
        result = []
        for category in categoryOrder :
            categorySuggestion = [category, Suggestions.getAmountSaved(category)]
            result.append(categorySuggestion)
        return result

    def getStringAnalysis() :
        avgSpending = Suggestions.avgMonthlyTotalSpending()[0]
        totalAmountSpent = Suggestions.getSpendingPercentage()
        # dictionary mapping category to its percentage of total spending
        categoryPercentages = Suggestions.getCategoryPercentages()
        result = f'''
Average Spending per Month: ${avgSpending}
You're spending {totalAmountSpent}% of your savings each month on average.
Where you're spending your money:\n'''
        for category in categoryPercentages :
            result += f'{category}: {categoryPercentages[category]}%\n'
        return result

    def getStringSavingSuggestions() :
        suggestionsList = Suggestions.savingSuggestions()
        result = ""
        for i in range(len(suggestionsList)) :
            category = suggestionsList[i][0]
            number = i + 1
            result += f"\n\n{number}. {category}\n"
            dataList = suggestionsList[i][1:][0]
            spendingType = dataList[0]
            savingsList = dataList[1:]
            for suggestion in savingsList :
                percentage = suggestion[0]
                amountSaved = suggestion[1]
                suggestionString = f'Cut back {percentage}% on spending \
to save approximately ${Suggestions.roundHalfUp(amountSaved)}/month.\n'
                result += suggestionString
        return result