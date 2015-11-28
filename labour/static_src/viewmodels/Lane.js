import _ from 'lodash';

import {EmptyCell, Shift, Slot} from './ShiftCell';


export default class Lane {
  constructor(app, job, laneNum) {
    this.app = app;
    this.job = job;
    this.laneNum = laneNum;
    this.cells = this.makeCells();
  }

  makeCells() {
    const cells = [];
    var currentEmptyCell = null;

    _.zip(this.app.config.workHours, this.job.requirements).forEach(([hour, requirement]) => {
      if (requirement > this.laneNum) {
        currentEmptyCell = null;
        cells.push(new Slot(this, hour.startTime));
      } else if (currentEmptyCell !== null) {
        ++currentEmptyCell.hours;
      } else {
        currentEmptyCell = new EmptyCell(this, hour.startTime);
        cells.push(currentEmptyCell);
      }
    });

    return cells;
  }
}
