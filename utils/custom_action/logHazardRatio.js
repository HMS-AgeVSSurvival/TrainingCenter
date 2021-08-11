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

    let mainCategory1 = getSpreadSheet().getSheetByName(mainCategoryName + " 1");
    let mainCategory2 = getSpreadSheet().getSheetByName(mainCategoryName + " 2");
    let lastRowMainCategory = mainCategory1.getLastRow();

    let summaryMainCategory = getSpreadSheet().getSheetByName("summary " + mainCategoryName);

    for (let idxAlgorithm = 0; idxAlgorithm <= 1; idxAlgorithm++) {
        let logHazardRatioCol = findSpecificCell(mainCategory1, "log hazard ratio", metricsColOrderAge[algorithms[idxAlgorithm]]).getColumn();
        let pValueCol = findSpecificCell(mainCategory1, "p-value", metricsColOrderAge[algorithms[idxAlgorithm]]).getColumn();

        let summaryLogHazardRatioCol = findSpecificCell(summaryMainCategory, "log hazard ratio", metricsColOrderAge[algorithms[idxAlgorithm]]).getColumn();
        let summaryPValueCol = findSpecificCell(summaryMainCategory, "p-value", metricsColOrderAge[algorithms[idxAlgorithm]]).getColumn();

        for (let categoryRowMainCategory = 4; categoryRowMainCategory <= lastRowMainCategory; categoryRowMainCategory++) {
            let logHazardRatio1 = mainCategory1.getRange(categoryRowMainCategory, logHazardRatioCol).getValue();
            let pValue1 = mainCategory1.getRange(categoryRowMainCategory, pValueCol).getValue();
            let logHazardRatio2 = mainCategory2.getRange(categoryRowMainCategory, logHazardRatioCol).getValue();
            let pValue2 = mainCategory2.getRange(categoryRowMainCategory, pValueCol).getValue();

            if (pValue1 == "" && pValue1 != "0" && pValue2 == "" && pValue2 != "0") {
                continue;
            } else if (pValue2 == "" || (pValue1 != "" && pValue1 < pValue2)) {
                pValue = pValue1;
                logHazardRatio = logHazardRatio1;
            } else {
                pValue = pValue2;
                logHazardRatio = logHazardRatio2;
            };

            let category = mainCategory1.getRange(categoryRowMainCategory, categoryColMainCategory).getValue();
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