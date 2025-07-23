import ko from "knockout";
import page from "page";

import { getJobCategories } from "../services/RosterService";
import RequirementCell from "./RequirementCell";
import { sumRequirements, sumAllocated } from "../helpers/RequirementHelper";

export default class Overview {
  constructor(app) {
    this.app = app;
    this.jobCategories = ko.observable([]);
    this.totals = ko.observable([]);
    this.setupRoutes();
  }

  setupRoutes() {
    page("/", (ctx) => {
      getJobCategories().then((jobCategories) => {
        jobCategories.forEach((jobCategory) => {
          jobCategory.requirementCells = RequirementCell.forJobCategory(
            this.app,
            jobCategory,
          );
        });
        this.totals(
          RequirementCell.forOverview(
            this.app,
            sumRequirements(jobCategories),
            sumAllocated(jobCategories),
          ),
        );
        this.jobCategories(jobCategories);
        this.app.activeView("Overview");
      });
    });
  }
}
