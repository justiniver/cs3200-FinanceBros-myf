import streamlit as st
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

SideBarLinks()

st.write("# About this App")

st.markdown (
    """
    Our project aims to empower users to make strategic financial decisions by 
    providing insights derived from the expertise of top traders, political influencers, 
    and comprehensive market analyses, all tailored to their personal financial choices. 
    Through our platform, users will have the ability to view detailed performance metrics 
    and strategies employed by leading financial figures, offering a unique perspective on 
    investment opportunities. Additionally, the platform will incorporate real-time data and 
    trends, enabling users to stay informed about the latest developments in the financial world. 
    By leveraging personalized recommendations, our product will help users navigate the complexities 
    of the market, optimize their investment portfolios, and achieve their financial goals with greater 
    confidence and precision. Finance Bros are not financial advisors.

    The goal of this demo is to provide how certain users will interact with our software data!
    Stay tuned for more information and features to come!

    Disclaimer: The information provided on this platform is for informational purposes only 
    and should not be construed as financial advice. We are not licensed financial advisors. 
    Any investment decisions or financial strategies discussed here should be considered with caution 
    and consulted with a qualified financial advisor. Your financial situation is unique, 
    and it is important to seek personalized advice before making any financial decisions.

    """
        )
