google.charts.load('current', {
        'packages':['geochart'],
        // Note: you will need to get a mapsApiKey for your project.
        // See: https://developers.google.com/chart/interactive/docs/basic_load_libs#load-settings
        'mapsApiKey': 'AIzaSyD-9tSrke72PouQMnMX-a7eZSW0jkFMBWY'
      });

      google.charts.setOnLoadCallback(drawRegionsMap);

      function drawRegionsMap() {


        var datatable = new google.visualization.DataTable();

        datatable.addColumn('string', 'Countries');
        datatable.addColumn('number', 'Cases');


        const covid_api = "https://disease.sh/v3/covid-19/countries"
        fetch(covid_api)
        .then(response => response.json())
        .then(result => {


        result.forEach((element, index, array) => {


          datatable.addRow([element.country, element.cases]);
        });
        
    })


   
        var options = {
          colorAxis: {colors: ['#F5F3F4', '#F0A1A1', '#F43331']},
          backgroundColor: {
            // stroke: '#BDA4DC',
            // strokeWidth: 5,
          },
          datalessRegionColor: '#f8bbd0',
          defaultColor: '#f5f5f5',
        };

        var chart = new google.visualization.GeoChart(document.getElementById('regions_div'));

        chart.draw(datatable, options);
  }