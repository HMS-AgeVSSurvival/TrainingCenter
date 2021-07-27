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

    let mainCategory1 = getSpreadSheet().getSheetByName(mainCategoryName + " 1");
    let mainCategory2 = getSpreadSheet().getSheetByName(mainCategoryName + " 2");
    let lastRowMainCategory = mainCategory1.getLastRow();

    let summaryMainCategory = getSpreadSheet().getSheetByName("summary " + mainCategoryName);

    let testColElasticNet = findSpecificCell(mainCategory1, "test r²", metricsColOrderAge["elastic_net"]).getColumn();
    let testColLightGBM = findSpecificCell(mainCategory1, "test r²", metricsColOrderAge["light_gbm"]).getColumn();

    let bestTestCol = findCell(summaryMainCategory, "best test r²").getColumn();

    for (let categoryRowMainCategory = 4; categoryRowMainCategory <= lastRowMainCategory; categoryRowMainCategory++) {
        let category = mainCategory1.getRange(categoryRowMainCategory, categoryColMainCategory).getValue();
        let testScoreElasticNet1 = mainCategory1.getRange(categoryRowMainCategory, testColElasticNet).getValue();
        let testScoreLightGBM1 = mainCategory1.getRange(categoryRowMainCategory, testColLightGBM).getValue();
        let testScoreElasticNet2 = mainCategory2.getRange(categoryRowMainCategory, testColElasticNet).getValue();
        let testScoreLightGBM2 = mainCategory2.getRange(categoryRowMainCategory, testColLightGBM).getValue();

        let categoryRowSummary = findCell(summaryMainCategory, category).getRow();

        let bestScore = Math.max(testScoreElasticNet1, testScoreLightGBM1, testScoreElasticNet2, testScoreLightGBM2);

        if (bestScore == "") {
            continue;
        } else if (bestScore == testScoreElasticNet1 || bestScore == testScoreElasticNet2) {
            let rangeCategory = summaryMainCategory.getRange(categoryRowSummary, bestTestCol);
            rangeCategory.setValue(bestScore);
            rangeCategory.setBackground("#BA6DF7");  // purple
        } else {
            let rangeCategory = summaryMainCategory.getRange(categoryRowSummary, bestTestCol);
            rangeCategory.setValue(bestScore);
            rangeCategory.setBackground("#A1F76D");  // green
        };
    };
}