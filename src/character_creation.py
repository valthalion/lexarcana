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

virtus_age_modifiers = {
    'Young (16-30)': {'Coordinatio': 3, 'Sensibilitas': 3, 'Ingenium': 3, 'Ratio': 3, 'Auctoritas': 3, 'Vigor': 3},
    'Adult (31-45)': {'Coordinatio': 2, 'Sensibilitas': 3, 'Ingenium': 3, 'Ratio': 4, 'Auctoritas': 4, 'Vigor': 2},
    'Mature (46+)': {'Coordinatio': 1, 'Sensibilitas': 3, 'Ingenium': 3, 'Ratio': 5, 'Auctoritas': 5, 'Vigor': 1},
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


st.markdown('### Assign the Scores')

st.markdown('Choose a Virtus for each value')
basic_virtus = {}
for n, value in enumerate(virtus_rolls):
    c1, c2 = st.columns([1, 9])
    c1.markdown(f'{value}:')
    virt = c2.selectbox(f'{value}', [v for v in virtus if v not in basic_virtus], key=f'virtus{n}', label_visibility='collapsed')
    basic_virtus[virt] = value


st.markdown('### Chose Province')

st.markdown('Each province will provide different Peritiae modifiers')
province = st.selectbox('Province', provinces.keys())
province_modifiers = provinces[province]

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

c1, c2 = st.columns(2, border=True)

with c1:
    for virt, (peritia1, peritia2) in contributions.items():
        st.markdown(f'<center>{peritia1} <-  {virt} -> {peritia2}</center>', unsafe_allow_html=True)
        split2 = st.slider(virt, 0, basic_virtus[virt], 1, label_visibility='collapsed')
        split1 = basic_virtus[virt] - split2
        peritiae_values[peritia1][virt] = split1
        peritiae_values[peritia2][virt] = split2


with c2:
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

if errors:
    error_msg = '\n'.join(f'*    {error}' for error in errors)
    st.error(f'### Invalid Peritiae values:\n\n{error_msg}')

st.markdown('### Select Age')
age = st.selectbox('Age', virtus_age_modifiers.keys(), label_visibility='collapsed')

final_virtus = {v: basic + virtus_age_modifiers[age][v] for v, basic in basic_virtus.items()}
st.write(age, final_virtus)
