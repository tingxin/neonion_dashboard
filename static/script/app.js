/**
 * Created by tingxxu on 1/20/16.
 */
function App(){
    this.host = window.location;
    this.currentIndex = 0;
    this.alphabet=["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"];
    this.debug = false;
}

App.prototype={
    cache:null,
    diagnostics:function(data) {
        var max= 5;
        var container= $(".diagnosticContainer");
        var diagnosticItemRights= $('.diagnosticItemRight');
        var isAddedUI = diagnosticItemRights.length>0;
        for(var index=0; index<data.length;index++){
            var diagnostic = data[index];
            var title = diagnostic["title"];
            var level = diagnostic["level"];

            if(isAddedUI){
                var diagnosticItemRight =  $(diagnosticItemRights[index]);
                var children=diagnosticItemRight.children();
                if(children.length !=max){
                    console.warn("error:diagnosticItemRight children should be "+max);
                }
                else{
                    for(var i=0;i<max;i++){
                        var child = $(children[i]);
                        child.removeClass('roundDivHighlight');
                        child.removeClass('roundDivNormal');
                        if(i<level){
                            child.addClass('roundDivHighlight');
                        }
                        else{
                            child.addClass('roundDivNormal');
                        }
                    }
                }

            }
            else{

                var newItem = $('<div/>',{
                    class:"diagnosticItem"
                }).appendTo(container);

                var newTitle = $('<div/>',{
                    class:"diagnosticItemLeft",
                    text:title
                }).appendTo(newItem);

                var newRight = $('<div/>',{
                    class:"diagnosticItemRight"
                }).appendTo(newItem)

                for(var i=0;i<max;i++){
                    if(i<level){
                        $('<div/>',{
                            class:"roundDivHighlight"
                        }).appendTo(newRight);
                    }
                    else{
                        $('<div/>',{
                            class:"roundDivNormal"
                        }).appendTo(newRight);
                    }
                }
            }

        }

    },

    layoutUI:function(gauges){

        //layout gauges
        var gaugeCount = gauges.length;
        var splictV = 100;

        $("#gauge_container").height(window.screen.height*45/100)
        var gaugeCWidth=  $("#gauge_container").width();
        var gaugeCHeight =  $("#gauge_container").height();

        var unitHWidth = gaugeCWidth/gaugeCount;
        var unitVHeight = gaugeCHeight /splictV;

        for(var index=0;index<gaugeCount;index++){
            $("#"+gauges[index]).css("left",index*unitHWidth+"px");
        }

        //layout map


    },

    //navigation
    navigation:function() {
        var naviItems = $("#navigationBar").children();
        var self = this;
        $.each(naviItems, function (index, item) {
            $(item).click(function () {
                console.info("item click");
                $.each(naviItems, function (i, innerItem) {
                    $(innerItem).removeClass("active");
                });
                $(item).addClass("active");

                if(index !=self.currentIndex){
                    $("#chart").empty();
                    $("#chart").hide();
                    if(index==0){
                        $("#chart").show();
                        self.showFuelChart();
                    }
                    else if(index ==1){
                        $("#chart").show();
                        self.showFuelChart();
                    }
                    else if(index ==2){
                        $("#chart").show();
                        self.showFuelChart();
                    }
                    else{

                    }
                    self.currentIndex = index;
                }
            });
        });
    },

    showFuelChart:function(){
        Highcharts.setOptions({
            global : {
                useUTC : false
            }
        });

        // Create the chart
        $('#chart').highcharts('StockChart', {
            chart : {
                events : {
                    load : function () {

                        // set up the updating of the chart each second
                        var series = this.series[0];
                        var series2 = this.series[1];
                        var series3 = this.series[2];
                        setInterval(function () {
                            var x = (new Date()).getTime(), // current time
                                y = Math.round(Math.random() * 100);
                            var x2 = (new Date()).getTime(), // current time
                                y2 = Math.round(Math.random() * 100);
                            var x3 = (new Date()).getTime(), // current time
                                y3 = Math.round(Math.random() * 10000);
                            series.addPoint([x, y], true, true);
                            series2.addPoint([x2, y2], true, true);
                            series3.addPoint([x3, y3], true, true);
                        }, 1000);
                    }
                }
            },

            rangeSelector: {
                buttons: [{
                    count: 1,
                    type: 'Day',
                    text: 'Day'
                }, {
                    count: 7,
                    type: 'Day',
                    text: 'Week'
                }, {
                    count: 30,
                    type: 'Month',
                    text: 'Month'
                }],
                inputEnabled: false,
                selected: 0
            },

            title : {
                text : 'Kpi with history'
            },

            exporting: {
                enabled: false
            },

            yAxis: [{ // Primary yAxis
                labels: {
                    format: '{value}%',
                    style: {
                        color: Highcharts.getOptions().colors[0]
                    }
                },
                title: {
                    text: 'KPI',
                    style: {
                        color: Highcharts.getOptions().colors[0]
                    }
                },
                opposite: false

            }

            ],

            series : [{
                name : 'Fuel',
                yAxis: 0,
                data : (function () {
                    // generate an array of random data
                    var data = [], time = (new Date()).getTime(), i;

                    for (i = -999; i <= 0; i += 1) {
                        data.push([
                                time + i * 1000,
                            Math.round(Math.random() * 100)
                        ]);
                    }
                    return data;
                }())
            }
            ]
        });
    },

    showLocationChart:function(){
        var map = $("<img/>",{
            src:"assets/map.png"
        });

        $("#chart").append(map);
    },

    refresh:function(){
        var owner =this;
        $.get(this.host+"api/all", function(data){
            owner.cache = data

            $("#locationNumber").text(data["distance"]);


        });

        $.get(this.host+"api/diagnostics", function(data){
            owner.diagnostics(data)
        });


    },

    formatTime:function(minutes){
        var hours = minutes/60;
        var min = minutes%60;
        return hours +"hours"
    },

    convertLocationToUIPos:function(pos){
        return pos
        //TODO
    }

}