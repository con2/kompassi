import ko from "knockout";
import page from "page";

import config from "../services/ConfigService";
import { getJobCategory } from "../services/RosterService";
import Overview from "./Overview";
import JobCategory from "./JobCategory";

export default class Roster {
  constructor() {
    this.config = config;
    this.overview = new Overview(this);
    this.jobCategory = new JobCategory(this);
    this.activeView = ko.observable("Overview");

    this.setupRoutes();
  }

  setupRoutes() {
    page("*", (ctx) => {
      this.activeView("NotFound");
    });
  }
}
