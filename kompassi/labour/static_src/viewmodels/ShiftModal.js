import ko from "knockout";
import _ from "lodash";

import "../helpers/KoHelper"; // fmap

export default class ShiftModal {
  constructor(app) {
    this.app = app;
    this.job = ko.observable(null);

    this.$el = $("#roster-shift-modal");
    this.startTime = ko.observable("");
    this.id = ko.observable(null);
    this.hours = ko.observable(1);
    this.person = ko.observable(null);
    this.notes = ko.observable("");

    this.shiftWishes = this.person.fmap((person) => {
      if (person) {
        return person.shiftWishes || "";
      } else {
        return "Henkilön työvuorotoiveet näkyvät tässä valittuasi henkilön...";
      }
    });
    this.shiftType = this.person.fmap((person) => {
      if (person) {
        return person.shiftType || "";
      } else {
        return "Henkilön toivoma vuorojen pituus näkyy tässä valittuasi henkilön...";
      }
    });

    this.people = ko.observable([]);

    this.resolve = null;
  }

  prompt(shiftCell) {
    this.job(shiftCell.lane.job);

    this.id(shiftCell.id);
    this.people(shiftCell.lane.job.jobCategory.people);
    this.startTime(shiftCell.startTime);
    this.hours(shiftCell.hours);
    this.person(shiftCell.person);

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
        job: this.job().slug,
        startTime: this.startTime(),
        hours: parseInt(this.hours()),
        person: this.person().id,
        notes: this.notes(),
      },
    });
  }

  canRemove() {
    const id = this.id();
    return !!id;
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
}
