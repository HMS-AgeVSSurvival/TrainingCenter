function reportAgeRangeExamination() {
    for (let targetIdx = 0; targetIdx < targets.length; targetIdx++) {
        reportAgeRangeMainCategory("examination", targets[targetIdx]);
    };
}


function reportAgeRangeLaboratoryAll() {
    reportAgeRangeMainCategory("laboratory", "all");
}


function reportAgeRangeLaboratoryCVD() {
    reportAgeRangeMainCategory("laboratory", "cvd");
}


function reportAgeRangeLaboratoryCancer() {
    reportAgeRangeMainCategory("laboratory", "cancer");
}


function reportAgeRangeQuestionnaire() {
    for (let targetIdx = 0; targetIdx < targets.length; targetIdx++) {
        reportAgeRangeMainCategory("questionnaire", targets[targetIdx]);
    };
}

function reportAgeRangeMainCategory(mainCategoryName, target) {
    let categoryColMainCategory = 1;

    let mainCategory = getSpreadSheet().getSheetByName(mainCategoryName + " 1");

    let lastRowMainCategory = mainCategory.getLastRow();

    let minColMainCategory = findSpecificCell(mainCategory, "min", shapeColOrderTarget[target]).getColumn();
    let maxColMainCategory = findSpecificCell(mainCategory, "max", shapeColOrderTarget[target]).getColumn();

    let summaryMainCategory = getSpreadSheet().getSheetByName("summary " + mainCategoryName);

    let minColSummary = findSpecificCell(summaryMainCategory, "min", shapeColOrderTarget[target]).getColumn();
    let maxColSummary = findSpecificCell(summaryMainCategory, "max", shapeColOrderTarget[target]).getColumn();

    for (let categoryRowMainCategory = 4; categoryRowMainCategory <= lastRowMainCategory; categoryRowMainCategory++) {
        let category = mainCategory.getRange(categoryRowMainCategory, categoryColMainCategory).getValue();
        let min = mainCategory.getRange(categoryRowMainCategory, minColMainCategory).getValue();
        let max = mainCategory.getRange(categoryRowMainCategory, maxColMainCategory).getValue();

        let categoryRowSummary = findCell(summaryMainCategory, category).getRow();

        summaryMainCategory.getRange(categoryRowSummary, minColSummary).setValue(min);
        summaryMainCategory.getRange(categoryRowSummary, maxColSummary).setValue(max);
    };
};
