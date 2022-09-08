# project: p3
# submitter: zzhou443
# partner: none
# hours: 7

import os
from collections import deque
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
import pandas as pd
import time
import requests

class GraphSearcher:
    def __init__(self):
        self.visited = set()
        self.order = []

    def go(self, node):
        raise Exception("must be overridden in sub classes -- don't change me here!")

    def dfs_search(self, node):
        # 1. clear out visited set
        # 2. start recursive search by calling dfs_visit
        self.visited.clear()
        self.order.clear()
        return self.dfs_visit(node)
        

    def dfs_visit(self, node):
        # 1. if this node has already been visited, just `return` (no value necessary)
        if node in self.visited:
            return
        # 2. mark node as visited by adding it to the set
        self.visited.add(node)
        # 3. add this node to the end of self.order
        self.order.append(node)
        # 4. get list of node's children with this: self.go(node)
        children = self.go(node)
        # 5. in a loop, call dfs_visit on each of the children
        for i in children:
            self.dfs_visit(i)
            
    def bfs_search(self, node):
        # the first node to explore is the starting point
        self.order.clear()
        self.visited.clear()
        todo = deque([node])

        # keep looping while there are unexplored nodes
        while len(todo) > 0:
            curr = todo.popleft() # pop from beginning
            self.visited.add(curr)
            self.order.append(curr)
            children = self.go(curr)
            print(children)
            for i in self.go(curr):
                if i not in self.visited:
                    todo.append(i)
                    self.visited.add(i)
            
import pandas as pd

            
class MatrixSearcher(GraphSearcher):
    def __init__(self, df):
        super().__init__() # call constructor method of parent class
        self.df = df

    def go(self, node):
        children = []
        # TODO: use `self.df` to determine what children the node has and append them
        for node, has_edge in self.df.loc[node].items():
            if has_edge == 1:
                children.append(node)
        return children
    
class FileSearcher(GraphSearcher):
    def __init__(self):
        super().__init__()
    
    def __init__(self):
        super().__init__()
    
    def go(self, file):
        path = os.path.join("file_nodes", file)
        with open(path) as f:
            data = f.read().strip().replace("\n", ",")
            data_list = data.split(",")
        return data_list[1:]
        
    def message(self):
        msg = ""
        for child in self.order:
            path = os.path.join("file_nodes", child)
            with open(path) as f:
                data = f.read().strip().replace("\n", ",")
                data_list = data.split(",")
            msg = msg + data_list[0]
        return msg
    
class WebSearcher(GraphSearcher):
    def __init__(self, driver):
        super().__init__()
        self.driver = driver
        
    def go (self, url):
        self.driver.get(url)
        s = self.driver.page_source
        index_list = [i for i in range(len(s)) if s.startswith('<a href=', i)]
        list_node = []
        url_index = url.find("Node")
        url_front = url[:url_index]
        for i in index_list:
            list_node.append(s[i+9:i+20])
        return [url_front + i for i in list_node]
    
    def table(self):
        df = ""
        df_list = []
        for i in self.order:
            df1 = pd.read_html(i)
            df_list.append(df1[0])
        return pd.concat(df_list).reset_index(drop = True)
    
def reveal_secrets(driver, url, travellog):
    list_password = list(travellog["clue"])
    password = ""
    for i in list_password:
        password = password + str(i)
    password = int(password)
    driver.get(url)
    time.sleep(3)
    search = driver.find_element(by = "id", value = "password")
    button = driver.find_element(by = "id", value = "attempt-button")
    search.clear()
    search.send_keys(password)
    button.click()
    time.sleep(3)
    button2 = driver.find_element(by = "id", value = "securityBtn")
    button2.click()
    time.sleep(3)
    image = driver.find_element(by = "id", value = "image").get_attribute("src")
    response = requests.get(image)
    if response.status_code == 200:
        with open("Current_Location.jpg", 'wb') as f:
            f.write(response.content)
    location = driver.find_element(by = "id", value = "location").text
    return location