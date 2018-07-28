var getLawler = require('./test');

const nba = require('nba.js').default;
const data = nba.data;

data.schedule({ year: 2017 })
  .then(function(res) {
      const schedule = res.league.standard;

      let rv = getLawler(schedule);
      //soooo hacky pls fix this for pride sake (not even running in the web app u DUM shit)
      setTimeout(function(){
        console.log(rv)
      }, 5000);
      

  })
  .catch(function(err) {
      console.error(err);
  }
);