var TangleDown = this.TangleDown = function(){
    
    var log = function(msg){
        if(window.console){
            console.log(msg)
        }
    }
    
    return {
        tangledownload: _.memoize(
            // synchronous get function 
            function(tangle){
                var result = {},
                    system = {
                        'constraints': tangle.__constraints,
                        'suggestions': []
                    };
	        
                for(var k in tangle){
                    if(!_.include(['__constraints', 'initialize', 'update'], k)){
                        system.suggestions.push(["#"+k, tangle[k]]);
                        log([k, tangle[k]])
                    }
                }
                log(JSON.stringify(system))

                $.ajax({
                    url: '/tangle/' + encodeURIComponent(JSON.stringify(system)),
                    success: function(data){
                            if(data.solution){
                                result = data.solution;
                            }
                        },
                    async: false
                })
                return result;
            },
            // hash function
            function(tangle){
                var hash = "";
                for (var k in tangle){
                    if(!_.include(['__constraints', 'initialize', 'update'], k)){
                        hash += k+"="+tangle[k];
                    }
                }
                return hash;
            }
        )
    }
};

//make it
TangleDown = this.TangleDown = TangleDown();

Tangle.formats.cents_as_dollars = function (value) {
    var dollars = Math.floor(value/100);
    return sprintf("$%d.", dollars) + sprintf("%02d", value - dollars * 100);
};