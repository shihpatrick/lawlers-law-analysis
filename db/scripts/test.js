const nba = require('nba.js').default;
const data = nba.data;
const NOLAWLER = -1;
const HOMETEAM = 0;
const AWAYTEAM = 1;
const BADVARIABLE = 2;

let totalLawler = 0;
let trueLawler = 0;

function getLawler(schedule){
  schedule.forEach(function(game){
    if (game.seasonStageId == 2){
      data.pbp({
        date: game.startDateEastern,
        gameId: game.gameId,
        period: 4,
      })
      .then(function(res) {
        let winner = (parseInt(game.hTeam.score) > parseInt(game.vTeam.score)) ? HOMETEAM : AWAYTEAM;
        let firstTo100 = NOLAWLER;
        const plays = res.plays;
        for (let i = 0; i < plays.length; i += 1){
          let homeTeamScore = parseInt(plays[i].hTeamScore);
          let awayTeamScore = parseInt(plays[i].vTeamScore);
          if (awayTeamScore >= 100 && homeTeamScore < 100){
            firstTo100 = AWAYTEAM;
            break;
          }
          else if (homeTeamScore >= 100 && awayTeamScore < 100){
            firstTo100 = HOMETEAM;
            break;
          }
          else if (homeTeamScore >= 100 && awayTeamScore >= 100){
            //BOTH TEAMS HIT 100 BEFORE 3RD QUARTER, FIX LATER
            //temporary variable, just set to hometeam -- likely wrong
            firstTo100 = BADVARIABLE; 
            break;
          }
          else{
            //CHECK OVERTIME
          }
        }
        if (firstTo100 == winner || firstTo100 == BADVARIABLE){
          trueLawler += 1;
          totalLawler += 1;
        }
        else if (firstTo100 != NOLAWLER && firstTo100 != winner){
          totalLawler += 1;
        }
        console.log("trueLawler: " + trueLawler + "\ntotalLawler: " + totalLawler);
      })
      .catch(function(err) {
        console.error(err);
      })
    }
  })
}

module.exports = getLawler;