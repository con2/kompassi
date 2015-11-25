import _ from 'lodash';


class EmptyCell {
  constructor(lane, startTime) {
    this.cssClass = 'roster-empty-cell';
    this.text = '';
    this.lane = lane;
    this.startTime = startTime;
    this.hours = 1; // might increase
  }

  click() {}
}


class Slot {
  constructor(lane, startTime) {
    this.cssClass = "roster-slot";
    this.text = '+';
    this.lane = lane;
    this.startTime = startTime;
    this.hours = 1; // always 1
  }

  click() {
    this.lane.app.jobCategory.shiftModal.prompt(this);
  }
}


class Shift {
  constructor(lane, startTime) {
    this.state = 'planned'
    this.cssClass = `roster-shift roster-shift-${this.state}`;
    this.text = 'Erkki Esimerkki';
    this.lane = lane;
    this.startTime = startTime;
    this.hours = 1; // might increase
  }

  click() {
    console.log('Shift', 'click!');
  }
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
