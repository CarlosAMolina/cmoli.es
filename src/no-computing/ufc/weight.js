const tagsPrefixIdToConvert = [
  "strawweight",
  "flyweight",
  "bantamweight",
  "featherweight",
  "lightweight",
  "welterweight",
  "middleweight",
  "light-heavyweight",
  "heavyweight",
]

for (const tagPrefixId of tagsPrefixIdToConvert) {
  setKg(tagPrefixId)
}

function setKg(tagPrefixId) {
  var tagKg = tagPrefixId+"-kg";
  var tagPounds = tagPrefixId+"-pounds";
  var pounds = document.getElementById(tagPounds).innerHTML;
  var kg = getKgFromPounds(pounds);
  kg = getNumberRoundDecimals(kg, 3);
  document.getElementById(tagKg).innerHTML = kg;
}

function getKgFromPounds(pounds) {
  const poundAsKg = 0.4535924;
  return pounds * poundAsKg;
}

function getNumberRoundDecimals(number, decimals) {
  const tenRaised = 10 ** decimals;
  return Math.round(number * tenRaised) / tenRaised;
}
