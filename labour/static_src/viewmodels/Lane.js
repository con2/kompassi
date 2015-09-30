import _ from 'lodash';


class EmptyCell {
  constructor(lane, startTime) {
    this.type = 'EmptyCell';
    this.lane = lane;
    this.startTime = startTime;
    this.hours = 1; // might increase
  }

  click() {}
}


class Slot {
  constructor(lane, startTime) {
    this.type = 'Slot';
    this.lane = lane;
    this.startTime = startTime;
    this.hours = 1; // always 1
  }

  click() {}
}


class Shift {
}


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
