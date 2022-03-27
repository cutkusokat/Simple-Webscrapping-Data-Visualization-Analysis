#!/usr/bin/env python
# coding: utf-8

# In[63]:


#pip install bs4 Anaconda command line
#!pip install requests 

from bs4 import BeautifulSoup # this module helps in web scrapping.
import requests  # this module helps us to download a web page
import pandas as pd # required to store the requested table in a dataframe
import matplotlib.pyplot as plt # data visualization
import seaborn as sns


# In[64]:


# this link contains information about cities and towns in Turkey

url = "https://en.wikipedia.org/wiki/Provinces_of_Turkey"


# In[65]:


#store the information of webpage in text format and assign it to the variable named city_data

city_data  = requests.get(url).text


# In[66]:


soup = BeautifulSoup(city_data,"html5lib")


# In[67]:


#find all html tables in the web page
tables = soup.find_all('table') # in html table is represented by the tag <table>

# examine how many tables were found
len(tables)


# In[18]:


##display tables 
tables


# In[68]:


for index,table in enumerate(tables):
    if ("Provinces of the Republic of Turkey" in str(table)):
        table_index = index
print(table_index)


# In[69]:


print(tables[table_index].prettify())


# In[79]:


population_data = pd.DataFrame(columns=["Rank", "Province", "Area(km^2)", "Population(2000 census)", "Population(2020)"])

for row in tables[table_index].tbody.find_all("tr"):
    col = row.find_all("td")
    if (col != []):
        rank = col[0].text
        province = col[1].text
        area = col[2].text.strip()
        population_2000 = col[3].text.strip()
        population_2020 = col[4].text.strip()
        population_data = population_data.append({"Rank":rank, "Province":province, "Area(km^2)":area, "Population(2000 census)":population_2000, "Population(2020)":population_2020}, ignore_index=True)

population_data


# In[80]:


## /n from the Rank column and Province column
for i in range(0,len(population_data)):
        population_data["Province"][i] = population_data["Province"][i][:-1]
        population_data["Rank"][i] = population_data["Rank"][i][:-1]


# In[82]:


#glimpse at population data
population_data.head()


# In[83]:


#check whether there is any undescribed values or not 
population_data.isnull().sum()


# In[77]:


#observe the type of numeric columns
type(population_data["Population(2020)"])


# In[84]:


for i in range(0,len(population_data)):
    population_data["Population(2020)"][i] = population_data["Population(2020)"][i].replace(",","")
    population_data["Population(2000 census)"][i] = population_data["Population(2000 census)"][i].replace(",","")
    population_data["Area(km^2)"][i] = population_data["Area(km^2)"][i].replace(",","")
population_data


# In[90]:


## change the type of numeric colums to integer
population_data[["Population(2020)"]] = population_data[["Population(2020)"]].astype(int)
population_data[["Population(2000 census)"]] = population_data[["Population(2000 census)"]].astype(int)


# In[94]:


## sort according to population 2020
sorted_pop = population_data.sort_values("Population(2020)", ascending = False)


# In[95]:


# visualize the top ten cities according to population 2020
plt.figure(figsize=(20,9))
sns.barplot(x = sorted_pop["Province"].head(10), y = sorted_pop["Population(2020)"].head(10))


# In[96]:


## sort according to population 2000
sorted_pop_2000 = population_data.sort_values("Population(2000 census)", ascending = False)


# In[97]:


# visualize the top ten cities according to population 2000
plt.figure(figsize=(20,9))
sns.barplot(x = sorted_pop["Province"].head(10), y = sorted_pop["Population(2000 census)"].head(10))

