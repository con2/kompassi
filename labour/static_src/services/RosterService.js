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
        requirements: []
      },
      {
        title: "Johtokeskuspäivystäjä",
        slug: "jkp",
        requirements: []
      }
    ]
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
    detail: `${config.urls.base}/jobcategory/${jobCategory.slug}`,
    edit: `${config.urls.base}/jobcategory/${jobCategory.slug}/edit`
  };
});


export function getJobCategories() {
  return Promise.resolve(MOCK_JOB_CATEGORIES);
}


export function getJobCategory(slug) {
  return Promise.resolve(MOCK_JOB_CATEGORIES_BY_SLUG[slug]);
}


export function saveJobCategory(newJobCategory) {
  return getJobCategory.then(oldJobCategory => { _.extend(oldJobCategory, newJobCategory)});
}
