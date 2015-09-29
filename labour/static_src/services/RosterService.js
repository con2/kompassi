import _ from 'lodash';

import config from './ConfigService';

// TODO mock data
const MOCK_JOB_CATEGORIES = [
  {
    title: "Conitea",
    slug: "conitea",
    jobs: [
      {
        title: "Tapahtumavastaava",
        slug: "tapv",
        requirements: [1, 1, 1, 1]
      },
      {
        title: "Johtokeskuspäivystäjä",
        slug: "jkp",
        requirements: []
      }
    ],
  },
  {
    title: "Erikoistehtävä",
    slug: "erikoistehtava"
  },
  {
    title: "Järjestyksenvalvoja",
    slug: "jarjestyksenvalvoja"
  },
  {
    title: "Kasaus ja purku",
    slug: "kasaus-ja-purku"
  },
  {
    title: "Logistiikka",
    slug: "logistiikka"
  },
  {
    title: "Majoitusvalvoja",
    slug: "majoitusvalvoja"
  },
  {
    title: "Myynti",
    slug: "myynti"
  },
  {
    title: "Narikka",
    slug: "narikka"
  },
  {
    title: "Ohjelma-avustaja",
    slug: "ohjelma-avustaja"
  },
  {
    title: "Green room",
    slug: "green-room"
  },
  {
    title: "Taltiointi",
    slug: "taltiointi"
  },
  {
    title: "Tekniikka",
    slug: "tekniikka"
  },
  {
    title: "Valokuvaus",
    slug: "valokuvaus"
  },
  {
    title: "Yleisvänkäri",
    slug: "yleisvankari"
  },
  {
    title: "Info",
    slug: "info"
  },
  {
    title: "Ohjelmanpitäjä",
    slug: "ohjelmanpitaja"
  },
];

const MOCK_JOB_CATEGORIES_BY_SLUG = _.indexBy(MOCK_JOB_CATEGORIES, 'slug')


MOCK_JOB_CATEGORIES.forEach(jobCategory => {

});


function enrichJobCategories(jobCategories) {
  jobCategories.forEach(enrichJobCategory);
  return jobCategories;
}


function enrichJobCategory(jobCategory) {
  jobCategory.urls = {
    detail: `${config.urls.base}/${jobCategory.slug}`
  };

  if(jobCategory.jobs) {
    jobCategory.jobs.forEach(job => {
      job.jobCategory = jobCategory;
      job.requirementCells = requirementsToCells(job.requirements);
    });

    if(!jobCategory.requirements) {
      jobCategory.requirements = _.zip.apply(_, _.pluck(jobCategory.jobs, 'requirements')).map(_.sum);
    }
  }

  jobCategory.requirementCells = requirementsToCells(jobCategory.requirements);

  return jobCategory;
}


function requirementsToCells(requirements) {
  return _.chain(config.workHours)
  .zip(requirements)
  .map(([hour, numPeopleRequired]) => ({
    hour: hour,
    allocated: 0, // TODO
    required: numPeopleRequired || 0, // XXX || 0 is for early devt
  })).value();
}


export function getJobCategories() {
  return fetch(config.urls.jobCategoryApi, {credentials: 'include'})
  .then(response => response.json())
  .then(enrichJobCategories);
}


export function getJobCategory(slug) {
  return fetch(`${config.urls.jobCategoryApi}/${slug}`, {credentials: 'include'})
  .then(response => response.json())
  .then(enrichJobCategory);
}


export function saveJobCategory(newJobCategory) {
  return getJobCategory(newJobCategory.slug).then(oldJobCategory => { _.extend(oldJobCategory, newJobCategory)});
}
