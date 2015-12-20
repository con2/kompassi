import _ from 'lodash';

import {EmptyCell, Shift, Slot} from './ShiftCell';


export default class LaneBuilder {
  constructor(app, job) {
    this.app = app;
    this.job = job;
    this.hours = app.config.workHours.map(() => null);
    this.lastShift = null;
  }

  addShift(shift) {
    const startingIndex = this.app.config.workHoursByStartTime[shift.startTime],
          endingIndexExcl = startingIndex + shift.hours;

    for(let i = startingIndex; i < endingIndexExcl; ++i) {
      if (this.hours[i]) {
        throw new Exception('Lane blocked');
      }

      this.hours[i] = shift;
    }
  }

  isFreeAt(startTime) {
    return true;
  }

  build() {
    console.log('LaneBuilder', 'build!', this);
    const cells = [];

    // TODO

    return new Lane(this.app, this.job, cells);
  }
}

class Lane {
  constructor(app, job, cells) {
    this.app = app;
    this.job = job;
    this.cells = cells;
  }
}