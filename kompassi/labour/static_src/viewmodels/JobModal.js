import _ from "lodash";
import ko from "knockout";
// import $ from 'jquery';
// import 'bootstrap';

import moment from "moment";

export default class JobModal {
  constructor(app) {
    this.app = app;
    this.job = ko.observable(null);

    this.$el = $("#roster-job-modal");
    this.title = ko.observable("");

    this.resolve = null;
  }

  prompt(job) {
    this.job(job);
    this.title(job.title);

    this.$el.modal("show");
    return new Promise((resolve, reject) => {
      this.resolve = resolve;
    });
  }

  cancel() {
    this.$el.modal("hide");
    this.resolve({ result: "cancelled" });
  }

  ok() {
    this.$el.modal("hide");
    this.resolve({
      result: "ok",
      request: {
        title: this.title(),
      },
    });
  }

  isRemoveButtonShown() {
    const job = this.job();
    return job && typeof job.slug !== "undefined";
  }

  canRemove() {
    const job = this.job();
    return (
      this.isRemoveButtonShown() &&
      _.sum(job.requirements) == 0 &&
      _.sum(job.allocated) == 0
    );
  }

  remove() {
    if (!this.canRemove()) {
      return;
    }
    this.$el.modal("hide");
    this.resolve({
      result: "delete",
    });
  }

  removeButtonTitle() {
    if (this.canRemove()) {
      return "";
    } else {
      return "Tehtävää ei voi poistaa, jos sille on määritelty työvoimatarpeita tai työvuoroja.";
    }
  }
}
