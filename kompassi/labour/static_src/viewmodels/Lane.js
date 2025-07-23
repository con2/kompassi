import _ from "lodash";

import { EmptyCell, Shift, Slot } from "./ShiftCell";

export default class LaneBuilder {
  constructor(app, job, laneIndex) {
    this.app = app;
    this.job = job;
    this.hours = app.config.workHours.map(() => null);
    this.laneIndex = laneIndex;
  }

  addShift(shift) {
    this.getWorkHours(shift).forEach((workingHour) => {
      if (this.hours[workingHour.index]) {
        throw new Error("Lane blocked");
      }

      this.hours[workingHour.index] = shift;
    });
  }

  isFreeFor(shift) {
    return _.every(
      this.getWorkHours(shift),
      (workingHour) => !this.hours[workingHour.index],
    );
  }

  getWorkHours(shift) {
    const startingIndex =
        this.app.config.workHoursByStartTime[shift.startTime].index,
      endingIndexExcl = startingIndex + shift.hours;

    return this.app.config.workHours.slice(startingIndex, endingIndexExcl);
  }

  build() {
    const cells = [],
      lane = new Lane(this.app, this.job, cells, this.laneIndex);

    let currentShift, currentShiftCell;

    this.hours.forEach((shift, i) => {
      const workHour = this.app.config.workHours[i],
        requirementCell = this.job.requirementCells[i];

      if (shift) {
        if (shift === currentShift) {
          return;
        } else {
          currentShift = shift;
          currentShiftCell = new Shift(lane, shift);
          cells.push(currentShiftCell);
        }
      } else {
        currentShift = null;
        if (this.laneIndex < requirementCell.required) {
          cells.push(new Slot(lane, workHour.startTime));
        } else {
          cells.push(new EmptyCell(lane, workHour.startTime));
        }
      }
    });

    return lane;
  }
}

class Lane {
  constructor(app, job, cells, laneIndex) {
    this.app = app;
    this.job = job;
    this.cells = cells;
    this.laneIndex = laneIndex;
  }

  get text() {
    return `${this.job.title} ${this.laneIndex + 1}`;
  }
}
