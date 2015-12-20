class LaneAllocator {
  constructor(app, job) {
    this.app = app;
    this.job = job;
    this.laneBuilders = [];
  }

  getFreeLane(time) {
    console.log('getFreeLane', time);

    for (let laneBuilder of this.laneBuilders) {
      if (laneBuilder.isFreeAt(time)) {
        return laneBuilder;
      }
    }

    // No free lanes, create a new one
    const newLaneBuilder = new LaneBuilder(this.app, this.job);
    this.laneBuilders.push(newLaneBuilder);
    return newLaneBuilder;
  }

  buildLanes() {
    console.log('buildLanes', this);
    this.job.shifts.forEach(shift => this.getFreeLane(shift.startTime).addShift(shift));

    return this.laneBuilders.map(laneBuilder => laneBuilder.build());
  }
}

export default function buildLanes(app, job) {
  const allocator = new LaneAllocator(app, job);
  return allocator.buildLanes();
}