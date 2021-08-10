const metricsColOrderSurvival = { "full_training": { "all": { "elastic_net": 0, "light_gbm": 1 }, "cvd": { "elastic_net": 2, "light_gbm": 3 }, "cancer": { "elastic_net": 4, "light_gbm": 5 } }, "basic_training": { "all": { "elastic_net": 6, "light_gbm": 7 }, "cvd": { "elastic_net": 8, "light_gbm": 9 }, "cancer": { "elastic_net": 10, "light_gbm": 11 } } };

const bestMetricsColOrderSurvival = { "all": 0, "cvd": 1, "cancer": 2 };


function reportCindexesExamination() {
    reportCindexesMainCategory("examination");
}


function reportCindexesLaboratory() {
    reportCindexesMainCategory("laboratory");
}


function reportCindexesQuestionnaire() {
    reportCindexesMainCategory("questionnaire");
}


function reportCindexesMainCategory(mainCategoryName) {
    let categoryColMainCategory = 1;

    let mainCategory1 = getSpreadSheet().getSheetByName(mainCategoryName + " 1");
    let mainCategory2 = getSpreadSheet().getSheetByName(mainCategoryName + " 2");
    let lastRowMainCategory = mainCategory1.getLastRow();

    let summaryMainCategory = getSpreadSheet().getSheetByName("summary " + mainCategoryName);

    for (let idxTarget = 0; idxTarget < targets.length; idxTarget++) {
        if (targets[idxTarget] == "age") {
            continue
        };
        let target = targets[idxTarget];
        let testColFullTrainingElasticNet = findSpecificCell(mainCategory1, "test C-index", metricsColOrderSurvival["full_training"][target]["elastic_net"]).getColumn();
        let testColFullTrainingLightGBM = findSpecificCell(mainCategory1, "test C-index", metricsColOrderSurvival["full_training"][target]["light_gbm"]).getColumn();
        let testColBasicTrainingElasticNet = findSpecificCell(mainCategory1, "test C-index", metricsColOrderSurvival["basic_training"][target]["elastic_net"]).getColumn();
        let testColBasicTrainingLightGBM = findSpecificCell(mainCategory1, "test C-index", metricsColOrderSurvival["basic_training"][target]["light_gbm"]).getColumn();

        let bestTestCol = findSpecificCell(summaryMainCategory, "best test C-index", bestMetricsColOrderSurvival[target]).getColumn();
        let differenceTestCol = findSpecificCell(summaryMainCategory, "difference test C-index", bestMetricsColOrderSurvival[target]).getColumn();


        for (let categoryRowMainCategory = 4; categoryRowMainCategory <= lastRowMainCategory; categoryRowMainCategory++) {
            let category = mainCategory1.getRange(categoryRowMainCategory, categoryColMainCategory).getValue();

            let testScoreFullTrainingElasticNet1 = mainCategory1.getRange(categoryRowMainCategory, testColFullTrainingElasticNet).getValue();
            let testScoreFullTrainingLightGBM1 = mainCategory1.getRange(categoryRowMainCategory, testColFullTrainingLightGBM).getValue();
            let testScoreBasicTrainingElasticNet1 = mainCategory1.getRange(categoryRowMainCategory, testColBasicTrainingElasticNet).getValue();
            let testScoreBasicTrainingLightGBM1 = mainCategory1.getRange(categoryRowMainCategory, testColBasicTrainingLightGBM).getValue();

            let testScoreFullTrainingElasticNet2 = mainCategory2.getRange(categoryRowMainCategory, testColFullTrainingElasticNet).getValue();
            let testScoreFullTrainingLightGBM2 = mainCategory2.getRange(categoryRowMainCategory, testColFullTrainingLightGBM).getValue();
            let testScoreBasicTrainingElasticNet2 = mainCategory2.getRange(categoryRowMainCategory, testColBasicTrainingElasticNet).getValue();
            let testScoreBasicTrainingLightGBM2 = mainCategory2.getRange(categoryRowMainCategory, testColBasicTrainingLightGBM).getValue();

            let categoryRowSummary = findCell(summaryMainCategory, category).getRow();

            let bestFullTraining = Math.max(testScoreFullTrainingElasticNet1, testScoreFullTrainingLightGBM1, testScoreFullTrainingElasticNet2, testScoreFullTrainingLightGBM2);
            let bestBasicTraining = Math.max(testScoreBasicTrainingElasticNet1, testScoreBasicTrainingLightGBM1, testScoreBasicTrainingElasticNet2, testScoreBasicTrainingLightGBM2);

            if (bestFullTraining == "") {
                continue;
            } else if (bestFullTraining == testScoreFullTrainingElasticNet1 || bestFullTraining == testScoreFullTrainingElasticNet2) {
                let rangeCategory = summaryMainCategory.getRange(categoryRowSummary, bestTestCol);
                rangeCategory.setValue(bestFullTraining);
                rangeCategory.setBackground("#BA6DF7");  // purple
            } else {
                let rangeCategory = summaryMainCategory.getRange(categoryRowSummary, bestTestCol);
                rangeCategory.setValue(bestFullTraining);
                rangeCategory.setBackground("#A1F76D");  // green
            };

            if (bestFullTraining != "" && bestBasicTraining != "") {
                let rangeCategory = summaryMainCategory.getRange(categoryRowSummary, differenceTestCol);
                rangeCategory.setValue(parseFloat(bestFullTraining) - parseFloat(bestBasicTraining));
                rangeCategory.setHorizontalAlignment("left");

                if (parseFloat(bestFullTraining) - parseFloat(bestBasicTraining) > 0) {
                    rangeCategory.setFontWeight("bold");
                };
            };
        };
    };
}