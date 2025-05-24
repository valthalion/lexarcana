from __future__ import annotations

import streamlit as st


#st.set_page_config(page_title='Lex Arcana', page_icon=':crossed_swords:')

roll_explorer = st.Page('roll_explorer.py', title='Roll Explorer', icon=':material/monitoring:')
character_creation = st.Page('character_creation.py', title='Character Creation', icon=':material/edit:')
character_sheet = st.Page('character_sheet.py', title='Character Sheet', icon=':material/description:')

pg = st.navigation([roll_explorer, character_creation, character_sheet])
pg.run()
