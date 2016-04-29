var app=angular.module('ita',['angularUtils.directives.dirPagination']);

app.controller("DocumentController",['$scope','$http',function($scope,$http){
	$scope.message="Hello World";


	$http.get("http://127.0.0.1:5000/display").then(function(response){
		$scope.docs=response.data;
		console.log($scope.docs);
	});

	


}]);