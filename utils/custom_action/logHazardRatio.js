const algorithms = ["elastic_net", "light_gbm"];


function reportLogHazardRatioExamination() {
    reportLogHazardRatioMainCategory("examination");
}


function reportLogHazardRatioLaboratory() {
    reportLogHazardRatioMainCategory("laboratory");
}


function reportLogHazardRatioQuestionnaire() {
    reportLogHazardRatioMainCategory("questionnaire");
}


function reportLogHazardRatioMainCategory(mainCategoryName) {
    let categoryColMainCategory = 1;

    let mainCategory = getSpreadSheet().getSheetByName(mainCategoryName);
    let lastRowMainCategory = mainCategory.getLastRow();

    let summaryMainCategory = getSpreadSheet().getSheetByName("summary " + mainCategoryName);

    for (let idxAlgorithm = 0; idxAlgorithm <= 1; idxAlgorithm++) {
        let logHazardRatioCol = findSpecificCell(mainCategory, "log hazard ratio", metricsColOrderAge[algorithms[idxAlgorithm]]).getColumn();
        let pValueCol = findSpecificCell(mainCategory, "p-value", metricsColOrderAge[algorithms[idxAlgorithm]]).getColumn();

        let summaryLogHazardRatioCol = findSpecificCell(summaryMainCategory, "log hazard ratio", metricsColOrderAge[algorithms[idxAlgorithm]]).getColumn();
        let summaryPValueCol = findSpecificCell(summaryMainCategory, "p-value", metricsColOrderAge[algorithms[idxAlgorithm]]).getColumn();

        for (let categoryRowMainCategory = 4; categoryRowMainCategory <= lastRowMainCategory; categoryRowMainCategory++) {
            let category = mainCategory.getRange(categoryRowMainCategory, categoryColMainCategory).getValue();
            let logHazardRatio = mainCategory.getRange(categoryRowMainCategory, logHazardRatioCol).getValue();
            let pValue = mainCategory.getRange(categoryRowMainCategory, pValueCol).getValue();

            let categoryRowSummary = findCell(summaryMainCategory, category).getRow();

            let rangeSummaryLogHazardRatio = summaryMainCategory.getRange(categoryRowSummary, summaryLogHazardRatioCol);
            let rangeSummaryPValue = summaryMainCategory.getRange(categoryRowSummary, summaryPValueCol);

            rangeSummaryLogHazardRatio.setValue(logHazardRatio);
            rangeSummaryLogHazardRatio.setHorizontalAlignment("right");
            rangeSummaryPValue.setValue(pValue);
            rangeSummaryPValue.setHorizontalAlignment("left");

            if ((pValue == "0") || ((pValue != "") && (parseFloat(pValue) < 0.05 / (lastRowMainCategory - 4 + 1)))) {  // Bonferroni correction
                rangeSummaryLogHazardRatio.setFontWeight("bold");
                if (logHazardRatio >= 0) {
                    rangeSummaryLogHazardRatio.setBackground("red");
                };
            };
        };
    };
}