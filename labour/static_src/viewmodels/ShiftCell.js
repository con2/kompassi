import {createShift} from '../services/RosterService';

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

    this.cssClass = "roster-empty-cell"
    this.text = ''
  }

  click() {}
}


export class Slot extends ShiftCell {
  constructor(lane, startTime) {
    super(lane, startTime);

    this.cssClass = "roster-slot"
    this.text = '+'
  }

  click() {
    const jobCategoryViewModel = this.lane.app.jobCategory,
          jobCategory = jobCategoryViewModel.jobCategory();

    jobCategoryViewModel.shiftModal.prompt(this).then(result => {
      if (result.result === 'ok') {
        createShift(jobCategory, result.request).then(jobCategory => jobCategoryViewModel.loadJobCategory(jobCategory));
      }
    });
  }
}


export class Shift extends ShiftCell {
  constructor(lane, shift) {
    super(lane, startTime);

    this.state = 'planned'
    this.cssClass = `roster-shift roster-shift-${this.state}`;
    this.text = 'Erkki Esimerkki';
  }

  click() {
    console.log('Shift', 'click!');
  }
}