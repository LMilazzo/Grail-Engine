import pandas as pd
import plotly.express as px

from Utils.RandomUtils import format_text

# >>> PLOT CONTROLLER >>>
class PlotController():
    def __init__(self):

        #--------------------------------------------------  
        #---------------------- DATA ----------------------
        #--------------------------------------------------
        self.DATA_COLUMNS = ["content", "text_formated", "role", "x", "y"]
        self._DATA = pd.DataFrame(columns=self.DATA_COLUMNS)

        #--------------------------------------------------  
        #--------------------- FIGURE ---------------------
        #--------------------------------------------------
        self._FIGURE = None
        self._HTML = None

#__________________________________________________________________________________________________________

    def addDataPlot(self, datalist: list):
        self.addData(datalist)
        return self.plot()

    def addData(self, datalist: list):
                
        # EXAMPLE
        #res = [
        #    {"role" : "user", "content": prompt["content"], "x": p_res[0,0], "y": p_res[0,1]},
        #    {"role" : "assistant", "content": response["content"], "x": r_res[0,0], "y": r_res[0,1]},
        #]

        data = pd.DataFrame(datalist)

        data["text_formated"] = data["content"].apply(lambda x: format_text(x, 25))

        self._DATA = pd.concat([self._DATA, data])
    
#__________________________________________________________________________________________________________

    def plot(self):

        self._FIGURE= px.scatter(
            self._DATA,
            x="x", y="y", color="role",
            color_discrete_map={
                "user": "#6EFF8E",
                "assistant" : "#E13FED"
            },
            custom_data=["text_formated"]
        )

        # Show
        self.updateLayout()
        self.toHtml()

        return self._HTML

    def updateLayout(self):

        self._FIGURE.update_layout(
            # Overall figure size and background
            paper_bgcolor="#000000",   # plot_background
            plot_bgcolor="#000000",    # panel_background

            # Grid lines
            xaxis=dict(
                gridcolor="#191919",   # panel_grid_major/minor
                gridwidth=1,
                zerolinecolor="#191919",
                zerolinewidth=1,
                title_text="",
                showticklabels=False
            ),
            yaxis=dict(
                gridcolor="#191919",
                gridwidth=1,
                zerolinecolor="#191919",
                zerolinewidth=1,
                title_text="",
                showticklabels=False
            ),

            # Axis ticks
            xaxis_tickcolor="#686868",
            yaxis_tickcolor="#686868",

            # Legend styling
            legend=dict(
                orientation='h',     # horizontal legend
                yanchor='bottom',    # anchor at the bottom of the plot area
                y=-0.2,              # move it below the plot (negative moves it down)
                xanchor='center',    # center horizontally
                x=0.5,
                bgcolor="#000000",   # dark background
                bordercolor="#000000",
                font=dict(color="#686868"),
                title_text = ""
            ),

            margin=dict(l=0, r=20, t=20, b=0)
        )

        self._FIGURE.update_traces(hovertemplate="%{customdata[0]}<extra></extra>")
        self._FIGURE.update_traces(marker=dict(opacity=0.5))

    def toHtml(self):

        intermediate = self._FIGURE.to_html(
            include_plotlyjs='cdn', full_html=False, 
            default_height=272, default_width=272
        )

        html = f"""
            <html><head>
                <style>
                    body {{
                        margin: 0px;
                        padding: 0px;
                        background-color: black;
                    }}
                </style>
            </head>
                <body>
                    <div id="plot">
                        {intermediate}
                    </div>
                </body>
             </html>
        """

        self._HTML = html

        return self._HTML

#__________________________________________________________________________________________________________

    def clear(self):
        self.DATA_COLUMNS = ["content", "text_formated", "role", "x", "y"]
        self._DATA = pd.DataFrame(columns=self.DATA_COLUMNS)

        return self.plot()
    
    def clearLast(self):
        self._DATA = self._DATA.iloc[:-2]
        return self.plot()
# <<< PLOT CONTROLLER <<<
