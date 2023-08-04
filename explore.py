import pandas as pd
import requests
import os


if __name__ == '__main__':

    if not os.path.exists('../Data'):
        os.mkdir('../Data')

    # Download data if it is unavailable.
    if ('A_office_data.xml' not in os.listdir('../Data') and
        'B_office_data.xml' not in os.listdir('../Data') and
        'hr_data.xml' not in os.listdir('../Data')):
        print('A_office_data loading.')
        url = "https://www.dropbox.com/s/jpeknyzx57c4jb2/A_office_data.xml?dl=1"
        r = requests.get(url, allow_redirects=True)
        open('../Data/A_office_data.xml', 'wb').write(r.content)
        print('Loaded.')

        print('B_office_data loading.')
        url = "https://www.dropbox.com/s/hea0tbhir64u9t5/B_office_data.xml?dl=1"
        r = requests.get(url, allow_redirects=True)
        open('../Data/B_office_data.xml', 'wb').write(r.content)
        print('Loaded.')

        print('hr_data loading.')
        url = "https://www.dropbox.com/s/u6jzqqg1byajy0s/hr_data.xml?dl=1"
        r = requests.get(url, allow_redirects=True)
        open('../Data/hr_data.xml', 'wb').write(r.content)
        print('Loaded.')


A_office = pd.read_xml('../Data/A_office_data.xml')
B_office = pd.read_xml('../Data/B_office_data.xml')
HR = pd.read_xml('../Data/hr_data.xml')



A_office['modified_employee_office_id'] = 'A' + A_office['employee_office_id'].astype(str)
A_office.set_index('modified_employee_office_id', inplace=True)
A_office.rename_axis(None, inplace=True)

B_office['modified_employee_office_id'] = 'B' + B_office['employee_office_id'].astype(str)
B_office.set_index('modified_employee_office_id', inplace=True)
B_office.rename_axis(None, inplace=True)

HR.set_index('employee_id', inplace=True)

AB_office = pd.concat([A_office, B_office], join='outer')
ABHR_office = AB_office.merge(HR, how='inner',indicator=True,
                              right_index=True,left_index=True)
ABHR_office.sort_values(by='employee_office_id',
                        inplace=True, ascending=False)

ABHR_office.drop(columns=['employee_office_id','_merge'],
                 inplace=True)
ABHR_office.sort_index(inplace=True)
ABHR_office.sort_index


# def count_bigger_5(series):
#     return (series > 5).sum()
# x = ABHR_office.groupby('left').agg({'number_project':['median', count_bigger_5],
#                                  'time_spend_company':['mean','median'],
#                                  'Work_accident':'mean',
#                                  'last_evaluation':['mean', 'std']}).round(2)
ABHR_office.head()
pivot1 = ABHR_office.pivot_table(index='Department',
                        columns=['left','salary'],
                        values='average_monthly_hours',
                        aggfunc='median').round(2)

pivot1_filtered = pivot1[(pivot1[(0,'high')] < pivot1[(0,'medium')]) | (pivot1[(1,'low')] < pivot1[(1,'high')])]

pivot2 = ABHR_office.pivot_table(index='time_spend_company',
                        columns=['promotion_last_5years'],
                        values=['last_evaluation', 'satisfaction_level'] ,
                        aggfunc=['max', 'mean','min']).round(2)

pivot2_filtered = pivot2[(pivot2[('mean','last_evaluation',0)]) > (pivot2[('mean','last_evaluation',1)])]

print(pivot1_filtered.to_dict())
print(pivot2_filtered.to_dict())
