'use strict';

/* App Module */
var yoloApp = angular.module('yoloApp', [
    'ngRoute',
    'yoloControllers'
    ]);

yoloApp.config(['$routeProvider', '$locationProvider',
    function($routeProvider, $locationProvider){
        $routeProvider.
        when('/', {
            templateUrl: 'partials/main.html',
            controller: 'MainCtrl' }).
        when('/dashboard', {
            templateUrl: '/partials/bucketlists.html',
            controller: 'DashboardCtrl'
        });
        $locationProvider.html5Mode(false).hashPrefix('!');
        }]);