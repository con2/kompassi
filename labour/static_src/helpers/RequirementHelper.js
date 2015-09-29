import _ from 'lodash';


export function sumRequirements(hosts) {
  return _.zip.apply(_, _.pluck(hosts, 'requirements')).map(_.sum);
}
