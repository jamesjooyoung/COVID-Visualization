# Covid 19 Dashboard
>Project: Miru Yang, James Ro

        Since 2020, there have been over 50 million recorded Covid-19 cases in the United States.
        While vaccinations and public safety measures have greatly reduced the spread and impact of 
        covid on daily life, new variants and surges mean that continued testing and vigiliance is called for.
        Most cases currently are asymptotic and minor, meaning that contagious individuals may not get tested.
        This is why reported case counts are not accurate representations of the actual spread of covid within a
        region.
        **This Covid Dashboard estimates the actual prevalence of covid in different states.**
        It can be used to see the new and probable new cases in different areas over time.
        ### Data Source
        This dashboard utilizes case data from the [Centers for Disease Control and Prevention]
        (https://www.cdc.gov/). \n
        The [data source](https://data.cdc.gov/Case-Surveillance/United-States-COVID-19-Cases-and-Deaths-by-State-o/9mfq-cb36) 
        **updates twice every 24 hours**. 
        
        # Project Architecture
        This project uses MongoDB as the database. All data acquired are stored in raw form to the
        database. An abstract layer is built in `database.py` so all queries can be done via function call.
        For a more complicated app, the layer will also be responsible for schema consistency. 
        A `plot.ly` & `dash` app is serving this web page through. Actions on responsive components
        on the page is redirected to `app.py` which will then update certain components on the page. 


