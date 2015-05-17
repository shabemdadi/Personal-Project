"""Utility file to seed crime statistics and victim data"""

from model import Crime_Stat, Victim_Stats, connect_to_db, db
from server import app
import csv
from datetime import datetime


def load_crime_stats():
    """Load crime statistics from CSV file into database"""
    
    # variables in this dataset: 'IncidntNum','Category','Descript','DayOfWeek','Date','Time','PdDistrict','Resolution','Address','X','Y','Location'


    map_category_dict = {'LARCENY/THEFT':'rape/sexual assault',
                         'BURGLARY':'robbery',
                         'SEX OFFENSES, FORCIBLE':'rape/sexual assault',
                         'VEHICLE THEFT':'personal theft/larceny',
                         'ROBBERY':'personal theft/larceny',
                         'ARSON':'personal theft/larceny',
                         'STOLEN PROPERTY':'personal theft/larceny',
                         'SEX OFFENSES, NON FORCIBLE':'rape/sexual assault'
                         }

    with open('Data\Map__Crime_Incidents_-_from_1_Jan_2003.csv', 'rb') as f:
        reader = csv.reader(f)
    
        for i, row in enumerate(reader):
            if i > 1:
                category = row[1]
                description = row[2]
                if category == "ASSAULT":
                    if "AGGRAVATED" in description:
                        map_category = "aggravated assault"
                    else:
                        map_category = "simple assault"
                else:
                    if category in map_category_dict:
                        map_category = map_category_dict[category]
                    else:
                        map_category = "Other"
                day_of_week = row[3]
                date_input = row[4]
                date = datetime.strptime(date_input, "%m/%d/%Y %H:%M")
                time_input = row[5]
                time = datetime.strptime(time_input,"%H:%M").time()
                district = row[6]
                address = row[8]
                x_cord = row[9]
                y_cord = row[10]
                
                incident = Crime_Stat(category=category,description=description,map_category=map_category,day_of_week=day_of_week,date=date,time=time,district=district,x_cord=x_cord,y_cord=y_cord)
                db.session.add(incident)
                if i % 1000 == 0:
                    db.session.commit()

        db.session.commit()

def load_victim_stats():
    """Load victim stats from csv file into database"""
    
    # variables in this dataset: 'ethnic1', 'weight', 'locationr', 'newoff', 'race1', 'notify', 'year', 'direl', 'marital2', 'treatment', 'hincome', 'injury', 
    #            'msa', 'vicservices', 'ethnic', 'newcrime', 'weapon', 'gender', 'age', 'popsize', 'hispanic', 'race', 'seriousviolent', 'region', 
    #            'weapcat'
    

    with open('Data\Victim_Stats.csv', 'rb') as f:
        reader = csv.reader(f)
                              
        for i, row in enumerate(reader):
            if i > 1:
                category = row[0]
                age_range = row[1]
                gender = row[2]
                percent = row[3]

                victim = Victim_Stats(age_range=age_range,gender=gender,category=category,percent=percent)
                db.session.add(victim)
        
        db.session.commit()
        

if __name__ == "__main__":
    connect_to_db(app)

    #load_crime_stats()
    load_victim_stats()