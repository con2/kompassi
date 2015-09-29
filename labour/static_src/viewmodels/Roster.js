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

    this.setupRoutes();
  }

  // Not sure if $root is the best place for this
  requirementCellCss(requirementCell) {
    const {required, allocated} = requirementCell;

    return {
      'text-muted': required === 0,
       danger: allocated === 0 && required > 0,
       success: allocated > 0 && allocated === required,
       info: allocated > required
    };
  }

  setupRoutes() {
    page('*', (ctx) => { this.activeView('NotFound'); });
  }
}
