import _ from "lodash";
import ko from "knockout";
import page from "page";

import {
  createJob,
  deleteJob,
  getJobCategory,
  setRequirement,
  updateJob,
} from "../services/RosterService";

import JobModal from "./JobModal";
import RequirementCell from "./RequirementCell";
import RequirementModal from "./RequirementModal";
import ShiftModal from "./ShiftModal";
import Lane from "./Lane";
import buildLanes from "../helpers/LaneAllocator";

export default class JobCategory {
  constructor(app) {
    this.app = app;
    this.jobCategory = ko.observable(null);

    this.requirementModal = new RequirementModal(app);
    this.jobModal = new JobModal(app);
    this.shiftModal = new ShiftModal(app);

    this.setupRoutes();
  }

  loadJobCategory(jobCategory) {
    jobCategory.requirementCells = RequirementCell.forJobCategory(
      this.app,
      jobCategory,
    );
    jobCategory.jobs.forEach((job) => {
      job.requirementCells = RequirementCell.forJob(this.app, job);
      job.lanes = buildLanes(this.app, job);
    });

    this.jobCategory(jobCategory);
    this.app.activeView("JobCategory");
  }

  editRequirement(requirementCell) {
    this.requirementModal.prompt(requirementCell).then((result) => {
      if (result.result === "ok") {
        setRequirement(requirementCell.job, result.request).then(
          (jobCategory) => this.loadJobCategory(jobCategory),
        );
      }
    });
  }

  editJob(job) {
    this.jobModal.prompt(job).then((result) => {
      if (result.result === "ok") {
        updateJob(job, result.request).then((jobCategory) =>
          this.loadJobCategory(jobCategory),
        );
      } else if (
        result.result === "delete" &&
        typeof job.slug !== "undefined"
      ) {
        deleteJob(job).then((jobCategory) => this.loadJobCategory(jobCategory));
      }
    });
  }

  createJob() {
    this.jobModal
      .prompt({ title: "Uusi tehtävä", jobCategory: this.jobCategory() })
      .then((result) => {
        if (result.result === "ok") {
          createJob(this.jobCategory(), result.request).then((jobCategory) =>
            this.loadJobCategory(jobCategory),
          );
        }
      });
  }

  setupRoutes() {
    page("/:jobCategorySlug", (ctx) => {
      getJobCategory(ctx.params.jobCategorySlug).then((jobCategory) =>
        this.loadJobCategory(jobCategory),
      );
    });
  }
}
