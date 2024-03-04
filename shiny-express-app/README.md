# Shiny Express Application


[Shiny for Python](https://shiny.posit.co/py/) provides a quick way to
create apps that are
[reactive](https://shiny.posit.co/py/docs/overview.html#reactivity),
flexible, and scalable. It comes in two flavors:

- Shiny Express - a lightweight syntax for rapid development
- Shiny Core - a more detailed syntax for robust development

This template uses Shiny Express to recast our static dashboard as an
interactive dashboard that allows users to toggle between cities.

![](images/app.png)

## Setup

Shiny Express comes in the `shiny` library, which is installed with the
`requirements.txt` file of this repository.

You can also
[install](https://shiny.posit.co/py/docs/install-create-run.html) the
`shiny` library with:

``` bash
pip install shiny
```

Tip - if you use VS Code, install the helpful [Shiny for Python VS Code
Extension](https://marketplace.visualstudio.com/items?itemName=Posit.shiny-python),
which will allow you to preview apps as you build them.

## The Idea

With Shiny, you provide your user input widgets that collect values from
the user. You then use the values to create specially rendered output
objects.

Behind the scenes, Shiny tracks dependencies for you between values and
objects and also handles caching.

Whenever a user changes an input widget’s value, Shiny automatically
updates every output that depends on those values—and only the outputs
that depend on those values.

## Get started

Save your Shiny app as a directory that contains a file named `app.py`.

- `app.py` will contain the code that creates the app.
- The directory will contain any files that support the app. Being
  self-contained makes it easy to published the finished app.

Be sure to import the `shiny` and `shiny.express` modules ot use within
your app.

## Add an input

Use a `ui.input_*()` function to place an interactive widget in your
app. Users can use the widget to provide a value.

For example, we add a radio button widget with:

```` markdown
```{python}
ui.input_radio_buttons(  
   "city",  
   "Select a city:",  
   {"austin": "Austin", "chicago": "Chicago", "dc": "Washington DC"}, 
   selected = "dc"   
)
```
````

**See the the [Shiny Components
Gallery](https://shiny.posit.co/py/components/) to see the complete
collection of available widgets.** The Gallery also contains demo code
for each widget that explains the widget’s cod syntax.

### How to look up an input’s value

Pay attention to the first argument you pass to the widget. This will be
the name you can use to look up the user’s value. For example, we named
our widget `"city"`, so we can look up its value as `input.city()`.

Note - widget values are special because they can change without notice.
As a result, you can only look up an input value from within a Shiny
function that knows how to use it—like the functions that create outputs
and calculations, detailed below.

## Add an output

1.  Use a `@render*` decorator to create an output.
2.  Define the output as a function, usually one that uses an input
    value. The function should return the output object. Shiny will
    rerun this function whenever it needs to recreate the output.

Our template creates a variety of outputs:

```` markdown
```{python}
@render.text
    def bikes_available():
        n_bikes = bike_data()['num_bikes_available'].sum()
        return f"{n_bikes:,}"
```
````

```` markdown
```{python}
@render_widget  
    def map():
        return show_city(stations = station_data())
```
````

```` markdown
```{python}
@render.data_frame  
    def table():
        return render.DataTable(bike_data())
```
````

Shiny provides a specific `@render*` decorator for each type of output.
Visit the [Shiny Components
Gallery](https://shiny.posit.co/py/components/) to see them all.

Notice that none of our outputs call `input.city()` directly. That is
because they all rely on intermediate calculations that use
`input.city()` and return a downstream object (in our case a filtered
data set).

## Add an intermediate calculation

A [reactive calculation]() uses a reactive input value to create a new
object, which itself becomes reactive. Shiny updates the new object (and
anything that depends on it whenever the input changes).

Reactive calculations are an efficient way to create an object that
*multiple* outputs will rely on (so you do not need to recreate the
object for each output).

1.  Use the `@reactive.calc` decorator to create a reactive calculation
2.  Define the reactive calculation as a function that uses zero or more
    input values and returns an object. Shiny will rerun this function
    whenever it needs to update the calculation.

Here is how we create a reactive calculation in our template:

```` markdown
```{python}
@reactive.calc
def bike_data():
    return bikes[bikes['city'] == input.city()]
```
````

### Use a reactive calculation

To use the output of a reactive calculation, call the name of the
calculation as a function. For example, we can access the value of
`bike_data` from above, as `bike_data()`, e.g. 

```` markdown
```{python}
@render.data_frame  
    def table():
        return render.DataTable(bike_data())
```
````

Like input values, reactive calculations can only be called from within
Shiny functions, which know how to handle reactive values.

## Provide some layout

As the number of elements in your app increases, it becomes helpful to
organize them into a layout.

See the [Shiny Layouts Gallery](https://shiny.posit.co/py/layouts/) to
skim all of Shiny’s tools for building layouts and customizing the UI.
We use several in the template:

```` markdown
```{python}
with ui.sidebar():
    # elements to appear in a sidebar
```
````

```` markdown
```{python}
with ui.layout_columns(col_widths=[5, 7]):
    # two elements to appear side by side
    # (i.e. each in their own column)
    # The first column will be 5 units wide
    # (out of a total span of 12)
    # The second column will be 7 units wide 
```
````

```` markdown
```{python}
with ui.value_box(...):
    # elements to appear in a valuebox
```
````

```` markdown
```{python}
with ui.card():
    ui.card_header("<title for the card>")
    # elements to appear in a card
```
````

## Run the application

You can run you application by clicking the play button at the top of
your `app.py` file in VS Code, or with

``` bash
shiny run --reload --launch-browser shiny-express-app/app.py
```

## Going further

The “Learn Shiny” overview page walks you through the basics of creating
a shiny express application:
<https://shiny.posit.co/py/docs/overview.html> - [Shiny
Layouts](https://shiny.posit.co/py/layouts/): provide you with examples
of all the UI elements you can use to design your application - [Shiny
Components](https://shiny.posit.co/py/components/): provides a gallery
of the various inputs, outputs and display messages you can use in
Shiny.
