(function(window, document, $, angular) {

  var UPDATE_DONE_EVENT = 'aft-updated-done';

  function api_url(list_id, action) {
    return '/api/list/' + list_id + '/' + action;
  };

  var app = angular.module('todo-list', ['ui.sortable']);
  
  // The server template uses {{ }}, which means Angular needs to use something
  // else, like {[ ]}
  app.config(['$interpolateProvider', function($interpolateProvider) {
    $interpolateProvider.startSymbol('{[');
    $interpolateProvider.endSymbol(']}');
  }]);
  
  // Todo model: id, text, done, ordering
  
  // Manages adding, listing and sorting of todo:s.
  app.controller('TodoListController',
      ['$scope', '$http', function($scope, $http) {
    var ctrl = this;
    ctrl.list_id = null;
    ctrl.todos = [];
    ctrl.new_todo = {}
    ctrl.todos_left = 0;
    // When a todo changes position, change the ordering on the server as well.
    // The moved element gets the ordering from (now) next element in the list.
    // This all elements after the current move one up the ordering list.
    // Element with ordering 1 is displayed on top of the page.
    ctrl.sort_options = {
      stop: function( event, ui ) {
        var index = $(ui.item).index();
        ctrl.sort_options.disabled = true;
        var todo = ctrl.todos[index];
        var replacing_ordering = null;
        if (index < ctrl.todos.length - 1) {
          replacing_ordering = ctrl.todos[index + 1].ordering;
        } else{
          replacing_ordering = ctrl.todos[index - 1].ordering;
        }
        var data = {todo_id: todo.id, ordering: replacing_ordering};
        console.log(data);
        var url = api_url(ctrl.list_id, 'reorder');
        $http.post(url, data).success(function(res) {
          // Build updated ordering as: {todo_id: ordering} for easy access
          // in the following part.
          var new_ordering = {};
          for (var i = 0; i < res.ordering.length; i++) {
            new_ordering[res.ordering[i][0]] = res.ordering[i][1];
          }
          // Update all todo objects with their new ordering value.
          // This does not change the sortable, since that already happened
          // before the request was sent to the server.
          for (var i = 0; i < ctrl.todos.length; i++) {
            var ordering = new_ordering[ctrl.todos[i].id];
            if (ordering) {
              ctrl.todos[i].ordering = ordering;
            }
          }
          ctrl.sort_options.disabled = false;
        });
      }
      , disabled: false
    };
    // Count how many are not yet done.
    function count_left() {
      var left = 0;
      for (var i = 0; i < ctrl.todos.length; i++) {
        if (!ctrl.todos[i].done) {
          left += 1;
        }
      }
      ctrl.todos_left = left;
    }
    // Get initial todo:s.
    this.load = function(list_id) {
      ctrl.list_id = list_id;
      $http.get(api_url(list_id, '')).success(function(res) {
        ctrl.todos = res.todos;
        count_left(); 
      });
    };
    // Add a new todo.
    this.add = function($event) {
      $event.preventDefault();
      if (ctrl.list_id) {
        var data = {todo_text: ctrl.new_todo.text};
        $http.post(api_url(ctrl.list_id, 'add'), data).success(function(res) {
          if (res.todo_id) {
            ctrl.new_todo.done = false;
            ctrl.new_todo.id = res.todo_id;
            ctrl.new_todo.ordering = res.ordering;
            ctrl.todos.push(ctrl.new_todo);
            ctrl.new_todo = {};
            count_left();
          }
        });
      }
    };
    // Mark all todo:s as done.
    this.all = function($event) {
      $event.preventDefault();
      if (ctrl.list_id) {
        $http.get(api_url(ctrl.list_id, 'all')).success(function(res) {
          if (res.updated) {
            for (var i = 0; i < ctrl.todos.length; i++) {
              ctrl.todos[i].done = true;
            }
            count_left();
          }
        });
      }
    };
    $scope.$on(UPDATE_DONE_EVENT, function (event, args) {
      // A todo was set to done, update counter.
      count_left();
    });
  }]);

  // Controls the mark-as-done process of a single todo.
  app.controller('TodoController',
      ['$scope', '$http', function($scope, $http) {
    var ctrl = this;
    ctrl.todo = null;  
    var is_marked_done = null;  // can 'done' request be send?
    this.set_todo = function(todo) {
      ctrl.todo = todo;
      is_marked_done = todo.done;
    }
    this.mark_done = function(list_id) {
      if (ctrl.todo) {
        if (!is_marked_done) {
          var data = {todo: ctrl.todo.id};
          $http.post(api_url(list_id, 'done'), data).success(function(res) {
            if (res.success) {
              ctrl.todo.done = true;
              is_marked_done = true;
              $scope.$emit(UPDATE_DONE_EVENT);
            }
          });
        } else {
          // Keep element from being unchecked.
          ctrl.todo.done = true;
        }
      }
    };
  }]);
})(window, window.document, window.jQuery, window.angular);
