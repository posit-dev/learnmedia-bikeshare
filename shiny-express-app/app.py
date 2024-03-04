# app.py
  
from shiny import reactive
from shiny.express import input, ui, render
from shinywidgets import render_widget  
from faicons import icon_svg as icon

import shared
from helpers import show_city, show_trend

ui.page_opts(title="Bikeshare availability in three cities", )

with ui.sidebar():
    ui.input_radio_buttons(  
        "city",  
        "Select a city:",  
        {"austin": "Austin", "chicago": "Chicago", "dc": "Washington DC"}, 
        selected = "dc"   
    )  

@reactive.calc
def bike_data():
    return shared.bikes[shared.bikes['city'] == input.city()]

@reactive.calc
def station_data():
    return shared.stations[shared.stations['city'] == input.city()]

with ui.layout_columns():

    with ui.value_box(
        showcase = icon("bicycle"),
        theme = ui.value_box_theme(bg = "#9FD8CB")
    ):
        "Bikes available"
        @render.text
        def bikes_available():
            latest_day_data = shared.bikes[shared.bikes['time'].dt.date == shared.bikes['time'].dt.date.max()]

            n_bikes = (
              latest_day_data.groupby("time")["num_bikes_available"]
              .sum()
              .max()
            )
            
            return f"{n_bikes:,}"
    
    with ui.value_box(
        showcase = icon("square", style="regular"),
        theme = ui.value_box_theme(bg = "#517664", fg = "#FFFFFF")
    ):
        "Average bikes available"
        @render.text
        def average_bikes_available():
            avg_bikes = bike_data()['num_bikes_available'].median().astype(int)
            return f"{avg_bikes:,}"

    with ui.value_box(
        showcase=icon("building", style="regular"),
        theme = ui.value_box_theme(bg = "#2D3319", fg = "#FFFFFF")
    ):
        "Number of stations"
        @render.text
        def number_of_stations():
            n_stations = bike_data()['station_id'].nunique()
            return f"{n_stations:,}"

with ui.layout_columns(col_widths=[5, 7]):

    with ui.card():
        ui.card_header("Station Map")
        @render_widget  
        def map():
            return show_city(stations = station_data())
            
    with ui.card():
        ui.card_header("Availability")
        @render_widget
        def line_chart():
            return show_trend(bike_data())

with ui.layout_columns():

    with ui.card():
        ui.card_header("Station information")
        @render.data_frame  
        def table():
            return render.DataTable(bike_data().head(1000))
