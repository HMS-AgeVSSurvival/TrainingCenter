function reportAgeRangeExamination() {
    reportAgeRangeMainCategory("examination");
}


function reportAgeRangeLaboratory() {
    reportAgeRangeMainCategory("laboratory");
}


function reportAgeRangeQuestionnaire() {
    reportAgeRangeMainCategory("questionnaire");
}

function reportAgeRangeMainCategory(mainCategoryName) {
    let categoryColMainCategory = 1;

    let mainCategory = getSpreadSheet().getSheetByName(mainCategoryName + " 1");

    let lastRowMainCategory = mainCategory.getLastRow();

    for (let targetIdx = 0; targetIdx < targets.length; targetIdx++) {
        let target = targets[targetIdx];

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
};
