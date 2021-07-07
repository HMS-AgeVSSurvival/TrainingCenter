const metricsColOrderAge = { "elastic_net": 0, "light_gbm": 1 };


function reportR2Examination() {
    reportR2MainCategory("examination");
}


function reportR2Laboratory() {
    reportR2MainCategory("laboratory");
}


function reportR2Questionnaire() {
    reportR2MainCategory("questionnaire");
}


function reportR2MainCategory(mainCategoryName) {
    let categoryColMainCategory = 1;

    let mainCategory = getSpreadSheet().getSheetByName(mainCategoryName);
    let lastRowMainCategory = mainCategory.getLastRow();

    let summaryMainCategory = getSpreadSheet().getSheetByName("summary " + mainCategoryName);

    let testColElasticNet = findSpecificCell(mainCategory, "test r²", metricsColOrderAge["elastic_net"]).getColumn();
    let testColLightGBM = findSpecificCell(mainCategory, "test r²", metricsColOrderAge["light_gbm"]).getColumn();

    let bestTestCol = findCell(summaryMainCategory, "best test r²").getColumn();

    for (let categoryRowMainCategory = 4; categoryRowMainCategory <= lastRowMainCategory; categoryRowMainCategory++) {
        let category = mainCategory.getRange(categoryRowMainCategory, categoryColMainCategory).getValue();
        let testScoreElasticNet = mainCategory.getRange(categoryRowMainCategory, testColElasticNet).getValue();
        let testScoreLightGBM = mainCategory.getRange(categoryRowMainCategory, testColLightGBM).getValue();

        let categoryRowSummary = findCell(summaryMainCategory, category).getRow();

        let bestScore = Math.max(testScoreElasticNet, testScoreLightGBM);

        if (bestScore == "") {
            continue;
        } else if (testScoreElasticNet >= testScoreLightGBM) {
            let rangeCategory = summaryMainCategory.getRange(categoryRowSummary, bestTestCol);
            rangeCategory.setValue(testScoreElasticNet);
            rangeCategory.setBackground("#BA6DF7");  // purple
        } else {
            let rangeCategory = summaryMainCategory.getRange(categoryRowSummary, bestTestCol);
            rangeCategory.setValue(testScoreLightGBM);
            rangeCategory.setBackground("#A1F76D");  // green
        };
    };
}