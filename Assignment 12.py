
# coding: utf-8
Read the following data set:
https://archive.ics.uci.edu/ml/machine-learning-databases/adult/
Rename the columns as per the description from this file:
https://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.names
Task:
Create a sql db from adult dataset and name it sqladb
# In[1]:


import numpy as np
import pandas as pd
import sqlite3
import pandasql


# In[2]:


adult_data = pd.read_csv("https://archive.ics.uci.edu//ml//machine-learning-databases//adult/adult.data", header = None,index_col= False)
adult_data.head()


# In[3]:


adult_col_name = pd.read_csv('https://archive.ics.uci.edu//ml//machine-learning-databases//adult//adult.names', sep=":")
adult_col_name=adult_col_name.iloc[91:106].index.tolist() 
adult_col_name=adult_col_name[1:]+adult_col_name[0::-1]
adult_data.columns = adult_col_name
adult_data.head()


# In[5]:



sqladb = sqlite3.connect("sqladb.db")
sqladb.execute('''
    CREATE TABLE IF NOT EXISTS ADULTS (
         AGE             INTEGER,
         WORKCLASS       VARCHAR(100),
         FNLWGT          INTEGER,
         EDUCATION       VARCHAR(100),
         EDUCATION_NUM   INTEGER,         
         MARITAL_STATUS  VARCHAR(100),         
         OCCUPATION      VARCHAR(100),
         RELATIONSHIP    VARCHAR(100),
         RACE            VARCHAR(100),
         SEX             VARCHAR(20),
         CAPITAL_GAIN    INTEGER,
         CAPITAL_LOSS    INTEGER,
         HOURS_PER_WEEK  INTEGER,
         NATIVE_COUNTRY  VARCHAR(100),
         GT50_OR_LT50K   VARCHAR(20))
''')


# In[6]:


sql_insert = "INSERT INTO ADULTS (                                      AGE,                                                WORKCLASS,                                          FNLWGT,                                             EDUCATION,                                          EDUCATION_NUM,                                      MARITAL_STATUS,                                     OCCUPATION,                                         RELATIONSHIP,                                       RACE,                                               SEX,                                                CAPITAL_GAIN,                                       CAPITAL_LOSS,                                       HOURS_PER_WEEK,                                     NATIVE_COUNTRY,                                     GT50_OR_LT50K) values                               (%d,'%s', %d, '%s', %d, '%s','%s','%s','%s','%s',%d,%d,%d,'%s','%s')"

for index, row in adult_data.iterrows():
    sqladb.execute(sql_insert % (row['age'], 
                                 row['workclass'], 
                                 row['fnlwgt'], 
                                 row['education'],
                                 row['education-num'],
                                 row['marital-status'],
                                 row['occupation'],
                                 row['relationship'],
                                 row['race'],row['sex'],
                                 row['capital-gain'],
                                 row['capital-loss'],
                                 row['hours-per-week'],
                                 row['native-country'],
                                 row['>50K, <=50K.']))
    
sqladb.commit()


# ##1. Select 10 records from the adult sqladb

# In[7]:


sql_select="SELECT * FROM ADULTS LIMIT 10;"
conn=sqladb

result_adult_data=pd.read_sql_query(sql_select, conn) 
result_adult_data


# ##2. Show me the average hours per week of all men who are working in private sector

# In[8]:


sql_select="SELECT SEX, WORKCLASS, AVG(HOURS_PER_WEEK) FROM ADULTS WHERE SEX=' Male' and WORKCLASS=' Private'"
result_avg_hr_per_week=pd.read_sql_query(sql_select, conn)
result_avg_hr_per_week


# ##3. Show me the frequency table for education, occupation and relationship, separately

# In[9]:


## Education

sql_select="SELECT EDUCATION, COUNT(EDUCATION) FROM ADULTS GROUP BY EDUCATION;"
frequency_education=pd.read_sql_query(sql_select, conn)
frequency_education


# In[15]:


##Occupation

sql_select="SELECT OCCUPATION, COUNT(OCCUPATION) FROM ADULTS GROUP BY EDUCATION;"
frequency_occupation=pd.read_sql_query(sql_select, conn)
frequency_occupation


# In[10]:


sql_select="SELECT RELATIONSHIP, COUNT(RELATIONSHIP) FROM ADULTS GROUP BY RELATIONSHIP;"
frequency_relationship=pd.read_sql_query(sql_select, conn)
frequency_relationship


# In[ ]:


##4. Are there any people who are married, working in private sector and having a masters
degree


# In[11]:


sql_select = "SELECT MARITAL_STATUS, WORKCLASS, EDUCATION, COUNT(*) FROM ADULTS "
sql_select = sql_select + " WHERE MARITAL_STATUS like ' Married%' AND WORKCLASS = ' Private' AND EDUCATION = ' Masters'"
sql_select = sql_select + " GROUP BY MARITAL_STATUS, WORKCLASS, EDUCATION;"

result_married_private_sector_masters=pd.read_sql_query(sql_select, conn)
result_married_private_sector_masters


# 5. What is the average, minimum and maximum age group for people working in different sectors

# In[12]:


sql_select = "SELECT WORKCLASS, AVG(AGE) , MIN(AGE), MAX(AGE) FROM ADULTS GROUP BY WORKCLASS;"
people_diff_sector=pd.read_sql_query(sql_select, conn)
people_diff_sector


# ##6. Calculate age distribution by country

# In[13]:


sql_select = "SELECT NATIVE_COUNTRY, AGE, COUNT(AGE) FROM ADULTS GROUP BY NATIVE_COUNTRY, AGE;"
age_distribution_by_country=pd.read_sql_query(sql_select, conn)
age_distribution_by_country


# ##7. Compute a new column as 'Net-Capital-Gain' from the two columns 'capital-gain' and
# 'capital-loss'

# In[14]:


sql_select = "SELECT ADULTS.*, (capital_gain + capital_loss) as 'Net-Capital-Gain' FROM ADULTS;"
Capital_Gain=pd.read_sql_query(sql_select, conn)
Capital_Gain.head()

