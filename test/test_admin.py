from featurefactory.admin.admin import Commands
admin_commands = Commands()
admin_commands.set_up(drop=True)

name = 'airbnb'
problem_type = 'classification'
data_path = '/data/airbnb'
files = ['train_users_2.csv', 'sessions.csv', 'countries.csv', 'age_gender_bkts.csv']
y_index = 0
y_column = 'country_destination'

admin_commands.create_problem(name, problem_type, data_path, files, y_index, y_column)