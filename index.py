import streamlit as st
from streamlit_option_menu import option_menu
import Main, instruction

st.set_page_config(
    page_title="Whatsapp chat Analyzer",
    page_icon="Images\Designer.jpeg"
)

class MultiPage:
    def __init__(self):
        self.pages = []
    def addPage(self, title, func):
        self.pages.append({
            "title": title,
            "function": func
        })
    def run():
        with st.sidebar:
            app = option_menu(
                menu_title='WA Analyzer',
                options=['Instruction','Application'],
                icons=['info-circle-fill','gear','chat-fill'],
                menu_icon='chat-text-fill',
                default_index=0,
                styles={
                    "container": {"padding": "5!important","background-color":'black'},
        "icon": {"color": "white", "font-size": "23px"}, 
        "nav-link": {"color":"white","font-size": "20px", "text-align": "left", "margin":"0px", "--hover-color": "blue"},
        "nav-link-selected": {"background-color": "#02ab21"},}
                
                )
        if app == 'Instruction':
            instruction.content()
        if app == 'Application':
            Main.page_content()
    run()


    



def main():  
    pass
        
    

if __name__ == "__main__":
    main()
