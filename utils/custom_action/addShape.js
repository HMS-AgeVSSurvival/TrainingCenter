function reportShape() {
    let categoryColMainCategory = 1;

    for (let idxMainCategories = 0; idxMainCategories < mainCategories.length; idxMainCategories++) {
        let mainCategory = getSpreadSheet().getSheetByName(mainCategories[idxMainCategories]);

        let lastRowMainCategory = mainCategory.getLastRow();
        let nParticipantsColMainCategory = findCell(mainCategory, "n_participants").getColumn();
        let nVariablesColMainCategory = findCell(mainCategory, "n_variables").getColumn();

        let summaryMainCategory = getSpreadSheet().getSheetByName("summary " + mainCategories[idxMainCategories]);

        let nParticipantsColSummary = findCell(summaryMainCategory, "n_participants").getColumn();
        let nVariablesColSummary = findCell(summaryMainCategory, "n_variables").getColumn();

        for (let categoryRowMainCategory = 4; categoryRowMainCategory <= lastRowMainCategory; categoryRowMainCategory++) {
            let category = mainCategory.getRange(categoryRowMainCategory, categoryColMainCategory).getValue();
            let nParticipants = mainCategory.getRange(categoryRowMainCategory, nParticipantsColMainCategory).getValue();
            let nVariables = mainCategory.getRange(categoryRowMainCategory, nVariablesColMainCategory).getValue();

            let categoryRowSummary = findCell(summaryMainCategory, category).getRow();

            summaryMainCategory.getRange(categoryRowSummary, nParticipantsColSummary).setValue(nParticipants);
            summaryMainCategory.getRange(categoryRowSummary, nVariablesColSummary).setValue(nVariables);
        };
    };
};
