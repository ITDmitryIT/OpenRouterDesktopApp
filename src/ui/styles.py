import flet as ft

class AppStyles:
    MAIN_COLUMN = {
        "scroll": "auto",
        "expand": True,
        "horizontal_alignment": ft.CrossAxisAlignment.STRETCH
    }
    
    MODEL_SELECTION_COLUMN = {
        "spacing": 10,
        "horizontal_alignment": ft.CrossAxisAlignment.STRETCH
    }
    
    CHAT_BUBBLE_USER = {
        "bgcolor": ft.Colors.BLUE_100,        # ИСПРАВЛЕНО
        "padding": 10,
        "border_radius": 15,
        "margin": ft.margin.only(right=50, bottom=10)
    }
    
    CHAT_BUBBLE_AI = {
        "bgcolor": ft.Colors.GREY_300,        # ИСПРАВЛЕНО
        "padding": 10,
        "border_radius": 15,
        "margin": ft.margin.only(left=50, bottom=10)
    }