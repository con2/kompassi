const gulp = require("gulp");
// const gutil = require("gulp-util");
const less = require("gulp-less");
const autoprefixer = require("gulp-autoprefixer");
const sourcemaps = require("gulp-sourcemaps");
// const cssnano = require("gulp-cssnano");
const rename = require("gulp-rename");
const size = require("gulp-size");

gulp.task("style:build", () => {
    return gulp.src("core/static_src/less/kompassi.less")
        .pipe(sourcemaps.init())
        .pipe(less())
        .pipe(autoprefixer())
        // .pipe(cssnano() : gutil.noop()))
        .pipe(rename("kompassi.css"))
        .pipe(size())
        .pipe(sourcemaps.write("."))
        .pipe(gulp.dest("core/static"));
});

gulp.task("style:watch", () => {
    return gulp.watch([
        "core/static_src/less/**/*.less",
        "feedback/static_src/less/**/*.less",
    ],
        gulp.series("style:build")
    );
});
