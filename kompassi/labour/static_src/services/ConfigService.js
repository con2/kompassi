import _ from "lodash";
import moment from "moment";
import page from "page";

const config = window.kompassiLabourRosterConfig;

moment.locale(config.lang);
page.base(config.urls.base);

config.workHours.forEach((hour, index) => {
  hour.index = index;
  hour.moment = moment(hour.startTime);
  hour.formatted = hour.moment.format("LLL");
});

config.workHoursByStartTime = _.keyBy(config.workHours, "startTime");

export default config;
