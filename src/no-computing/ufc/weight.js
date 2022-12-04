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
const log = document.querySelector("#log");
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
    if (conversionType == "conversion-kg-to-lb") {
      setLbConversor();
    }
    log.innerText = output;
    event.preventDefault();
  },
  false
);


function setLbConversor() {
  const kg = document.getElementById('kg-input').value;
  let lb_description;
  let category_description;
  const inputMin = 0;
  const inputMax = 500;
  if (kg <= inputMin || kg > inputMax) {
    lb_description = '-';
    category_description = `Peso no válido. Debe ser mayor que ${inputMin} y menor o igual a ${inputMax}`;
  } else {
    var lb = getLbFromKg(kg);
    lb = getNumberRoundDecimals(lb, 3);
    lb_description = `${lb} lb`;
    category_en = getCategoryFromLb(lb);
    category_es = categoresEnglishAndSpanish.get(category_en);
    category_description = `${category_en} (${category_es})`;
  }
  document.getElementById('convert-kg-to-lb').innerHTML = lb_description;
  document.getElementById('convert-kg-to-lb-category').innerHTML = category_description;
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

