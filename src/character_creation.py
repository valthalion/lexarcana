from __future__ import annotations
from random import randint

import streamlit as st

# Set page config
app_title = 'Lex Arcana'
st.set_page_config(page_title=app_title, page_icon=':pencil2:')  # Different icon because :pencil: doesn't render as a page icon
st.title(app_title)
st.markdown('## :pencil: Character Creation')

virtus = ['Coordinatio', 'Sensibilitas', 'Ingenium', 'Ratio', 'Auctoritas', 'Vigor']
peritiae = ['De Natura', 'De Magia', 'De Scientia', 'De Societate', 'De Bello', 'De Corpore']
experience_fields = peritiae + ['Mos Arcanorum', 'Pax Deorum']

provinces = {
    'Roma Urbe': {'De Bello': 1, 'De Corpore': 2, 'De Magia': 3, 'De Natura': 0, 'De Scientia': 6, 'De Societate': 6},
    'Italia': {'De Bello': 1, 'De Corpore': 3, 'De Magia': 3, 'De Natura': 3, 'De Scientia': 4, 'De Societate': 4},
    'Illyricum': {'De Bello': 5, 'De Corpore': 4, 'De Magia': 1, 'De Natura': 3, 'De Scientia': 2, 'De Societate': 3},
    'Macedonia': {'De Bello': 2, 'De Corpore': 3, 'De Magia': 4, 'De Natura': 3, 'De Scientia': 3, 'De Societate': 3},
    'Achaia': {'De Bello': 1, 'De Corpore': 3, 'De Magia': 3, 'De Natura': 1, 'De Scientia': 5, 'De Societate': 5},
    'Gallia': {'De Bello': 3, 'De Corpore': 3, 'De Magia': 2, 'De Natura': 3, 'De Scientia': 4, 'De Societate': 3},
    'Iberia': {'De Bello': 3, 'De Corpore': 3, 'De Magia': 2, 'De Natura': 3, 'De Scientia': 3, 'De Societate': 4},
    'Britannia': {'De Bello': 3, 'De Corpore': 3, 'De Magia': 5, 'De Natura': 4, 'De Scientia': 2, 'De Societate': 1},
    'Germania': {'De Bello': 6, 'De Corpore': 3, 'De Magia': 3, 'De Natura': 4, 'De Scientia': 1, 'De Societate': 1},
    'Raetia': {'De Bello': 5, 'De Corpore': 3, 'De Magia': 3, 'De Natura': 5, 'De Scientia': 1, 'De Societate': 1},
    'Thracia': {'De Bello': 4, 'De Corpore': 4, 'De Magia': 3, 'De Natura': 4, 'De Scientia': 1, 'De Societate': 1},
    'Dacia': {'De Bello': 5, 'De Corpore': 4, 'De Magia': 3, 'De Natura': 3, 'De Scientia': 2, 'De Societate': 1},
    'Asia': {'De Bello': 1, 'De Corpore': 3, 'De Magia': 3, 'De Natura': 2, 'De Scientia': 5, 'De Societate': 4},
    'Armenia': {'De Bello': 3, 'De Corpore': 4, 'De Magia': 1, 'De Natura': 5, 'De Scientia': 3, 'De Societate': 2},
    'Mesopotamia': {'De Bello': 3, 'De Corpore': 3, 'De Magia': 5, 'De Natura': 2, 'De Scientia': 3, 'De Societate': 2},
    'Aegyptus': {'De Bello': 2, 'De Corpore': 2, 'De Magia': 5, 'De Natura': 1, 'De Scientia': 5, 'De Societate': 3},
    'Syria': {'De Bello': 3, 'De Corpore': 2, 'De Magia': 3, 'De Natura': 1, 'De Scientia': 4, 'De Societate': 5},
    'Arabia': {'De Bello': 2, 'De Corpore': 2, 'De Magia': 4, 'De Natura': 2, 'De Scientia': 3, 'De Societate': 5},
    'Numidia': {'De Bello': 4, 'De Corpore': 3, 'De Magia': 1, 'De Natura': 5, 'De Scientia': 2, 'De Societate': 3},
    'Mauretania': {'De Bello': 3, 'De Corpore': 3, 'De Magia': 3, 'De Natura': 6, 'De Scientia': 1, 'De Societate': 2},
}

ages = {
    'Young (16-30)': {'modifiers': {'Coordinatio': 3, 'Sensibilitas': 3, 'Ingenium': 3, 'Ratio': 3, 'Auctoritas': 3, 'Vigor': 3}, 'min': 16, 'max': 30},
    'Adult (31-45)': {'modifiers': {'Coordinatio': 2, 'Sensibilitas': 3, 'Ingenium': 3, 'Ratio': 4, 'Auctoritas': 4, 'Vigor': 2}, 'min': 31, 'max': 45},
    'Mature (46+)': {'modifiers': {'Coordinatio': 1, 'Sensibilitas': 3, 'Ingenium': 3, 'Ratio': 5, 'Auctoritas': 5, 'Vigor': 1}, 'min': 46, 'max': 99},
}

specialties = {
    'De Bello': ['Axes and Maces', 'Bows', 'Castra', 'Daggers', 'Missiles', 'Swords', 'Spears', 'Tactics', 'Threaten'],
    'De Corpore': ['Brawling', 'Carousing', 'Climbing', 'Jumping', 'Larceny', 'Marching', 'Running', 'Stealth', 'Swimming'],
    'De Magia': ['Clairvoyance', 'Favor of the Gods', 'Forbidden Cults', 'Imperial Cults', 'Interpretation of Dreams',
                 'Interpretation of Omens', 'Precognition', 'Retrocognition', 'Superstitions'],
    'De Natura': ['Beast Lore', 'Exploration', 'Foraging', 'Herb Lore', 'Hunting', 'Navigation', 'Riding', 'Sailing', 'Weather'],
    'De Scientia': ['Architecture', 'Crafts', 'Machinae', 'Decipher', 'Geography', 'History', 'Investigation', 'Medicine', 'Philosophy'],
    'De Societate': ['Command', 'Deceit', 'Decorum', 'Negotiation', 'Oratory', 'Performance', 'Politics', 'Seduction', 'Streetwise'],
}

offices = {
    'Assasin': 'De Corpore',
    'Augur': 'De Magia',
    'Diplomat': 'De Societate',
    'Explorer': 'De Natura',
    'Fighter': 'De Bello',
    'Scholar': 'De Scientia',
}

office_modifiers = {
    'Assasin': {'hp': 1, 'pietas': 1},
    'Augur': {'hp': -1, 'pietas': 3},
    'Diplomat': {'hp': 1, 'pietas': 1},
    'Explorer': {'hp': 2, 'pietas': 0},
    'Fighter': {'hp': 3, 'pietas': -1},
    'Scholar': {'hp': 0, 'pietas': 2},
}

hp_and_pietas = {'hp': ['Coordinatio', 'Vigor'], 'pietas': ['Sensibilitas', 'Ratio']}

errors = []  # No errors, add as they are encountered to process later


st.divider()


st.markdown('### Personal Details')

name = st.text_input('Name')
col1, col2 = st.columns(2, gap='large', vertical_alignment='bottom')
with col1:
    age_value = st.number_input('Age (this will impact HP and Pietas)', min_value=16, max_value=99, step=1)
with col2:
    for age in ages:
        if ages[age]['max'] >= age_value:
            break
    st.markdown(f'Age range: {age}')
sex = st.radio('Sex', ['Male', 'Female'])


st.divider()


st.markdown('### Determine Basic Virtutes')

st.markdown('Roll 2d6 for each virtus, click the button below for a random roll, or keep the standard array. You will assign the rolls later.')
random_roll = st.button('Random Roll')
if random_roll:
    initial_rolls = tuple(
        sorted(
            (randint(1, 6) + randint(1, 6) for _ in range(len(virtus))),
            reverse=True
        )
    )
else:
    initial_rolls = (11, 9, 7, 7, 5, 3)  # Default array
virtus_rolls_columns = st.columns(len(virtus))
virtus_rolls_fields = [
    col.number_input(
        f'Virtus roll {n}', min_value=2, max_value=12, value=initial_rolls[n], step=1,
        label_visibility='collapsed', help='roll 2d6'
    )
    for n, col in enumerate(virtus_rolls_columns)
]
virtus_rolls = tuple(sorted(virtus_rolls_fields, reverse=True))


st.divider()


st.markdown('### Assign the Scores')

st.markdown('Choose a Virtus for each value')
basic_virtutes = {}
for n, value in enumerate(virtus_rolls):
    c1, c2 = st.columns([1, 9])
    c1.markdown(f'{value}:')
    virt = c2.selectbox(f'{value}', [v for v in virtus if v not in basic_virtutes], key=f'virtus{n}', label_visibility='collapsed')
    basic_virtutes[virt] = value


st.divider()


st.markdown('### Chose Province')

st.markdown('Each province will provide different Peritiae modifiers')
province = st.selectbox('Province', provinces.keys())
province_modifiers = provinces[province]


st.divider()


st.markdown('### Determine Peritiae')

st.markdown('Split each virtus into the corresponding Peritiae')
contributions = {
    'Sensibilitas': ['De Natura', 'De Magia'],
    'Ingenium': ['De Magia', 'De Scientia'],
    'Ratio': ['De Scientia', 'De Societate'],
    'Auctoritas': ['De Societate', 'De Bello'],
    'Vigor': ['De Bello', 'De Corpore'],
    'Coordinatio': ['De Corpore', 'De Natura'],
}

peritiae_values = {peritia: {province: province_modifiers[peritia]} for peritia in peritiae}

col1, col2 = st.columns(2, border=True)

with col1:
    for virt, (peritia1, peritia2) in contributions.items():
        st.markdown(f'<center>{peritia1} <-  {virt} -> {peritia2}</center>', unsafe_allow_html=True)
        split2 = st.slider(virt, 0, basic_virtutes[virt], 1, label_visibility='collapsed')
        split1 = basic_virtutes[virt] - split2
        peritiae_values[peritia1][virt] = split1
        peritiae_values[peritia2][virt] = split2


with col2:
    for peritia, values in peritiae_values.items():
        explanation = ' | '.join(f'{origin}: {value}' for origin, value in values.items())
        peritia_value = sum(values.values())
        if 3 <= peritia_value <= 18:  # Valid values, default formatting
            st.markdown(f'#### {peritia}: {peritia_value}')
        else:  # Invalid peritia value: set red background to highlight
            st.markdown(f'#### :red-background[{peritia}: {peritia_value}]')
            reason = 'Too low, must be at least 3' if peritia_value < 3 else f'Too high, must be at most 18'
            error = f'{peritia}: {peritia_value} -> {reason}'
            errors.append(error)
        st.markdown(explanation)

final_peritiae = {peritia: sum(values.values()) for peritia, values in peritiae_values.items()}
if not any(value >= 15 for value in final_peritiae.values()):
    errors.append('At least one Peritia value must be 15 or more to qualify for an office')

if errors:
    error_msg = '\n'.join(f'*    {error}' for error in errors)
    st.error(f'### Invalid Peritiae values:\n\n{error_msg}')
    st.stop()

final_virtutes = {v: basic + ages[age]['modifiers'][v] for v, basic in basic_virtutes.items()}


st.divider()


st.markdown('### Choose Background Specialties')
chosen_specialties = {}

st.markdown('Select a specialty with a rating of +2')
col1, col2 = st.columns(2)
with col1:
    peritia = st.selectbox('Peritia', specialties.keys(), key='sp_2_per')
with col2:
    specialty = st.selectbox('Specialty', specialties[peritia], key='sp_2_sp')
    chosen_specialties[specialty] = 2

st.markdown('Select a specialty with a rating of +1')
col1, col2 = st.columns(2)
with col1:
    peritia = st.selectbox('Peritia', specialties.keys(), key='sp_1_1_per')
with col2:
    specialty = st.selectbox('Specialty', [specialty for specialty in specialties[peritia] if specialty not in chosen_specialties], key='sp_1_1_sp')
    chosen_specialties[specialty] = 1

st.markdown('Select a specialty with a rating of +1')
col1, col2 = st.columns(2)
with col1:
    peritia = st.selectbox('Peritia', specialties.keys(), key='sp_1_2_per')
with col2:
    specialty = st.selectbox('Specialty', [specialty for specialty in specialties[peritia] if specialty not in chosen_specialties], key='sp_1_2_sp')
    chosen_specialties[specialty] = 1



st.divider()


st.markdown('### Choose Office')
office = st.selectbox('Office', [office for office in offices if final_peritiae[offices[office]] >= 15])

st.markdown('### Tirocinium')
st.markdown('Select two new specialties at +1 from the Peritia associated to the Office')
peritia = offices[office]

col1, col2 = st.columns(2)
with col1:
    specialty = st.selectbox('Specialty', [specialty for specialty in specialties[peritia] if specialty not in chosen_specialties], key='sp_1_3_sp')
    chosen_specialties[specialty] = 1
with col2:
    specialty = st.selectbox('Specialty', [specialty for specialty in specialties[peritia] if specialty not in chosen_specialties], key='sp_1_4_sp')
    chosen_specialties[specialty] = 1

hp = sum(final_virtutes[virt] for virt in hp_and_pietas['hp']) + office_modifiers[office]['hp']
pietas = sum(final_virtutes[virt] for virt in hp_and_pietas['pietas']) + office_modifiers[office]['pietas']


st.divider()


st.markdown('### Experience Multipliers')

st.markdown(f'''
    Select experience multipliers. Each must be between 2 and 10, and the highest one (ties allowed) should correspond
    to the Peritia associated to the Office ({offices[office]}). A total of 24 points should be allocated.
''')
exp_multipliers = {}
for field in experience_fields:
    col1, col2, col3 = st.columns([3, 5, 2], vertical_alignment='center', gap='medium')
    with col1:
        st.markdown(f'#### {field}')
    with col2:
        multiplier = st.slider(field, min_value=2, max_value=10, step=1, key=f'xpmultiplier_{field}', label_visibility='hidden')
        exp_multipliers[field] = multiplier
    with col3:
        st.markdown(f'#### {multiplier}')
    exp_multipliers[field] = multiplier
allocated = sum(exp_multipliers.values())
st.markdown(f'#### :red-background[Allocated: {allocated}]' if allocated > 24 else f'#### Allocated: {allocated}')
if allocated > 24:
    errors.append(f'Too many points allocated ({allocated})')
if any(value > exp_multipliers[offices[office]] for value in exp_multipliers.values()):
    errors.append(f'Multiplier for {offices[office]} is not the highest')

if errors:
    error_msg = '\n'.join(f'*    {error}' for error in errors)
    st.error(f'### Invalid Experience Multipliers allocation:\n\n{error_msg}')
    st.stop()


st.divider()


st.markdown('### Hit Points and Pietas')

col1, col2 = st.columns(2)
with col1:
    st.markdown(f'#### Hit Points: {hp}')
    contributors = hp_and_pietas['hp'] + [office]
    contributions = [final_virtutes[virt] for virt in contributors[:2]] + [office_modifiers[office]['hp']]
    st.markdown(' | '.join(f'{contributor}: {contribution}' for contributor, contribution in zip(contributors, contributions)))
with col2:
    st.markdown(f'#### Pietas: {pietas}')
    contributors = hp_and_pietas['pietas'] + [office]
    contributions = [final_virtutes[virt] for virt in contributors[:2]] + [office_modifiers[office]['pietas']]
    st.markdown(' | '.join(f'{contributor}: {contribution}' for contributor, contribution in zip(contributors, contributions)))


character = {
    'name': name,
    'age': age_value,
    'sex': sex,
    'province': province,
    'office': office,
    'rank': 'Gregarius',  # Starting rank
    'virtutes': final_virtutes,
    'peritiae': final_peritiae,
    'specialties': chosen_specialties,
    'hp': hp,
    'pietas': pietas,
    'exp_multipliers': exp_multipliers,
}
