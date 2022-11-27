const tags_prefix_id_to_convert = [
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

for (const tag_prefix_id of tags_prefix_id_to_convert) {
  setKg(tag_prefix_id)
}

function setKg(tag_prefix_id) {
  var tag_kg = tag_prefix_id+"-kg";
  var tag_pounds = tag_prefix_id+"-pounds";
  var pounds = document.getElementById(tag_pounds).innerHTML;
  var kg = getKgFromPounds(pounds);
  kg = getNumberRoundDecimals(kg, 3);
  document.getElementById(tag_kg).innerHTML = kg;
}

function getKgFromPounds(pounds) {
  const POUND_AS_KG = 0.4535924;
  return pounds * POUND_AS_KG;
}

function getNumberRoundDecimals(number, decimals) {
  const TEN_RAISED = 10 ** decimals;
  return Math.round(number * TEN_RAISED) / TEN_RAISED;
}