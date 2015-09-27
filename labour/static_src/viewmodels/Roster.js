import ko from 'knockout';
import page from 'page';

import Overview from './Overview';
import JobCategory from './JobCategory';
import config from '../services/ConfigService';
import {getJobCategory} from '../services/RosterService';


export default class Roster {
  constructor() {
    this.config = config;
    this.overview = new Overview();
    this.jobCategory = new JobCategory();
    this.activeView = ko.observable('Overview');

    page('/', () => { this.activeView('Overview')});
    page('/jobcategory/:jobCategorySlug', (ctx) => {
      getJobCategory(ctx.params.jobCategorySlug)
      .then(jobCategory => {
        this.jobCategory.jobCategory(jobCategory);
        this.activeView('JobCategory');
      });
    });
  }
}
