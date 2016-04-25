import _ from 'lodash';

import {EmptyCell, Shift, Slot} from './ShiftCell';


export default class LaneBuilder {
  constructor(app, job, laneNumber) {
    this.app = app;
    this.job = job;
    this.hours = app.config.workHours.map(() => null);
    this.laneNumber = laneNumber;
  }

  addShift(shift) {
    const
      startingIndex = this.app.config.workHoursByStartTime[shift.startTime],
      endingIndexExcl = startingIndex + shift.hours;

    for(let i = startingIndex; i < endingIndexExcl; ++i) {
      if (this.hours[i]) {
        throw new Error('Lane blocked');
      }

      this.hours[i] = shift;
    }
  }

  isFreeAt(startTime) {
    return true;
  }

  build() {
    const
      cells = [],
      lane = new Lane(this.app, this.job, cells);

    this.hours.forEach((shift, i) => {
      const
        workHour = this.app.config.workHours[i],
        requirementCell = this.job.requirementCells[i];

      let currentShift;

      if (shift) {
        if (shift === currentShift) return;
        currentShift = shift;
        cells.push(new Shift(lane, shift));
      } else {
        currentShift = null;
        if (this.laneNumber < requirementCell.required) {
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
  constructor(app, job, cells) {
    this.app = app;
    this.job = job;
    this.cells = cells;
  }
}
