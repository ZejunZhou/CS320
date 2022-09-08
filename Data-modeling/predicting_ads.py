from sklearn.linear_model import LogisticRegression
import pandas as pd
from sklearn.preprocessing import PolynomialFeatures, OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import make_column_transformer
from sklearn.model_selection import cross_val_score



class UserPredictor:
    
    def __init__(self):
        self.model = None
    
    def fit(self, train_users, train_logs, train_y):
        dic_id = train_logs.groupby("user_id").sum("seconds").to_dict()["seconds"]
        for i in train_users["user_id"]:
            if i not in dic_id:
                dic_id[i] = 0
        dic_id = dict(sorted(dic_id.items()))
        train_users["total seconds"] = dic_id.values()  ## add total seconds from train_logs to train_users
        
        
        dic_id_num = train_logs.groupby("user_id")["user_id"].count().to_dict()
        for i in train_users["user_id"]:
            if i not in dic_id_num:
                dic_id_num[i] = 0
        dic_id_num = dict(sorted(dic_id_num.items()))
        train_users["id num"] = dic_id_num.values()
        
        
        trans = make_column_transformer(
        (OneHotEncoder(), ["badge"]),
        (PolynomialFeatures(1, include_bias = False), ["past_purchase_amt", "age", "total seconds", "id num"]),
        ) ## set the transformer
        
        model = Pipeline([
        ("trans", trans),
        ("logistic", LogisticRegression(max_iter = 200))]
        )
        
        self.model = model
        
        self.model.fit(train_users[["badge", "past_purchase_amt", "age", "total seconds", "id num"]], train_y["y"])
        
        scores = cross_val_score(self.model, train_users[["badge", "past_purchase_amt", "age", "total seconds", "id num"]], train_y["y"])
        print(f"AVG: {scores.mean()}, STD: {scores.std()}\n")
        
        
    def predict(self, test_users, test_logs):
        dic_id = test_logs.groupby("user_id").sum("seconds").to_dict()["seconds"]
        for i in test_users["user_id"]:
            if i not in dic_id:
                dic_id[i] = 0
        dic_id = dict(sorted(dic_id.items()))
        test_users["total seconds"] = dic_id.values()  ## add total seconds from train_logs to test_users 
        
        
        dic_id_num = test_logs.groupby("user_id")["user_id"].count().to_dict()
        for i in test_users["user_id"]:
            if i not in dic_id_num:
                dic_id_num[i] = 0
        dic_id_num = dict(sorted(dic_id_num.items()))
        test_users["id num"] = dic_id_num.values()
        
        return self.model.predict(test_users[["badge", "past_purchase_amt", "age", "total seconds", "id num"]])
    
    
        
        
        
        
        
        
        