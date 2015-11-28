export class ShiftCell {
  constructor(lane, startTime) {
    this.text = '';
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
    this.lane.app.jobCategory.shiftModal.prompt(this);
  }
}


export class Shift extends ShiftCell {
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