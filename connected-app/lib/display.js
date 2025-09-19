const chalk = require('chalk');

function displayHistory(explanations) {
  console.log(chalk.green(`\n📚 Your Organization's Recent Explanations (${explanations.length} found):\n`));

  explanations.forEach((item, index) => {
    const number = chalk.blue(`${index + 1}.`);
    const topic = chalk.bold.white(item.topic);
    const explanation = chalk.gray(item.explanation);

    console.log(`${number} ${topic}`);
    console.log(`   ${explanation}\n`);
  });
}

module.exports = { displayHistory };