$(function(){
    $('a').filter(function() {
        return $(this).text().indexOf('tk:') === 0;
    }).each(function(){
        var link_data = td_parse_link($(this));
        $(this).attr('data-var', link_data.variable)
            .addClass(link_data.cls)
            .click(function(evt){evt.preventDefault()})
            .text(link_data.label);
    })
})

function td_parse_link(link){
    var href_matches = link.attr('href').match(/([^#:]*):/),
        txt_matches = link.text().match(/tk:(.*)( .*)/),
        result = {};
    console.log(link.attr('href'))
    result.variable = href_matches[1];
    result.cls = txt_matches[1] + " tangledown_"+result.variable;
    result.label = txt_matches[2];
    
    console.log(result)
    return result;
}