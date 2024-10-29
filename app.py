import plotly.express as px
from shiny.express import input, ui
from shinywidgets import output_widget, render_widget, render_plotly
from shiny import render
import seaborn as sns

import palmerpenguins  # This package provides the Palmer Penguins dataset
from palmerpenguins import load_penguins

# Add a sidebar
with ui.sidebar(position="left", bg="#f8f8f8", open="open"):
    ui.h2("Sidebar")  # Sidebar header
    # Insert Drop-Down menu
    ui.input_selectize(
        id="selected_attribute",
        label="Selected Attribute",
        choices=["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"],
    )
    # Insert Numeric Input field
    ui.input_numeric(id="plotly_bin_count", label="Bin Count (Plotly)", value=5)
    # Insert a slider input
    ui.input_slider(
        id="seaborn_bin_count", label="Bin Count (Seaborn)", min=3, max=21, value=7
    )

    # Insert checkbox filter
    ui.input_checkbox_group(
        id="selected_species_list",
        label="Species",
        choices=["Adelie", "Gentoo", "Chinstrap"],
        selected=["Adelie", "Gentoo", "Chinstrap"],
        inline=False,
    )
    # Inster a dividing line
    ui.hr()
    # Insert a link
    ui.a(
        "Source code on GitHub",
        href="https://github.com/matthewpblock/cintel-02-data/tree/main",
        target="_blank",
    )

# Main content

# Use the built-in function to load the Palmer Penguins dataset
penguins_df = palmerpenguins.load_penguins()
penguins = load_penguins()

ui.page_opts(title="Matt's Penguin Block", fillable=True)  # Insert page header
with ui.layout_columns():  # Format into columns

    with ui.card():
        ui.card_header("Data Table")

        @render.data_frame
        def penguins_dt():
            return render.DataTable(penguins)

    with ui.card():
        ui.card_header("Data Grid")

        @render.data_frame
        def penguins_dg():
            return render.DataGrid(penguins)


with ui.layout_columns():  # Create a second row of columns

    with ui.card(fill=True):
        ui.card_header("Plotly Histogram")

        @render_widget
        def plot1():
            scatterplot = px.histogram(
                data_frame=penguins,
                x=input.selected_attribute(),
                nbins=input.plotly_bin_count(),
            ).update_layout(
                title={"text": "Palmer Penguins", "x": 0.5},
                yaxis_title="Count",
                xaxis_title=input.selected_attribute(),
            )
            return scatterplot

    with ui.card():
        ui.card_header("Seaborn Histogram")

        @render.plot
        def plot2():
            ax = sns.histplot(
                data=penguins,
                x=input.selected_attribute(),
                bins=input.seaborn_bin_count(),
            )
            ax.set_title("Palmer Penguins")
            ax.set_xlabel(input.selected_attribute())
            ax.set_ylabel("Number")
            return ax


# Insert a Plotly Scatterplot (not in a column)
with ui.card(full_screen=True):
    ui.card_header("Plotly Scatterplot: Species")

    @render_plotly
    def plotly_scatterplot():
        return px.scatter(
            data_frame=penguins,
            x="bill_length_mm",
            y="bill_depth_mm",
            color="species",
            symbol="island",
            labels={
                "bill_depth_mm": "Bill Depth",
                "bill_length_mm": "Bill Length",
                "species": "Species",
                "island": "Island"
            },
        )