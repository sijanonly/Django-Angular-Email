'use strict';
angular.module('calendarApp')

.directive('emailCompose', function() {
    return {
        restrict: 'E',
        templateUrl: '/templates/email/compose.html',
        
    }
});
