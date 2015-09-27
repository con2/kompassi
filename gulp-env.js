var gutil = require('gulp-util');
var assert = require("assert");
var gulp = require("gulp");

module.exports.production = (process.env.NODE_ENV === "production" || gutil.env.production);

module.exports.verifyPrefixes = function verifyPrefixes() {
    const errors = [];
    Object.keys(gulp.tasks).forEach((name) => {
        if(name.indexOf(":") == -1) return errors.push(name + " - not prefixed");
        (gulp.tasks[name].dep || []).forEach((dep) => {
            if(dep.indexOf(":") == -1) errors.push(name + " - nonprefixed dependency " + name);
        });
    });
    if(errors.length) {
        throw new Error(errors.sort().join("\n"));
    }
};

module.exports.registerMetatask = function registerMetatask(task) {
    const re = new RegExp(":" + task + "$");
    const test = re.test.bind(re);
    const subtasks = Object.keys(gulp.tasks).filter(test);
    gulp.task(task, subtasks);
};
