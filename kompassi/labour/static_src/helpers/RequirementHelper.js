import _ from "lodash";

export function sumRequirements(hosts) {
  return _.zip.apply(_, _.map(hosts, "requirements")).map(_.sum);
}

export function sumAllocated(hosts) {
  return _.zip.apply(_, _.map(hosts, "allocated")).map(_.sum);
}
