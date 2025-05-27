from __future__ import annotations

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

from lexarcana.cfg import config
from lexarcana.roll_selection import Chooser
from lexarcana.tables import roll_stats_tables


# Set page config
app_title = 'Lex Arcana'
st.set_page_config(page_title=app_title, page_icon=':game_die:')
st.title(app_title)
st.markdown('## :game_die: Roll Explorer')


# Load data tables
rolls, stats = roll_stats_tables()
chooser = Chooser(rolls, stats)


# Set up roll parameters in sidebar
min_dp, max_dp = min(rolls), max(rolls)
min_diff, max_diff = min(config.difficulty_targets), max(config.difficulty_targets)
diff_step = config.difficulty_targets[1] - config.difficulty_targets[0]

st.sidebar.markdown("""# Roll Configuration""")
fate = st.sidebar.checkbox('Fate', value=True)
dice_points = st.sidebar.slider('Dice Points', min_value=min_dp, max_value=max_dp)
difficulty = st.sidebar.slider('Difficulty', min_value=0, max_value=max_diff, step=diff_step, value=min_diff)
score_function = st.sidebar.radio('Choice metric', chooser.score_functions)

if score_function == 'success_probability':
    kwargs = {'difficulty': difficulty}
elif score_function == 'beat_roll':
    roll_to_beat = st.sidebar.text_input('Roll to beat', value=rolls[dice_points][0].name)
    kwargs = {'roll_to_beat': roll_to_beat}
else:
    kwargs = {}

best, prob = chooser.choose_best(score_function, dice_points=dice_points, fate=fate, **kwargs)
st.sidebar.markdown(f"""
    # Best roll
    
    | Roll | **{best}** |
    |--|--|
    | Probability | **{prob:.2%}** |
    """)

# Plot probabilities of (selected) rolls

st.markdown('### Probability Graph')

prob_field = 'success_probs_fate' if fate else 'success_probs_no_fate'
options = [roll.name for roll in rolls[dice_points]]
y_max = max(prob for roll in options for prob in stats[roll][prob_field].values())
if len(options) <= 6:
    default_options = options
else:
    # If there is a large number of options, preselect only those that are optimal at some dt
    default_options = set()
    for dt in config.difficulty_targets:
        prob, roll = max((stats[r.name][prob_field][dt], r.name) for r in rolls[dice_points])
        default_options.add(roll)
selected = st.multiselect('Select rolls to display:', options, default=default_options)
if selected:
    fig = plt.figure()
    for roll in selected:
        plt.plot(config.difficulty_targets, stats[roll][prob_field].values(), label=roll)
    plt.title(f'Probability curve @ Dice Points = {dice_points}')
    plt.xticks(ticks=config.difficulty_targets)
    plt.xlabel('Difficulty Target')
    plt.ylabel('Probability')
    plt.vlines(difficulty, 0, y_max, linestyles='dashed', colors='black')
    if len(selected) > 1:
       plt.legend(loc='upper right')
    st.pyplot(fig)

st.markdown('### Probability Table')

probs_table = pd.DataFrame(
    [list(stats[roll.name][prob_field].values()) for roll in rolls[dice_points]],
    columns=[f'DT{dt}' for dt in config.difficulty_targets],
    index=[roll.name for roll in rolls[dice_points]]
)
st.dataframe(probs_table.style.format('{:,.2%}'))
