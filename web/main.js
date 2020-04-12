
col = 0;


var msg = function(txt) {
    var el = $("<p>"+txt+"</p>");
	el.hide();
	$('#msg').prepend(el);
	el.slideDown();
    window.setTimeout(function() {  el.slideUp(); }, 2500);

}


var update = function() {
     $.getJSON("/plotterflut/data", function(data) {
     	$.each(data, function(i, item) {
                if (item.i == 23) {
		     $("#"+item.x+"_"+item.y).addClass("blocked");
			
		} else {
	        var r = 233-(255 * (item.i/9));
		var newcol =  'rgb('+r+','+r+','+r+')';
		$("#"+item.x+"_"+item.y).css("background-color", newcol);
		}
	});
     
     });
    window.setTimeout(update, 10000);
}


var init = function() {
    for (y=0; y<69; y++) {
    	for (x=0; x<104; x++) {
		var elem = $('<div data-x="'+x+'" data-y="'+y+'" style="top:'+y*8+'; left:'+x*8+'" class="sq" id="'+x+'_'+y+'"></div>');
		elem.click(function(ev) {
			var el = $(ev.target);
			var bgbefore = el.css('background-color');
	                var r = 233-(255 * (col/9));
			var newcol =  'rgb('+r+','+r+','+r+')';
			el.addClass('spinner');
			el.css('background-color',newcol);
			$.get('/plotterflut/api', { 
				x: el.data('x'),
				y: el.data('y'),
				intensity: col },
			function(data) {
				el.removeClass('spinner');
				if (data =='Success') {
				el.css('background-color',newcol);
				} else {
				el.css('background-color', 'lightblue');
				msg(data);
				}
			}
			).fail(function(data) {
				el.removeClass('spinner');
				msg(data.responseText);	
				el.css('background-color',bgbefore);
			});
		
		});
    		$('body').append(elem);
    	}
    }

    for (c=0; c<8; c++) {
	        var r = 233-(255 * (c/9));
		var elem = $('<div data-c="'+c+'" style="background-color: rgb('+r+','+r+','+r+'); top:'+c*8+'; left:'+((108*8)+50)+'" class="sq col"></div>');
		elem.click(function(ev) {
			el = $(ev.target);
			$('div.col').removeClass('act');
	    		el.addClass('act');
			col = el.data('c');
		
		});
    		$('body').append(elem);
    }

    $('body').append('<div id="msg"></div>');
    var home = $('<button id="home">HOME</button>');
    home.click(function(ev) {
    	
			$.get('/plotterflut/home').fail(function(data) {
				msg(data.responseText);	
			});
    
    });
    $('body').append(home);
update();
}

$(document).ready(init);
