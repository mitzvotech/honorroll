// $.getJSON('/api/organizations', function (d) {
// 	$("#organization_name").autocomplete("search",{
// 		source: d
// 	})
// })

// $(function () {
// 	$.getJSON('/api/organizations', function (data) {
// 		$("#organization_name").autocomplete({
// 			source:data
// 		})
// 	})
// })

$(function () {
	$.getJSON('/api/organizations', function (data) {

		var input = document.querySelector("input[name=organization_name]");
		autoComplt.enable(input, {
		    // the hintsFetcher is your customized function which searchs the proper autocomplete hints based on the user's input value.
		    hintsFetcher : function (v, openList) {
		        var hints = [],
		            names = data;
		        for (var i = 0; i < names.length; i++) {
		            if (names[i].indexOf(v) >= 0) {
		                hints.push(names[i]);
		            }
		        }
		        openList(hints);
		    }
		});
	})
})