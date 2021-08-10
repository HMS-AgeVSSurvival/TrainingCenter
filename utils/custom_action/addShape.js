const shapeColOrderTarget = { "age": 0, "all": 1, "cvd": 2, "cancer": 3 };

function reportShapeExamination() {
    reportShapeMainCategory("examination");
}


function reportShapeLaboratory() {
    reportShapeMainCategory("laboratory");
}


function reportShapeQuestionnaire() {
    reportShapeMainCategory("questionnaire");
}


function reportShapeMainCategory(mainCategoryName) {
    let categoryColMainCategory = 1;

    let mainCategory = getSpreadSheet().getSheetByName(mainCategoryName + " 1");

    let lastRowMainCategory = mainCategory.getLastRow();

    for (let targetIdx = 0; targetIdx < targets.length; targetIdx++) {
        let target = targets[targetIdx];

        let nParticipantsColMainCategory = findSpecificCell(mainCategory, "n_participants", shapeColOrderTarget[target]).getColumn();
        let nVariablesColMainCategory = findSpecificCell(mainCategory, "n_variables", shapeColOrderTarget[target]).getColumn();

        let summaryMainCategory = getSpreadSheet().getSheetByName("summary " + mainCategoryName);

        let nParticipantsColSummary = findSpecificCell(summaryMainCategory, "n_participants", shapeColOrderTarget[target]).getColumn();
        let nVariablesColSummary = findSpecificCell(summaryMainCategory, "n_variables", shapeColOrderTarget[target]).getColumn();

        for (let categoryRowMainCategory = 4; categoryRowMainCategory <= lastRowMainCategory; categoryRowMainCategory++) {
            let category = mainCategory.getRange(categoryRowMainCategory, categoryColMainCategory).getValue();
            let nParticipants = mainCategory.getRange(categoryRowMainCategory, nParticipantsColMainCategory).getValue();
            let nVariables = mainCategory.getRange(categoryRowMainCategory, nVariablesColMainCategory).getValue();

            let categoryRowSummary = findCell(summaryMainCategory, category).getRow();

            summaryMainCategory.getRange(categoryRowSummary, nParticipantsColSummary).setValue(nParticipants);
            summaryMainCategory.getRange(categoryRowSummary, nVariablesColSummary).setValue(nVariables);
        };
    };
}
