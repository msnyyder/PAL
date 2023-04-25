import pandas as pd
from datetime import date

class Schedule:
    def __init__(self, ACT, MPE, taken):
        self.ACT = ACT
        self.MPE = MPE
        self.hour_limit = 19
        self.taken = taken
        self.data = pd.read_csv('.\\course_data_2017_cleaner.csv')
        self.data.dropna(subset=['CRN', 'Title', 'Crse'], inplace=True)
        self.data = self.data[self.data["Crse"].str.isnumeric()]
        self.NUM_COLLONADES = 9

        self.constraints = {
            'COMM' : [],
            'STAT' : ['M136', 'M142'],
            'C146' : [], 
            'C157': [],
            'C170' : ['MPEX', 'M115', 'M116'],
            'C175' : [],
            'C180' : ['C170', '_ACT', 'M116', 'M123'],
            'C221' : ['_ACT', 'M117', 'M118', 'M136', 'M137', 'C180'], 
            'C239' : ['M117', 'M118', 'M136', 'M137', 'M237', 'M331'], 
            'C245' : ['C146'], 
            'C250' : ['C180'],
            'C257' : ['C257'],
            'C270' : ['C180'],
            'C290' : ['C180', 'M117', 'M118', 'M136', 'M137'],
            'C295' : [],
            'C299' : ['C180|C221'],
            'C301' : ['C146', 'C170', 'C180', 'C239'],
            'C315' : ['C290'],
            'C325' : ['C290'],
            'C331' : ['C290'],
            'C339' : ['C290|M136'],
            'C351' : ['C290'],
            'C360' : ['C331|C351', 'C239', 'C180', 'COMM'],
            'C369' : [],
            'C370' : [],
            'C372' : ['C290'],
            'C381' : ['C290'],
            'C382' : ['C221', 'C290'],
            'C389' : ['C351'],
            'C396' : ['C351|C331|COMM|ENGL'],
            'C405' : ['M137|M300|C180', 'M137|M300|C146'],
            'C406' : ['M307|M327|M331|C405'],
            'C421' : ['C339|C331|STAT'],
            'C425' : ['C325|C382'],
            'C443' : ['C331|C351'],
            'C445' : ['C425'],
            'C446' : ['M307|C331'],
            'C450' : ['C325|C381'],
            'C456' : ['C331|C339'],
            'C473' : ['M307|M310'],
            'C475' : [],
            'C476' : ['C360'],
            'C496' : ['C360|C396']
        }

        self.reqs = [
            'STAT',
            'C180', 
            'C290',
            'C331',
            'C325',
            'C339',
            'C351',
            'C360',
            'C382',
            'C396',
            'C421',
            'C425',
            'C496'
            ]
        
    def req_satisfied(self, condition, satisfied):
        if condition == '_ACT':
            return self.ACT
        elif condition == 'MPEX':
            return self.MPE
        else:
            return condition in satisfied

    def get_hours(self, course):
        if course in ['C180', 'C290']:
            return 4
        return 3
    
    def min_to_take(self, req, satisfied):
        if req[0] != 'C' or len(self.constraints[req]) == 0:
            return [req]

        min = [None] * 100
        for prereq in self.constraints[req]:
            to_take = []
            for indiv in prereq.split('|'):
                if not self.req_satisfied(indiv, satisfied) and indiv not in ['MPEX', '_ACT']:
                    to_take.extend(self.min_to_take(indiv, satisfied))
                elif indiv in ['MPEX', '_ACT']:
                    to_take = min = [None] * 100 
                    break
            to_take = to_take + [req]
            if len(to_take) < len(min):
                min = to_take
        return min
    
    def gen_paths(self, taken):
        in_schedule = []
        for req in self.reqs:
            if req not in taken:
                in_schedule.extend(self.min_to_take(req, taken + in_schedule))
        return in_schedule
    
    def eligible(self, course, credits_recieved):
        if course[0] != 'C' or len(self.constraints[course]) == 0:
            return True
        
        conditions = self.constraints[course]
        for condition in conditions:
            if all([self.req_satisfied(prereq, credits_recieved) for prereq in condition.split('|')]):
                return True

        return False
    
    def find_courses_after(self, course, afteryear, curterm):
        if course[0] == 'C' and course != 'COMM':
            return self.data.loc[((self.data['Crse'].astype('int32') == int(course[-3:])) & (self.data['Year'] >= afteryear) & ((self.data['Term'] == 'Spring') | (curterm == 'Fall')))]
        return []
     
    def find_courses_in(self, course, curyear, curterm):
        if course[0] == 'C' and course != 'COMM':
            return self.data.loc[((self.data['Crse'].astype('int32') == int(course[-3:])) & (self.data['Year'] == curyear) & (self.data['Term'] == curterm))]
        return []
    
    def schedule(self):
        main_schedule = self.gen_paths(self.taken)
        taken_so_far = []
        collonades = taken_so_far.count('COLL')

        [Y, M, D] = [int(val) for val in str(date.today()).split('-')]

        term = 'Fall' if M < 8 else 'Spring'
        year = Y if M < 8 else Y + 1

        titles = []
        crns = []
        profs = []
        hours = []

        while len(main_schedule) > 0:

            num_hours = 0
            can_take = [req for req in main_schedule if self.eligible(req, self.taken + taken_so_far)]
            for course in can_take:
                if num_hours + self.get_hours(course) > self.hour_limit:
                    continue
                courses = self.find_courses_in(course, year, term)
                #print(courses)
                all_left = self.find_courses_after(course, year, term)
                if len(courses) > 0:
                    for idx, row in courses.iterrows():
                        titles.append(row['Title'])
                        crns.append(row['CRN'])
                        profs.append(row['Instructor'])
                        hours.append(round(float(row['Cred'])))
                elif len(all_left) == 0:
                    titles.append(course)
                    crns.append('')
                    profs.append('')
                    hours.append(self.get_hours(course))
                else:
                    continue

                num_hours += self.get_hours(course)
                taken_so_far.append(course)
                main_schedule.remove(course)
            
            while collonades < self.NUM_COLLONADES and num_hours + self.get_hours('COLL') < self.hour_limit:
                titles.append('COLL')
                crns.append('')
                profs.append('')
                hours.append(3)
                taken_so_far.append('COLL')
                num_hours += self.get_hours('COLL')
                collonades += 1

            if term == 'Fall':
                term = 'Spring'
            else:
                term = 'Fall'
                year += 1
        
        return titles, crns, profs, hours