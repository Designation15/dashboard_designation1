import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder

import config

# --- Récupération des données ---
rencontres_df = st.session_state.get('rencontres_df', pd.DataFrame())
competitions_df = st.session_state.get('competitions_df', pd.DataFrame())

st.title("📅 Liste des Rencontres")
st.markdown("RS_OVALE2-024 - Vue consolidée de toutes les rencontres")

if not rencontres_df.empty and 'rencontres_date_dt' in rencontres_df.columns:
    rencontres_filtrees = rencontres_df.copy()

    # Utilisation de la liste centralisée depuis config.py
    competitions_filtre_defaut = config.COMPETITIONS_FILTRE_DEFAUT
    
    # Bouton toggle pour activer/désactiver le filtre par défaut
    filtre_actif = st.checkbox("Activer le filtre par compétitions", value=True)
    
    if filtre_actif:
        rencontres_filtrees = rencontres_filtrees[rencontres_filtrees[config.COLUMN_MAPPING['rencontres_competition']].isin(competitions_filtre_defaut)]

    if not rencontres_filtrees.empty:
        cols_to_display = [
            config.COLUMN_MAPPING['rencontres_date'],
            config.COLUMN_MAPPING['rencontres_competition'],
            config.COLUMN_MAPPING['rencontres_locaux'],
            config.COLUMN_MAPPING['rencontres_visiteurs']
        ]
        display_df = rencontres_filtrees[cols_to_display].copy()

        # Formater la date pour l'affichage final
        display_df[config.COLUMN_MAPPING['rencontres_date']] = pd.to_datetime(display_df[config.COLUMN_MAPPING['rencontres_date']], errors='coerce').dt.strftime('%d/%m/%Y')

        display_df = display_df.rename(columns={
            config.COLUMN_MAPPING['rencontres_date']: 'Date',
            config.COLUMN_MAPPING['rencontres_competition']: 'Compétition',
            config.COLUMN_MAPPING['rencontres_locaux']: 'Locaux',
            config.COLUMN_MAPPING['rencontres_visiteurs']: 'Visiteurs'
        })

        gb = GridOptionsBuilder.from_dataframe(display_df)
        gb.configure_pagination(paginationAutoPageSize=True)
        gb.configure_side_bar()
        gb.configure_default_column(groupable=True, value=True, enableRowGroup=True, aggFunc='sum', editable=False)
        gridOptions = gb.build()

        AgGrid(
            display_df,
            gridOptions=gridOptions,
            enable_enterprise_modules=False,
            height=600,
            width='100%',
            reload_data=True,
            allow_unsafe_jscode=True,
            theme='streamlit'
        )
    else:
        st.info("Aucune rencontre trouvée avec les filtres appliqués.")
else:
    st.warning("Impossible de charger les données des rencontres.")
