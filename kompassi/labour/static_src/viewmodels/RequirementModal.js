import ko from "knockout";

export default class RequirementModal {
  constructor(app) {
    this.app = app;
    this.job = ko.observable(null);

    this.$el = $("#roster-requirement-modal");
    this.startTime = ko.observable("");
    this.hours = ko.observable(1);
    this.required = ko.observable(0);

    this.resolve = null;
  }

  prompt(requirementCell) {
    this.job(requirementCell.job);
    this.startTime(requirementCell.startTime);
    this.hours(1);
    this.required(requirementCell.required);

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
        startTime: this.startTime(),
        hours: parseInt(this.hours()),
        required: parseInt(this.required()),
      },
    });
  }
}
