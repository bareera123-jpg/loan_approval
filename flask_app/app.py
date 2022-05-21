# import a library

from itertools import count
from flask import Flask , render_template, request
import numpy as np
from pandas import to_datetime
import joblib

# instance of an app
app = Flask(__name__)

dt_model = joblib.load('loan_80.pkl')

@app.route('/')
def contact():
    return render_template('form.html')

@app.route("/data" , methods = ["POST"])
def data():
    Amount_Of_Loan_Required =np.array([float(request.form.get('Loan Amount'))])
    What_is_the_turnover_of_your_company_in_Cr =np.array([float(request.form.get('Turnover or AUM'))])
    Total_Payroll_Employee_Before_Year = np.array([int(request.form.get('Employee Payroll Year Before'))])
    Total_Payroll_Employee= np.array([int(request.form.get('Employee Payroll Current'))])
    total_payroll_womens =  int(request.form.get('Women Employee Current'))
    Ratio_of_women_employees = np.array([round(total_payroll_womens/100,2)])

    director_name = []
    director_name.append(request.form.get('Directors_Name'))
    bod_counts = np.array([len(director_name)])
    
    kmp_name = []
    kmp_name.append(request.form.get('Personnel_Name'))
    kmp_counts =np.array([len(kmp_name)])
   
    nominated = request.form.get('Nominated')
    if nominated == 'yes' or nominated == 'Yes':
        nominated = 1
        nom = []
        nom.append(nominated)
        Percentage_of_nominated = len(nom)/bod_counts
    else:
        nominated = 0
        nom = []
        nom.append(nominated)
        Percentage_of_nominated = len(nom)/bod_counts

    todays_date = to_datetime(request.form.get('Form_created_Date'))
    director_bod = to_datetime(request.form.get('Directors_BOD'))
    directors_age = np.array([np.average((todays_date - director_bod)/(12*(np.timedelta64(1, 'M'))))])
    percent_change_employees = (Total_Payroll_Employee - Total_Payroll_Employee_Before_Year)/Total_Payroll_Employee_Before_Year


    director_doj = to_datetime(request.form.get('Directors_DOJ'))
    directors_tenure = np.array([np.average((todays_date - director_doj)/(12*(np.timedelta64(1, 'M'))))])

    kmp_doj = to_datetime(request.form.get('Personnel_DOJ'))
    kmp_tenure = np.array([np.average((todays_date - kmp_doj)/(12*(np.timedelta64(1, 'M'))))])
    
    kmp_bod_ratio = kmp_counts/bod_counts
    kmp_as_bod = request.form.get('Director Also')
    if kmp_as_bod == 'yes' or kmp_as_bod == 'Yes':
        kmp_as_bod = 1
        kmp_bod = []
        kmp_bod.append(kmp_as_bod)
        kmp_as_bod_count_ratio = len(kmp_bod)/bod_counts
    else:
        kmp_as_bod = 0
        kmp_bod = []
        kmp_bod.append(kmp_as_bod)
        kmp_as_bod_count_ratio = len(kmp_bod)/bod_counts
    
####one hot encoding features

    Raised_funds_arr = np.zeros(1)
    Sector_of_Operation_arr = np.zeros(17)
    business_age_arr = np.zeros(1)
    social_sustaianability_arr = np.zeros(1)
    legal_form_of_company_arr = np.zeros(1)
    loan_pupose_arr = np.zeros(8)
    Business_Model_arr = np.zeros(6)
    client_type_arr = np.zeros(4)
    optional_debt_arr = np.zeros(1)
    out_standing_debt_arr = np.zeros(1)
    internal_audit_arr = np.zeros(1)
    rating_And_agency_arr = np.zeros(7)
    ratings_received_arr = np.zeros(4) 
    legal_issues_arr = np.zeros(1)
    fi_nonfi_arr = np.zeros(1)           

   

    if request.method=="POST":

        Raised_funds = request.form.get('External Funds Raised- VC/ Pvt Equity/ Angel Inv')
        if Raised_funds == 'yes' or Raised_funds == 'Yes':
            Raised_funds_arr[0] = 1 


        Sector_of_Operation = request.form.get('Sector of Operation')
        if Sector_of_Operation == 'Business Correspondent for NBFC/Banks':
            Sector_of_Operation_arr[0] = 1
        elif Sector_of_Operation=='Cleantech':
            Sector_of_Operation_arr[1] = 1
        elif Sector_of_Operation == 'Drinking Water':
            Sector_of_Operation_arr[2] =1
        elif Sector_of_Operation == 'Education':
            Sector_of_Operation_arr[3]=1
        elif Sector_of_Operation == 'Financial Services (non-lending)':
            Sector_of_Operation_arr[4] =1
        elif Sector_of_Operation == 'Food & Agriculture':
            Sector_of_Operation_arr[5] =1
        elif Sector_of_Operation == 'Healthcare':
            Sector_of_Operation_arr[6] =1
        elif Sector_of_Operation =='Housing Finance':
            Sector_of_Operation_arr[7] =1
        elif Sector_of_Operation == 'ICT for Development':
            Sector_of_Operation_arr[8] =1
        elif Sector_of_Operation == 'Microfinance':
            Sector_of_Operation_arr[9] = 1
        elif Sector_of_Operation == 'Non-farm Livelihoods':
            Sector_of_Operation_arr[10] = 1
        elif Sector_of_Operation == 'Others':
            Sector_of_Operation_arr[11] = 1
        elif Sector_of_Operation == 'Others (Financial Inclusion)':
            Sector_of_Operation_arr[12] =1
        elif Sector_of_Operation == 'Rural Distribution Channels':
            Sector_of_Operation_arr[13] =1
        elif Sector_of_Operation == 'Sanitation & Hygiene':
            Sector_of_Operation_arr[14] = 1
        elif Sector_of_Operation == 'Skill Development':
            Sector_of_Operation_arr[15] =1
        elif Sector_of_Operation == 'Small Business Finance':
            Sector_of_Operation_arr[16] =1
            
        business_age = request.form.get('Age of Business')
        if business_age == 'yes' or business_age == 'Yes':
            business_age_arr[0] = 1 

        social_sustaianability = request.form.get('Social/Sustainability Certification')
        if social_sustaianability == 'yes' or social_sustaianability == 'Yes':
            social_sustaianability_arr[0] = 1
        
        legal_form_of_company = request.form.get('Legal Form of Company')
        if legal_form_of_company == 'Public Limited' or legal_form_of_company == 'public limited':
            legal_form_of_company_arr[0] = 1

        loan_pupose = request.form.get('Purpose of Loan')
        if loan_pupose == 'Capital Expenditure':
            loan_pupose_arr[0] =1
        elif loan_pupose == 'Equipment financing':
            loan_pupose_arr[1] = 1
        elif loan_pupose == 'OnLending':
            loan_pupose_arr[2] =1
        elif loan_pupose == 'Operating Expenditure (eg: Paying Salaries)':
            loan_pupose_arr[3] =1
        elif loan_pupose == 'Others':
            loan_pupose_arr[4] = 1
        elif loan_pupose == 'Purchase order finance/Invoice Finance':
            loan_pupose_arr[5] =1
        elif loan_pupose == 'Unknown':
            loan_pupose_arr[6] =1
        elif loan_pupose == 'Working Capital':
            loan_pupose_arr[7] =1
        
        
        Business_Model = request.form.get('Business Model')
        if Business_Model == 'Financing':
            Business_Model_arr[0] =1
        elif Business_Model == 'Manufacturing':
            Business_Model_arr[1] =1
        elif Business_Model == 'Others':
            Business_Model_arr[2] =1
        elif Business_Model == 'SAAS/ Subscription':
            Business_Model_arr[3] =1
        elif Business_Model == 'Services':
            Business_Model_arr[4] =1
        elif Business_Model == 'Trading':
            Business_Model_arr[5] =1

        client_type = request.form.get('Type of Company(Client Type)')
        if client_type == 'Government':
            client_type_arr[0] =1
        elif client_type == 'Individual':
            client_type_arr[1] =1
        elif client_type == 'Public Sector Enterprise':
            client_type_arr[2] =1
        elif client_type == 'Unknown':
            client_type_arr[3] = 1

    
        optional_debt = request.form.get('Optional Convertible Debt')
        if optional_debt == 'yes' or optional_debt == 'Yes':
            optional_debt_arr[0] = 1
    
        out_standing_debt = request.form.get('Outstanding Debt')
        if out_standing_debt == 'yes' or out_standing_debt == 'Yes':
            out_standing_debt_arr[0] = 1
  
        internal_audit = request.form.get('Internal Audit')
        if internal_audit == 'yes' or internal_audit == 'Yes':
            internal_audit_arr[0] = 1

        
        rating_And_agency = request.form.get('Rating agency name')
        if rating_And_agency == 'Brickworks':
            rating_And_agency_arr[0] = 1
        elif rating_And_agency == 'CARE':
            rating_And_agency_arr[1] = 1
        elif rating_And_agency == 'CRISIL':
            rating_And_agency_arr[2] = 1
        elif rating_And_agency == 'ICRA':
            rating_And_agency_arr[3] = 1
        elif rating_And_agency == 'Ind Ra':
            rating_And_agency_arr[4] = 1
        elif rating_And_agency == 'Not rated':
            rating_And_agency_arr[5] = 1
        elif rating_And_agency == 'Other':
            rating_And_agency_arr[6] = 1

        ratings_received = request.form.get('Rating Received')
        if ratings_received == 'BB, BB+, BB-':
            ratings_received_arr[0] = 1
        elif ratings_received =='BBB, BBB+, BBB-':
            ratings_received_arr[1] = 1
        elif ratings_received == 'Not rated':
            ratings_received_arr[2] = 1
        elif ratings_received == 'Other':
            ratings_received_arr[3] = 1

        legal_issues = request.form.get('Legal Cases')
        if legal_issues == 'yes' or legal_issues == 'Yes':
            legal_issues_arr[0] = 1

        fi_nonfi = request.form.get('Financial or Non_Financial')
        if fi_nonfi == 'Non Financial' or fi_nonfi == 'non financial':
            fi_nonfi_arr[0] = 1


    print('Amount_Of_Loan_Required:',Amount_Of_Loan_Required)
    print('What_is_the_turnover_of_your_company_in_Cr:',What_is_the_turnover_of_your_company_in_Cr)
    print('Total_Payroll_Employee_Before_Year:',Total_Payroll_Employee_Before_Year)
    print('Total_Payroll_Employee:',Total_Payroll_Employee)
    print('Ratio_of_women_employees:' ,Ratio_of_women_employees)
    print('bod_counts:',bod_counts)
    print('kmp_counts:0:',kmp_counts)
    print('Percentage_of_nominated:', Percentage_of_nominated)
    print('directors_age:',directors_age)
    print('percent_change_employees:',percent_change_employees)
    print('directors_tenure:',directors_tenure)
    print('kmp_tenure:',kmp_tenure)
    print('kmp_bod_ratio:',kmp_bod_ratio)
    print('kmp_as_bod_count_ratio:',kmp_as_bod_count_ratio)

    print('Raised_funds_arr:',Raised_funds_arr)
    print('Sector_of_Operation_arr:',Sector_of_Operation_arr)
    print('business_age_arr:',business_age_arr)
    print('social_sustaianability_arr:',social_sustaianability_arr)
    print('legal_form_of_company_arr:',legal_form_of_company_arr)
    print('loan_pupose_arr:',loan_pupose_arr)
    print('Business_Model_arr:',Business_Model_arr)
    print('client_type_arr:',client_type_arr)
    print('optional_debt_arr:',optional_debt_arr)
    print('out_standing_debt_arr:',out_standing_debt_arr)
    print('internal_audit_arr:',internal_audit_arr)
    print('rating_And_agency_arr:',rating_And_agency_arr)
    print('ratings_received_arr:',ratings_received_arr)
    print('legal_issues_arr:',legal_issues_arr)
    print('fi_nonfi_arr:',fi_nonfi_arr)


    data = np.concatenate([Amount_Of_Loan_Required,What_is_the_turnover_of_your_company_in_Cr,Total_Payroll_Employee_Before_Year ,Total_Payroll_Employee,Ratio_of_women_employees,bod_counts,kmp_counts, Percentage_of_nominated,directors_age,percent_change_employees,directors_tenure,kmp_tenure ,kmp_bod_ratio,kmp_as_bod_count_ratio,Raised_funds_arr,Sector_of_Operation_arr,business_age_arr,social_sustaianability_arr,legal_form_of_company_arr,loan_pupose_arr,Business_Model_arr,client_type_arr,optional_debt_arr,out_standing_debt_arr,internal_audit_arr,rating_And_agency_arr,ratings_received_arr,legal_issues_arr,fi_nonfi_arr])
    prediction= int(dt_model.predict([data])[0])
    
    if prediction ==1:
        output = 'Loan Approved'
    else:
        output = 'Loan Not Approved'

    return render_template('result.html',predict = output)

if __name__ == '__main__':
    app.run(debug = True)