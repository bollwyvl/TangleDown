function tangledownload(tangle){
    var system = {
        'constraints': tangle.__constraints,
        'suggestions': []
    };
		        
    for(var v in tangle){
        if(v == '__constraints' || v == 'initialize' || v == 'update'){
            continue;
        }
        system.suggestions.push(["#"+v, tangle[v]])
    }


    $.ajax({
        url: '/tangle/' + encodeURIComponent(JSON.stringify(system)),
        success: function(data){
                if(data.solution){
                    for(var v in data.solution){
                        tangle[v] = data.solution[v]
                    }
                }
            },
        async: false
    })
}