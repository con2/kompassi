import {
  createShift,
  updateShift,
  deleteShift,
} from "../services/RosterService";

export class ShiftCell {
  constructor(lane, startTime) {
    this.lane = lane;
    this.startTime = startTime;
    this.hours = 1; // might increase
  }
}

export class EmptyCell extends ShiftCell {
  constructor(lane, startTime) {
    super(lane, startTime);
  }

  get cssClass() {
    return "roster-empty-cell";
  }

  get text() {
    return "";
  }

  get title() {
    return "";
  }

  click() {}
}

export class Slot extends ShiftCell {
  constructor(lane, startTime) {
    super(lane, startTime);
  }

  get cssClass() {
    return "roster-slot";
  }

  get text() {
    return "+";
  }

  get title() {
    return "Lisää työvuoro";
  }

  click() {
    const jobCategoryViewModel = this.lane.app.jobCategory,
      jobCategory = jobCategoryViewModel.jobCategory();

    jobCategoryViewModel.shiftModal.prompt(this).then((result) => {
      if (result.result === "ok") {
        createShift(jobCategory, result.request).then((jobCategory) =>
          jobCategoryViewModel.loadJobCategory(jobCategory),
        );
      }
    });
  }
}

export class Shift extends ShiftCell {
  constructor(lane, shift) {
    super(lane, shift.startTime);

    this.shift = shift;
    this.hours = shift.hours;
  }

  get cssClass() {
    return `roster-shift roster-shift-${this.shift.state}`;
  }

  get id() {
    return this.shift.id;
  }

  get text() {
    return this.shift.person.fullName;
  }

  get title() {
    return this.text;
  }

  get person() {
    return this.shift.person;
  }

  click() {
    const jobCategoryViewModel = this.lane.app.jobCategory,
      jobCategory = jobCategoryViewModel.jobCategory();

    jobCategoryViewModel.shiftModal.prompt(this).then((result) => {
      if (result.result === "ok") {
        updateShift(this.shift, result.request).then((jobCategory) =>
          jobCategoryViewModel.loadJobCategory(jobCategory),
        );
      } else if (result.result === "delete") {
        deleteShift(this.shift).then((jobCategory) =>
          jobCategoryViewModel.loadJobCategory(jobCategory),
        );
      }
    });
  }
}
