var getLawler = require('./test');

const nba = require('nba.js').default;
const data = nba.data;

data.schedule({ year: 2017 })
  .then(function(res) {
      const schedule = res.league.standard;

      getLawler(schedule);
  })
  .catch(function(err) {
      console.error(err);
  }
);