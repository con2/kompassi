import _ from 'lodash';
import moment from 'moment';

const config = window.kompassiLabourRosterConfig;

config.workHours.forEach((hour) => {
  hour.moment = moment(hour.timestamp);
});

export default config;
