angular.module('recEngineApp', [])
 .controller('recEngineController', function($location, $http, $q) {

  var engine = this;

  engine.pageTitle = 'Recommendation Engine';

  // AWS API Gateway host + deployment
  var host = 'https://xxxxxxxxxx.execute-api.us-east-1.amazonaws.com/production';

  // API Gateway event API endpoint
  var endpoint = '/event/';

  // default event_id
  var defaultEventId = 'ce12eb28-f04c-11e5-bcad-22000bb26533';

  var base = host + endpoint;

     console.error('location ', $location);
  var eventId = $location.search()['id'];

  recommendations = [];
  engine.recommendations = [];

  $http.get(base + (eventId || defaultEventId))
   .then(
    function(response) {

     engine.event = response.data;

     console.error('found event ', response.data);

     // from here on out we assume that each event in DynamoDB contains
     // a "recommendations" element with a list of event ids
     angular.forEach(response.data.recommendations, function(rec) {
      recommendations.push($http.get(base + rec));
     });

     $q.all(recommendations)
      .then(function(responses) {
        angular.forEach(responses, function(response) {
         console.error('found recommendation ', response.data);
         engine.recommendations.push(response.data);
        })
       },
       function(error) {
        console.error('http GET error ', error);
       });
    },
    function(error) {
     console.error('http GET error ', error);
    });

 });
