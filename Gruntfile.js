module.exports = function(grunt) {

  // Project configuration.
  grunt.initConfig({
      pkg: grunt.file.readJSON('package.json')
    , watch: {
          files: ['frontend/**']
        , tasks: ['requirejs:dev', 'copy:css']
    }
    , requirejs: {
        dev: {
            options: {
                appDir: './frontend/js'
              , baseUrl: './'
              , paths: {
                    'angular': '../../bower_components/angular/angular'
                  , 'jquery': '../../bower_components/jquery/dist/jquery'
                  , 'jquery-ui': '../../bower_components/jquery-ui/jquery-ui'
                  , 'angular-ui-sortable':
                      '../../bower_components/angular-ui-sortable/sortable'
              }
              , dir: './backend/flask_todo/static/js'
              , optimize: 'none'
              , modules: [
                  {'name': 'list'}
              ]
              , generateSourceMaps: false
              , preserveLicenseComments: false
              , wrap: false
              , skipModuleInsertion: true
              , useStrict: true
              , logLevel: 0
              , shim: {
                  'list': {
                    deps: [
                      'jquery', 'nojs', 'jquery-ui', 'angular',
                      'angular-ui-sortable']
                  }
              }
            }
        }
    }
    , copy: {
      css: {
          expand: true
        , cwd: 'frontend/css/'
        , src: '**'
        , dest: 'backend/flask_todo/static/css/'
        , flatten: true
        , filter: 'isFile'
      }
    }
  });

  grunt.loadNpmTasks('grunt-contrib-requirejs');
  grunt.loadNpmTasks('grunt-contrib-watch');
  grunt.loadNpmTasks('grunt-contrib-copy');

  // Default tasks.
  grunt.registerTask('default', ['requirejs:dev', 'copy:css']);
};
