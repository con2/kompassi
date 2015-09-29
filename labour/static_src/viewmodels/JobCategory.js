import _ from 'lodash';
import ko from 'knockout';
import page from 'page';

import {getJobCategory, setRequirement} from '../services/RosterService';
import RequirementCell from './RequirementCell';


export default class JobCategory {
  constructor(app) {
    this.app = app;
    this.jobCategory = ko.observable(null);

    this.setupRoutes();
  }

  setupRoutes() {
    page('/:jobCategorySlug', (ctx) => {
      getJobCategory(ctx.params.jobCategorySlug)
      .then((jobCategory) => { this.loadJobCategory(jobCategory); })
    });
  }

  loadJobCategory(jobCategory) {
    jobCategory.requirementCells = RequirementCell.forJobCategory(this.app, jobCategory);
    jobCategory.jobs.forEach(job => {
      job.requirementCells = RequirementCell.forJob(this.app, job);
    });

    this.jobCategory(jobCategory);
    this.app.activeView('JobCategory');
  }

  promptForRequirementCell(requirementCell) {
    this.app.requirementModal.prompt(requirementCell)
    .then(result => {
      if (result.result === 'ok') {
        setRequirement(requirementCell.job, result.request)
        .then((jobCategory) => { this.loadJobCategory(jobCategory) });
      }
    });
  }
}
