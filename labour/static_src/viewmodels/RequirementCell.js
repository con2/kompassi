import _ from 'lodash';


export default class RequirementCell {
  constructor(app, jobCategory, job, startTime, required) {
    this.app = app;
    this.jobCategory = jobCategory;
    this.job = job; // might be null
    this.startTime = startTime;
    this.allocated = 0;
    this.required = required;
  }

  edit() {
    this.app.jobCategory.editRequirement(this);
  }

  css() {
    const {required, allocated} = this;

    return {
      'text-muted': required === 0,
       danger: allocated === 0 && required > 0,
       success: allocated > 0 && allocated === required,
       info: allocated > required
    };
  }

  static forJob(app, job) {
    return _.zip(app.config.workHours, job.requirements)
    .map(([hour, required]) => new RequirementCell(app, job.jobCategory, job, hour.startTime, required));
  }

  static forJobCategory(app, jobCategory) {
    return _.zip(app.config.workHours, jobCategory.requirements)
    .map(([hour, required]) => new RequirementCell(app, jobCategory, null, hour.startTime, required));
  }
}
