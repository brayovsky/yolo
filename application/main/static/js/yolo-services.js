var yoloServices = angular.module('yoloServices', ['ngResource', 'ngCookies']);

//Bucketlist services
yoloServices.factory('Bucketlist', ['$resource', 'getAuthTokens',
    function ($resource, getAuthTokens) {
        return $resource(
            "http://127.0.0.1:5000/api/v1/bucketlists/",
        {}, {
        get: {
            method: 'GET',
            cache: false,
            isArray: false,
            headers: { Authorization: 'Basic ' + getAuthTokens() }},
        create: {
            method: 'POST',
            cache: false,
            isArray: false,
            headers: { Authorization: 'Basic ' + getAuthTokens(), 'Content-Type': 'application/x-www-form-urlencoded'}}
    });
}]);

// Store auth tokens
yoloServices.factory('saveAuthToken',['$cookies',
    function($cookies) {
        return function(token) {
        var encodedToken = btoa(token + ':');
        $cookies.authToken = encodedToken;
    };
}]);

// Check for auth-tokens
yoloServices.factory('getAuthTokens', ['$cookies',
    function($cookies) {
        return function() {
            var authentication = $cookies.authToken;
            if (authentication !== undefined && authentication !== "") {
                return authentication;
            }
            return "";
        };
    }]);

// Delete auth credentials
yoloServices.factory('deleteAuthToken', ['$cookies',
    function($cookies) {
        return function() {
        if ($cookies.authToken !== '' || $cookies.authToken !== undefined){
            $cookies.authToken = "";
        }
    };
}]);