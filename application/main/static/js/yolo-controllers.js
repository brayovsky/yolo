'use strict';
/* Controllers */
var yoloControllers = angular.module('yoloControllers', []);

yoloControllers.controller('MainCtrl', ['$scope','$http',
    function MainCtrl($scope, $http) {
        $scope.appName = 'yolo';
        $scope.hideLogin = false;
        $scope.hideSignup = false;

        // Toggle login form
        $scope.toggleLogin = function(){
            $scope.hideLogin = !$scope.hideLogin;
            $scope.hideSignup = $scope.hideSignup ? !$scope.hideSignup : $scope.hideSignup;
        };
        // Toggle signup form
        $scope.toggleSignup = function(){
            $scope.hideSignup = !$scope.hideSignup;
            $scope.hideLogin = $scope.hideLogin ? !$scope.hideLogin : $scope.hideLogin;
         };

         // Access register endpoint
        $scope.yoloRegister = function(){
            $http({
                method : 'POST',
                url : 'api/v1/auth/register',
                data: $.param({
                    'username': $scope.signupUsername,
                    'email': $scope.signupEmail,
                    'password': $scope.signupPassword
                }),
                headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
                }
            }).then(function success(response) {
            // Log in user
            $scope.loginUsername = response.data.username;
            $scope.loginPassword = $scope.signupPassword;
            $scope.yoloLogin();
        },
        function error(response){
            // Highlight errors
            if (response.status_code == 400){  // Form errors

            }
        });
        };

        // Access login endpoint
        $scope.yoloLogin = function(){
            $http({
                method : 'POST',
                url : 'api/v1/auth/login',
                data: $.param({
                    'username': $scope.loginUsername,
                    'password': $scope.loginPassword
                }),
                headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
                }
            }).then(function success(response) {
            // Switch to dashboard
            console.log(response.data)
        },
        function error(response){
            // Highlight form errors
        });
        };
    }]);

yoloControllers.filter('capitalize', function() {
    return function(input) {
      return (!!input) ? input.charAt(0).toUpperCase() +
      input.substr(1).toLowerCase() : '';
    }
});