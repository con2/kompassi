/*eslint "no-var":0 */
'use strict';

var browserify = require('browserify');
var browserSync = require('browser-sync');
var duration = require('gulp-duration');
var gulp = require('gulp');
var gutil = require('gulp-util');
var jade = require('gulp-jade');
var nib = require('nib');
var notifier = require('node-notifier');
var path = require('path');
var prefix = require('gulp-autoprefixer');
var replace = require('gulp-replace');
var rev = require('gulp-rev');
var rimraf = require('rimraf');
var source = require('vinyl-source-stream');
var sourcemaps = require('gulp-sourcemaps');
var streamify = require('gulp-streamify');
var stylus = require('gulp-stylus');
var uglify = require('gulp-uglify');
var watchify = require('watchify');
var genv = require("./gulp-env");

/*eslint "no-process-env":0 */
var production = genv.production;

var config = {
  destination: './labour/static/labour',
  scripts: {
    source: './labour/static_src/roster.js',
    destination: './labour/static/labour/js/',
    extensions: ['.jsx'],
    filename: 'roster.js'
  },
  templates: {
    source: './labour/static_src/*.pug',
    watch: './labour/static_src/*.pug',
    destination: './labour/static/labour/',
    revision: './labour/static/labour/**/*.html'
  },
  styles: {
    source: './labour/static_src/roster.styl',
    watch: './labour/static_src/**/*.styl',
    destination: './labour/static/labour/css/'
  },
  assets: {
    source: './labour/static_src/assets/**/*.*',
    watch: './labour/static_src/assets/**/*.*',
    destination: './labour/static/labour/'
  },
  revision: {
    source: ['./labour/static/labour/**/*.css', './labour/static/labour/**/*.js'],
    base: path.join(__dirname, 'labour/static/labour'),
    destination: './labour/static/labour/'
  }
};

var browserifyConfig = {
  entries: ['node_modules/babel-polyfill/dist/polyfill', config.scripts.source],
  extensions: config.scripts.extensions,
  debug: !production,
  cache: {},
  packageCache: {}
};

function handleError(err) {
  gutil.log(err);
  gutil.beep();
  notifier.notify({
    title: 'Compile Error',
    message: err.message
  });
  return this.emit('end');
}

gulp.task('roster:scripts', function() {
  var pipeline = browserify(browserifyConfig)
    .bundle()
    .on('error', handleError)
    .pipe(source(config.scripts.filename));

  if(production) {
    pipeline = pipeline.pipe(streamify(uglify()));
  }

  return pipeline.pipe(gulp.dest(config.scripts.destination));
});

gulp.task('roster:templates', function() {
  var pipeline = gulp.src(config.templates.source)
  .pipe(jade({
    // Always minify HTML in order to get rid of whitespace between elements
    pretty: false
  }))
  .on('error', handleError)
  .pipe(gulp.dest(config.templates.destination));

  if(production) {
    return pipeline;
  }

  return pipeline.pipe(browserSync.reload({
    stream: true
  }));
});

gulp.task('roster:styles', function() {
  var pipeline = gulp.src(config.styles.source);

  if(!production) {
    pipeline = pipeline.pipe(sourcemaps.init());
  }

  pipeline = pipeline.pipe(stylus({
    'include css': true,
    compress: production,
    use: nib(),
  }))
  .on('error', handleError)
  .pipe(prefix('last 2 versions', 'Chrome 34', 'Firefox 28', 'iOS 7'));

  if(!production) {
    pipeline = pipeline.pipe(sourcemaps.write('.'));
  }

  pipeline = pipeline.pipe(gulp.dest(config.styles.destination));

  if(production) {
    return pipeline;
  }

  return pipeline.pipe(browserSync.stream({
    match: '**/*.css'
  }));
});

gulp.task('roster:assets', function() {
  return gulp.src(config.assets.source)
    .pipe(gulp.dest(config.assets.destination));
});

gulp.task('roster:watch', function() {
  gulp.watch(config.templates.watch, ['roster:templates']);
  gulp.watch(config.styles.watch, ['roster:styles']);
  gulp.watch(config.assets.watch, ['roster:assets']);

  var bundle = watchify(browserify(browserifyConfig));

  bundle.on('update', function() {
    var build = bundle.bundle()
      .on('error', handleError)
      .pipe(source(config.scripts.filename));

    build.pipe(gulp.dest(config.scripts.destination))
    .pipe(duration('Rebundling browserify bundle'))
    .pipe(browserSync.reload({stream: true}));
  }).emit('update');
});

var buildTasks = ['roster:templates', 'roster:styles', 'roster:assets'];

gulp.task('roster:revision', buildTasks.concat(['roster:scripts']), function() {
  return gulp.src(config.revision.source, {base: config.revision.base})
    .pipe(rev())
    .pipe(gulp.dest(config.revision.destination))
    .pipe(rev.manifest())
    .pipe(gulp.dest('./'));
});

gulp.task('roster:replace-revision-references', ['roster:revision', 'roster:templates'], function() {
  var revisions = require('./rev-manifest.json');

  var pipeline = gulp.src(config.templates.revision);

  pipeline = Object.keys(revisions).reduce(function(stream, key) {
    return stream.pipe(replace(key, revisions[key]));
  }, pipeline);

  return pipeline.pipe(gulp.dest(config.templates.destination));
});

gulp.task('roster:build', function() {
  rimraf.sync(config.destination);
  gulp.start(buildTasks.concat(['roster:scripts', 'roster:revision', 'roster:replace-revision-references']));
});
