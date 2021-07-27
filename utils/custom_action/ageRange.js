function reportAgeRange() {
    let categoryColMainCategory = 1;

    for (let idxMainCategories = 0; idxMainCategories < mainCategories.length; idxMainCategories++) {
        let mainCategory = getSpreadSheet().getSheetByName(mainCategories[idxMainCategories] + " 1");

        let lastRowMainCategory = mainCategory.getLastRow();
        let minColMainCategory = findCell(mainCategory, "min").getColumn();
        let maxColMainCategory = findCell(mainCategory, "max").getColumn();

        let summaryMainCategory = getSpreadSheet().getSheetByName("summary " + mainCategories[idxMainCategories]);

        let minColSummary = findCell(summaryMainCategory, "min").getColumn();
        let maxColSummary = findCell(summaryMainCategory, "max").getColumn();

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
