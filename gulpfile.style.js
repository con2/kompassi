import gulp from "gulp";
import gutil from "gulp-util";
import less from "gulp-less";
import autoprefixer from "gulp-autoprefixer";
import sourcemaps from "gulp-sourcemaps";
import cssnano from "gulp-cssnano";
import rename from "gulp-rename";
import size from "gulp-size";
import {production} from "./gulp-env";

gulp.task("style:build", () => {
    return gulp.src("static_src/less/kompassi.less")
        .pipe(sourcemaps.init())
        .pipe(less())
        .pipe(autoprefixer())
        .pipe((production ? cssnano() : gutil.noop()))
        .pipe(rename("kompassi.css"))
        .pipe(size())
        .pipe(sourcemaps.write("."))
        .pipe(gulp.dest("core/static"));
});

gulp.task("style:watch", () => {
    gulp.watch("static_src/less/**/*.less", ["style:build"]);
});
