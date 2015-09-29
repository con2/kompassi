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
    requirements: [1, 1, 1, 1]
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
  jobCategory.urls = {
    detail: `${config.urls.base}/${jobCategory.slug}`
  };
});


export function getJobCategories() {
  return Promise.resolve(MOCK_JOB_CATEGORIES)
  .then(jobCategories => {
    jobCategories.forEach(jobCategory => {
      jobCategory.requirementCells = requirementsToCells(jobCategory.requirements);
    });

    return jobCategories;
  })
}


export function getJobCategory(slug) {
  return Promise.resolve(MOCK_JOB_CATEGORIES_BY_SLUG[slug])
  .then(jobCategory => {
    jobCategory.requirementCells = requirementsToCells(jobCategory.requirements);

    // XXX || [] is for early devt
    (jobCategory.jobs || []).forEach(job => {
      job.jobCategory = jobCategory;
      job.requirementCells = requirementsToCells(job.requirements);
    });

    return jobCategory;
  });
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


export function saveJobCategory(newJobCategory) {
  return getJobCategory(newJobCategory.slug).then(oldJobCategory => { _.extend(oldJobCategory, newJobCategory)});
}
