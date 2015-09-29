import ko from 'knockout';
import page from 'page';

import Overview from './Overview';
import JobCategory from './JobCategory';
import JobRequirementModal from './JobRequirementModal';
import config from '../services/ConfigService';
import {getJobCategory} from '../services/RosterService';


export default class Roster {
  constructor() {
    this.config = config;
    this.overview = new Overview(this);
    this.jobCategory = new JobCategory(this);
    this.jobRequirementModal = new JobRequirementModal(this);
    this.activeView = ko.observable('Overview');
  }
}
