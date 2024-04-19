# -*- coding: utf-8 -*-
"""
Created on Thu Apr 18 17:45:40 2024

@author: yashj
"""

from flask import Flask, render_template, request
from experta import *
import random
app = Flask(__name__)

class TaxFacts(Fact):
    pass

class Tax_calculator(KnowledgeEngine):

    @Rule(TaxFacts(income=P(lambda x: x <= 55867)))
    def federal_tax_bracket_1(self):
        self.declare(TaxFacts(federal_tax_rate=0.15))

    @Rule(TaxFacts(income=P(lambda x: 55867 < x <= 111733)))
    def federal_tax_bracket_2(self):
        self.declare(TaxFacts(federal_tax_rate=0.205))

    @Rule(TaxFacts(income=P(lambda x: 111733 < x <= 173205)))
    def federal_tax_bracket_3(self):
        self.declare(TaxFacts(federal_tax_rate=0.26))

    @Rule(TaxFacts(income=P(lambda x: 173205 < x <= 246752)))
    def federal_tax_bracket_4(self):
        self.declare(TaxFacts(federal_tax_rate=0.29))

    @Rule(TaxFacts(income=P(lambda x: x > 246752)))
    def federal_tax_bracket_5(self):
        self.declare(TaxFacts(federal_tax_rate=0.33))

    # Rules for Provincial tax rates for each province
    @Rule(TaxFacts(province='Ontario'))
    def provincial_tax_ontario(self):
        self.declare(TaxFacts(provincial_tax_rate_1=0.0505, provincial_tax_rate_2=0.091))

    @Rule(TaxFacts(province='Quebec'))
    def provincial_tax_quebec(self):
        self.declare(TaxFacts(provincial_tax_rate_1=0.15, provincial_tax_rate_2=0.20))
    
    @Rule(TaxFacts(province='BC'))
    def provincial_tax_quebec(self):
        self.declare(TaxFacts(provincial_tax_rate_1=0.506, provincial_tax_rate_2=0.77))
    
    @Rule(TaxFacts(province='Alberta'))
    def provincial_tax_quebec(self):
        self.declare(TaxFacts(provincial_tax_rate_1=0.10, provincial_tax_rate_2=0.12))
    
    @Rule(TaxFacts(province='Manitoba'))
    def provincial_tax_quebec(self):
        self.declare(TaxFacts(provincial_tax_rate_1=0.108, provincial_tax_rate_2=0.127))
    
    @Rule(TaxFacts(province='NS'))
    def provincial_tax_quebec(self):
        self.declare(TaxFacts(provincial_tax_rate_1=0.087, provincial_tax_rate_2=0.149))

class TaxCalculator():
    
    def __init__():
        pass
    
    def calculate_tax(income,province,child):
        if income <= 55867:
            federal_tax = income * 0.15
        elif 55867 < income <= 111733:
            federal_tax = 55867 * 0.15 + (income - 55867) * 0.205
        elif 111733 < income <= 173205:
            federal_tax = 55867 * 0.15 + (111733 - 55867) * 0.205 + (income - 111733) * 0.26
        elif 173205 < income <= 246752:
            federal_tax = 55867 * 0.15 + (111733 - 55867) * 0.205 + (173205 - 111733) * 0.26 + (
                        income - 173205) * 0.29
        else:
            federal_tax = 55867 * 0.15 + (111733 - 55867) * 0.205 + (173205 - 111733) * 0.26 + (
                        246752 - 173205) * 0.29 + (income - 246752) * 0.33
        
        if province == 'Ontario':
            provincial_tax = income * 0.0505
            OSTC = 345
            OTB = 360
        elif province == 'Quebec':
            provincial_tax = income * 0.15
            OTB = 0
            OSTC = 0
        elif province == 'BC':
            provincial_tax = income * 0.506
            OSTC = 0
            OTB = 0
        elif province == 'Alberta':
            provincial_tax = income * 0.10
            OSTC = 0
            OTB = 0
        elif province == 'Manitoba':
            provincial_tax = income * 0.108
            OSTC = 0
            OTB = 0
        elif province == 'NS':
            provincial_tax = income * 0.087
            OSTC = 0
            OTB = 0
        else:
            provincial_tax = income * 0.1
            OSTC = 0
            OTB = 0
            

        Total_tax = federal_tax + provincial_tax
        cpp = Total_tax * 0.595
        ei = (Total_tax/100) * 1.66
        after_tax = income - Total_tax - cpp - ei
        Tax_returns = Total_tax * 0.23
        GST = random.randint(385, 496)
        carbon = 504
        child_benifit = 104.45 * child
        
        calculated_tax = {
                            'federal_tax': round(federal_tax,2),
                          'provincial_tax': round(provincial_tax,2),
                          'total_tax': round(Total_tax,2),
                          'cpp': round(cpp,2),
                          'ei': round(ei,2),
                          'income_after': round(after_tax,2),
                          'ostc': OSTC,
                          'otb': OTB,
                          'tax_return': round(Tax_returns,2),
                          'gst': GST,
                          'carbon': carbon,
                          'childB': child_benifit}
        return calculated_tax
            
            

@app.route('/', methods=['GET', 'POST'])
def index():
    # try:
    if request.method == 'POST':
        if 'calculate_tax' in request.form:
            income = float(request.form['income'])
            province = str(request.form['province'])
            child = float(request.form['child'])
            engine = Tax_calculator()
            engine.reset()
            calculated_tax = TaxCalculator.calculate_tax(income,province,child)
            print(calculated_tax)  
            federal_tax = 0
            test_tax = 0
            return render_template('index1.html', tax_result=True, calculated_tax=calculated_tax,income=income)
        else:
            return render_template('index1.html')
    return render_template('index1.html')


        

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)