import logging
logger = logging.getLogger(__name__)
import streamlit as st
import requests
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks
import json

SideBarLinks()

st.subheader("You found an easter egg: Mark Fontenont is about to fire you! Wish him a happy birthday before...")
