import plotly.express as px
import pandas as pd
import plotly.io as pio
pio.renderers.default='browser'
import pandas as pd



def show_capacity(stations, bikes):
    # Your Mapbox access token
    mapbox_access_token = 'pk.eyJ1IjoiYXZlcnlzbWl0aCIsImEiOiJjbDBhMnZzajUwOGkwM2pvYTdzYmdod2Z3In0.Frv1JuzmSJxP2K7Bs3YVcA'

    px.set_mapbox_access_token(mapbox_access_token)


    chi = bikes
    chi = stations.merge(chi, how='inner', on='station_id')
    chi['totals'] = chi['num_docks_available'] + chi ['num_bikes_available']

    chi_short = chi.head(500)
    chi_short.to_csv('short_chi.csv')
    print(chi.columns)

    chi['time_dt'] = pd.to_datetime(chi['time'])  # Ensure it's a datetime
    df_grouped_by_hour = chi.groupby([chi['time_dt'].dt.hour,'station_id']).agg({'num_bikes_available': 'mean'}).reset_index()
    df_grouped_by_hour = df_grouped_by_hour.merge(stations, on='station_id', how='inner')


    # Flag for no bikes available
    df_grouped_by_hour['out_of_bikes'] = df_grouped_by_hour['num_bikes_available'] < 1

    # Create percentages being used
    df_max_capacity = chi.groupby('station_id').agg({'totals': 'max'}).reset_index()
    df_max_capacity.to_csv('capacity.csv')
    df_grouped_by_hour = df_grouped_by_hour.merge(df_max_capacity, on='station_id', how='inner')
    df_grouped_by_hour['capacity'] = df_grouped_by_hour['num_bikes_available'] / df_grouped_by_hour['totals']
    df_grouped_by_hour.to_csv('df_grouped_by_hour.csv')



    # Choose Color
    #color_choice = 'out_of_bikes'
    #color_choice = 'num_bikes_available'
    color_choice = 'capacity'


    # Create the animated scatter plot
    fig = px.scatter_mapbox(df_grouped_by_hour,
                        lat='lat',
                        lon='lon',
                        color = color_choice,
                        animation_frame='time_dt',  # Animate by time
                        #projection='equirectangular',  # Choose the map style
                        #title='Animated Geographical Scatter Plot Example'
                        zoom=10
                        )


    # focus point
    lat_foc = chi['lat'].mean()
    lon_foc = chi['lon'].mean()
    fig.update_layout(
            geo = dict(
                #projection_scale=1000, #this is kind of like zoom
                center=dict(lat=lat_foc, lon=lon_foc), # this will center on the point
            ),

            transition = {'duration': 1}

            )



    return fig
