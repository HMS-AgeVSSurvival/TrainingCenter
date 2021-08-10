function onOpen(e) {
    let ui = SpreadsheetApp.getUi();

    let subMenuShape = ui.createMenu("Report shape").addItem("Examination", "reportShapeExamination").addItem("Laboratory", "reportShapeLaboratory").addItem("Questionnaire", "reportShapeQuestionnaire");

    let subMenuAgeRange = ui.createMenu("Report age range").addItem("Examination", "reportAgeRangeExamination").addItem("Laboratory", "reportAgeRangeLaboratory").addItem("Questionnaire", "reportAgeRangeQuestionnaire");

    let subMenuR2 = ui.createMenu("Report r²").addItem("Examination", "reportR2Examination").addItem("Laboratory", "reportR2Laboratory").addItem("Questionnaire", "reportR2Questionnaire");

    let subMenuCindexes = ui.createMenu("Report C-indexes").addItem("Examination", "reportCindexesExamination").addItem("Laboratory", "reportCindexesLaboratory").addItem("Questionnaire", "reportCindexesQuestionnaire");

    let subMenuLogHazardRatio = ui.createMenu("Report log Hazard Ratio").addItem("Examination", "reportLogHazardRatioExamination").addItem("Laboratory", "reportLogHazardRatioLaboratory").addItem("Questionnaire", "reportLogHazardRatioQuestionnaire");

    ui.createMenu("Fill Summary").addSubMenu(subMenuShape).addSubMenu(subMenuAgeRange).addSubMenu(subMenuR2).addSubMenu(subMenuCindexes).addSubMenu(subMenuLogHazardRatio).addToUi();
}
