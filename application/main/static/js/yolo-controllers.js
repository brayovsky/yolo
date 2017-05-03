'use strict';
/* Controllers */
var yoloControllers = angular.module('yoloControllers', []);

yoloControllers.controller('MainCtrl', ['$scope','$http',
    function MainCtrl($scope, $http) {
        $scope.appName = 'yolo';
        $scope.showLogin = false;
        $scope.showSignup = false;
        $scope.userExists = false;

        // Highlight inputs if they have errors
        $scope.highlightInput = function(inputid){
            $('#' + inputid).css('border', '1px solid #f00');
        }

        // Toggle login form
        $scope.toggleLogin = function(){
            $scope.showLogin = !$scope.showLogin;
            $scope.showSignup = $scope.showSignup ? !$scope.showSignup : $scope.showSignup;
        };
        // Toggle signup form
        $scope.toggleSignup = function(){
            $scope.showSignup = !$scope.showSignup;
            $scope.showLogin = $scope.showLogin ? !$scope.showLogin : $scope.showLogin;
         };

         // Access register endpoint
        $scope.yoloRegister = function(){
            // Check passwords match
            if ($scope.signupPassword !== $scope.signupRepeatPassword){
                // Highlight errors
                $scope.highlightInput('signup-password');
                $scope.highlightInput('signup-repeat-password');

                // Display message
                $scope.errors.signupRepeatPassword = ["Passwords don't match"];
                return
            }
            // Access API
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
            // Highlight new errors
            if (response.status == 400){  // Form errors
                 if (response.data.username){
                    $scope.highlightInput('signup-username');
                 }
                 if (response.data.email){
                    $scope.highlightInput('signup-email');
                    $scope.errors.signupEmail = response.data.email;
                 }
                 if (response.data.password){
                    $scope.highlightInput('signup-password');
                 }
            }
            else if (response.status == 403){ // User exists
                // Go to login
                $scope.userExists = true;
                $scope.showSignup = false;
                $scope.showLogin = true;
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
