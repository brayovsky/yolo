'use strict';
/* Controllers */
var yoloControllers = angular.module('yoloControllers', []);

yoloControllers.controller('MainCtrl', ['$scope',
    function MainCtrl($scope) {
        $scope.appName = "yolo";
        $scope.hideLogin = false;
        $scope.hideSignup = false;
        $scope.toggleLogin = function(){
                        $scope.hideLogin = !$scope.hideLogin;
                        $scope.hideSignup = $scope.hideSignup ? !$scope.hideSignup : $scope.hideSignup;
                        };
        $scope.toggleSignup = function(){
                        $scope.hideSignup = !$scope.hideSignup;
                        $scope.hideLogin = $scope.hideLogin ? !$scope.hideLogin : $scope.hideLogin;
                        };
    }]);

yoloControllers.filter('capitalize', function() {
    return function(input) {
      return (!!input) ? input.charAt(0).toUpperCase() +
      input.substr(1).toLowerCase() : '';
    }
});