const categories = [
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

const categoryAndLb = new Map([
  [categories[0], 115],
  [categories[1], 125],
  [categories[2], 135],
  [categories[3], 145],
  [categories[4], 155],
  [categories[5], 170],
  [categories[6], 185],
  [categories[7], 205],
  [categories[8], 265]
]);

for (const category of categories) {
  setLbTable(category);
  setKgTable(category);
}

function setLbTable(category) {
  const tagLb = getTagLbFromCategory(category);
  const lb = categoryAndLb.get(category);
  document.getElementById(tagLb).innerHTML = lb;
}

function getTagLbFromCategory(category) {
  return category+"-lb";
}

function getTagKgFromCategory(category) {
  return category+"-kg";
}

function setKgTable(category) {
  const tagKg = getTagKgFromCategory(category);
  const tagLb = getTagLbFromCategory(category);
  const lb = document.getElementById(tagLb).innerHTML;
  var kg = getKgFromLb(lb);
  kg = getNumberRoundDecimals(kg, 3);
  document.getElementById(tagKg).innerHTML = kg;
}

function getKgFromLb(lb) {
  return lb * getKgPerLb();
}

function getKgPerLb() {
  return 0.4535924;
}

function getLbFromKg(kg) {
  const libPerKg = 1 / getKgPerLb();
  return kg * libPerKg;
}


function getNumberRoundDecimals(number, decimals) {
  const tenRaised = 10 ** decimals;
  return Math.round(number * tenRaised) / tenRaised;
}

function setLbConversor() {
  const kg = document.getElementById("kg-input").value;
  console.log(kg);
  var result = getLbFromKg(kg);
  result = getNumberRoundDecimals(result, 3);
  document.getElementById("convert-kg-result").innerHTML = result;
}
