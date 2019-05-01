//  Ajax Query

$( ".load_dia" ).click(function() {
    $( "#slider-range" ).slider({
    range: true,
    min: 2017,
    max: 2030,
    values: [ 2017, 2022 ],
    slide: function( event, ui ) {

    $( "#amount" ).val( ui.values[ 0 ] + " to " + ui.values[ 1 ] );


    $.ajax({
        url: "/suggestions",
        type: "get",
        data: {jsdata: ui.values[ 0 ] + " to " + ui.values[ 1 ]},
        success: function(response) {
        var myChart_1 = echarts.init(document.getElementById('level_1'));
        myChart_1.setOption(response);
        console.log(text);
    },
        error: function(xhr) {
        //Do Something to handle error
    }

    });

  }

    });
    $( "#amount" ).val( $( "#slider-range" ).slider( "values", 0 ) +
      " to " + $( "#slider-range" ).slider( "values", 1 ) );

});

