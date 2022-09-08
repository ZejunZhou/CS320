import pandas as pd
import zipfile
import io
import csv

race_lookup = {
    "1": "American Indian or Alaska Native",
    "2": "Asian",
    "21": "Asian Indian",
    "22": "Chinese",
    "23": "Filipino",
    "24": "Japanese",
    "25": "Korean",
    "26": "Vietnamese",
    "27": "Other Asian",
    "3": "Black or African American",
    "4": "Native Hawaiian or Other Pacific Islander",
    "41": "Native Hawaiian",
    "42": "Guamanian or Chamorro",
    "43": "Samoan",
    "44": "Other Pacific Islander",
    "5": "White",
}

class Applicant:
    def __init__(self, age, race):
        self.age = age
        self.race = set()
        if  type(race) is int:
            if str(race) in race_lookup:
                self.race.add(race_lookup[str(race)])
        else:
            for r in race:
                if str(r) in race_lookup:
                    self.race.add(race_lookup[str(r)])
    def __repr__(self):
        sort_list = sorted(list(self.race))
        return "Applicant(" + "\'" + self.age + "\'" + ", " + str(sort_list) + ")"
    
    def lower_age(self):
        if "<" in self.age:
            index = self.age.find("<")
            return int(self.age[index+1:])
        if ">" in self.age:
            index = self.age.find(">")
            return int(self.age[index+1:])
        if "-" in self.age:
            index = self.age.find("-")
            return int(self.age[0:index])
        
    def __lt__(self, other):
        return self.lower_age() < other.lower_age()
    

class Loan:
    def __init__(self, values):
        self.loan_amount = values["loan_amount"]
        self.property_value = values["property_value"]
        self.interest_rate = values["interest_rate"]
        self.applicants = []
        
        if self.loan_amount == "NA" or self.loan_amount == "Exempt":
            self.loan_amount = -1
        if self.property_value == "NA" or self.property_value == "Exempt":
            self.property_value = -1
        if self.interest_rate == "NA" or self.interest_rate == "Exempt":
            self.interest_rate = -1
        self.loan_amount = float(self.loan_amount)
        self.property_value = float(self.property_value)
        self.interest_rate = float(self.interest_rate)
        
        applicant_race_list = []
        applicant_race_list.append(values["applicant_race-1"])
        applicant_race_list.append(values["applicant_race-2"])
        applicant_race_list.append(values["applicant_race-3"])
        applicant_race_list.append(values["applicant_race-4"])
        applicant_race_list.append(values["applicant_race-5"])
        
        co_applicant_race_list = []
        co_applicant_race_list.append(values["co-applicant_race-1"])
        co_applicant_race_list.append(values["co-applicant_race-2"])
        co_applicant_race_list.append(values["co-applicant_race-3"])
        co_applicant_race_list.append(values["co-applicant_race-4"])
        co_applicant_race_list.append(values["co-applicant_race-5"])
        
        self.applicants.append(Applicant(values["applicant_age"], applicant_race_list))
        
        if values["co-applicant_age"] != "9999":
            self.applicants.append(Applicant(values["co-applicant_age"], co_applicant_race_list))
            
    def __str__(self):
        if len(self.applicants) == 1:
            return "<Loan: " + str(self.interest_rate) + "% on $" + str(self.property_value) +  " with 1 applicant(s)>"
        else:
            return "<Loan: " + str(self.interest_rate) + "% on $" + str(self.property_value) +  " with 2 applicant(s)>"
        
    def __repr__(self):
        if len(self.applicants) == 1:
            return "<Loan: " + str(self.interest_rate) + "% on $" + str(self.property_value) +  " with 1 applicant(s)>"
        else:
            return "<Loan: " + str(self.interest_rate) + "% on $" + str(self.property_value) +  " with 2 applicant(s)>"
        
    def yearly_amounts(self, yearly_payment):
    # TODO: assert interest and amount are positive
        result = []
        amt = self.loan_amount
        assert self.interest_rate > 0 and amt > 0

        while amt > 0:
            yield amt
            # TODO: add interest rate multiplied by amt to amt
            amt =  amt + (amt * self.interest_rate) / 100
            # TODO: subtract yearly payment from amt
            amt = amt - yearly_payment
            
class Bank:
    def __init__(self, name):
        list_bank = pd.read_json("banks.json")
        self.lei = 0
        for i in range(len(list_bank)):
            if list_bank.loc[i]["name"] == name:
                self.lei = list_bank.loc[i]["lei"]
                
        zf = zipfile.ZipFile("wi.zip")
        f = zf.open("wi.csv")
        reader = csv.DictReader(io.TextIOWrapper(f))
        self.bank_loan_list = []
        for row in reader:
            if row["lei"] != self.lei:
                continue
            else:
                self.bank_loan_list.append(Loan(row))
                
    def __len__(self):
        return len(self.bank_loan_list)
    
    def __getitem__(self, lookup):
        return self.bank_loan_list[lookup]
                
        
                
                
       
        
    
        
    
            
        
        
        
            
