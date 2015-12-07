export default class LaneAllocator {
  constructor(app, job) {
    this.app = app;
    this.job = job;
    this.lanes = [];
  }

  getFreeLane(time) {
    for (let lane of this.lanes) {
      if (lane.isFreeAt(time)) {
        return lane;
      }
    }
  }

  buildLanes() {
    this.job.shifts.forEach(shift => this.getFreeLane(shift.startTime).addShift(shift));

    return this.lanes;
  }
}
