$(document).ready(function(){

// var countries = new Bloodhound({
//   datumTokenizer: Bloodhound.tokenizers.obj.whitespace('name'),
//   queryTokenizer: Bloodhound.tokenizers.whitespace,
//   limit: 10,
//   prefetch: {
//     // url points to a json file that contains an array of country names, see
//     url: "/words_json",
//     // url: '../data/countries.json',
//     // the json file contains an array of strings, but the Bloodhound
//     // suggestion engine expects JavaScript objects so this converts all of
//     // those strings
//     filter: function(list) {
//       return $.map(list, function(country) { return { name: country }; });
//     }
//   }
// });

// // kicks off the loading/processing of `local` and `prefetch`
// countries.initialize();

// // passing in `null` for the `options` arguments will result in the default
// // options being used
// $('input[name=text]').typeahead({
//     highlight: true
// }, {
//   name: 'countries',
//   displayKey: 'name',
//   // `ttAdapter` wraps the suggestion engine in an adapter that
//   // is compatible with the typeahead jQuery plugin
//   source: countries.ttAdapter()
// }).bind('typeahead:selected', function(obj, datum) {
//         $('form').submit();
//     });
});

var pie_options = {
    //Boolean - Whether we should show a stroke on each segment
    segmentShowStroke : true,

    //String - The colour of each segment stroke
    segmentStrokeColor : "#fff",

    //Number - The width of each segment stroke
    segmentStrokeWidth : 2,

    //Number - The percentage of the chart that we cut out of the middle
    // percentageInnerCutout : 50, // This is 0 for Pie charts

    //Number - Amount of animation steps
    animationSteps : 100,

    //String - Animation easing effect
    animationEasing : "easeOutBounce",

    //Boolean - Whether we animate the rotation of the Doughnut
    animateRotate : true,

    //Boolean - Whether we animate scaling the Doughnut from the centre
    animateScale : false,
};

function chart_update(lang, data){
    var ctx = document.getElementById("chart_" + lang).getContext("2d");
    var myPieChart = new Chart(ctx).Pie(data, pie_options);
}

function chart_update_G(data){
    chart_update('G', data);
}

function chart_update_H(data){
    chart_update('H', data);
}

function scrollToAnchor(aid){
    var aTag = $("a[name='"+ aid +"']");
    $('html,body').animate({scrollTop: aTag.offset().top},'slow');
}

function resize_charts(){
    var widths = [];
    $('canvas').each(function(i, el){{
        var canvas = $(el);
        widths.push(canvas.parent().width());
        }});
    $('.lang').each(function(i, el){{
        var lang = $(el);
        widths.push(lang.height());
        }});
    console.log(widths);
    var min_width = Math.min.apply(Math, widths) - 20;
    $('canvas')
        .attr('width', min_width)
        .attr('height', min_width);
}

function strongs_change_group(el, group){
    $(el).parent().children().removeClass('selected');
    $(el).addClass('selected');
    $('.strongs_group').hide();
    $('.' + group).show();
}
