import _ from "lodash";

export default class RequirementCell {
  constructor(app, jobCategory, job, startTime, required, allocated) {
    this.app = app;
    this.jobCategory = jobCategory;
    this.job = job; // might be null
    this.startTime = startTime;
    this.allocated = allocated || 0;
    this.required = required || 0;
  }

  edit() {
    this.app.jobCategory.editRequirement(this);
  }

  css() {
    const { required, allocated } = this;

    return {
      "text-muted": required === 0,
      danger: allocated === 0 && required > 0,
      warning: allocated > 0 && required > 0 && required > allocated,
      success: allocated > 0 && allocated === required,
      info: allocated > required,
    };
  }

  static forJob(app, job) {
    return _.zip(app.config.workHours, job.requirements, job.allocated).map(
      ([hour, required, allocated]) =>
        new RequirementCell(
          app,
          job.jobCategory,
          job,
          hour.startTime,
          required,
          allocated,
        ),
    );
  }

  static forJobCategory(app, jobCategory) {
    return _.zip(
      app.config.workHours,
      jobCategory.requirements,
      jobCategory.allocated,
    ).map(
      ([hour, required, allocated]) =>
        new RequirementCell(
          app,
          jobCategory,
          null,
          hour.startTime,
          required,
          allocated,
        ),
    );
  }

  static forOverview(app, requirements, allocated) {
    return _.zip(app.config.workHours, requirements, allocated).map(
      ([hour, required, allocated]) =>
        new RequirementCell(
          app,
          null,
          null,
          hour.startTime,
          required,
          allocated,
        ),
    );
  }
}
