import pandas as pd
from pathlib import Path

# Leer el Calendario de Disponibilidad
FILE_PATH = Path(__file__).parent / "tables" / "Encuesta Alabanza Templo Zuriel.csv"
table = pd.read_csv(FILE_PATH)

# Dar formato para organizar los dias
calendar_col_name = 'Días en Los que Puede Ministrar sin Conflictos Horarios'
table[calendar_col_name] = table[calendar_col_name].apply(lambda x: x.split(';'))
idx = table[calendar_col_name].apply(lambda x: len(x)).idxmax()

names = table['Nombre'].to_list()
service_days = table.iloc[idx][calendar_col_name]

bin_lists:list = table[calendar_col_name].apply(lambda x: [service_days[i] in x for i in range(len(service_days))]).to_list()
avaliable_calendar = pd.DataFrame(bin_lists, index=names, columns=service_days)

# Disponibilidad por Dia
day_avaliable_persons = {day.split()[0]: avaliable_calendar.loc[avaliable_calendar[day]==True].index.tolist() for day in avaliable_calendar.columns}
for key, val in day_avaliable_persons.items(): print(key, val)
print()

# Disponibilidad por persona
person_avaliable_days = {name: avaliable_calendar.T.loc[avaliable_calendar.T[name]==1].index.tolist() for name in avaliable_calendar.index}
person_avaliable_days = {name: [day.split()[0]for day in days] for name, days in person_avaliable_days.items() }
for key, val in person_avaliable_days.items(): print(key, val)
print()

# Persona mas disponible
most_available = {person: avaliable_calendar.loc[avaliable_calendar.index==person].sum(axis=1).values[0] for person in avaliable_calendar.index}
for key, val in most_available.items(): print(key, val)
print()

# import numpy as np
# import matplotlib.pyplot as plt
# import datetime

# arr = np.array(bin_lists)
# plt.plot_date(pd.date_range(datetime.date.today(), periods=30), range(30))
# plt.show()