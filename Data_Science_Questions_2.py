import pandas as pd

dir_loc = '...TitanicData.csv'

data = pd.read_csv(dir_loc)
#%%
data.describe()
#We see that there were 714 passengers in total. The oldest passenger was 80 and youngest was under a year. 
#The maximum number of siblings and spuses were 5, while the maximum number of parents and children were 6.
#Furthermore, the average amount spent on fare was $34.7

#%%
data.info()
#There are 12 features in total with 714 enteries per feature, except for cabin and embarked, which have 
#185 and 712, respectively. 5 of the features have interger values, 2 features have float values, and 5 
#features are of type object.

#%%
#Check to make sure there are only two unique var (Male, Female)
data['Sex'].describe()

def male_female_survival(titanic_data):
    '''
    Parameters
    ----------
    titanic_data : DataFrame
        Takes as input the titanic data.

    Returns
    -------
    None.

    '''
    #Create a list with the 2 classes of sex
    sex = ['male', 'female']
    #Iterate over each class
    for value in sex:
        #Print the number of passengers and the number that survived per class
        print(f"{len(titanic_data[titanic_data['Sex']==value])} {value}'s were on the ship and {len(titanic_data[(titanic_data['Sex']==value) & (titanic_data['Survived']==1)])} survived")
    
male_female_survival(data)
#%%
def male_female_family_survival(titanic_data):
    '''
    Parameters
    ----------
    titanic_data : DataFrame
        Takes as input the titanic data.

    Returns
    -------
    titanic_data : DataFrame
        Returns the titanic dataframe with the number of relatives grouped.
.

    '''
    #Initiatlize a list with the 2 classes of sex
    sex = ['male', 'female']
    #Combine the two columns to get a single number of relatives on the ship.  
    sum_relatives = titanic_data['SibSp'] + titanic_data['Parch']

    titanic_data['relative_groups'] = pd.cut(x = sum_relatives,
                                        bins = [float("-inf"),0,1,float("inf")],
                                        labels = ['alone','pairs','3+'])    
    
    #Insert new column for total number of relatives
    titanic_data.insert(13,'sum_relatives', sum_relatives)
    
    #Iterate over each class
    for value in sex:
        #Determine if there are equal to or more than 3 relatives 
        three_or_more = len(titanic_data[(titanic_data['Sex']==value) & (titanic_data['sum_relatives']>=2)])
        #Determine if there are no relatives
        alone = len(titanic_data[(titanic_data['Sex']==value) & (titanic_data['sum_relatives']==0)])
        #Determine if there is a single relative
        pairs = len(titanic_data[(titanic_data['Sex']==value) & (titanic_data['sum_relatives']==1)])
        
        print(f"{three_or_more} {value}'s were traveling with 3 or more family members, {alone} {value}'s were traveling alone, and {pairs} {value}'s were traveling in pairs")
        
    return titanic_data
    
titanic_data = male_female_family_survival(data)
#%%
def passengers_departed(titanic_data):
    '''
    Parameters
    ----------
    titanic_data : DataFrame
        Takes as input the titanic data.

    Returns
    -------
    None.

    '''
    #Create a dictionary that contains the number of passengers, which embarked per location 
    embarked = titanic_data['Embarked'].value_counts().to_dict()
    #Create a dct where we define each location
    dct = {'S':'Southampton',
           'Q':'Queenstown',
           'C':'Cherbourg'
           }
    
    #Iterate over the embarked locations
    for key, value in embarked.items():
        print(f"{value} passengers departed from {dct[key]}")
    
passengers_departed(data)
#%%
def passengers_class(titanic_data):
    '''
    Parameters
    ----------
    titanic_data : DataFrame
        Takes as input the titanic data.

    Returns
    -------
    None.

    '''
    #Create a dictionary that contains the number of passengers per class
    pass_class = titanic_data['Pclass'].value_counts().to_dict()
    #Create a dct where we define each class
    dct = {1:'1st Class',
           2:'2nd Class',
           3:'3rd Class'
          }
    
    #Iterate over the classes
    for key, value in pass_class.items():
        print(f"{value} passengers were in {dct[key]}")
    
passengers_class(data)
#%%                                         
def passengers_fare(titanic_data):
    '''
    Parameters
    ----------
    titanic_data : DataFrame
        Takes as input the titanic data.

    Returns
    -------
    None.

    '''
    #Determine if the data is skewed
    fare_skew = titanic_data['Fare'].skew()
    #Determine the mean and median values
    fare_describe = titanic_data['Fare'].describe()
    
    #If the data is not highly skewed we will use mean to identify the high/low fare
    if -1 < fare_skew < 1:
        pass_fare = (titanic_data['Fare'] >= fare_describe.loc['mean']).to_frame() 
    #If the data is highly skewed we will use the median
    else:
        pass_fare = (titanic_data['Fare'] >= fare_describe.loc['50%']).to_frame() 
    
    #Determine how many passengers paid high and low fares
    pass_fare = pass_fare['Fare'].value_counts().to_dict()
    #Create a dictionary, which defines true and false values 
    dct = {True:'High Fare',
           False:'Low Fare',
          }
    #Iterate over the fare values
    for key, value in pass_fare.items():
        print(f"{value} passengers paid a {dct[key]}")
    
passengers_fare(data)
#%%
def bin_passenger_age(titanic_data):
    '''
    Parameters
    ----------
    titanic_data : DataFrame
        Takes as input the titanic data.

    Returns
    -------
    titanic_data : DataFrame
        Returns the titanic dataframe with the ages binned.

    '''
    #Create a list, which defines the age groups
    age_groups = ['0-10','11-20','21-30','31-40','41-50','51-60','61+']
    
    #Bin the different ages
    titanic_data['age_labels'] = pd.cut(x = titanic_data['Age'],
                                        bins = [0,10,20,30,40,50,60,float("inf")],
                                        labels = age_groups)
    #Iterate over the age groups
    for age_group in age_groups:
        print(f"{len(titanic_data[(titanic_data['age_labels']==age_group) & (titanic_data['Survived']==1)])} passengers aged {age_group} survived.")

    return titanic_data

titanic_data = bin_passenger_age(titanic_data)

#%%

survival_grouped_1 = titanic_data.groupby(['Survived'])[['Age','Fare']].aggregate(['min','mean','max'])
#Here we see that age was fairly similar between passengers who survived (28) and those who didn't (30). We also see that passengers who survived
#paided on average a higher fare ($52).

survival_grouped_2 = titanic_data.groupby(['Pclass'])['Survived'].sum()
#Here we see that the largest proportion of pasengers who survived were from first class.

survival_grouped_3 = titanic_data.groupby(['Sex'])['Survived'].sum()
#Here we see that the largest proportion of pasengers who survived were female.

survival_grouped_4 = titanic_data.groupby(['Embarked'])['Survived'].sum()
#Here we see that the largest proportion of pasengers who survived Embarked from Southampton. 

survival_grouped_5 = titanic_data.groupby(['relative_groups'])['Survived'].sum()
#Here we see that the largest proportion of pasengers who survived travelled alone.

survival_grouped_6 = titanic_data.groupby(['Sex','Pclass','relative_groups'])['Survived'].sum()
#When we combine the variables together we find that the largest proportion of passengers who survived were females in first class who were
#travelling in pairs. This was closely followed by females in first class who were travelling alone.    

#%%
#I used the pandas groupby function to approach the final question. The groupby function allowed me to perform a number of 
#analyses such a aggregation and sum, in conjunction to filtering the data by categories. This was beneficial as the DataFrame 
#contained both continuous and categorical data.Therefore, I was able to analyze them seperatly and together. 

























