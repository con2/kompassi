import _ from "lodash";
import LaneBuilder from "../viewmodels/Lane";

class LaneAllocator {
  constructor(app, job) {
    this.app = app;
    this.job = job;
    this.laneBuilders = [];
  }

  getFreeLaneBuilder(shift) {
    for (let laneBuilder of this.laneBuilders) {
      if (laneBuilder.isFreeFor(shift)) {
        return laneBuilder;
      }
    }

    // No free lanes, create a new one
    return this.addLaneBuilder();
  }

  addLaneBuilder() {
    const newLaneBuilder = new LaneBuilder(
      this.app,
      this.job,
      this.laneBuilders.length,
    );
    this.laneBuilders.push(newLaneBuilder);
    return newLaneBuilder;
  }

  buildLanes() {
    this.job.shifts.forEach((shift) =>
      this.getFreeLaneBuilder(shift).addShift(shift),
    );

    const largestRequirement = _.maxBy(this.job.requirementCells, "required"),
      minLanes = largestRequirement ? largestRequirement.required : 0;

    // Ensure minimum number of lanes
    while (this.laneBuilders.length < minLanes) this.addLaneBuilder();

    return this.laneBuilders.map((laneBuilder) => laneBuilder.build());
  }
}

export default function buildLanes(app, job) {
  const allocator = new LaneAllocator(app, job);
  return allocator.buildLanes();
}
