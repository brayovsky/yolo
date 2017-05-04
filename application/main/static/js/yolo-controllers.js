'use strict';
/* Controllers */
var yoloControllers = angular.module('yoloControllers', ['yoloServices']);

yoloControllers.controller('MainCtrl', ['$scope','$http','$location','saveAuthToken','deleteAuthToken',
    function MainCtrl($scope, $http, $location, saveAuthToken, deleteAuthToken) {
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
                    $scope.errors.signupUsername = response.data.username;
                 }
                 if (response.data.email){
                    $scope.highlightInput('signup-email');
                    $scope.errors.signupEmail = response.data.email;
                 }
                 if (response.data.password){
                    $scope.highlightInput('signup-password');
                    $scope.errors.signupPassword = response.data.password;
                 }
            }
            else if (response.status == 403){ // User exists
                // Go to login
                $scope.userExists = true;
                $scope.showSignup = false;
                $scope.showLogin = true;
                $scope.loginUsername = $scope.signupUsername;
                $scope.userErrorMessage = 'User exists. Could you be trying to log in?';
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
            // Delete existing tokens, save new ones, switch to dashboard
            deleteAuthToken();
            saveAuthToken(response.data.token);
            $location.path('/dashboard');
        },
        function error(response){
            // Highlight form errors
            if (response.status == 400){
                if (response.data.username){
                    $scope.highlightInput('login-username');
                    $scope.errors.loginUsername = response.data.username;
                 }
                 if (response.data.password){
                    $scope.highlightInput('login-password');
                    $scope.errors.loginPassword = response.data.password;
                 }
            }
            // Bad credentials but no form error
            else if (response.status == 401){
                $scope.userErrorMessage = 'Wrong username or password';
                $scope.userExists = true
            }

        });
        };
    }]);

yoloControllers.controller('DashboardCtrl', ['$scope', '$http','Bucketlist','$location','SharedData',
    function DashboardCtrl($scope, $http, Bucketlist, $location, SharedData){
        // Get all bucketlists
        Bucketlist.get({}, function success(response){
            $scope.bucketlists = response.bucketlists;
        },
        function error(response){
            console.log(response.data);
            // Lacks authentication, go back home
        });
        $scope.loadBucketlist = function(){
//            alert($scope.bucketlistToView)
            $location.path('/viewbucketlist/1');
        };

        $scope.searchBucketlists = function(){
            // send request to search
            if($scope.searchTerm !== '' || $scope.searchTerm !== undefined){
                SharedData.setSearchTerm($scope.searchTerm);
                $location.path('/search');
            }
            return;
        };

        $scope.showBucketlistForm = false;
        $scope.toggleBucketlistForm = function(){
            $scope.showBucketlistForm = !$scope.showBucketlistForm;
        };
        $scope.errors = {
            bucketlistName: []
        };
        $scope.createBucketlist = function(){
            if($scope.bucketlistName === '' || $scope.bucketlistName === undefined){
                // Add errors
                $scope.errors.bucketlistName.push('Name cannot be empty');
                return;
            }
            // Post to API
            Bucketlist.create({}, $.param({ 'name': $scope.bucketlistName }), function success(response){
                // Add new bucketlist
                $scope.bucketlists.push(response);
            }, function error(response){
                if (response.status == 400){ // Form errors
                    for (var i=0;i<response.data.name.length;i++){
                        $scope.errors.bucketlistName.push(response.data.name[i]);
                    }
                }
                else if (response.status == 403){
                    // Lacks authentication, go home
                    $location.path("/");
                }

            });
        };
    }]);

yoloControllers.controller('BucketlistCtrl', ['$scope','$routeParams','SingleBucketlist',
    function($scope, $routeParams, SingleBucketlist){
        console.log($routeParams);
        // Get the bucketlist
        SingleBucketlist.get({id: $routeParams.id}, function success(response){
            $scope.bucketlist = response
        }, function error(response){
            console.log(response);
        });

        $scope.errors = {
            itemName: []
        }

        $scope.addNewItem = function() {
            // Use item service to add item if name is present
            if($scope.newItemName === '' || $scope.newItemName === undefined) {
                $scope.errors.itemName.push('Item name cannot be empty');
                return;
                }

        };

    }
]);

yoloControllers.controller('SearchCtrl', ['$scope','SharedData','Bucketlist',
    function($scope, SharedData, Bucketlist){
        $scope.searchTerm = SharedData.getSearchTerm();
        Bucketlist.get({q: $scope.searchTerm}, function success(response){
            $scope.bucketlists = response.bucketlists
        });
    }

]);

yoloControllers.filter('capitalize', function() {
    return function(input) {
      return (!!input) ? input.charAt(0).toUpperCase() +
      input.substr(1).toLowerCase() : '';
    }
});

yoloControllers.factory('SharedData', function () {
    var data = {
        searchTerm: ''
    };
    return {
        getSearchTerm: function () {
            return data.searchTerm;
        },
        setSearchTerm: function (searchTerm) {
            data.searchTerm = searchTerm;
        }
    };
});
