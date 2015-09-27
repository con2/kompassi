import ko from 'knockout';

import Overview from './Overview';
import JobCategory from './JobCategory';
import config from '../services/ConfigService';

export default class Roster {
  constructor() {
    this.config = config;
    this.overview = new Overview();
    this.jobCategory = new JobCategory();
    this.activeView = ko.observable('Overview');
  }
}
