export class ShiftCell {
  constructor(lane, startTime) {
    this.text = '';
    this.lane = lane;
    this.startTime = startTime;
    this.hours = 1; // might increase
  }
}


export class EmptyCell extends ShiftCell {
  cssClass: "roster-empty-cell"
  text: ''

  click() {}
}


export class Slot {
  cssClass: "roster-slot";
  text: '+'

  click() {
    this.lane.app.jobCategory.shiftModal.prompt(this);
  }
}


export class Shift {
  constructor(lane, startTime) {
    super(lane, startTime);

    this.state = 'planned'
    this.cssClass = `roster-shift roster-shift-${this.state}`;
    this.text = 'Erkki Esimerkki';
  }

  click() {
    console.log('Shift', 'click!');
  }
}