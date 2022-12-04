const categories = [
  'strawweight',
  'flyweight',
  'bantamweight',
  'featherweight',
  'lightweight',
  'welterweight',
  'middleweight',
  'light-heavyweight',
  'heavyweight',
]

const categoresEnglishAndSpanish = new Map([
  [categories[0], 'peso paja'],
  [categories[1], 'peso mosca'],
  [categories[2], 'peso gallo'],
  [categories[3], 'peso pluma'],
  [categories[4], 'peso ligero'],
  [categories[5], 'peso wélter'],
  [categories[6], 'peso mediano'],
  [categories[7], 'peso semipesado'],
  [categories[8], 'peso pesado o completo'],
]);

const categoryAndLb = new Map([
  [categories[0], 115],
  [categories[1], 125],
  [categories[2], 135],
  [categories[3], 145],
  [categories[4], 155],
  [categories[5], 170],
  [categories[6], 185],
  [categories[7], 205],
  [categories[8], 265],
]);

for (const category of categories) {
  setLbTable(category);
  setKgTable(category);
}

function setLbTable(category) {
  const tagLb = getTagLbFromCategory(category);
  const tagCategoryEn = getTagCategoryEnFromCategory(category);
  const tagCategoryEs = getTagCategoryEsFromCategory(category);
  const lb = categoryAndLb.get(category);
  document.getElementById(tagCategoryEn).innerHTML = category;
  document.getElementById(tagCategoryEs).innerHTML = categoresEnglishAndSpanish.get(category);
  document.getElementById(tagLb).innerHTML = lb;
}

function getTagCategoryEsFromCategory(category) {
  return category+'-category-es';
}

function getTagCategoryEnFromCategory(category) {
  return category+'-category-en';
}

function getTagLbFromCategory(category) {
  return category+'-lb';
}

function getTagKgFromCategory(category) {
  return category+'-kg';
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

const conversorForm = document.querySelector("form");
conversorForm.addEventListener(
  "submit",
  (event) => {
    const data = new FormData(conversorForm);
    let output = "";
    let conversionType = "";
    for (const entry of data) {
      conversionType = entry[1];
      output = `${output}${entry[0]}=${conversionType}\r`;
    }
    setResultConversor(conversionType);
    event.preventDefault();
  },
  false
);


function setResultConversor(conversionType) {
  const weightInput = document.getElementById('conversor-input').value;
  const inputMin = 0;
  if (weightInput <= inputMin) {
    errorMsg = `Peso no válido. Debe ser mayor que ${inputMin}`;
    document.getElementById('error-output').innerHTML = errorMsg;
    document.getElementById('error-output').classList.remove("hidden");
    document.getElementById('conversor-output').classList.add("hidden");
  } else {
    let enCategory;
    let weightOutput;
    let kgWeightOutput;
    let lbWeightOutput;
    if (conversionType == "conversion-kg-to-lb") {
      weightOutput = getLbFromKg(weightInput);
      enCategory = getCategoryFromLb(weightOutput);
      kgWeightOutput = weightInput;
      lbWeightOutput = weightOutput;
    } else {
      weightOutput = getKgFromLb(weightInput);
      enCategory = getCategoryFromLb(weightInput);
      kgWeightOutput = weightOutput;
      lbWeightOutput = weightInput;
    }
    kgWeightOutput = getNumberRoundDecimals(kgWeightOutput, 3);
    lbWeightOutput = getNumberRoundDecimals(lbWeightOutput, 3);
    const esCategory = categoresEnglishAndSpanish.get(enCategory);
    document.getElementById('kg-weight-output').innerHTML = kgWeightOutput;
    document.getElementById('lb-weight-output').innerHTML = lbWeightOutput;
    document.getElementById('en-category-output').innerHTML = enCategory;
    document.getElementById('es-category-output').innerHTML = esCategory;
    document.getElementById('error-output').classList.add("hidden");
    document.getElementById('conversor-output').classList.remove("hidden");
  }
}

function getCategoryFromLb(lb_input) {
  let result = categories[categories.length -1];
  for (let [category, lb] of categoryAndLb.entries()) {
    if (lb_input <= lb) {
      result = category
      break;
    }
  }
  return result;
}

