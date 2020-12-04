
$( document ).ready(function() {
	console.log("Document loaded.")

	let button = document.getElementById("detect-button");
	console.log(button);
	button.addEventListener("click", function() {
		console.log("Clicked");
		let loading = document.getElementById("loading");
		loading.style.display = "block";
		let results = document.getElementById("results");
		results.innerHTML = "";
	})

	$(function() {
		$("#author-textbox-input").autocomplete({
			source : function(request, response) {
				console.log(request.term);
				$.ajax({
					type: "POST",
					url : "http://localhost:5000/search",
					dataType : "json",
					cache: false,
					data : {
						term : request.term,
						category : "author"
					},
					success : function(data) {
						//alert(data);
						response(data);
					},
					error: function(jqXHR, textStatus, errorThrown) {
						console.log(textStatus + " " + errorThrown);
					}
				});
			},
			minLength : 2
		});
	});
	$(function() {
		$("#context-textbox-input").autocomplete({
			source : function(request, response) {
				console.log(request.term);
				$.ajax({
					type: "POST",
					url : "http://localhost:5000/search",
					dataType : "json",
					cache: false,
					data : {
						term : request.term,
						category : "context"
					},
					success : function(data) {
						//alert(data);
						response(data);
					},
					error: function(jqXHR, textStatus, errorThrown) {
						console.log(textStatus + " " + errorThrown);
					}
				});
			},
			minLength : 1
		});
	});
});