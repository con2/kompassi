import _ from 'lodash';
import ko from 'knockout';
import page from 'page';

import {getJobCategory, saveJobCategory} from '../services/RosterService';


class Editor {
  constructor(jobCategory) {
    // editable clone of JobCategory.jobCategory
    this.masterJobCategory = jobCategory;
    this.editableJobCategory = ko.observable(null);
    this.masterJobCategory.subscribe(this.reset, this);
    this.$el = $('#labour-admin-roster-job-category-editor');

    this.actions = {
      show: (ctx, next) => { this.$el.modal('show'); },
      hide: (ctx, next) => { this.$el.modal('hide'); },
    }
  }

  save() {
    saveJobCategory(this.editableJobCategory()).then(this.masterJobCategory);
    this.close();
  }

  cancel() {
    console.log('cancel');
    this.reset();
    this.close();
  }

  reset() {
    this.editableJobCategory(_.pick(this.masterJobCategory(), 'slug', 'title'));
  }

  close() {
    page(`/jobcategory/${this.masterJobCategory().slug}`);
  }
}


export default class JobCategory {
  constructor(app) {
    this.app = app;
    this.jobCategory = ko.observable(null);
    this.editor = new Editor(this.jobCategory);

    this.setupRoutes();
  }

  setupRoutes() {
    this.actions = {
      selectJobCategory: (ctx, next) => { getJobCategory(ctx.params.jobCategorySlug).then(this.jobCategory).then(next); },
      showEditor: (ctx, next) => { this.editor.visible(true); next(); },
      hideEditor: (ctx, next) => { this.editor.visible(false); next(); },
      activate: (ctx) => { this.app.activeView('JobCategory'); },
    }

    page('/jobcategory/:jobCategorySlug',
      this.actions.selectJobCategory,
      this.editor.actions.hide,
      this.actions.activate
    );

    page('/jobcategory/:jobCategorySlug/edit',
      this.actions.selectJobCategory,
      this.editor.actions.show,
      this.actions.activate
    );
  }
}
