var assert = require('assert');
var gulp = require('gulp');
var genv = require('./gulp-env');
var browserSync = require('browser-sync');
var childProcess = require('child_process');
// Insert subgulps here ===========>
require('./gulpfile.roster.js');
// <================================
genv.verifyPrefixes();
genv.registerPkgBuildAliases();  // `foo:build` available as `foo`, etc.
genv.registerMetatask('watch');  // `watch` = foo:watch, bar:watch, quux:watch, etc.
genv.registerMetatask('build');  // `build` = foo:build, bar:build, quux:build, etc.

gulp.task('browsersync-server', function() {
  return browserSync({
    open: false,
    port: 9001,
    proxy: {
      target: 'http://localhost:9002',
      ws: true
    }
  });
});

gulp.task('django-server', function() {
  return childProcess.spawn('/usr/bin/env', ['python', 'manage.py', 'runserver', '127.0.0.1:9002'], {
    stdio: [null, process.stdout, process.stderr]
  }).on("error", function(e) {
    console.error("Unable to spawn Django server for you :(", e);
  });
});


gulp.task('default', ['build', 'watch', 'browsersync-server', 'django-server']);
