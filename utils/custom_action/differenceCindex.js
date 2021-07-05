const metricsColOrderSurvival = { "full_training": { "all": { "elastic_net": 0, "light_gbm": 1 }, "cvd": { "elastic_net": 2, "light_gbm": 3 }, "cancer": { "elastic_net": 4, "light_gbm": 5 } }, "basic_training": { "all": { "elastic_net": 6, "light_gbm": 7 }, "cvd": { "elastic_net": 8, "light_gbm": 9 }, "cancer": { "elastic_net": 10, "light_gbm": 11 } } };

const bestMetricsColOrderSurvival = { "all": 0, "cvd": 1, "cancer": 2 };


function reportCindexes() {
    let categoryColMainCategory = 1;

    for (let idxMainCategories = 0; idxMainCategories < mainCategories.length; idxMainCategories++) {
        let mainCategory = spreadSheetResults.getSheetByName(mainCategories[idxMainCategories]);
        let lastRowMainCategory = mainCategory.getLastRow();

        let summaryMainCategory = spreadSheetResults.getSheetByName("summary " + mainCategories[idxMainCategories]);

        for (let idxTarget = 0; idxTarget < targets.length; idxTarget++) {
            let target = targets[idxTarget];
            let testColFullTrainingElasticNet = findSpecificCell(mainCategory, "test C-index", metricsColOrderSurvival["full_training"][target]["elastic_net"]).getColumn();
            let testColFullTrainingLightGBM = findSpecificCell(mainCategory, "test C-index", metricsColOrderSurvival["full_training"][target]["light_gbm"]).getColumn();
            let testColBasicTrainingElasticNet = findSpecificCell(mainCategory, "test C-index", metricsColOrderSurvival["basic_training"][target]["elastic_net"]).getColumn();
            let testColBasicTrainingLightGBM = findSpecificCell(mainCategory, "test C-index", metricsColOrderSurvival["basic_training"][target]["light_gbm"]).getColumn();

            let bestTestCol = findSpecificCell(summaryMainCategory, "best test C-index", bestMetricsColOrderSurvival[target]).getColumn();
            let differenceTestCol = findSpecificCell(summaryMainCategory, "difference test C-index", bestMetricsColOrderSurvival[target]).getColumn();


            for (let categoryRowMainCategory = 4; categoryRowMainCategory <= lastRowMainCategory; categoryRowMainCategory++) {
                let category = mainCategory.getRange(categoryRowMainCategory, categoryColMainCategory).getValue();
                let testScoreFullTrainingElasticNet = mainCategory.getRange(categoryRowMainCategory, testColFullTrainingElasticNet).getValue();
                let testScoreFullTrainingLightGBM = mainCategory.getRange(categoryRowMainCategory, testColFullTrainingLightGBM).getValue();
                let testScoreBasicTrainingElasticNet = mainCategory.getRange(categoryRowMainCategory, testColBasicTrainingElasticNet).getValue();
                let testScoreBasicTrainingLightGBM = mainCategory.getRange(categoryRowMainCategory, testColBasicTrainingLightGBM).getValue();

                let categoryRowSummary = findCell(summaryMainCategory, category).getRow();

                let bestBasicTraining = Math.max(testScoreBasicTrainingElasticNet, testScoreBasicTrainingLightGBM);
                let bestFullTraining = Math.max(testScoreFullTrainingElasticNet, testScoreFullTrainingLightGBM);

                if (bestFullTraining == "") {
                    continue;
                } else if (testScoreFullTrainingElasticNet >= testScoreFullTrainingLightGBM) {
                    let rangeCategory = summaryMainCategory.getRange(categoryRowSummary, bestTestCol);
                    rangeCategory.setValue(testScoreFullTrainingElasticNet);
                    rangeCategory.setBackground("#BA6DF7");  // purple
                } else {
                    let rangeCategory = summaryMainCategory.getRange(categoryRowSummary, bestTestCol);
                    rangeCategory.setValue(testScoreFullTrainingLightGBM);
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
    };
}